"""
CREW DUTY ENGINE V2 - Dispatch Terminal
整合直覺式前台上傳入口與無縫後台控制
"""
import json
from datetime import datetime
import streamlit as st
import streamlit.components.v1 as components

from modules.services import parse_master_excel, build_exchange_candidates_dynamic

# 1. 頁面初始化
st.set_page_config(
    page_title="CREW DUTY ENGINE — Dispatch Terminal",
    page_icon="🚆",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 2. 全域 Session State
if "all_rosters" not in st.session_state:
    st.session_state.all_rosters = {}
if "current_emp_id" not in st.session_state:
    st.session_state.current_emp_id = None
if "current_unit_code" not in st.session_state:
    st.session_state.current_unit_code = "--"
if "current_unit_name" not in st.session_state:
    st.session_state.current_unit_name = "未載入"
if "last_sync_time" not in st.session_state:
    st.session_state.last_sync_time = "尚未同步"
if "user_role" not in st.session_state:
    st.session_state.user_role = "ADMIN"

# 3. 側邊欄：管理者與大表上傳控制台
with st.sidebar:
    st.title("⚙️ 乘務調度控制台")
    st.caption("CREW DUTY ENGINE V2 · Real-Data Engine")
    st.divider()

    # 權限切換
    role_option = st.radio("系統權限", ["👑 系統管理者 (ADMIN)", "🚆 一般乘務組員 (CREW)"], index=0)
    st.session_state.user_role = "ADMIN" if "ADMIN" in role_option else "CREW"

    # 上傳大表
    st.subheader("📤 乘務大表 Excel 上傳")
    uploaded_file = st.file_uploader("選擇月度大表 Excel (.xls, .xlsx)", type=["xls", "xlsx"])
    
    if uploaded_file is not None:
        success, rosters, df, (u_code, u_name) = parse_master_excel(uploaded_file)
        if success and rosters:
            st.session_state.all_rosters = rosters
            st.session_state.current_unit_code = u_code
            st.session_state.current_unit_name = u_name
            st.session_state.last_sync_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            st.session_state.current_emp_id = list(rosters.keys())[0]
            st.success(f"成功解析【{u_name} ({u_code})】大表！共 {len(rosters)} 位組員。")
            st.dataframe(df.head(10), use_container_width=True)
        else:
            st.error("大表解析失敗，請確認檔案格式是否正確。")

    # 動態組員切換
    st.divider()
    st.subheader("👤 模擬登入 / 切換組員")
    if st.session_state.all_rosters:
        emp_options = {f"{info['name']} ({emp}) - {info['role_title']}": emp for emp, info in st.session_state.all_rosters.items()}
        selected_label = st.selectbox("切換檢視組員", list(emp_options.keys()))
        st.session_state.current_emp_id = emp_options[selected_label]
    else:
        st.warning("⚠️ 請上傳 Excel 大表以載入基地組員名單。")

    st.divider()
    st.metric("大表基地", f"{st.session_state.current_unit_name} ({st.session_state.current_unit_code})")
    st.metric("最後同步", st.session_state.last_sync_time)

# 4. 滿版 CSS + 側邊欄按鈕強化
st.markdown(
    """
    <style>
    [data-testid="stHeader"] { background: transparent !important; height: 0px !important; }
    [data-testid="stToolbar"], footer { display: none !important; }

    [data-testid="stSidebarCollapsedControl"], button[aria-label="Open sidebar"] {
        position: fixed !important;
        top: 10px !important;
        left: 10px !important;
        z-index: 99999999 !important;
        background-color: rgba(20, 28, 38, 0.85) !important;
        border: 1px solid #232E3A !important;
        border-radius: 8px !important;
        color: #4C9AE0 !important;
        backdrop-filter: blur(8px) !important;
    }

    html, body, .stApp, [data-testid="stAppViewContainer"] {
        padding: 0 !important; margin: 0 !important; background-color: #070B10 !important;
        overflow: hidden !important; height: 100dvh !important;
    }
    [data-testid="stMainBlockContainer"], .block-container {
        padding: 0 !important; margin: 0 !important; max-width: 100% !important;
        height: 100dvh !important; overflow: hidden !important;
    }
    div[data-testid="stElementContainer"] { margin: 0 !important; padding: 0 !important; }
    iframe {
        border: none !important; width: 100vw !important; height: 100dvh !important;
        position: fixed !important; top: 0 !important; left: 0 !important; z-index: 99999 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 5. 抓取當前真實選取的組員資料
current_crew = None
if st.session_state.all_rosters and st.session_state.current_emp_id:
    current_crew = st.session_state.all_rosters.get(st.session_state.current_emp_id)

user_sched = current_crew["schedule"] if current_crew else []
formatted_schedule = {
    "week1": user_sched[:7],
    "week2": user_sched[7:14],
    "week3": user_sched[14:21]
}

dynamic_exchange = build_exchange_candidates_dynamic(st.session_state.all_rosters)

# 6. 純前端 HTML 模板 (含點擊自動開啟管理側邊欄 JS)
RAW_HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
<title>CREW DUTY ENGINE — Dispatch Terminal</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&family=IBM+Plex+Sans+TC:wght@400;500;600;700&display=swap');

:root{
  --ink-900:#070B10; --ink-800:#0E141C; --ink-700:#141C26; --ink-600:#1B2530;
  --line:#232E3A; --line-soft:#1A222C; --paper:#ECF1F5; --dim:#8492A1; --dim-2:#59636E;
  --blue:#4C9AE0; --blue-dim:rgba(76,154,224,0.13); --amber:#E3A13D; --amber-dim:rgba(227,161,61,0.14);
  --red:#E1615C; --red-dim:rgba(225,97,92,0.14); --green:#4FB88A; --green-dim:rgba(79,184,138,0.14);
}

*{box-sizing:border-box;}
html,body{margin:0;padding:0;}
body{
  background:var(--ink-900); color:var(--paper);
  font-family:'IBM Plex Sans TC','IBM Plex Mono',sans-serif;
  -webkit-font-smoothing:antialiased; min-height:100vh;
}
.mono{font-family:'IBM Plex Mono',monospace;font-variant-numeric:tabular-nums;}

.app{
  max-width:480px; margin:0 auto; min-height:100vh;
  display:flex; flex-direction:column; position:relative;
  background:
    radial-gradient(1200px 400px at 50% -120px, rgba(76,154,224,0.08), transparent 60%),
    var(--ink-900);
}

.topbar{
  position:sticky; top:0; z-index:20;
  display:flex; align-items:center; justify-content:space-between;
  padding:14px 16px 10px 48px;
  background:linear-gradient(var(--ink-900) 70%, transparent);
}
.brand{display:flex; align-items:center; gap:9px;}
.brand-mark{
  width:26px;height:26px;border-radius:6px;
  background:var(--ink-700); border:1px solid var(--line);
  display:flex;align-items:center;justify-content:center;
  font-size:11px;font-weight:700;color:var(--blue);
  font-family:'IBM Plex Mono',monospace;
}
.brand-name{font-size:13px;font-weight:600;letter-spacing:0.3px;color:var(--paper);}
.brand-sub{font-size:9.5px;color:var(--dim-2);margin-top:1px;}

.unit-chip{
  display:flex;align-items:center;gap:6px;
  background:var(--ink-700); border:1px solid var(--line);
  padding:6px 10px 6px 12px; border-radius:8px;
  font-size:12.5px;font-weight:600; color:var(--paper);
  font-family:'IBM Plex Mono',monospace; cursor:pointer;
}
.unit-chip .dot{width:6px;height:6px;border-radius:50%;background:var(--green);flex:none;}

main{flex:1; padding:0 16px 96px; overflow-x:hidden;}
.screen{display:none; animation:fadeIn 0.28s ease;}
.screen.active{display:block;}
@keyframes fadeIn{from{opacity:0; transform:translateY(4px);} to{opacity:1; transform:none;}}

.section-label{
  font-size:11px; color:var(--dim-2); font-weight:600;
  letter-spacing:0.2px; margin:22px 2px 10px;
}
.section-label:first-child{margin-top:6px;}

.hero{
  border:1px solid var(--line); border-radius:14px;
  background:linear-gradient(165deg, var(--ink-700), var(--ink-800));
  padding:20px 18px 18px; position:relative; overflow:hidden;
}

.panel{
  border:1px solid var(--line); border-radius:12px;
  background:var(--ink-800); padding:4px 14px;
}

.week-head{
  display:flex;justify-content:space-between;align-items:baseline;
  padding:12px 2px 8px; margin-top:4px;
}
.week-head .w-title{font-size:12px;font-weight:600;color:var(--dim);}

.duty-row{
  display:flex;align-items:center;gap:12px; padding:11px 2px;
  border-bottom:1px solid var(--line-soft);
}
.duty-row:last-child{border-bottom:none;}
.duty-date{width:38px;flex:none;text-align:center;}
.duty-date .d{font-family:'IBM Plex Mono',monospace;font-size:16px;font-weight:600;color:var(--paper);}
.duty-date .w{font-size:9.5px;color:var(--dim-2);}
.duty-bar{width:3px;align-self:stretch;border-radius:3px;flex:none;background:var(--blue);}
.duty-bar.off{background:var(--red);}
.duty-main{flex:1;min-width:0;}
.duty-times{font-family:'IBM Plex Mono',monospace;font-size:14.5px;font-weight:600;color:var(--paper);}
.duty-off-label{font-size:13.5px;font-weight:600;color:var(--red);}
.duty-meta{font-size:11px;color:var(--dim-2);margin-top:2px;display:flex;gap:8px;}

.tag{
  font-size:9.5px;font-weight:600;padding:2.5px 6px;border-radius:5px;
  white-space:nowrap; font-family:'IBM Plex Sans TC',sans-serif;
}
.tag.amber{color:var(--amber);background:var(--amber-dim);}
.tag.red{color:var(--red);background:var(--red-dim);}

.empty-box {
  text-align: center; padding: 36px 16px; background: var(--ink-800);
  border: 1px solid var(--line); border-radius: 14px; margin-top: 16px;
}
.empty-box .title { font-size: 16px; font-weight: 700; color: var(--paper); margin-bottom: 6px; }
.empty-box .sub { font-size: 12.5px; color: var(--dim-2); line-height: 1.6; margin-bottom: 20px; }

.btn{
  display:block; width:100%; text-align:center; padding:13px; border-radius:10px; border:none;
  font-size:14.5px; font-weight:600; cursor:pointer; font-family:'IBM Plex Sans TC',sans-serif;
}
.btn-primary{background:var(--blue); color:var(--ink-900);}

.role-tabs{display:flex; gap:8px; margin-bottom:14px;}
.role-tab{
  flex:1; text-align:center; padding:9px 0; border-radius:9px;
  font-size:13px; font-weight:600; color:var(--dim);
  background:var(--ink-800); border:1px solid var(--line); cursor:pointer;
}
.role-tab.active{color:var(--ink-900); background:var(--blue); border-color:var(--blue);}

.result-card{
  border:1px solid var(--line); border-radius:12px; background:var(--ink-800);
  padding:13px 14px; margin-bottom:10px;
}

.profile-head{display:flex; align-items:center; gap:12px; padding:8px 2px 20px;}
.avatar{
  width:48px;height:48px;border-radius:11px; background:var(--ink-700); border:1px solid var(--line);
  display:flex;align-items:center;justify-content:center;
  font-family:'IBM Plex Mono',monospace; font-weight:700; color:var(--blue); font-size:15px;
}

.list-row{display:flex; justify-content:space-between; align-items:center; padding:13px 2px; border-bottom:1px solid var(--line-soft); cursor:pointer;}
.list-row-label{font-size:13.5px; color:var(--paper);}
.list-row-value{font-size:12.5px; color:var(--dim-2); font-family:'IBM Plex Mono',monospace;}

.tabbar{
  position:fixed; bottom:0; left:50%; transform:translateX(-50%);
  width:100%; max-width:480px; display:flex;
  background:rgba(14,20,28,0.92); backdrop-filter:blur(10px); border-top:1px solid var(--line);
  padding:8px 6px calc(8px + env(safe-area-inset-bottom)); z-index:30;
}
.tab-item{
  flex:1; display:flex; flex-direction:column; align-items:center; gap:4px;
  padding:6px 0; cursor:pointer; color:var(--dim-2);
}
.tab-item svg{width:19px;height:19px; stroke:var(--dim-2); fill:none;}
.tab-item span{font-size:10px; font-weight:600;}
.tab-item.active{color:var(--blue);}
.tab-item.active svg{stroke:var(--blue);}
</style>
</head>
<body>
<div class="app">

  <header class="topbar">
    <div class="brand">
      <div class="brand-mark">CD</div>
      <div>
        <div class="brand-name">CREW DUTY ENGINE</div>
        <div class="brand-sub">redesign concept · C.L.F</div>
      </div>
    </div>
    <div class="unit-chip" onclick="openAdminPanel()">
      <span class="dot"></span>
      <span id="unitText">--</span>
    </div>
  </header>

  <main>
    <!-- HOME -->
    <section class="screen active" id="screen-home">
      <div id="homeContent"></div>
    </section>

    <!-- SCHEDULE -->
    <section class="screen" id="screen-schedule">
      <div class="section-label" style="margin-top:6px;" id="schedTitle">我的月班表</div>
      <div id="scheduleContent"></div>
    </section>

    <!-- EXCHANGE -->
    <section class="screen" id="screen-exchange">
      <div class="section-label" style="margin-top:6px;">換班快搜</div>
      <div class="role-tabs">
        <div class="role-tab active" onclick="filterRole('服勤員', this)">服勤員</div>
        <div class="role-tab" onclick="filterRole('駕駛', this)">駕駛</div>
        <div class="role-tab" onclick="filterRole('列車長', this)">列車長</div>
      </div>
      <div id="searchResults"></div>
    </section>

    <!-- PROFILE -->
    <section class="screen" id="screen-profile">
      <div id="profileContent"></div>
    </section>
  </main>

  <nav class="tabbar">
    <div class="tab-item active" data-tab="home" onclick="showTab('home')">
      <svg viewBox="0 0 24 24" stroke-width="1.8" fill="none" stroke="currentColor"><path d="M4 11l8-6 8 6v8a1 1 0 01-1 1h-4v-6H9v6H5a1 1 0 01-1-1z"/></svg>
      <span>今日</span>
    </div>
    <div class="tab-item" data-tab="schedule" onclick="showTab('schedule')">
      <svg viewBox="0 0 24 24" stroke-width="1.8" fill="none" stroke="currentColor"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M8 3v4M16 3v4M3 10h18"/></svg>
      <span>我的班表</span>
    </div>
    <div class="tab-item" data-tab="exchange" onclick="showTab('exchange')">
      <svg viewBox="0 0 24 24" stroke-width="1.8" fill="none" stroke="currentColor"><path d="M7 7h11M18 7l-3-3M18 7l-3 3M17 17H6M6 17l3 3M6 17l3-3"/></svg>
      <span>換班快搜</span>
    </div>
    <div class="tab-item" data-tab="profile" onclick="showTab('profile')">
      <svg viewBox="0 0 24 24" stroke-width="1.8" fill="none" stroke="currentColor"><circle cx="12" cy="8" r="3.4"/><path d="M4.5 20c1.5-4 4.5-6 7.5-6s6 2 7.5 6"/></svg>
      <span>我的</span>
    </div>
  </nav>
</div>

<script>
const crewData = __CREW_JSON__;
const scheduleData = __SCHEDULE_JSON__;
const exchangeData = __EXCHANGE_JSON__;
const syncTimeStr = "__SYNC_TIME__";

// JS 觸發開關：自動打開 Streamlit 側邊欄抽屜
function openAdminPanel(){
  try {
    const btn = window.parent.document.querySelector('button[aria-label="Open sidebar"], [data-testid="stSidebarCollapsedControl"]');
    if(btn) btn.click();
  } catch(e) {
    console.log(e);
  }
}

// 頂部基地顯示
document.getElementById('unitText').textContent = crewData ? crewData.unit : '點此上傳';

// 渲染首頁 (HOME)
const homeBox = document.getElementById('homeContent');
if(!crewData){
  homeBox.innerHTML = `
    <div class="empty-box">
      <div class="title">尚未載入乘務大表</div>
      <div class="sub">歡迎使用 CREW DUTY ENGINE。<br>請點擊下方按鈕上傳月度 Excel 大表，或切換登入組員。</div>
      <button class="btn btn-primary" onclick="openAdminPanel()">📤 點此開啟控制台／上傳大表</button>
    </div>`;
} else {
  homeBox.innerHTML = `
    <div class="hero">
      <div style="font-size:14px;font-weight:700;color:var(--paper);">登入組員：${crewData.name} (${crewData.emp_id})</div>
      <div style="font-size:11.5px;color:var(--dim-2);margin-top:3px;">基地：${crewData.unit_name} (${crewData.unit}) · 職掌：${crewData.role_title}</div>
    </div>
    <div class="section-label">快速功能</div>
    <div class="panel">
      <div class="duty-row" onclick="showTab('schedule')" style="cursor:pointer;padding:12px 0;">
        <div style="flex:1;"><div style="font-size:14px;font-weight:600;">我的月班表</div><div style="font-size:11.5px;color:var(--dim-2);">逐日清單・含班間合規標示</div></div>
        <span style="color:var(--dim-2);">›</span>
      </div>
      <div class="duty-row" onclick="showTab('exchange')" style="cursor:pointer;padding:12px 0;">
        <div style="flex:1;"><div style="font-size:14px;font-weight:600;">換班快搜</div><div style="font-size:11.5px;color:var(--dim-2);">依 Sign-in 時間窗篩選可換組員</div></div>
        <span style="color:var(--dim-2);">›</span>
      </div>
    </div>`;
}

// 渲染班表 (SCHEDULE)
const schedBox = document.getElementById('scheduleContent');
if(!crewData || !scheduleData.week1 || scheduleData.week1.length === 0){
  schedBox.innerHTML = `
    <div class="empty-box">
      <div class="title">無班表資料</div>
      <div class="sub">請先開啟控制台上傳大表 Excel。</div>
      <button class="btn btn-primary" onclick="openAdminPanel()">📤 上傳大表 Excel</button>
    </div>`;
} else {
  document.getElementById('schedTitle').textContent = `我的月班表 · ${crewData.emp_id} ${crewData.name}`;
  
  function renderWeekHtml(days){
    if(!days || days.length === 0) return '';
    return days.map(day => {
      if(day.off){
        return `
          <div class="duty-row">
            <div class="duty-date"><div class="d mono">${day.d}</div><div class="w">${day.wd}</div></div>
            <div class="duty-bar off"></div>
            <div class="duty-main"><div class="duty-off-label">${day.off}</div></div>
            <span class="tag red">休假日</span>
          </div>`;
      }
      const tagsHtml = (day.tags||[]).map(t => `<span class="tag amber">${t}</span>`).join(' ');
      const restHtml = day.rest ? `<span style="color:var(--${day.restTag==='red'?'red':day.restTag==='amber'?'amber':'green'})">班間 ${day.rest}</span>` : '';
      return `
        <div class="duty-row">
          <div class="duty-date"><div class="d mono">${day.d}</div><div class="w">${day.wd}</div></div>
          <div class="duty-bar"></div>
          <div class="duty-main">
            <div class="duty-times">${day.start} → ${day.end}</div>
            <div class="duty-meta"><span>${day.code}</span><span>${day.dur}</span>${restHtml}</div>
          </div>
          <div>${tagsHtml}</div>
        </div>`;
    }).join('');
  }

  schedBox.innerHTML = `
    <div class="week-head"><span class="w-title">第 1 週</span></div>
    <div class="panel">${renderWeekHtml(scheduleData.week1)}</div>
    <div class="week-head"><span class="w-title">第 2 週</span></div>
    <div class="panel">${renderWeekHtml(scheduleData.week2)}</div>
    <div class="week-head"><span class="w-title">第 3 週</span></div>
    <div class="panel">${renderWeekHtml(scheduleData.week3)}</div>`;
}

// 換班搜尋 (EXCHANGE)
function filterRole(role, btn){
  document.querySelectorAll('.role-tab').forEach(t=>t.classList.remove('active'));
  btn.classList.add('active');
  renderExchange(role);
}

function renderExchange(role){
  const container = document.getElementById('searchResults');
  if(!exchangeData || !exchangeData[role] || exchangeData[role].length === 0){
    container.innerHTML = `<div class="empty-box"><div class="title">無符合資料</div><div class="sub">目前大表中無該職務可換班之組員。</div></div>`;
    return;
  }
  const pool = exchangeData[role];
  container.innerHTML = pool.map(c => `
    <div class="result-card">
      <div style="display:flex;justify-content:space-between;align-items:center;">
        <div>
          <div class="mono" style="font-size:11px;color:var(--dim-2);">${c.id}</div>
          <div style="font-size:14px;font-weight:600;">${c.name}</div>
        </div>
        <span class="tag ${c.restTag}">${c.restBefore}</span>
      </div>
      <div class="mono" style="font-size:18px;font-weight:600;margin-top:6px;">${c.start} → ${c.end}</div>
      <div style="font-size:11px;color:var(--dim-2);margin-top:4px;">${c.streak}</div>
    </div>
  `).join('');
}
renderExchange('服勤員');

// 個人頁面 (PROFILE) - 包含管理者選單入口
const profBox = document.getElementById('profileContent');
if(!crewData){
  profBox.innerHTML = `
    <div class="empty-box">
      <div class="title">未載入組員</div>
      <div class="sub">請開啟控制台進行上傳。</div>
      <button class="btn btn-primary" onclick="openAdminPanel()">⚙️ 開啟管理控制台</button>
    </div>`;
} else {
  profBox.innerHTML = `
    <div class="profile-head">
      <div class="avatar">${crewData.name ? crewData.name.charAt(0) : 'CD'}</div>
      <div>
        <div style="font-size:15px;font-weight:600;">${crewData.name}</div>
        <div style="font-size:11.5px;color:var(--dim-2);font-family:monospace;">${crewData.emp_id} · ${crewData.unit} · ${crewData.role_title}</div>
      </div>
    </div>
    <div class="section-label">帳號與資料</div>
    <div class="panel">
      <div class="list-row"><span class="list-row-label">所屬單位</span><span class="list-row-value">${crewData.unit_name} (${crewData.unit})</span></div>
      <div class="list-row"><span class="list-row-label">大表同步時間</span><span class="list-row-value">${syncTimeStr}</span></div>
    </div>
    <div class="section-label">系統管理</div>
    <div class="panel">
      <div class="list-row" onclick="openAdminPanel()"><span class="list-row-label">⚙️ 管理者控制台／上傳大表</span><span style="color:var(--blue);">›</span></div>
    </div>`;
}

function showTab(name){
  document.querySelectorAll('.screen').forEach(s=>s.classList.remove('active'));
  document.getElementById('screen-'+name).classList.add('active');
  document.querySelectorAll('.tab-item').forEach(t=>t.classList.toggle('active', t.dataset.tab===name));
}
</script>
</body>
</html>
"""

HTML_CODE = RAW_HTML_TEMPLATE.replace(
    "__CREW_JSON__", json.dumps(current_crew, ensure_ascii=False) if current_crew else "null"
).replace(
    "__SCHEDULE_JSON__", json.dumps(formatted_schedule, ensure_ascii=False)
).replace(
    "__EXCHANGE_JSON__", json.dumps(dynamic_exchange, ensure_ascii=False)
).replace(
    "__SYNC_TIME__", st.session_state.last_sync_time
)

components.html(HTML_CODE, height=1000, scrolling=False)
