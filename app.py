import json
from datetime import datetime, timedelta
import streamlit as st
import streamlit.components.v1 as components

# 1. 載入核心模組與算力服務
from config import DEFAULT_UNIT, UNIT_NAME
from modules.utils import format_day_duty_to_v2
from modules.services import get_current_duty_status

# 2. Streamlit 視口重置
st.set_page_config(
    page_title="CREW DUTY ENGINE V2",
    page_icon="🚆",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    header[data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"], footer {
        display: none !important; height: 0px !important;
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
        position: fixed !important; top: 0 !important; left: 0 !important; z-index: 999999 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# 3. 動態時間計算 (基於目前真實時間產生對應班別)
# ---------------------------------------------------------
now = datetime.now()
t_day1 = now + timedelta(days=1)
t_day2 = now + timedelta(days=2)
t_day3 = now + timedelta(days=3)

raw_schedule_data = [
    {"date_info": {"day": now.day, "weekday": "今", "full_date": now.strftime("%Y-%m-%d")}, "duty_code": "DO1"},
    {"date_info": {"day": t_day1.day, "weekday": "明", "full_date": t_day1.strftime("%Y-%m-%d")}, "duty_code": "NG0001", "start_time": "07:24", "end_time": "15:24", "duration_str": "8h00m", "prev_end_time": "20:00"},
    {"date_info": {"day": t_day2.day, "weekday": "後", "full_date": t_day2.strftime("%Y-%m-%d")}, "duty_code": "NH0543", "start_time": "14:34", "end_time": "24:16", "duration_str": "9h42m", "prev_end_time": "15:24"},
    {"date_info": {"day": t_day3.day, "weekday": "大後", "full_date": t_day3.strftime("%Y-%m-%d")}, "duty_code": "DO3X"},
]

processed_week = [format_day_duty_to_v2(**item) for item in raw_schedule_data]

for idx, item in enumerate(raw_schedule_data):
    processed_week[idx]["full_date"] = item["date_info"]["full_date"]

duty_status = get_current_duty_status(processed_week)

backend_schedule = {
    "week1": processed_week,
    "week2": [],
    "week3": []
}

backend_user_info = {
    "emp_id": "A023001",
    "name": "江立夫",
    "unit": DEFAULT_UNIT,
    "unit_name": UNIT_NAME,
    "title": "車務幹部/組員",
}

backend_exchange_candidates = {
    "服勤員": [
        {"id": "A024118", "name": "林彥廷", "start": "06:01", "end": "16:01", "dur": "10h00m", "restBefore": "13.2h", "restTag": "green", "streak": "連續值勤 2 日"},
        {"id": "A021987", "name": "陳淨怡", "start": "07:30", "end": "16:30", "dur": "9h00m", "restBefore": "9.8h", "restTag": "red", "streak": "連續值勤 5 日 · 前一班間隔不足"},
    ],
    "駕駛": [
        {"id": "A011203", "name": "李國安", "start": "05:10", "end": "13:40", "dur": "8h30m", "restBefore": "15.0h", "restTag": "green", "streak": "連續值勤 1 日"}
    ],
    "列車長": []
}

# ---------------------------------------------------------
# 4. 全介面 HTML / CSS / JS 模板 (修復 4 欄導覽列)
# ---------------------------------------------------------
RAW_HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
<title>CREW DUTY ENGINE V2</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&family=IBM+Plex+Sans+TC:wght@400;500;600;700&display=swap');

:root {
  --ink-900:#070B10; --ink-800:#0E141C; --ink-700:#141C26; --ink-600:#1B2530;
  --line:#232E3A; --line-soft:#1A222C; --paper:#ECF1F5; --dim:#8492A1; --dim-2:#59636E;
  --blue:#4C9AE0; --blue-dim:rgba(76,154,224,0.13); --amber:#E3A13D; --amber-dim:rgba(227,161,61,0.14);
  --red:#E1615C; --red-dim:rgba(225,97,92,0.14); --green:#4FB88A; --green-dim:rgba(79,184,138,0.14);
  --purple:#9B8CE0; --purple-dim:rgba(155,140,224,0.14); --grey:#7A8794; --grey-dim:rgba(122,135,148,0.14);
}

*{box-sizing:border-box;}
html,body{margin:0;padding:0;background:var(--ink-900);color:var(--paper);font-family:'IBM Plex Sans TC','IBM Plex Mono',sans-serif;-webkit-font-smoothing:antialiased;height:100%;overflow:hidden;}
.mono{font-family:'IBM Plex Mono',monospace;font-variant-numeric:tabular-nums;}

.app{max-width:480px;margin:0 auto;height:100dvh;display:flex;flex-direction:column;position:relative;background:var(--ink-900);}
.topbar{position:sticky;top:0;z-index:20;display:flex;align-items:center;justify-content:space-between;padding:calc(10px + env(safe-area-inset-top,0px)) 16px 10px;background:rgba(7,11,16,0.92);backdrop-filter:blur(10px);border-bottom:1px solid rgba(35,46,58,0.5);}
.brand-mark{width:26px;height:26px;border-radius:6px;background:var(--ink-700);border:1px solid var(--line);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;color:var(--blue);font-family:monospace;}
.brand-name{font-size:13px;font-weight:600;color:var(--paper);}
.unit-chip{display:flex;align-items:center;gap:6px;background:var(--ink-700);border:1px solid var(--line);padding:6px 10px;border-radius:8px;font-size:12.5px;font-weight:600;color:var(--paper);font-family:monospace;cursor:pointer;}
.unit-chip .dot{width:6px;height:6px;border-radius:50%;background:var(--green);}

main{flex:1;padding:12px 16px calc(76px + env(safe-area-inset-bottom,0px));overflow-y:auto;}
.screen{display:none;}
.screen.active{display:block;}

.section-label{font-size:11px;color:var(--dim-2);font-weight:600;margin:16px 2px 8px;}
.section-label:first-child{margin-top:2px;}
.panel{border:1px solid var(--line);border-radius:12px;background:var(--ink-800);padding:2px 12px;margin-bottom:12px;}

/* Hero 卡片與倒數計時 */
.hero{
  border:1px solid var(--line);
  border-radius:14px;
  background:linear-gradient(165deg, var(--ink-700), var(--ink-800));
  padding:18px 16px;
  margin-bottom:14px;
  position:relative;
  overflow:hidden;
}
.hero::before{
  content:"";
  position:absolute; right:-40px; top:-40px;
  width:160px;height:160px;border-radius:50%;
  background:radial-gradient(circle, rgba(76,154,224,0.16), transparent 70%);
}
.hero-top{display:flex;justify-content:space-between;align-items:flex-start;}
.hero-status{
  display:inline-flex;align-items:center;gap:6px;
  font-size:11.5px;color:var(--amber);font-weight:600;
  background:var(--amber-dim); border:1px solid rgba(227,161,61,0.35);
  padding:4px 9px;border-radius:20px;
}
.hero-status .dot{width:5px;height:5px;border-radius:50%;background:var(--amber);}
.hero-cycle{font-size:10.5px;color:var(--dim-2);font-family:'IBM Plex Mono',monospace;}

.hero-label{font-size:12px;color:var(--dim);margin-top:14px;}
.countdown{display:flex;align-items:baseline;gap:10px;margin-top:6px;}
.countdown .num{
  font-family:'IBM Plex Mono',monospace;
  font-size:36px;font-weight:600;letter-spacing:0.5px;color:var(--paper);
  line-height:1;
}
.countdown .unit{font-size:12px;color:var(--dim-2);}
.hero-next{
  margin-top:14px;padding-top:12px;border-top:1px solid var(--line);
  display:flex;justify-content:space-between;align-items:center;
}
.hero-next-left{display:flex;flex-direction:column;gap:2px;}
.hero-next-date{font-size:12px;color:var(--dim);}
.hero-next-times{font-family:'IBM Plex Mono',monospace;font-size:16px;font-weight:600;color:var(--paper);}
.hero-next-code{
  font-family:'IBM Plex Mono',monospace;font-size:11px;color:var(--blue);
  background:var(--blue-dim);border:1px solid rgba(76,154,224,0.3);
  padding:4px 8px;border-radius:8px;font-weight:600;
}

/* Duty Row */
.duty-row{display:flex;align-items:center;gap:12px;padding:10px 2px;border-bottom:1px solid var(--line-soft);cursor:pointer;}
.duty-row:last-child{border-bottom:none;}
.duty-date{width:36px;text-align:center;}
.duty-date .d{font-family:monospace;font-size:15px;font-weight:600;color:var(--paper);}
.duty-date .w{font-size:9.5px;color:var(--dim-2);}
.duty-bar{width:3px;align-self:stretch;border-radius:3px;background:var(--blue);}
.duty-bar.off{background:var(--red);}
.duty-main{flex:1;}
.duty-times{font-family:monospace;font-size:14px;font-weight:600;}
.duty-meta{font-size:10.5px;color:var(--dim-2);margin-top:2px;display:flex;gap:8px;}
.tag{font-size:9px;font-weight:600;padding:2px 5px;border-radius:4px;white-space:nowrap;}
.tag.amber{color:var(--amber);background:var(--amber-dim);}
.tag.red{color:var(--red);background:var(--red-dim);}

/* 4 欄式 Tab bar */
.tabbar{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:480px;display:flex;background:rgba(14,20,28,0.95);backdrop-filter:blur(12px);border-top:1px solid var(--line);padding:6px 4px calc(6px + env(safe-area-inset-bottom,0px));z-index:30;}
.tab-item{flex:1;display:flex;flex-direction:column;align-items:center;gap:3px;padding:5px 0;cursor:pointer;color:var(--dim-2);}
.tab-item svg{width:18px;height:18px;stroke:var(--dim-2);fill:none;}
.tab-item span{font-size:9.5px;font-weight:600;}
.tab-item.active{color:var(--blue);}
.tab-item.active svg{stroke:var(--blue);}

/* Bottom Sheet */
.sheet-overlay{position:fixed;inset:0;background:rgba(3,5,8,0.65);display:none;align-items:flex-end;justify-content:center;z-index:50;backdrop-filter:blur(4px);}
.sheet-overlay.open{display:flex;}
.sheet{width:100%;max-width:480px;background:var(--ink-800);border-top:1px solid var(--line);border-radius:18px 18px 0 0;padding:10px 18px calc(20px + env(safe-area-inset-bottom,0px));max-height:80vh;overflow-y:auto;}
.sheet-handle{width:36px;height:4px;border-radius:3px;background:var(--line);margin:2px auto 14px;}
.btn{display:block;width:100%;text-align:center;padding:12px;border-radius:9px;border:none;font-size:14px;font-weight:600;cursor:pointer;}
.btn-primary{background:var(--blue);color:var(--ink-900);}
</style>
</head>
<body>
<div class="app">
  <header class="topbar">
    <div style="display:flex;align-items:center;gap:9px;">
      <div class="brand-mark">CD</div>
      <div>
        <div class="brand-name">CREW DUTY ENGINE</div>
        <div style="font-size:9.5px;color:var(--dim-2);">V2 Modular Architecture</div>
      </div>
    </div>
    <div class="unit-chip" onclick="openSyncSheet()">
      <span class="dot"></span>
      <span id="headerUnit">--</span>
    </div>
  </header>

  <main id="mainContainer">
    <!-- 1. 今日首頁 -->
    <section class="screen active" id="screen-home">
      <div class="hero">
        <div class="hero-top">
          <span class="hero-status" id="heroStatus"><span class="dot"></span><span id="statusTxt">--</span></span>
          <span class="hero-cycle mono" id="heroCycle">--</span>
        </div>
        <div class="hero-label">距下次出勤簽到</div>
        <div class="countdown">
          <span class="num" id="cd-h">00</span><span class="unit">時</span>
          <span class="num" id="cd-m">00</span><span class="unit">分</span>
          <span class="num" id="cd-s">00</span><span class="unit">秒</span>
        </div>
        <div class="hero-next">
          <div class="hero-next-left">
            <div class="hero-next-date" id="nextDate">--</div>
            <div class="hero-next-times" id="nextTimes">--:-- → --:--</div>
          </div>
          <div class="hero-next-code" id="nextCode">--</div>
        </div>
      </div>

      <div class="section-label">目前登入組員</div>
      <div class="panel" style="padding:12px 14px;">
        <div style="font-size:18px;font-weight:700;" id="userName">--</div>
        <div style="font-size:12px;color:var(--dim-2);font-family:monospace;margin-top:2px;" id="userMeta">--</div>
      </div>

      <div class="section-label">快速功能</div>
      <div class="panel" style="padding:4px 12px;">
        <div class="duty-row" onclick="showTab('schedule')">
          <div style="font-size:14px;font-weight:600;flex:1;">我的月班表 (Modules 算力驅動)</div>
          <span style="color:var(--dim-2);">›</span>
        </div>
        <div class="duty-row" onclick="showTab('exchange')">
          <div style="font-size:14px;font-weight:600;flex:1;">換班快搜</div>
          <span style="color:var(--dim-2);">›</span>
        </div>
      </div>
    </section>

    <!-- 2. 我的班表 -->
    <section class="screen" id="screen-schedule">
      <div class="section-label" style="margin-top:2px;">個人班表 · 班間休息檢核</div>
      <div class="panel" id="scheduleContainer"></div>
    </section>

    <!-- 3. 換班快搜 -->
    <section class="screen" id="screen-exchange">
      <div class="section-label" style="margin-top:2px;">換班快搜名單</div>
      <div class="panel" id="exchangeContainer"></div>
    </section>

    <!-- 4. 我的 (Profile) -->
    <section class="screen" id="screen-profile">
      <div style="display:flex;align-items:center;gap:12px;padding:6px 2px 16px;">
        <div style="width:44px;height:44px;border-radius:10px;background:var(--ink-700);border:1px solid var(--line);display:flex;align-items:center;justify-content:center;font-family:monospace;font-weight:700;color:var(--blue);font-size:15px;" id="profileAvatar">江</div>
        <div>
          <div style="font-size:15px;font-weight:600;" id="profileName">--</div>
          <div style="font-size:11px;color:var(--dim-2);margin-top:2px;font-family:monospace;" id="profileMeta">--</div>
        </div>
      </div>

      <div class="section-label">帳號與權限</div>
      <div class="panel" style="padding:4px 12px;">
        <div class="duty-row" style="cursor:default;"><span style="font-size:13.5px;color:var(--paper);">所屬單位</span><span style="font-size:12.5px;color:var(--dim-2);font-family:monospace;" id="profUnit">TTN</span></div>
        <div class="duty-row" style="cursor:default;"><span style="font-size:13.5px;color:var(--paper);">權限層級</span><span style="font-size:12.5px;color:var(--dim-2);font-family:monospace;">CREW</span></div>
        <div class="duty-row" style="cursor:default;"><span style="font-size:13.5px;color:var(--paper);">大表同步時間</span><span style="font-size:12.5px;color:var(--dim-2);font-family:monospace;">2026-09-05 20:40</span></div>
      </div>

      <div class="section-label">系統資訊與設定</div>
      <div class="panel" style="padding:4px 12px;">
        <div class="duty-row"><span style="font-size:13.5px;color:var(--paper);flex:1;">問題回報與建議</span><span style="color:var(--dim-2);">›</span></div>
        <div class="duty-row"><span style="font-size:13.5px;color:var(--paper);flex:1;">系統使用須知</span><span style="color:var(--dim-2);">›</span></div>
        <div class="duty-row"><span style="font-size:13.5px;color:var(--red);flex:1;">登出系統</span><span style="color:var(--dim-2);">›</span></div>
      </div>
    </section>
  </main>

  <!-- 4 欄式 Tab Bar -->
  <nav class="tabbar">
    <div class="tab-item active" data-tab="home" onclick="showTab('home')">
      <svg viewBox="0 0 24 24" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 11l8-6 8 6v8a1 1 0 01-1 1h-4v-6H9v6H5a1 1 0 01-1-1z"/></svg>
      <span>今日</span>
    </div>
    <div class="tab-item" data-tab="schedule" onclick="showTab('schedule')">
      <svg viewBox="0 0 24 24" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M8 3v4M16 3v4M3 10h18"/></svg>
      <span>我的班表</span>
    </div>
    <div class="tab-item" data-tab="exchange" onclick="showTab('exchange')">
      <svg viewBox="0 0 24 24" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M7 7h11M18 7l-3-3M18 7l-3 3M17 17H6M6 17l3 3M6 17l3-3"/></svg>
      <span>換班快搜</span>
    </div>
    <div class="tab-item" data-tab="profile" onclick="showTab('profile')">
      <svg viewBox="0 0 24 24" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="3.4"/><path d="M4.5 20c1.5-4 4.5-6 7.5-6s6 2 7.5 6"/></svg>
      <span>我的</span>
    </div>
  </nav>

  <!-- Bottom Sheet Modal -->
  <div class="sheet-overlay" id="sheetOverlay" onclick="closeSheetOnBg(event)">
    <div class="sheet" id="sheet"></div>
  </div>
</div>

<script>
// 安全注入 JSON 資料
const userData = __USER_DATA__;
const scheduleData = __SCHEDULE_DATA__;
const exchangeData = __EXCHANGE_DATA__;
const statusData = __STATUS_DATA__;

// 渲染 Header & 個人資訊
document.getElementById('headerUnit').textContent = userData.unit + ' · 已同步';
document.getElementById('userName').textContent = userData.name + ' (' + userData.emp_id + ')';
document.getElementById('userMeta').textContent = userData.unit_name + ' · ' + userData.title;

// 渲染 Profile 頁面資訊
document.getElementById('profileAvatar').textContent = userData.name ? userData.name.charAt(0) : 'CD';
document.getElementById('profileName').textContent = userData.name + ' (' + userData.emp_id + ')';
document.getElementById('profileMeta').textContent = userData.unit + ' · ' + userData.title;
document.getElementById('profUnit').textContent = userData.unit_name + ' (' + userData.unit + ')';

// 渲染 Hero 英雄卡片內容
document.getElementById('statusTxt').textContent = statusData.status_text;
document.getElementById('heroCycle').textContent = statusData.current_cycle;
document.getElementById('nextDate').textContent = statusData.next_duty_title;
document.getElementById('nextTimes').textContent = statusData.next_duty_times;
document.getElementById('nextCode').textContent = statusData.next_duty_code;

// 精準時間差倒數計時引擎
function pad(n){ return String(n).padStart(2,'0'); }
function updateCountdown(){
  if(!statusData.target_timestamp_ms) {
    document.getElementById('cd-h').textContent = "00";
    document.getElementById('cd-m').textContent = "00";
    document.getElementById('cd-s').textContent = "00";
    return;
  }
  const now = new Date().getTime();
  let diff = Math.max(0, statusData.target_timestamp_ms - now);

  const h = Math.floor(diff / (1000 * 60 * 60));
  const m = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
  const s = Math.floor((diff % (1000 * 60)) / 1000);

  document.getElementById('cd-h').textContent = pad(h);
  document.getElementById('cd-m').textContent = pad(m);
  document.getElementById('cd-s').textContent = pad(s);
}
updateCountdown();
setInterval(updateCountdown, 1000);

// 渲染班表
const schedContainer = document.getElementById('scheduleContainer');
const days = scheduleData.week1 || [];

schedContainer.innerHTML = days.map(day => {
  if(day.off) {
    return `
      <div class="duty-row">
        <div class="duty-date"><div class="d mono">${day.d}</div><div class="w">${day.wd}</div></div>
        <div class="duty-bar off"></div>
        <div class="duty-main"><div style="color:var(--red);font-weight:600;font-size:13.5px;">${day.off}</div></div>
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
        <div class="duty-times mono">${day.start} → ${day.end}</div>
        <div class="duty-meta"><span>${day.code}</span><span>${day.dur}</span>${restHtml}</div>
      </div>
      <div>${tagsHtml}</div>
    </div>`;
}).join('');

// 渲染換班名單
const exContainer = document.getElementById('exchangeContainer');
const candidates = exchangeData['服勤員'] || [];
exContainer.innerHTML = candidates.map(c => `
  <div class="duty-row">
    <div class="duty-main">
      <div style="font-size:14px;font-weight:600;">${c.name} <span style="font-size:11px;color:var(--dim-2);" class="mono">(${c.id})</span></div>
      <div class="duty-times mono" style="margin-top:2px;">${c.start} → ${c.end}</div>
      <div style="font-size:10.5px;color:var(--dim-2);margin-top:2px;">${c.streak} · 前班間隔 ${c.restBefore}</div>
    </div>
  </div>
`).join('');

// 分頁切換邏輯
function showTab(name){
  document.querySelectorAll('.screen').forEach(s=>s.classList.remove('active'));
  document.getElementById('screen-'+name).classList.add('active');
  document.querySelectorAll('.tab-item').forEach(t=>t.classList.toggle('active', t.dataset.tab===name));
  document.getElementById('mainContainer').scrollTop = 0;
}

// 彈窗控制
function openSyncSheet(){
  const sheet = document.getElementById('sheet');
  sheet.innerHTML = `
    <div class="sheet-handle"></div>
    <div style="font-size:16px;font-weight:700;color:var(--paper);">大表同步資訊</div>
    <div style="font-size:12px;color:var(--dim-2);margin:4px 0 16px;">當前基地：${userData.unit_name} (${userData.unit})</div>
    <div style="background:var(--ink-700);padding:12px;border-radius:10px;border:1px solid var(--line);font-size:12.5px;color:var(--dim);">
      資料庫最後更新：2026-09-05 20:40<br>
      目前狀態：<span style="color:var(--green);font-weight:600;">已是最新大表版本</span>
    </div>
    <button class="btn btn-primary" style="margin-top:16px;" onclick="closeSheet()">關閉視窗</button>
  `;
  document.getElementById('sheetOverlay').classList.add('open');
}
function closeSheet(){ document.getElementById('sheetOverlay').classList.remove('open'); }
function closeSheetOnBg(e){ if(e.target.id==='sheetOverlay') closeSheet(); }
</script>
</body>
</html>
"""

# 使用 .replace() 安全注入 JSON
HTML_CODE = RAW_HTML_TEMPLATE.replace(
    "__USER_DATA__", json.dumps(backend_user_info, ensure_ascii=False)
).replace(
    "__SCHEDULE_DATA__", json.dumps(backend_schedule, ensure_ascii=False)
).replace(
    "__EXCHANGE_DATA__", json.dumps(backend_exchange_candidates, ensure_ascii=False)
).replace(
    "__STATUS_DATA__", json.dumps(duty_status, ensure_ascii=False)
)

components.html(HTML_CODE, height=1000, scrolling=False)
