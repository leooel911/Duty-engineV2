import io
import json
import os
import sys

# 🛠️ 自動加入專案根目錄，解決跨資料夾引用 config.py 問題
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import re
import smtplib
from datetime import date, datetime, timedelta, timezone
from email.header import Header
from email.mime.text import MIMEText
from typing import Any, Dict, List, Optional, Tuple, Union

import pandas as pd
import streamlit as st

try:
    from config import (
        DATA_DIR,
        LEAVE_CODES,
        LOG_FILE,
        NATIONAL_HOLIDAYS,
        TAIWAN_TZ,
        UNITS,
    )
except ImportError:
    DATA_DIR = os.path.join(BASE_DIR, "data")
    LOG_FILE = os.path.join(DATA_DIR, "activity_log.txt")
    TAIWAN_TZ = timezone(timedelta(hours=8))
    LEAVE_CODES = ["PAY", "FAC", "LEV", "MLP", "MTR", "UNP"]
    NATIONAL_HOLIDAYS = {}
    UNITS = {}

# (此處接續原本 utils.py 的完整內容)
