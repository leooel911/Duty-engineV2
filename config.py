# ==========================================
# CREW DUTY ENGINE V2 - 全域設定與法規參數
# ==========================================

# 1. 單位與基地設定
DEFAULT_UNIT = "TTN"
UNIT_NAME = "台中乘務區"

# 2. 勞基法與排班合規門檻 (單位：小時)
COMPLIANCE_RULES = {
    "MIN_REST_HOURS": 11.0,       # 法定最低班間休息門檻
    "WARNING_REST_HOURS": 12.0,   # 臨界預警門檻
    "LONG_DUTY_HOURS": 8.5,       # 長班工時標記門檻
    "MAX_CONSECUTIVE_DAYS": 6,    # 連續出勤上限天數
}

# 3. 班表語意色彩系統 (5色視覺語意 + 輔助色)
COLOR_PALETTE = {
    "blue": "#4C9AE0",        # 正常出勤 / 主色
    "amber": "#E3A13D",       # 班間臨界 / 工時>8.5h / 國定假日
    "red": "#E1615C",         # 班間不足 / 違規 / 排定休假
    "green": "#4FB88A",       # 班間合規 / 特休 / 正常狀態
    "purple": "#9B8CE0",      # 破輪 / 雙拼班
    "grey": "#7A8794",        # 非正線 / 偏駐 / TOWN
}

# 4. 休假與非正線勤務代號對照
OFF_DUTY_CODES = {
    "DO": "休假",
    "DO1": "排休 DO1",
    "DO3X": "排休 DO3X",
    "AL": "特休",
    "SL": "病假",
    "CL": "事假",
}

SPECIAL_DUTY_CODES = {
    "TOWN": {"label": "偏駐/外站", "color": "grey", "bar": "town"},
    "TRAIN": {"label": "訓練勤務", "color": "purple", "bar": "split"},
}

# 5. 國定假日與疏運期清單 (可依年度隨時擴充)
HOLIDAY_DATES = {
    "2026-09-24": "中秋節",
    "2026-09-25": "中秋疏運",
    "2026-10-10": "國慶日",
    "2026-10-11": "國慶疏運",
}
