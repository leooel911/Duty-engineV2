import re
from datetime import datetime
from config import COMPLIANCE_RULES, HOLIDAY_DATES, OFF_DUTY_CODES


def parse_time_to_minutes(time_str: str):
    """將 HH:MM 時間字串 (支援 24:16 等跨日格式) 轉換為分鐘數"""
    if not time_str or not isinstance(time_str, str):
        return None
    match = re.match(r"^(\d{1,2}):(\d{2})$", time_str.strip())
    if not match:
        return None
    hours, minutes = map(int, match.groups())
    return hours * 60 + minutes


def calculate_rest_interval(prev_end_time: str, curr_start_time: str):
    """
    計算前一班下班至下一班上班之間的班間休息小時數與合規狀態
    - green: >= 12.0h (完全合規)
    - amber: 11.0h ~ 11.9h (臨界)
    - red: < 11.0h (違規/不建議換班)
    """
    prev_end_min = parse_time_to_minutes(prev_end_time)
    curr_start_min = parse_time_to_minutes(curr_start_time)

    if prev_end_min is None or curr_start_min is None:
        return None, None

    # 跨日班間休息算式：(下一班簽到時間 + 24小時) - 前一班簽退時間
    rest_minutes = (curr_start_min + 1440) - prev_end_min
    rest_hours = round(rest_minutes / 60.0, 1)

    if rest_hours >= COMPLIANCE_RULES["WARNING_REST_HOURS"]:
        tag = "green"
    elif rest_hours >= COMPLIANCE_RULES["MIN_REST_HOURS"]:
        tag = "amber"
    else:
        tag = "red"

    return f"{rest_hours}h", tag


def format_day_duty_to_v2(date_info: dict, duty_code: str, start_time: str = "", end_time: str = "", duration_str: str = "", prev_end_time: str = None):
    """將單日班表轉換為 V2 前端需要的 JSON 字典格式"""
    
    # 判斷是否為休假代號
    if duty_code in OFF_DUTY_CODES:
        return {
            "d": date_info.get("day"),
            "wd": date_info.get("weekday"),
            "off": OFF_DUTY_CODES.get(duty_code, duty_code),
            "barType": "off",
            "tags": ["休假日"]
        }

    # 計算班間休息
    rest_str, rest_tag = None, None
    if prev_end_time:
        rest_str, rest_tag = calculate_rest_interval(prev_end_time, start_time)

    tags = []
    # 工時判斷 (> 8.5 小時)
    dur_min = parse_time_to_minutes(duration_str) if duration_str else 0
    if dur_min and dur_min > (COMPLIANCE_RULES["LONG_DUTY_HOURS"] * 60):
        tags.append("工時>8.5h")

    # 國定假日判斷
    full_date = date_info.get("full_date")
    if full_date in HOLIDAY_DATES:
        tags.append("國定假日")

    return {
        "d": date_info.get("day"),
        "wd": date_info.get("weekday"),
        "code": duty_code,
        "start": start_time,
        "end": end_time,
        "dur": duration_str,
        "rest": rest_str,
        "restTag": rest_tag,
        "tags": tags
    }
