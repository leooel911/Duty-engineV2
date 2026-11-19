"""
CREW DUTY ENGINE V2 - Global Configuration & Paths
全站路徑、單位班表、系統設定與日誌路徑配置檔
"""
import os

# 專案根目錄
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 資料與上傳檔案目錄
DATA_DIR = os.path.join(BASE_DIR, "data")
FEEDBACK_IMG_DIR = os.path.join(DATA_DIR, "feedback_images")

# 設定檔與日誌檔案路徑
SYSTEM_CONFIG_FILE = os.path.join(DATA_DIR, "system_config.json")
WHITELIST_FILE = os.path.join(DATA_DIR, "whitelist.json")
LOG_FILE = os.path.join(DATA_DIR, "system_logs.json")

# 自動建立必要資料夾，避免讀寫時找不到目錄
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(FEEDBACK_IMG_DIR, exist_ok=True)

# 各單位班表對應路徑
UNITS = {
    "TTN": {
        "服勤員": os.path.join(DATA_DIR, "TTN_TA.xlsx"),
        "駕駛": os.path.join(DATA_DIR, "TTN_TD.xlsx"),
        "列車長": os.path.join(DATA_DIR, "TTN_TM.xlsx"),
    },
    "TTC": {
        "服勤員": os.path.join(DATA_DIR, "TTC_TA.xlsx"),
        "駕駛": os.path.join(DATA_DIR, "TTC_TD.xlsx"),
        "列車長": os.path.join(DATA_DIR, "TTC_TM.xlsx"),
    },
    "TTS": {
        "服勤員": os.path.join(DATA_DIR, "TTS_TA.xlsx"),
        "駕駛": os.path.join(DATA_DIR, "TTS_TD.xlsx"),
        "列車長": os.path.join(DATA_DIR, "TTS_TM.xlsx"),
    },
}
