import streamlit as st

# 1. 頁面基礎設定
st.set_page_config(
    page_title="CREW DUTY ENGINE V2",
    page_icon="🚆",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# 2. 全域 CSS 設計變數注入 (暗黑科技風格 + 底部大拇指 Tab Bar)
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&family=IBM+Plex+Sans+TC:wght@400;500;600;700&display=swap');

    :root {
      --ink-900: #070B10;
      --ink-800: #0E141C;
      --ink-700: #141C26;
      --line: #232E3A;
      --line-soft: #1A222C;
      --paper: #ECF1F5;
      --dim: #8492A1;
      --dim-2: #59636E;
      --blue: #4C9AE0;
      --blue-dim: rgba(76,154,224,0.13);
      --amber: #E3A13D;
      --amber-dim: rgba(227,161,61,0.14);
      --red: #E1615C;
      --red-dim: rgba(225,97,92,0.14);
      --green: #4FB88A;
      --green-dim: rgba(79,184,138,0.14);
      --grey: #7A8794;
    }

    html, body, .stApp, [data-testid="stAppViewContainer"], .main, .block-container {
        background-color: var(--ink-900) !important;
        color: var(--paper) !important;
        font-family: 'IBM Plex Sans TC', 'IBM Plex Mono', sans-serif !important;
        -webkit-font-smoothing: antialiased;
        max-width: 100vw !important;
        overflow-x: hidden !important;
    }

    [data-testid="stMainBlockContainer"], .block-container {
        padding: 0.5rem 0.5rem 5.5rem 0.5rem !important;
        max-width: 480px !important;
        margin: 0 auto !important;
    }

    .topbar-card {
        display: flex; align-items: center; justify-content: space-between;
        padding: 12px 14px; background: linear-gradient(var(--ink-900) 70%, transparent);
        margin-bottom: 10px; position: sticky; top: 0; z-index: 20; backdrop-filter: blur(8px);
    }
    .brand-group { display: flex; align-items: center; gap: 9px; }
    .brand-mark {
        width: 28px; height: 28px; border-radius: 6px; background: var(--ink-700);
        border: 1px solid var(--line); display: flex; align-items: center;
        justify-content: center; font-size: 11px; font-weight: 700; color: var(--blue);
        font-family: 'IBM Plex Mono', monospace;
    }
    .brand-name { font-size: 13.5px; font-weight: 600; color: var(--paper); }
    .brand-sub { font-size: 9.5px; color: var(--dim-2); }

    .unit-chip {
        display: flex; align-items: center; gap: 6px; background: var(--ink-700);
        border: 1px solid var(--line); padding: 5px 12px; border-radius: 8px;
        font-size: 12px; font-weight: 600; color: var(--paper); font-family: monospace;
    }
    .unit-chip .dot { width: 6px; height: 6px; border-radius: 50%; background: var(--green); }

    .hero-card {
        border: 1px solid var(--line); border-radius: 14px;
        background: linear-gradient(165deg, var(--ink-700), var(--ink-800));
        padding: 18px 16px; margin-bottom: 14px;
    }

    .duty-row-card {
        display: flex; align-items: center; gap: 10px; padding: 10px 4px;
        border-bottom: 1px solid var(--line-soft);
    }
    .duty-date-box { width: 36px; flex: none; text-align: center; }
    .duty-date-box .d { font-family: 'IBM Plex Mono', monospace; font-size: 15px; font-weight: 600; color: var(--paper); }
    .duty-date-box .w { font-size: 9px; color: var(--dim-2); }
    
    .duty-bar { width: 3px; height: 36px; border-radius: 3px; flex: none; background: var(--blue); }
    .duty-bar.off { background: var(--red); }
    .duty-bar.holiday { background: var(--amber); }

    .duty-main-info { flex: 1; min-width: 0; }
    .duty-times { font-family: 'IBM Plex Mono', monospace; font-size: 14px; font-weight: 600; color: var(--paper); }
    .duty-meta { font-size: 10.5px; color: var(--dim-2); margin-top: 2px; display: flex; gap: 8px; }

    .tag-pill {
        font-size: 9px; font-weight: 600; padding: 2px 6px; border-radius: 4px;
        white-space: nowrap; font-family: 'IBM Plex Sans TC', sans-serif;
    }
    .tag-pill.blue { color: var(--blue); background: var(--blue-dim); }
    .tag-pill.amber { color: var(--amber); background: var(--amber-dim); }
    .tag-pill.red { color: var(--red); background: var(--red-dim); }

    div[data-testid="stRadio"] > label { display: none !important; }
    div[data-testid="stRadio"] > div {
        position: fixed !important; bottom: 0 !important; left: 50% !important;
        transform: translateX(-50%) !important; width: 100% !important;
        max-width: 480px !important; display: flex !important; flex-direction: row !important;
        background: rgba(14,20,28,0.96) !important; backdrop-filter: blur(12px) !important;
        border-top: 1px solid var(--line) !important; padding: 6px 4px calc(6px + env(safe-area-inset-bottom)) 4px !important;
        z-index: 9999 !important; justify-content: space-around !important;
    }
    div[data-testid="stRadio"] label {
        flex: 1 !important; text-align: center !important; padding: 8px 0 !important;
        margin: 0 !important; border-radius: 8px !important; background: transparent !important;
        color: var(--dim-2) !important; font-size: 12px !important; font-weight: 600 !important;
    }
    div[data-testid="stRadio"] label:has(input:checked) {
        color: var(--blue) !important; background: var(--blue-dim) !important;
    }

    button[data-testid="stBaseButton-primary"] {
        background: var(--blue) !important; color: var(--ink-900) !important;
        border: none !important; border-radius: 10px !important; font-weight: 700 !important;
        box-shadow: 0 4px 14px rgba(76,154,224,0.3) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 3. 頁首 Sticky Header
st.markdown(
    """
    <div class="topbar-card">
        <div class="brand-group">
            <div class="brand-mark">CD</div>
            <div>
                <div class="brand-name">CREW DUTY ENGINE</div>
                <div class="brand-sub">V2 Mobile Redesign · C.L.F</div>
            </div>
        </div>
        <div class="unit-chip"><span class="dot"></span>TTN</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# 4. 底部 Tab 頁籤控制
nav_tab = st.radio(
    "導覽選單",
    ["今日首頁", "月班表", "換班快搜", "換假快搜"],
    horizontal=True,
    label_visibility="collapsed",
    key="v2_main_tab",
)

# 5. 分頁畫面
if nav_tab == "今日首頁":
    st.markdown(
        """
        <div class="hero-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-size:11px; color:var(--amber); font-weight:600;">● V2 測試連線中</span>
                <span style="font-size:10.5px; color:var(--dim-2); font-family:monospace;">週期 09/06–10/03</span>
            </div>
            <div style="font-size: 12px; color: var(--dim); margin-top: 14px;">測試組員標記</div>
            <div style="font-size: 24px; font-weight: 700; color: var(--paper); font-family: monospace; margin-top: 2px;">
                A023001 <span style="font-size: 13px; color: var(--blue);">[TTN]</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.text_input("輸入員編測試", "A023001")
    st.button("開始測試圖片班表生成", type="primary", use_container_width=True)

elif nav_tab == "月班表":
    st.markdown('<div style="font-size:11px; color:var(--dim-2); font-weight:600; margin-bottom:8px;">個人月班表透視 · A023001</div>', unsafe_allow_html=True)
    sample_data = [
        {"d": "11", "w": "9月", "times": "05:26 → 15:06", "code": "NG0001", "dur": "9h40m", "tag": "工時>8.5h", "cls": "amber", "bar": ""},
        {"d": "12", "w": "9月", "times": "07:24 → 15:24", "code": "NF0018", "dur": "8h00m", "tag": "", "cls": "", "bar": ""},
        {"d": "13", "w": "9月", "times": "休假 (DO1)", "code": "DO", "dur": "0h00m", "tag": "休假日", "cls": "red", "bar": "off"},
    ]
    for row in sample_data:
        tag_html = f'<span class="tag-pill {row["cls"]}">{row["tag"]}</span>' if row["tag"] else ""
        st.markdown(
            f"""
            <div class="duty-row-card">
                <div class="duty-date-box"><div class="d">{row['d']}</div><div class="w">{row['w']}</div></div>
                <div class="duty-bar {row['bar']}"></div>
                <div class="duty-main-info">
                    <div class="duty-times">{row['times']}</div>
                    <div class="duty-meta"><span>{row['code']}</span><span>{row['dur']}</span></div>
                </div>
                {tag_html}
            </div>
            """,
            unsafe_allow_html=True,
        )

elif nav_tab == "換班快搜":
    st.selectbox("職位類別", ["服勤員", "列車長", "駕駛"])
    st.selectbox("換班日期", ["9/25 (中秋)", "9/26 (六)"])
    st.button("搜尋可換班名單", type="primary", use_container_width=True)

elif nav_tab == "換假快搜":
    st.info("V2 換假矩陣與合規驗證區塊")
