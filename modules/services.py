from datetime import datetime, timedelta
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


def process_uploaded_excel(uploaded_file):
    """
    處理並驗證上傳的乘務大表 Excel
    傳回：(是否成功, 解析報告/訊息, Dataframe數據集)
    """
    if uploaded_file is None:
        return False, "尚未上傳任何檔案", None

    try:
        # 讀取 Excel 檔案
        df = pd.read_excel(uploaded_file)
        row_count, col_count = df.shape
        
        sync_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        summary_msg = f"成功解析班表！共讀取 {row_count} 列資料，最後同步時間：{sync_time}"
        
        return True, summary_msg, df
    except Exception as e:
        return False, f"Excel 檔案格式解析失敗：{str(e)}", None
