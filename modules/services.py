from datetime import datetime, timedelta
import re
import pandas as pd
from modules.utils import format_day_duty_to_v2


def get_current_duty_status(schedule_list: list):
    """根據當前系統時間 (datetime.now())，計算今日狀態與下一次簽到目標毫秒戳"""
    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")

    status_info = {
        "status_text": "今日排休",
        "is_on_duty": False,
        "next_duty_title": "近期無待勤項目",
        "next_duty_times": "--:-- → --:--",
        "next_duty_code": "—",
        "target_timestamp_ms": None,
        "current_cycle": f"週期 {now.strftime('%m/%d')}–{(now + timedelta(days=28)).strftime('%m/%d')}"
    }

    for day in schedule_list:
        if "off" in day or not day.get("start"):
            continue

        try:
            full_date_str = day.get("full_date", today_str)
            start_time_str = day.get("start")
            duty_dt = datetime.strptime(f"{full_date_str} {start_time_str}", "%Y-%m-%d %H:%M")

            if duty_dt > now:
                status_info["status_text"] = f"待勤中 · {day.get('code')}"
                status_info["next_duty_title"] = f"{day.get('d')}日 ({day.get('wd')}) {day.get('code')}"
                status_info["next_duty_times"] = f"{day.get('start')} → {day.get('end')}"
                status_info["next_duty_code"] = day.get("dur", "8h00m")
                status_info["target_timestamp_ms"] = int(duty_dt.timestamp() * 1000)
                break
        except Exception:
            continue

    return status_info


def parse_excel_roster(file_obj, emp_id: str):
    """
    解析乘務 Excel 班表大表，抓取指定員編 (emp_id) 的整月班表
    """
    if file_obj is None:
        return None

    try:
        # 讀取 Excel 檔案
        df = pd.read_excel(file_obj, header=None)
        
        # 搜尋包含員編的目標列 (Row)
        target_row_idx = None
        for idx, row in df.iterrows():
            row_str = row.astype(str).str.cat(sep=' ')
            if emp_id in row_str:
                target_row_idx = idx
                break

        if target_row_idx is None:
            return None

        # 擷取該員編列的班號數據（擴充備用）
        user_row = df.iloc[target_row_idx].dropna().tolist()
        return user_row

    except Exception as e:
        print(f"Excel 解析異常: {e}")
        return None
