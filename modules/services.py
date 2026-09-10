from datetime import datetime, timedelta
import pandas as pd
from modules.utils import parse_time_to_minutes


def get_current_duty_status(schedule_list: list):
    """
    根據目前真實時間，比對班表找出：
    1. 今日出勤狀態 (休假/上班中/待勤中)
    2. 下一次出勤簽到時間點 (用於 Hero 倒數計時器)
    """
    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")

    # 預設狀態
    status_info = {
        "status_text": "今日排休",
        "is_on_duty": False,
        "next_duty_title": "無即將出勤項目",
        "next_duty_time_str": "--:-- → --:--",
        "next_duty_code": "—",
        "target_timestamp_ms": None,  # 給前端 JS 倒數計時用的毫秒時間戳
    }

    # 尋找未來最近的一班出勤
    for day in schedule_list:
        # 跳過休假或無效資料
        if "off" in day or not day.get("start"):
            continue

        # 組合出該班別的簽到 DateTime
        try:
            full_date_str = day.get("full_date", today_str)
            start_time_str = day.get("start")
            duty_datetime = datetime.strptime(f"{full_date_str} {start_time_str}", "%Y-%m-%d %H:%M")

            # 如果這個簽到時間在未來（尚未到來），這就是我們要倒數的目標班別！
            if duty_datetime > now:
                status_info["next_duty_title"] = f"{day.get('d')}日 ({day.get('wd')}) {day.get('code')}"
                status_info["next_duty_time_str"] = f"{day.get('start')} → {day.get('end')}"
                status_info["next_duty_code"] = day.get("dur", "8h00m")
                # 轉為 JS 可直接使用毫秒 Timestamp
                status_info["target_timestamp_ms"] = int(duty_datetime.timestamp() * 1000)
                status_info["status_text"] = "待勤中 · 預備簽到"
                break
        except Exception:
            continue

    return status_info
