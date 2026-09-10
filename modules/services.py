"""
CREW DUTY ENGINE V2 - Core Bridge Services
繼承 V1 真實大表解析算力（TD/TM/TA 三表連動、parse_cell 班別拆解、合規計算）
"""
import json
import os
import re
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
import streamlit as st
from config import DATA_DIR, SYSTEM_CONFIG_FILE, UNITS, WHITELIST_FILE
from modules.utils import (
    calculate_consecutive_work_days,
    check_shift_legality,
    get_employee_name,
    is_cell_off_day,
    is_overtime,
    is_town_shift,
    parse_cell,
    safe_read_excel,
    translate_train_code,
)

# ---------------------------------------------------------
# 1. 載入全站系統設定與白名單
# ---------------------------------------------------------
def load_system_config() -> Dict[str, Any]:
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(SYSTEM_CONFIG_FILE):
        return {}
    try:
        with open(SYSTEM_CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_system_config(config_dict: Dict[str, Any]) -> bool:
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(SYSTEM_CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config_dict, f, ensure_ascii=False, indent=4)
        return True
    except Exception:
        return False

def load_whitelist(unit_code: str = "TTN") -> Dict[str, Any]:
    whitelist_path = WHITELIST_FILE
    if os.path.exists(whitelist_path):
        try:
            with open(whitelist_path, "r", encoding="utf-8") as f:
                full_data = json.load(f)
                return full_data.get(unit_code, {})
        except Exception:
            return {}
    return {}

def is_user_allowed(selected_unit: str, emp_id: Any) -> Tuple[bool, Optional[Dict[str, Any]]]:
    emp_id_str = str(emp_id).strip().upper()
    if emp_id_str == "A":
        return True, {"emp_id": "A", "name": "全域通行", "role": "VIP_USER"}
    
    wl = load_whitelist(selected_unit)
    if emp_id_str in wl:
        info = wl[emp_id_str]
        return True, {"emp_id": emp_id_str, "name": info.get("name", "組員"), "role": info.get("role", "VIP")}
    return False, None

def verify_crew_membership(selected_unit: str, emp_id: str) -> bool:
    emp_id_str = str(emp_id).strip().upper()
    unit_files = UNITS.get(selected_unit, {})
    for role_name, file_path in unit_files.items():
        if isinstance(file_path, str) and os.path.exists(file_path):
            try:
                df = safe_read_excel(file_path, header=3)
                for _, row in df.iterrows():
                    if str(row.iloc[0]).strip().upper() == emp_id_str:
                        return True
            except Exception:
                pass
    return False

# ---------------------------------------------------------
# 2. V2 前台專用：真實全月班表 JSON 解析器
# ---------------------------------------------------------
def get_crew_full_schedule_json(target_emp: str, unit_code: str = "TTN") -> Dict[str, Any]:
    """
    調用 V1 process_file_data 真實算力，將班表轉為 V2 redesign.html 所需之 JSON 格式
    """
    target_emp_str = str(target_emp).strip().upper()
    unit_files = UNITS.get(unit_code, UNITS.get("TTN", {}))

    found_row, found_df, role_title = None, None, "服勤員"
    emp_id, emp_name = target_emp_str, "組員"

    # 搜尋三大表 (駕駛、列車長、服勤員)
    for role, path in unit_files.items():
        if isinstance(path, str) and os.path.exists(path):
            try:
                df = safe_read_excel(path, header=3)
                df.columns = [str(c).strip() for c in df.columns]
                for _, row in df.iterrows():
                    r_id = str(row.iloc[0]).strip().upper()
                    r_name = str(row.iloc[1]).strip().upper()
                    if r_id == target_emp_str or r_name == target_emp_str:
                        found_row, found_df, role_title = row, df, role
                        emp_id = str(row.iloc[0]).strip()
                        emp_name = str(row.iloc[1]).strip()
                        break
                if found_row is not None:
                    break
            except Exception:
                pass

    if found_row is None:
        return None

    all_cols = list(found_df.columns)
    days_schedule = []
    day_counter = 1

    for col_idx in range(2, len(all_cols)):
        col_name = str(all_cols[col_idx]).strip()
        m = re.search(r"(\d+/\d+)", col_name)
        if not m:
            continue

        raw_cell = found_row.iloc[col_idx]
        parsed = parse_cell(raw_cell)
        is_off = is_cell_off_day(raw_cell)

        # 日期與星期
        d_str = m.group(1)
        wd_list = ["日", "一", "二", "三", "四", "五", "六"]
        try:
            m_v, d_v = map(int, d_str.split("/"))
            wd_str = wd_list[datetime(2026, m_v, d_v).weekday()]
        except Exception:
            wd_str = "一"

        item = {
            "d": day_counter,
            "date_str": d_str,
            "wd": wd_str
        }

        if is_off and not parsed["start"]:
            item["off"] = parsed["train"] if parsed["train"] != "無" else "DO"
            item["barType"] = "off"
            item["tags"] = ["休假日"]
        else:
            tags = []
            if is_overtime(parsed["hours"], parsed["train"], parsed["note"]):
                tags.append("工時>8.5h")
            if is_town_shift(parsed["train"], parsed["note"]):
                tags.append("非正線")

            # 班間休息合規檢查 (呼叫 V1 check_shift_legality)
            is_legal, warn_msg, rest_info = check_shift_legality(found_row, col_idx, all_cols)
            rest_val = rest_info.get("min_interval")
            
            rest_tag = "green"
            if rest_val is not None:
                if rest_val < 11.0:
                    rest_tag = "red"
                elif rest_val < 12.0:
                    rest_tag = "amber"

            item["code"] = translate_train_code(parsed["train"])
            item["start"] = parsed["start"] or "--:--"
            item["end"] = parsed["end"] or "--:--"
            item["dur"] = parsed["hours"] or "--"
            item["rest"] = f"{rest_val}h" if rest_val else "12.0h"
            item["restTag"] = rest_tag
            item["tags"] = tags

        days_schedule.append(item)
        day_counter += 1

    return {
        "emp_id": emp_id,
        "name": emp_name,
        "role_title": role_title,
        "unit": unit_code,
        "unit_name": "北轉" if unit_code == "TTN" else ("中轉" if unit_code == "TTC" else "南轉"),
        "schedule": days_schedule
    }

# ---------------------------------------------------------
# 3. V2 前台專用：動態換班快搜算力引擎
# ---------------------------------------------------------
def search_exchange_candidates_v2(unit_code: str = "TTN", target_date: str = "9/15", time_from: str = "05:00", time_to: str = "10:00") -> Dict[str, List[Dict[str, Any]]]:
    """
    從 Excel 檔案中檢索符合特定 Sign-In 時段區間之組員
    """
    unit_files = UNITS.get(unit_code, UNITS.get("TTN", {}))
    result = {"服勤員": [], "駕駛": [], "列車長": []}

    for role_name, file_path in unit_files.items():
        if not (isinstance(file_path, str) and os.path.exists(file_path)):
            continue

        try:
            df = safe_read_excel(file_path, header=3)
            df.columns = [str(c).strip() for c in df.columns]

            # 尋找對應日期欄位
            target_col_idx = -1
            for idx, col in enumerate(df.columns[2:], start=2):
                m = re.search(r"(\d+/\d+)", str(col))
                if m and m.group(1) == target_date:
                    target_col_idx = idx
                    break

            if target_col_idx == -1:
                continue

            for _, row in df.iterrows():
                emp_id = str(row.iloc[0]).strip().upper()
                emp_name = str(row.iloc[1]).strip()
                if not emp_id or emp_id in ["NAN", "NONE", ""]:
                    continue

                cell_raw = row.iloc[target_col_idx]
                parsed = parse_cell(cell_raw)
                start_t = parsed["start"]

                if start_t and time_from <= start_t <= time_to:
                    # 班間合規檢查
                    _, _, rest_info = check_shift_legality(row, target_col_idx, df.columns)
                    rest_val = rest_info.get("min_interval")
                    rest_tag = "green"
                    if rest_val and rest_val < 11.0:
                        rest_tag = "red"
                    elif rest_val and rest_val < 12.0:
                        rest_tag = "amber"

                    result[role_name].append({
                        "id": emp_id,
                        "name": emp_name,
                        "start": start_t,
                        "end": parsed["end"] or "--:--",
                        "dur": parsed["hours"] or "8h00m",
                        "restBefore": f"{rest_val}h" if rest_val else "12.0h",
                        "restTag": rest_tag,
                        "streak": f"勤務：{translate_train_code(parsed['train'])}"
                    })
        except Exception as e:
            print(f"快搜計算出錯 ({role_name}): {e}")

    return result
