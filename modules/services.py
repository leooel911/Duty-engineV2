"""
CREW DUTY ENGINE V2 - Master Schedule Parser & Search Engine
100% 動態大表解析器 (限定單位：北轉 TTN / 中轉 TTC / 南轉 TTS)
"""
from datetime import datetime, timedelta
import re
import pandas as pd
from modules.utils import calc_duty_duration, calc_rest_interval, parse_time_str

def extract_unit_from_excel(df: pd.DataFrame):
    """動態掃描 Excel 表頭，辨識基地單位 (嚴格限定：北轉 TTN / 中轉 TTC / 南轉 TTS)"""
    if df is None or df.empty:
        return "TTN", "北轉"

    header_text = " ".join(df.iloc[:5].fillna("").astype(str).values.flatten())

    unit_mapping = {
        "台北": ("TTN", "北轉"),
        "北轉": ("TTN", "北轉"),
        "台中": ("TTC", "中轉"),
        "中轉": ("TTC", "中轉"),
        "左營": ("TTS", "南轉"),
        "南轉": ("TTS", "南轉"),
    }

    for key, (code, name) in unit_mapping.items():
        if key in header_text:
            return code, name

    return "TTN", "北轉"

def parse_cell_duty_info(cell_value: str):
    """從 Excel 儲存格提取班號與簽到退時間 (如 'NG0001\\n05:26-15:06' 或 'NF0018 07:24~15:24')"""
    if not isinstance(cell_value, str) or not cell_value.strip() or cell_value.strip().lower() == "nan":
        return None

    text = cell_value.strip()
    times = re.findall(r"(\d{1,2}:\d{2})", text)
    
    # 判斷是否為休假格
    if any(k in text.upper() for k in ["DO", "OFF", "休", "特休", "例休"]):
        code = text.split()[0] if text.split() else "DO1"
        return {"off": code, "tags": ["休假日"]}

    start_t, end_t = "07:30", "15:30"
    if len(times) >= 2:
        start_t, end_t = times[0], times[1]

    code = text.split("\n")[0].split()[0] if text else "DUTY"
    hrs_num, dur_str = calc_duty_duration(start_t, end_t)

    tags = []
    if hrs_num > 8.5:
        tags.append("工時>8.5h")

    return {
        "code": code,
        "start": start_t,
        "end": end_t,
        "dur": dur_str,
        "tags": tags
    }

def parse_master_excel(file_obj):
    """
    全動態大表 Excel 解析主函式
    讀取包含所有組員月度班表的 Excel 檔，回傳所有組員之結構化資料
    """
    if file_obj is None:
        return False, {}, None, ("TTN", "北轉")

    try:
        excel_file = pd.ExcelFile(file_obj)
        df = excel_file.parse(excel_file.sheet_names[0], header=None)
        unit_code, unit_name = extract_unit_from_excel(df)

        # 搜尋表頭中的日期列與日期數
        now = datetime.now()
        rosters = {}  # emp_id -> crew_info + daily_schedule

        # 遍歷所有 Dataframe 列尋找組員資料列
        for idx, row in df.iterrows():
            row_vals = row.fillna("").astype(str).tolist()
            row_str = " ".join(row_vals)

            # 搜尋格式如 A026047 或姓名列
            emp_match = re.search(r"([A-Z]\d{6})", row_str)
            if not emp_match:
                continue

            emp_id = emp_match.group(1)
            
            # 尋找姓名與職稱
            name = "組員"
            role_title = "服勤員"
            for v in row_vals[:5]:
                v_clean = v.strip()
                if v_clean and not re.search(r"[A-Z]\d{6}", v_clean) and len(v_clean) <= 4:
                    if any(c in v_clean for c in ["員", "長", "駕駛", "車務", "服勤"]):
                        role_title = "駕駛" if "駕" in v_clean else ("列車長" if "長" in v_clean else "服勤員")
                    elif len(v_clean) >= 2:
                        name = v_clean

            # 解析 1~31 日班表
            days_schedule = []
            prev_end_date = None
            prev_end_time = None

            day_counter = 1
            for col_idx in range(3, len(row_vals)):
                if day_counter > 31:
                    break
                
                cell_raw = row_vals[col_idx]
                duty_info = parse_cell_duty_info(cell_raw)
                
                if not duty_info:
                    day_counter += 1
                    continue

                curr_date_str = f"{now.year}-{now.month:02d}-{day_counter:02d}"
                wd_list = ["日", "一", "二", "三", "四", "五", "六"]
                try:
                    wd_str = wd_list[datetime.strptime(curr_date_str, "%Y-%m-%d").weekday()]
                except Exception:
                    wd_str = "一"

                entry = {
                    "d": day_counter,
                    "wd": wd_str,
                    "full_date": curr_date_str
                }

                if "off" in duty_info:
                    entry["off"] = duty_info["off"]
                    entry["barType"] = "off"
                    entry["tags"] = duty_info["tags"]
                    prev_end_date = None
                    prev_end_time = None
                else:
                    entry["code"] = duty_info["code"]
                    entry["start"] = duty_info["start"]
                    entry["end"] = duty_info["end"]
                    entry["dur"] = duty_info["dur"]
                    entry["tags"] = duty_info["tags"]

                    # 計算與前一班之班間休息時間
                    if prev_end_date and prev_end_time:
                        rest_str, rest_tag = calc_rest_interval(prev_end_date, prev_end_time, curr_date_str, duty_info["start"])
                        entry["rest"] = rest_str
                        entry["restTag"] = rest_tag

                    prev_end_date = curr_date_str
                    prev_end_time = duty_info["end"]

                days_schedule.append(entry)
                day_counter += 1

            rosters[emp_id] = {
                "emp_id": emp_id,
                "name": name,
                "role_title": role_title,
                "unit": unit_code,
                "unit_name": unit_name,
                "schedule": days_schedule
            }

        return True, rosters, df, (unit_code, unit_name)

    except Exception as e:
        print(f"Excel 動態解析出錯: {e}")
        return False, {}, None, ("TTN", "北轉")

def build_exchange_candidates_dynamic(rosters: dict, target_date_idx: int = 15, time_from: str = "05:00", time_to: str = "10:00"):
    """根據大表動態計算可換班組員名單 (無 hardcode)"""
    result = {"服勤員": [], "駕駛": [], "列車長": []}
    
    tf_min = parse_time_str(time_from)
    tt_min = parse_time_str(time_to)
    if not tf_min or not tt_min:
        return result

    tf_val = tf_min.hour * 60 + tf_min.minute
    tt_val = tt_min.hour * 60 + tt_min.minute

    for emp_id, crew in rosters.items():
        sched = crew.get("schedule", [])
        matching_day = next((d for d in sched if d.get("d") == target_date_idx and "start" in d), None)
        if not matching_day:
            continue

        st_obj = parse_time_str(matching_day["start"])
        if not st_obj:
            continue

        st_val = st_obj.hour * 60 + st_obj.minute
        if tf_val <= st_val <= tt_val:
            role = crew.get("role_title", "服勤員")
            if role not in result:
                result[role] = []

            result[role].append({
                "id": emp_id,
                "name": crew["name"],
                "start": matching_day["start"],
                "end": matching_day["end"],
                "dur": matching_day["dur"],
                "restBefore": matching_day.get("rest", "12.0h"),
                "restTag": matching_day.get("restTag", "green"),
                "streak": f"當日勤務 · {matching_day['code']}"
            })

    return result
