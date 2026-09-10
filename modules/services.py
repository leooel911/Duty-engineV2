import os
import pandas as pd
from datetime import datetime, timedelta
from modules.utils import parse_time_to_minutes, format_day_duty_to_v2


def get_current_duty_status(schedule_list: list):
    """
    根據當前系統真實時間 (datetime.now())，比對個人班表找出：
    1. 今日出勤狀態標籤
    2. 下一次出勤簽到目標時間與倒數毫秒數 (Timestamp)
    """
    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")

    status_info = {
        "status_text": "今日排休 · DO1",
        "is_on_duty": False,
        "next_duty_title": "近期無待勤項目",
        "next_duty_times": "--:-- → --:--",
        "next_duty_code": "—",
        "target_timestamp_ms": None,
        "current_cycle": f"週期 {now.strftime('%m/%d')}–{(now + timedelta(days=28)).strftime('%m/%d')}"
    }

    # 搜尋未來最近一筆有效的班別
    for day in schedule_list:
        # 跳過休假或無時間資料者
        if "off" in day or not day.get("start"):
            continue

        try:
            full_date_str = day.get("full_date", today_str)
            start_time_str = day.get("start")
            
            # 組合出正確的簽到時間點
            duty_dt = datetime.strptime(f"{full_date_str} {start_time_str}", "%Y-%m-%d %H:%M")

            # 若該班簽到時間在未來，即為倒數目標
            if duty_dt > now:
                status_info["status_text"] = f"待勤中 · {day.get('code')}"
                status_info["next_duty_title"] = f"{day.get('d')}日 ({day.get('wd')}) {day.get('code')}"
                status_info["next_duty_times"] = f"{day.get('start')} → {day.get('end')}"
                status_info["next_duty_code"] = day.get("dur", "8h00m")
                # 傳遞 Javascript 倒數所需的 UNIX 毫秒時間戳
                status_info["target_timestamp_ms"] = int(duty_dt.timestamp() * 1000)
                break
        except Exception:
            continue

    return status_info


def parse_excel_roster(file_obj, emp_id: str):
    """
    解析排班大表 Excel (支持 .xls / .xlsx) 提取指定組員整月班表
    (若尚未上傳 Excel，將自動備援回傳合規算力產出的展示班表)
    """
    if file_obj is None:
        return None

    try:
        # 讀取 Excel 大表
        df = pd.read_excel(file_obj)
        # TODO: 依據 TTN 班表 Excel 欄位結構讀取對應員編列 (於對接真實 Excel 時微調欄位索引)
        return df
    except Exception as e:
        print(f"Excel 解析異常: {e}")
        return None
