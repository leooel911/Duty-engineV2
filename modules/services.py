from datetime import datetime, timedelta
import pandas as pd
from modules.utils import format_day_duty_to_v2


def extract_unit_from_excel(df: pd.DataFrame):
    """自動掃描 Excel 表頭，辨識所屬乘務區單位"""
    if df is None or df.empty:
        return "TTN", "台中乘務區"

    header_text = " ".join(df.iloc[:5].fillna("").astype(str).values.flatten())

    unit_mapping = {
        "台北": ("TPN", "台北乘務區"),
        "台中": ("TTN", "台中乘務區"),
        "左營": ("ZUN", "左營乘務區"),
        "新竹": ("HCN", "新竹乘務區"),
    }

    for key, (code, name) in unit_mapping.items():
        if key in header_text:
            return code, name

    return "TTN", "台中乘務區"


def get_current_duty_status(schedule_list: list):
    """計算今日出勤狀態與下一次簽到倒數"""
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
    """解析上傳的大表 Excel 檔案"""
    if uploaded_file is None:
        return False, "尚未選擇任何檔案", None, ("TTN", "台中乘務區")

    try:
        df = pd.read_excel(uploaded_file)
        unit_code, unit_name = extract_unit_from_excel(df)
        row_count, _ = df.shape
        
        sync_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        summary_msg = f"成功解析【{unit_name}】乘務大表！共 {row_count} 列資料，更新時間：{sync_time}"
        
        return True, summary_msg, df, (unit_code, unit_name)
    except Exception as e:
        return False, f"Excel 解析失敗：{str(e)}", None, ("TTN", "台中乘務區")
