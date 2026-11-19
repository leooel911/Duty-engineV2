"""
CREW DUTY ENGINE V2 - Admin Console Views
系統管理員控制台（大表上傳、白名單管理、系統操作日誌）
"""
import json
import os
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd
import streamlit as st

# 自動錨定專案根目錄與路徑，不依賴外部 config.py 避免 ImportError
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
WHITELIST_FILE = os.path.join(DATA_DIR, "whitelist.json")
LOG_FILE = os.path.join(DATA_DIR, "system_logs.json")

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


def _get_file_mtime_str(file_path: str) -> str:
    if not file_path or not os.path.exists(file_path):
        return "尚未上傳檔案"
    try:
        mtime = os.path.getmtime(file_path)
        return datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return "未知時間"


def _load_activity_logs() -> List[Dict[str, Any]]:
    if not os.path.exists(LOG_FILE):
        return []
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            return json.loads(content) if content else []
    except Exception:
        return []


def _log_activity(action: str, user: str = "ADMIN") -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    logs = _load_activity_logs()
    logs.insert(
        0,
        {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user": user,
            "action": action,
        },
    )
    try:
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(logs[:500], f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def clear_logs() -> None:
    for p in [LOG_FILE, "activity.log", os.path.join(DATA_DIR, "activity.log")]:
        if os.path.exists(p):
            try:
                open(p, "w", encoding="utf-8").close()
            except Exception:
                pass


def load_whitelist(unit_code: str = "TTN") -> Dict[str, Any]:
    if os.path.exists(WHITELIST_FILE):
        try:
            with open(WHITELIST_FILE, "r", encoding="utf-8") as f:
                return json.load(f).get(unit_code, {})
        except Exception:
            return {}
    return {}


def save_whitelist(unit_code: str, unit_data: Dict[str, Any]) -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    full_data = {}
    if os.path.exists(WHITELIST_FILE):
        try:
            with open(WHITELIST_FILE, "r", encoding="utf-8") as f:
                full_data = json.load(f)
        except Exception:
            pass
    full_data[unit_code] = unit_data
    with open(WHITELIST_FILE, "w", encoding="utf-8") as f:
        json.dump(full_data, f, ensure_ascii=False, indent=2)


def render_admin_panel() -> None:
    current_unit = st.session_state.get("current_unit", "TTN")

    col_t, col_u, col_b = st.columns([2.5, 1.2, 1])
    with col_t:
        st.markdown("## ⚙️ 系統管理員控制台 (Admin Console)")
    with col_u:
        unit_opts = list(UNITS.keys())
        selected_u = st.selectbox(
            "營運單位",
            unit_opts,
            index=unit_opts.index(current_unit) if current_unit in unit_opts else 0,
        )
        if selected_u != current_unit:
            st.session_state["current_unit"] = selected_u
            st.rerun()
    with col_b:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        if st.button("返回前台首頁", type="primary", use_container_width=True):
            st.session_state["nav_mode"] = "user"
            st.session_state["admin_logged_in"] = False
            st.rerun()

    tab1, tab2, tab3 = st.tabs(["大表檔案上傳", "白名單管理", "系統日誌"])

    with tab1:
        st.markdown(f"### [{current_unit}] 乘務大表覆蓋上傳")
        unit_files = UNITS.get(current_unit, {})
        cols = st.columns(3)
        roles = [("駕駛", "TD", cols[0]), ("列車長", "TM", cols[1]), ("服勤員", "TA", cols[2])]
        for role_name, role_code, col in roles:
            with col:
                st.markdown(f"#### {role_name} ({role_code})")
                target_p = unit_files.get(role_name, "")
                st.caption(f"最後更新：{_get_file_mtime_str(target_p)}")
                up_file = st.file_uploader(
                    f"上傳 {role_name} Excel", type=["xlsx", "xls"], key=f"up_{role_code}"
                )
                if up_file and st.button(
                    f"確認更新 {role_name} 大表", key=f"btn_{role_code}", type="primary"
                ):
                    os.makedirs(os.path.dirname(target_p), exist_ok=True)
                    with open(target_p, "wb") as f:
                        f.write(up_file.getbuffer())
                    st.success(f"[{current_unit}] {role_name} 大表已更新！")
                    _log_activity(f"管理員上傳 {current_unit} - {role_name} 大表")
                    st.rerun()

    with tab2:
        st.markdown(f"### [{current_unit}] 白名單與組員權限設定")
        wl_data = load_whitelist(current_unit)
        uid_input = st.text_input("員編 / 帳號 ID", placeholder="例如: A026048")
        uname_input = st.text_input("姓名", placeholder="例如: 波莉")
        role_input = st.selectbox("權限角色", ["TESTER", "VIP_USER", "ADMIN"])
        if st.button("儲存 / 更新白名單人員", type="primary"):
            if uid_input.strip():
                clean_uid = uid_input.strip().upper()
                wl_data[clean_uid] = {"name": uname_input.strip(), "role": role_input}
                save_whitelist(current_unit, wl_data)
                _log_activity(f"更新白名單人員：{clean_uid} ({role_input})")
                st.success(f"已成功更新白名單：{clean_uid}")
                st.rerun()

    with tab3:
        st.markdown("### 系統操作日誌")
        logs = _load_activity_logs()
        if logs:
            st.dataframe(pd.DataFrame(logs), use_container_width=True, height=350)
        else:
            st.info("尚無日誌紀錄")
