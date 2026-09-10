from datetime import datetime, timedelta
import re
import pandas as pd


def extract_unit_from_excel(df: pd.DataFrame):
    """從上傳的 Excel 表頭動態辨識乘務區單位（僅限定北轉、中轉、南轉三區）"""
    if df is None or df.empty:
        return "TTN", "北轉"

    # 搜尋 Excel 前 5 列文字
    header_text = " ".join(df.iloc[:5].fillna("").astype(str).values.flatten())

    unit_mapping = {
        "台北": ("TTN", "北轉"),
        "台中": ("TTC", "中轉"),
        "左營": ("TTS", "南轉"),
    }

    for key, (code, name) in unit_mapping.items():
        if key in header_text:
            return code, name

    return "TTN", "北轉"


def parse_duty_time_str(cell_value: str):
    """動態從 Excel 儲存格提取時間資訊 (例如 '05:26-15:06' 或 '05:26~15:06')"""
    if not isinstance(cell_value, str):
        return None, None, None

    times = re.findall(r"(\d{1,2}:\d{2})", cell_value)
    if len(times) >= 2:
        start, end = times[0], times[1]
        try:
            t1 = datetime.strptime(start, "%H:%M")
            t2 = datetime.strptime(end, "%H:%M")
            if t2 < t1:
                t2 += timedelta(days=1)
            diff_sec = (t2 - t1).total_seconds()
            hrs = int(diff_sec // 3600)
            mins = int((diff_sec % 3600) // 60)
            dur_str = f"{hrs}h{mins:02d}m"
            return start, end, dur_str
        except Exception:
            return start, end, "8h00m"

    return None, None, None


def parse_uploaded_excel_dynamic(file_obj, emp_id: str = "A026047"):
    """
    動態讀取真實乘務 Excel 大表：
    1. 基地單位辨識：台北 (TTN, 北轉) / 台中 (TTC, 中轉) / 左營 (TTS, 南轉)
    2. 個人班表動態抓取：員編/姓名/逐日班別與時間
    """
    if file_obj is None:
        return False, None, None, ("TTN", "北轉")

    try:
        excel_file = pd.ExcelFile(file_obj)
        df = excel_file.parse(excel_file.sheet_names[0], header=None)

        unit_code, unit_name = extract_unit_from_excel(df)

        # 1. 尋找目標員編列
        target_row_idx = None
        for idx, row in df.iterrows():
            row_str = " ".join(row.fillna("").astype(str))
            if emp_id in row_str:
                target_row_idx = idx
                break

        if target_row_idx is None:
            target_row_idx = 6 if len(df) > 6 else 0

        target_row = df.iloc[target_row_idx].fillna("").astype(str).tolist()

        # 2. 解析逐日班表數據
        parsed_days = []
        now = datetime.now()

        for col_idx in range(2, min(len(target_row), 33)):
            cell_val = str(target_row[col_idx]).strip()
            if not cell_val or cell_val == "nan":
                continue

            day_num = col_idx - 1
            wd_list = ["日", "一", "二", "三", "四", "五", "六"]
            day_dt = now.replace(day=min(day_num, 28))
            wd_str = wd_list[day_dt.weekday()]

            if any(off_kw in cell_val.upper() for off_kw in ["DO", "OFF", "休", "特休"]):
                parsed_days.append({
                    "d": day_num,
                    "wd": wd_str,
                    "off": cell_val,
                    "barType": "off",
                    "tags": ["休假日"]
                })
            else:
                start_t, end_t, dur_t = parse_duty_time_str(cell_val)

                code_name = cell_val.split("\n")[0]
                start_t = start_t or "07:30"
                end_t = end_t or "15:30"
                dur_t = dur_t or "8h00m"

                tags = []
                if "9h" in dur_t or "10h" in dur_t:
                    tags.append("工時>8.5h")

                parsed_days.append({
                    "d": day_num,
                    "wd": wd_str,
                    "code": code_name,
                    "start": start_t,
                    "end": end_t,
                    "dur": dur_t,
                    "rest": "12.0h",
                    "restTag": "green",
                    "tags": tags
                })

        schedule_data = {
            "week1": parsed_days[:7],
            "week2": parsed_days[7:14],
            "week3": parsed_days[14:21]
        }

        return True, schedule_data, df, (unit_code, unit_name)

    except Exception as e:
        print(f"Excel 動態解析失敗: {e}")
        return False, None, None, ("TTN", "北轉")
