"""
CREW DUTY ENGINE V2 - Compliance & Time Math Engine
全動態班間休息、工時、連續出勤與合規檢核算力模組
"""
from datetime import datetime, timedelta
import os
import re
from typing import Any, Dict, List, Optional, Tuple
import pandas as pd

# =========================================================
# 1. 基礎時間與工時算力引擎 (保留你原本 V2 的核心函式)
# =========================================================

def parse_time_str(time_str: str):
    """將 HH:MM 格式字串轉為 datetime.time 物件"""
    if not time_str or not isinstance(time_str, str):
        return None
    match = re.search(r"(\d{1,2}):(\d{2})", time_str.strip())
    if match:
        hrs, mins = int(match.group(1)), int(match.group(2))
        return datetime.min.time().replace(hour=hrs % 24, minute=mins % 60)
    return None

def calc_duty_duration(start_str: str, end_str: str):
    """動態計算單班總工時 (支援跨夜班別)"""
    t1 = parse_time_str(start_str)
    t2 = parse_time_str(end_str)
    if not t1 or not t2:
        return 8.0, "8h00m"

    dt1 = datetime.combine(datetime.today(), t1)
    dt2 = datetime.combine(datetime.today(), t2)
    if dt2 <= dt1:
        dt2 += timedelta(days=1)

    diff_sec = (dt2 - dt1).total_seconds()
    hrs = diff_sec / 3600.0
    h_int = int(diff_sec // 3600)
    m_int = int((diff_sec % 3600) // 60)
    return hrs, f"{h_int}h{m_int:02d}m"

def calc_rest_interval(prev_end_date_str: str, prev_end_time_str: str, curr_start_date_str: str, curr_start_time_str: str):
    """
    動態計算班間休息時間與合規標記：
    - rest < 11.0h -> 'red' (違反/不足 11 小時法定門檻)
    - 11.0h <= rest < 12.0h -> 'amber' (臨界)
    - rest >= 12.0h -> 'green' (合規)
    """
    if not (prev_end_date_str and prev_end_time_str and curr_start_date_str and curr_start_time_str):
        return None, None

    t_prev_end = parse_time_str(prev_end_time_str)
    t_curr_start = parse_time_str(curr_start_time_str)
    if not (t_prev_end and t_curr_start):
        return None, None

    try:
        dt_prev_end = datetime.strptime(f"{prev_end_date_str} {t_prev_end.strftime('%H:%M')}", "%Y-%m-%d %H:%M")
        dt_curr_start = datetime.strptime(f"{curr_start_date_str} {t_curr_start.strftime('%H:%M')}", "%Y-%m-%d %H:%M")

        if dt_curr_start < dt_prev_end:
            dt_curr_start += timedelta(days=1)

        diff_hours = (dt_curr_start - dt_prev_end).total_seconds() / 3600.0
        rest_str = f"{diff_hours:.1f}h"

        if diff_hours < 11.0:
            return rest_str, "red"
        elif diff_hours < 12.0:
            return rest_str, "amber"
        else:
            return rest_str, "green"
    except Exception:
        return None, None


# =========================================================
# 2. Excel 讀取與班表解析引擎 (補齊 services.py 所需的 9 個函式)
# =========================================================

def safe_read_excel(file_path: str, header: int = 3) -> pd.DataFrame:
    """安全讀取 Excel 檔案，支援 .xlsx 與 .xls"""
    if not os.path.exists(file_path):
        return pd.DataFrame()
    try:
        return pd.read_excel(file_path, header=header, dtype=str)
    except Exception:
        return pd.read_excel(file_path, header=header, engine="openpyxl", dtype=str)

def get_employee_name(df: pd.DataFrame, emp_id: str) -> str:
    """根據員工編號取得姓名"""
    if df is None or df.empty:
        return "組員"
    emp_id_str = str(emp_id).strip().upper()
    for _, row in df.iterrows():
        if str(row.iloc[0]).strip().upper() == emp_id_str:
            return str(row.iloc[1]).strip()
    return "組員"

def parse_cell(raw_cell: Any) -> Dict[str, Any]:
    """
    解析單一班表儲存格內容，自動擷取：
    - start: 報到時間 (HH:MM)
    - end: 退勤時間 (HH:MM)
    - hours: 總工時字串 (如 8h30m)
    - train: 班別/車次代碼
    - note: 備註文字
    """
    if pd.isna(raw_cell) or raw_cell is None:
        return {"start": "", "end": "", "hours": "", "train": "無", "note": ""}

    text = str(raw_cell).strip()
    if not text or text.upper() in ["NAN", "NONE", ""]:
        return {"start": "", "end": "", "hours": "", "train": "無", "note": ""}

    # 搜尋時間區間 (支援 06:15-14:30、06:15~14:30 或多行時間)
    times = re.findall(r"\b(\d{1,2}:\d{2})\b", text)
    start_t = times[0] if len(times) >= 1 else ""
    end_t = times[1] if len(times) >= 2 else ""

    if start_t and len(start_t) == 4:
        start_t = "0" + start_t
    if end_t and len(end_t) == 4:
        end_t = "0" + end_t

    hours_str = ""
    if start_t and end_t:
        _, hours_str = calc_duty_duration(start_t, end_t)

    # 移除時間字串後，擷取第一行或主要字詞作為班別/車次代碼
    cleaned = re.sub(r"\b\d{1,2}:\d{2}\s*[-~～至]?\s*\d{1,2}:\d{2}\b", "", text).strip()
    lines = [line.strip() for line in cleaned.splitlines() if line.strip()]
    train_code = lines[0] if lines else text.splitlines()[0].strip()
    note_str = " ".join(lines[1:]) if len(lines) > 1 else ""

    return {
        "start": start_t,
        "end": end_t,
        "hours": hours_str,
        "train": train_code if train_code else "無",
        "note": note_str,
    }

def is_cell_off_day(raw_cell: Any) -> bool:
    """判斷該儲存格是否為休假日 (DO / RD / 休 / 例 / 假 / 特休 / 空白)"""
    if pd.isna(raw_cell) or raw_cell is None:
        return True
    text = str(raw_cell).strip().upper()
    if not text or text in ["NAN", "NONE", "-", "/"]:
        return True

    # 若包含明確的上下班時間，則視為出勤日
    if re.search(r"\b\d{1,2}:\d{2}\b", text):
        return False

    off_keywords = ["DO", "RD", "OFF", "休", "例", "假", "年假", "特休", "事假", "病假", "公假", "補休", "婚假", "喪假"]
    for kw in off_keywords:
        if kw in text:
            return True
    return False

def is_overtime(hours_str: str, train_code: str = "", note: str = "") -> bool:
    """判斷單班工時是否超過 8.5 小時 (或標註加班)"""
    if "加班" in str(train_code) or "加班" in str(note) or "OT" in str(train_code).upper():
        return True
    if not hours_str:
        return False
    m = re.search(r"(\d+)h(\d+)m", str(hours_str))
    if m:
        total_hrs = int(m.group(1)) + int(m.group(2)) / 60.0
        return total_hrs > 8.5
    return False

def is_town_shift(train_code: str, note: str = "") -> bool:
    """判斷是否為非正線勤務 (如待命、備勤、訓練、地面勤務等)"""
    combined = f"{train_code} {note}".upper()
    non_mainline_keywords = ["待命", "備勤", "訓練", "講習", "地面", "內勤", "體檢", "會議", "STBY", "STANDBY", "TRN"]
    return any(kw in combined for kw in non_mainline_keywords)

def translate_train_code(train_code: str) -> str:
    """清理並格式化車次或勤務代碼顯示"""
    if not train_code or str(train_code).strip().upper() in ["NAN", "NONE", ""]:
        return "無"
    return str(train_code).strip()

def calculate_consecutive_work_days(row: pd.Series, target_col_idx: int, all_cols: List[str]) -> int:
    """計算截至 target_col_idx 當天的連續出勤天數"""
    streak = 0
    for idx in range(target_col_idx, 1, -1):
        col_name = str(all_cols[idx]).strip()
        if not re.search(r"(\d+/\d+)", col_name):
            continue
        if is_cell_off_day(row.iloc[idx]):
            break
        streak += 1
    return streak

def check_shift_legality(row: pd.Series, col_idx: int, all_cols: List[str]) -> Tuple[bool, str, Dict[str, Any]]:
    """
    檢核當日班別與前一日班別之班間休息間隔與連續出勤合法性
    回傳: (是否合法, 警告訊息, {"min_interval": float | None, "consecutive_days": int})
    """
    consecutive_days = calculate_consecutive_work_days(row, col_idx, all_cols)
    curr_parsed = parse_cell(row.iloc[col_idx])

    if not curr_parsed["start"]:
        return True, "", {"min_interval": 12.0, "consecutive_days": consecutive_days}

    # 尋找前一個日期欄位
    prev_col_idx = -1
    for idx in range(col_idx - 1, 1, -1):
        if re.search(r"(\d+/\d+)", str(all_cols[idx]).strip()):
            prev_col_idx = idx
            break

    min_interval = 12.0
    if prev_col_idx != -1 and not is_cell_off_day(row.iloc[prev_col_idx]):
        prev_parsed = parse_cell(row.iloc[prev_col_idx])
        if prev_parsed["end"]:
            t_prev_end = parse_time_str(prev_parsed["end"])
            t_curr_start = parse_time_str(curr_parsed["start"])
            if t_prev_end and t_curr_start:
                dt_prev = datetime(2026, 1, 1, t_prev_end.hour, t_prev_end.minute)
                # 若前一日退勤時間 <= 報到時間，代表前一日班別跨夜至今日凌晨
                t_prev_start = parse_time_str(prev_parsed["start"])
                if t_prev_start and t_prev_end <= t_prev_start:
                    dt_prev += timedelta(days=1)

                dt_curr = datetime(2026, 1, 2, t_curr_start.hour, t_curr_start.minute)
                diff_hrs = round((dt_curr - dt_prev).total_seconds() / 3600.0, 1)
                if diff_hrs >= 0:
                    min_interval = diff_hrs

    warnings = []
    is_legal = True
    if min_interval < 11.0:
        is_legal = False
        warnings.append(f"班間休息僅 {min_interval}h（低於 11h 法定下限）")
    if consecutive_days > 6:
        is_legal = False
        warnings.append(f"已連續出勤 {consecutive_days} 天")

    return is_legal, "；".join(warnings), {"min_interval": min_interval, "consecutive_days": consecutive_days}
