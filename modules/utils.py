"""
CREW DUTY ENGINE V2 - Compliance & Time Math Engine
全動態班間休息、工時、連續出勤與合規檢核算力模組
"""
from datetime import datetime, timedelta
import re

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
