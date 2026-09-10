import streamlit as st
import streamlit.components.v1 as components

# 1. 頁面基礎設定
st.set_page_config(
    page_title="CREW DUTY ENGINE",
    page_icon="🚆",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 2. 徹底清空 Streamlit 所有原生外框 margin/padding，強制 iframe 填滿 100dvh 視口
st.markdown(
    """
    <style>
    /* 隱藏原生頁首、工具列與頁尾 */
    header[data-testid="stHeader"], 
    [data-testid="stToolbar"], 
    [data-testid="stDecoration"],
    footer {
        display: none !important;
        height: 0px !important;
    }
    
    /* 鎖定全螢幕視口 */
    html, body, .stApp, [data-testid="stAppViewContainer"] {
        padding: 0 !important;
        margin: 0 !important;
        background-color: #070B10 !important;
        overflow: hidden !important;
        height: 100vh !important;
        height: 100dvh !important;
    }

    [data-testid="stMainBlockContainer"], .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
        height: 100vh !important;
        height: 100dvh !important;
        overflow: hidden !important;
    }

    div[data-testid="stElementContainer"] {
        margin: 0 !important;
        padding: 0 !important;
    }

    /* 強制元件 iframe 固定填滿視窗 */
    iframe {
        border: none !important;
        width: 100vw !important;
        height: 100vh !important;
        height: 100dvh !important;
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        z-index: 999999 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 3. 貼齊視口與最佳化手機 Margins 的單頁應用 HTML/CSS/JS
HTML_CODE = """
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
<title>CREW DUTY ENGINE — Redesign Concept</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&family=IBM+Plex+Sans+TC:wght@400;500;600;700&display=swap');

:root{
  --ink-900:#070B10;
  --ink-800:#0E141C;
  --ink-700:#141C26;
  --ink-600:#1B2530;
  --line:#232E3A;
  --line-soft:#1A222C;
  --paper:#ECF1F5;
  --dim:#8492A1;
  --dim-2:#59636E;
  --blue:#4C9AE0;
  --blue-dim:rgba(76,154,224,0.13);
  --amber:#E3A13D;
  --amber-dim:rgba(227,161,61,0.14);
  --red:#E1615C;
  --red-dim:rgba(225,97,92,0.14);
  --green:#4FB88A;
  --green-dim:rgba(79,184,138,0.14);
  --purple:#9B8CE0;
  --purple-dim:rgba(155,140,224,0.14);
  --grey:#7A8794;
  --grey-dim:rgba(122,135,148,0.14);
}

*{box-sizing:border-box;}
html,body{
  margin:0;
  padding:0;
  background:var(--ink-900);
  color:var(--paper);
  font-family:'IBM Plex Sans TC','IBM Plex Mono',sans-serif;
  -webkit-font-smoothing:antialiased;
  height:100%;
  overflow:hidden;
}
.mono{font-family:'IBM Plex Mono',monospace;font-variant-numeric:tabular-nums;}

/* App Shell */
.app{
  max-width:480px;
  margin:0 auto;
  height:100vh;
  height:100dvh;
  display:flex;
  flex-direction:column;
  position:relative;
  background:
    radial-gradient(1200px 400px at 50% -120px, rgba(76,154,224,0.08), transparent 60%),
    var(--ink-900);
}

/* Topbar 頂部對齊 */
.topbar{
  position:sticky; top:0; z-index:20;
  display:flex; align-items:center; justify-content:space-between;
  padding:calc(10px + env(safe-area-inset-top, 0px)) 16px 10px;
  background:rgba(7, 11, 16, 0.92);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(35, 46, 58, 0.5);
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
  background:var(--ink-700);
  border:1px solid var(--line);
  padding:6px 10px 6px 12px;
  border-radius:8px;
  font-size:12.5px;font-weight:600;
  color:var(--paper);
  font-family:'IBM Plex Mono',monospace;
}
.unit-chip .dot{width:6px;height:6px;border-radius:50%;background:var(--green);flex:none;}
.unit-chip svg{width:11px;height:11px;opacity:0.5;}

/* Main 獨立滾動區域，預留底部 Tabbar 空間 */
main{
  flex:1;
  padding:12px 16px calc(76px + env(safe-area-inset-bottom, 0px));
  overflow-y:auto;
  -webkit-overflow-scrolling:touch;
}
.screen{display:none; animation:fadeIn 0.28s ease;}
.screen.active{display:block;}
@keyframes fadeIn{from{opacity:0; transform:translateY(4px);} to{opacity:1; transform:none;}}

.section-label{
  font-size:11px; color:var(--dim-2); font-weight:600;
  letter-spacing:0.2px; margin:16px 2px 8px;
}
.section-label:first-child{margin-top:2px;}

/* Hero (Home) */
.hero{
  border:1px solid var(--line);
  border-radius:14px;
  background:linear-gradient(165deg, var(--ink-700), var(--ink-800));
  padding:18px 16px;
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

/* Quick actions & Panel */
.action-row{
  display:flex; align-items:center; gap:12px;
  padding:12px 4px; border-bottom:1px solid var(--line-soft);
  cursor:pointer;
}
.action-row:last-child{border-bottom:none;}
.action-icon{
  width:34px;height:34px;border-radius:8px;flex:none;
  display:flex;align-items:center;justify-content:center;
  background:var(--ink-700); border:1px solid var(--line);
}
.action-icon svg{width:16px;height:16px;stroke:var(--blue);}
.action-body{flex:1;min-width:0;}
.action-title{font-size:13.5px;font-weight:600;color:var(--paper);}
.action-sub{font-size:11px;color:var(--dim-2);margin-top:1px;}
.action-chev{color:var(--dim-2);}

.panel{
  border:1px solid var(--line);
  border-radius:12px;
  background:var(--ink-800);
  padding:2px 12px;
}

/* Week group & Duty Row */
.week-head{
  display:flex;justify-content:space-between;align-items:baseline;
  padding:10px 2px 6px; margin-top:2px;
}
.week-head .w-title{font-size:12px;font-weight:600;color:var(--dim);}
.week-head .w-meta{font-size:10.5px;color:var(--dim-2);font-family:'IBM Plex Mono',monospace;}

.duty-row{
  display:flex;align-items:center;gap:12px;
  padding:10px 2px;
  border-bottom:1px solid var(--line-soft);
  cursor:pointer;
}
.duty-row:last-child{border-bottom:none;}
.duty-date{width:36px;flex:none;text-align:center;}
.duty-date .d{font-family:'IBM Plex Mono',monospace;font-size:15px;font-weight:600;color:var(--paper);line-height:1.1;}
.duty-date .w{font-size:9.5px;color:var(--dim-2);margin-top:1px;}
.duty-bar{width:3px;align-self:stretch;border-radius:3px;flex:none;background:var(--dim-2);}
.duty-bar.off{background:var(--red);}
.duty-bar.split{background:var(--purple);}
.duty-bar.town{background:var(--grey);}
.duty-bar.holiday{background:var(--amber);}
.duty-main{flex:1;min-width:0;}
.duty-times{
  font-family:'IBM Plex Mono',monospace;font-size:14px;font-weight:600;color:var(--paper);
  display:flex; align-items:center; gap:6px;
}
.duty-times .arrow{color:var(--dim-2);font-weight:400;font-size:12px;}
.duty-off-label{font-size:13px;font-weight:600;color:var(--red);}
.duty-off-label.holiday{color:var(--amber);}
.duty-meta{font-size:10.5px;color:var(--dim-2);margin-top:2px;display:flex;gap:8px;align-items:center;}
.duty-tags{display:flex;gap:5px;flex-wrap:wrap;justify-content:flex-end;flex:none;max-width:88px;}

.tag{
  font-size:9px;font-weight:600;padding:2px 5px;border-radius:4px;
  white-space:nowrap; font-family:'IBM Plex Sans TC',sans-serif;
}
.tag.blue{color:var(--blue);background:var(--blue-dim);}
.tag.amber{color:var(--amber);background:var(--amber-dim);}
.tag.red{color:var(--red);background:var(--red-dim);}
.tag.green{color:var(--green);background:var(--green-dim);}
.tag.purple{color:var(--purple);background:var(--purple-dim);}
.tag.grey{color:var(--grey);background:var(--grey-dim);}

.legend-strip{display:flex; flex-wrap:wrap; gap:6px; margin:14px 2px 4px;}
.legend-strip .tag{padding:3px 7px;}

/* Exchange & Search */
.role-tabs{display:flex; gap:8px; margin-bottom:12px;}
.role-tab{
  flex:1; text-align:center; padding:8px 0; border-radius:8px;
  font-size:12.5px; font-weight:600; color:var(--dim);
  background:var(--ink-800); border:1px solid var(--line);
  cursor:pointer;
}
.role-tab.active{color:var(--ink-900); background:var(--blue); border-color:var(--blue);}

.date-scroll{display:flex; gap:8px; overflow-x:auto; padding:2px 2px 10px; scrollbar-width:none;}
.date-scroll::-webkit-scrollbar{display:none;}
.date-chip{
  flex:none; min-width:50px; text-align:center; padding:7px 5px;
  border-radius:9px; border:1px solid var(--line); background:var(--ink-800);
  cursor:pointer;
}
.date-chip .dc-d{font-family:'IBM Plex Mono',monospace; font-size:14px; font-weight:600; color:var(--paper);}
.date-chip .dc-w{font-size:9px; color:var(--dim-2); margin-top:2px;}
.date-chip.holiday .dc-d{color:var(--amber);}
.date-chip.active{background:var(--blue-dim); border-color:var(--blue);}
.date-chip.active .dc-d{color:var(--blue);}

.field-label{font-size:11px; color:var(--dim); margin:12px 2px 6px; font-weight:600;}
.time-window{display:flex; align-items:center; gap:8px;}
.time-input{
  flex:1; background:var(--ink-800); border:1px solid var(--line);
  border-radius:9px; padding:9px 10px;
  font-family:'IBM Plex Mono',monospace; font-size:14px; color:var(--paper); font-weight:600;
  text-align:center; outline:none;
}
.time-input:focus{border-color:var(--blue);}
.time-window-sep{color:var(--dim-2); font-size:12px;}

.btn{
  display:block; width:100%; text-align:center;
  padding:12px; border-radius:9px; border:none;
  font-size:14px; font-weight:600; cursor:pointer;
  font-family:'IBM Plex Sans TC',sans-serif;
}
.btn-primary{background:var(--blue); color:var(--ink-900); margin-top:14px;}
.btn-ghost{background:var(--ink-700); color:var(--paper); border:1px solid var(--line);}

.result-count{font-size:11.5px; color:var(--dim-2); margin:16px 2px 8px;}
.result-card{
  border:1px solid var(--line); border-radius:11px; background:var(--ink-800);
  padding:12px 13px; margin-bottom:8px; cursor:pointer;
}
.rc-top{display:flex; justify-content:space-between; align-items:center;}
.rc-id{font-family:'IBM Plex Mono',monospace; font-size:11px; color:var(--dim-2);}
.rc-name{font-size:13.5px; font-weight:600; color:var(--paper); margin-top:1px;}
.rc-times{font-family:'IBM Plex Mono',monospace; font-size:18px; font-weight:600; color:var(--paper); margin-top:6px;}
.rc-times .arrow{color:var(--dim-2); font-weight:400; font-size:13px; margin:0 4px;}
.rc-bottom{display:flex; justify-content:space-between; align-items:center; margin-top:8px;}
.rc-streak{font-size:10.5px; color:var(--dim-2);}

.empty-state{text-align:center; padding:36px 16px; color:var(--dim-2);}
.empty-state .es-title{font-size:13px; color:var(--dim); font-weight:600; margin-bottom:4px;}
.empty-state .es-sub{font-size:11.5px; line-height:1.5;}

/* Profile */
.profile-head{display:flex; align-items:center; gap:12px; padding:6px 2px 16px;}
.avatar{
  width:44px;height:44px;border-radius:10px; background:var(--ink-700); border:1px solid var(--line);
  display:flex;align-items:center;justify-content:center;
  font-family:'IBM Plex Mono',monospace; font-weight:700; color:var(--blue); font-size:14px;
}
.profile-name{font-size:14.5px; font-weight:600;}
.profile-meta{font-size:11px; color:var(--dim-2); margin-top:2px; font-family:'IBM Plex Mono',monospace;}

.list-row{
  display:flex; justify-content:space-between; align-items:center;
  padding:12px 2px; border-bottom:1px solid var(--line-soft);
}
.list-row:last-child{border-bottom:none;}
.list-row-label{font-size:13px; color:var(--paper);}
.list-row-value{font-size:12px; color:var(--dim-2); font-family:'IBM Plex Mono',monospace;}

/* Bottom Tab Bar 貼齊底部 Safe Area */
.tabbar{
  position:fixed; bottom:0; left:50%; transform:translateX(-50%);
  width:100%; max-width:480px;
  display:flex;
  background:rgba(14,20,28,0.95);
  backdrop-filter:blur(12px);
  border-top:1px solid var(--line);
  padding:6px 4px calc(6px + env(safe-area-inset-bottom, 0px));
  z-index:30;
}
.tab-item{
  flex:1; display:flex; flex-direction:column; align-items:center; gap:3px;
  padding:5px 0; cursor:pointer; color:var(--dim-2);
}
.tab-item svg{width:18px;height:18px; stroke:var(--dim-2); fill:none;}
.tab-item span{font-size:9.5px; font-weight:600;}
.tab-item.active{color:var(--blue);}
.tab-item.active svg{stroke:var(--blue);}

/* Sheet Modal Overlay */
.sheet-overlay{
  position:fixed; inset:0; background:rgba(3,5,8,0.65);
  display:none; align-items:flex-end; justify-content:center; z-index:50;
  backdrop-filter: blur(4px);
}
.sheet-overlay.open{display:flex;}
.sheet{
  width:100%; max-width:480px;
  background:var(--ink-800);
  border-top:1px solid var(--line);
  border-radius:18px 18px 0 0;
  padding:10px 18px calc(20px + env(safe-area-inset-bottom, 0px));
  max-height:80vh; overflow-y:auto;
  animation:slideUp 0.24s ease;
}
@keyframes slideUp{from{transform:translateY(20px); opacity:0.6;} to{transform:none; opacity:1;}}
.sheet-handle{width:36px;height:4px;border-radius:3px;background:var(--line);margin:2px auto 14px;}
.sheet-title{font-size:15px; font-weight:700; color:var(--paper);}
.sheet-sub{font-size:11.5px; color:var(--dim-2); margin-top:2px; margin-bottom:16px;}
.sheet-big-times{
  display:flex; align-items:baseline; gap:8px;
  font-family:'IBM Plex Mono',monospace; font-size:24px; font-weight:600; color:var(--paper);
}
.sheet-big-times .arrow{font-size:15px; color:var(--dim-2); font-weight:400;}
.sheet-grid{display:grid; grid-template-columns:1fr 1fr; gap:10px; margin:16px 0;}
.sheet-stat{background:var(--ink-700); border:1px solid var(--line); border-radius:9px; padding:10px 11px;}
.sheet-stat .lbl{font-size:10px; color:var(--dim-2);}
.sheet-stat .val{font-family:'IBM Plex Mono',monospace; font-size:15px; font-weight:600; margin-top:2px;}
.sheet-actions{display:flex; gap:8px; margin-top:4px;}
.sheet-actions .btn{margin-top:0;}
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
    <div class="unit-chip">
      <span class="dot"></span>
      TTN
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg>
    </div>
  </header>

  <main id="mainContainer">

    <!-- ============ HOME ============ -->
    <section class="screen active" id="screen-home">
      <div class="hero">
        <div class="hero-top">
          <span class="hero-status" id="heroStatus"><span class="dot"></span>今日休假・DO1</span>
          <span class="hero-cycle mono">週期 09/06–10/03</span>
        </div>
        <div class="hero-label">距下次出勤簽到</div>
        <div class="countdown">
          <span class="num" id="cd-h">--</span><span class="unit">時</span>
          <span class="num" id="cd-m">--</span><span class="unit">分</span>
          <span class="num" id="cd-s">--</span><span class="unit">秒</span>
        </div>
        <div class="hero-next">
          <div class="hero-next-left">
            <div class="hero-next-date">9/17（四）NG1547</div>
            <div class="hero-next-times">16:24 <span style="color:var(--dim-2);font-weight:400;font-size:13px;">→</span> 24:30</div>
          </div>
          <div class="hero-next-code">8h06m</div>
        </div>
      </div>

      <div class="section-label">快速功能</div>
      <div class="panel">
        <div class="action-row" onclick="showTab('schedule')">
          <div class="action-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M8 3v4M16 3v4M3 10h18"/></svg></div>
          <div class="action-body">
            <div class="action-title">我的月班表</div>
            <div class="action-sub">逐日清單・含班間合規標示</div>
          </div>
          <span class="action-chev">›</span>
        </div>
        <div class="action-row" onclick="showTab('exchange')">
          <div class="action-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M7 7h11M18 7l-3-3M18 7l-3 3M17 17H6M6 17l3 3M6 17l3-3"/></svg></div>
          <div class="action-body">
            <div class="action-title">換班快搜</div>
            <div class="action-sub">依 Sign-in 時間窗篩選可換組員</div>
          </div>
          <span class="action-chev">›</span>
        </div>
        <div class="action-row" onclick="showTab('exchange')">
          <div class="action-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg></div>
          <div class="action-body">
            <div class="action-title">換假快搜</div>
            <div class="action-sub">尋找同單位可交換之休假日</div>
          </div>
          <span class="action-chev">›</span>
        </div>
      </div>

      <div class="section-label">本週提醒</div>
      <div class="panel" style="padding:12px 13px;">
        <div style="display:flex; gap:10px; align-items:flex-start;">
          <span class="tag amber" style="margin-top:2px;">連續4日</span>
          <div style="font-size:12px; color:var(--dim); line-height:1.5;">
            9/20–9/23 為連續 4 日出勤，9/23 下班至 9/24 上班間隔 9h42m，已低於 11 小時法定門檻，系統標示為「不建議換班」時段。
          </div>
        </div>
      </div>
    </section>

    <!-- ============ SCHEDULE ============ -->
    <section class="screen" id="screen-schedule">
      <div class="section-label" style="margin-top:2px;">我的月班表 · A023001 王志遠</div>

      <div class="week-head">
        <span class="w-title">09/06 — 09/12</span>
        <span class="w-meta">36h00m</span>
      </div>
      <div class="panel" id="week1"></div>

      <div class="week-head">
        <span class="w-title">09/13 — 09/19</span>
        <span class="w-meta">33h50m</span>
      </div>
      <div class="panel" id="week2"></div>

      <div class="week-head">
        <span class="w-title">09/20 — 09/26</span>
        <span class="w-meta">37h50m ⚠︎</span>
      </div>
      <div class="panel" id="week3"></div>

      <div class="legend-strip">
        <span class="tag grey">偏駐</span>
        <span class="tag red">休假日</span>
        <span class="tag green">特休</span>
        <span class="tag amber">工時 &gt; 8.5h</span>
        <span class="tag amber">國定假日</span>
        <span class="tag purple">破輪</span>
        <span class="tag grey">非正線勤務</span>
      </div>
    </section>

    <!-- ============ EXCHANGE ============ -->
    <section class="screen" id="screen-exchange">
      <div class="section-label" style="margin-top:2px;">換班快搜</div>

      <div class="role-tabs">
        <div class="role-tab" data-role="駕駛">駕駛</div>
        <div class="role-tab" data-role="列車長">列車長</div>
        <div class="role-tab active" data-role="服勤員">服勤員</div>
      </div>

      <div class="field-label">選擇換班日期</div>
      <div class="date-scroll" id="dateScroll"></div>

      <div class="field-label">Sign-in 時間窗</div>
      <div class="time-window">
        <input class="time-input" id="timeFrom" value="05:00">
        <span class="time-window-sep">至</span>
        <input class="time-input" id="timeTo" value="10:00">
      </div>

      <button class="btn btn-primary" onclick="runSearch()">開始搜尋</button>

      <div id="searchResults"></div>
    </section>

    <!-- ============ PROFILE ============ -->
    <section class="screen" id="screen-profile">
      <div class="profile-head">
        <div class="avatar">王</div>
        <div>
          <div class="profile-name">王志遠</div>
          <div class="profile-meta">A023001 · TTN · 服勤員</div>
        </div>
      </div>

      <div class="section-label">帳號</div>
      <div class="panel">
        <div class="list-row"><span class="list-row-label">所屬單位</span><span class="list-row-value">TTN</span></div>
        <div class="list-row"><span class="list-row-label">權限層級</span><span class="list-row-value">CREW</span></div>
        <div class="list-row"><span class="list-row-label">大表更新時間</span><span class="list-row-value">2026-09-05 20:40</span></div>
      </div>

      <div class="section-label">其他</div>
      <div class="panel">
        <div class="list-row"><span class="list-row-label">問題回報與建議</span><span class="action-chev">›</span></div>
        <div class="list-row"><span class="list-row-label">系統使用須知</span><span class="action-chev">›</span></div>
        <div class="list-row"><span class="list-row-label">登出</span><span class="action-chev">›</span></div>
      </div>
    </section>

  </main>

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

  <div class="sheet-overlay" id="sheetOverlay" onclick="closeSheetOnBg(event)">
    <div class="sheet" id="sheet"></div>
  </div>

</div>

<script>
/* Mock Data & Render Engine */
const schedule = {
  week1:[
    {d:9,wd:'日',code:'NH1005',start:'05:51',end:'13:51',dur:'8h00m',rest:'11.0h',restTag:'green',tags:[]},
    {d:10,wd:'一',code:'NF0018',start:'07:24',end:'15:24',dur:'8h00m',rest:'16.0h',restTag:'green',tags:[]},
    {d:11,wd:'二',code:'NG0001',start:'05:26',end:'15:06',dur:'9h40m',rest:'23.5h',restTag:'green',tags:['工時>8.5h']},
    {d:12,wd:'三',code:'NH0543',start:'14:34',end:'24:16',dur:'9h42m',rest:null,restTag:null,tags:['工時>8.5h']},
    {d:13,wd:'四',off:'DO1',barType:'off',tags:['休假日']},
    {d:14,wd:'五',off:'DO3X',barType:'off',tags:['休假日']},
  ],
  week2:[
    {d:12,wd:'六',code:'NF1518',start:'14:06',end:'22:06',dur:'8h00m',rest:'13.2h',restTag:'green',tags:[]},
    {d:13,wd:'日',code:'NF2531',start:'15:16',end:'23:16',dur:'8h00m',rest:'12.0h',restTag:'amber',tags:[]},
    {d:14,wd:'一',code:'NH1032',start:'11:16',end:'19:16',dur:'8h00m',rest:'12.1h',restTag:'green',tags:[]},
    {d:15,wd:'二',code:'TOWN',start:'07:30',end:'16:30',dur:'9h00m',rest:null,restTag:null,tags:['非正線勤務'],barType:'town'},
    {d:16,wd:'三',off:'DO1',barType:'off',tags:['休假日']},
    {d:17,wd:'四',code:'NG1547',start:'16:24',end:'24:30',dur:'8h06m',rest:'9.7h',restTag:'red',tags:[]},
    {d:18,wd:'五',code:'NF0542',start:'15:49',end:'24:01',dur:'8h12m',rest:'14.7h',restTag:'green',tags:[]},
  ],
  week3:[
    {d:19,wd:'六',off:'DO3X',barType:'off',tags:['休假日']},
    {d:20,wd:'日',code:'NG1548',start:'14:46',end:'24:30',dur:'9h44m',rest:'10.1h',restTag:'red',tags:['工時>8.5h']},
    {d:21,wd:'一',code:'NG0543',start:'14:34',end:'24:16',dur:'9h42m',rest:'10.3h',restTag:'red',tags:['工時>8.5h']},
    {d:22,wd:'二',code:'NG0549',start:'16:34',end:'24:38',dur:'8h04m',rest:'13.9h',restTag:'green',tags:[]},
    {d:23,wd:'三',code:'NG0543',start:'14:34',end:'24:16',dur:'9h42m',rest:'9.7h',restTag:'red',tags:['工時>8.5h']},
    {d:24,wd:'四',off:'DO1',barType:'off',tags:['休假日','國定假日'],barType2:'holiday'},
    {d:25,wd:'五',code:'NG0006',start:'06:01',end:'16:01',dur:'10h00m',rest:null,restTag:null,tags:['國定假日','工時>8.5h'],barType:'holiday'},
    {d:26,wd:'六',code:'NG0023',start:'07:46',end:'16:51',dur:'9h05m',rest:null,restTag:null,tags:['國定假日'],barType:'holiday'},
  ]
};

const exchangeCandidates = {
  '服勤員':[
    {id:'A024118', name:'林彥廷', start:'06:01', end:'16:01', dur:'10h00m', restBefore:'13.2h', restTag:'green', streak:'連續值勤 2 日'},
    {id:'A021987', name:'陳淨怡', start:'07:30', end:'16:30', dur:'9h00m', restBefore:'9.8h', restTag:'red', streak:'連續值勤 5 日 · 前一班間隔不足'},
    {id:'A024373', name:'蔡明鈞', start:'05:26', end:'15:06', dur:'9h40m', restBefore:'23.5h', restTag:'green', streak:'休假後首日出勤'},
    {id:'A023295', name:'黃振山', start:'08:15', end:'16:30', dur:'8h15m', restBefore:'11.4h', restTag:'amber', streak:'連續值勤 3 日'},
  ],
  '駕駛':[
    {id:'A011203', name:'李國安', start:'05:10', end:'13:40', dur:'8h30m', restBefore:'15.0h', restTag:'green', streak:'連續值勤 1 日'},
    {id:'A011488', name:'周文彬', start:'06:40', end:'14:20', dur:'7h40m', restBefore:'10.5h', restTag:'red', streak:'連續值勤 4 日 · 前一班間隔不足'},
  ],
  '列車長':[
    {id:'A017702', name:'許家豪', start:'05:00', end:'13:00', dur:'8h00m', restBefore:'12.4h', restTag:'green', streak:'連續值勤 2 日'},
  ]
};

const dateOptions = [
  {d:'9/16', wd:'三', holiday:false},
  {d:'9/17', wd:'四', holiday:false},
  {d:'9/24', wd:'四', holiday:true, name:'中秋節'},
  {d:'9/25', wd:'五', holiday:true, name:'中秋疏運'},
  {d:'9/28', wd:'一', holiday:true, name:'教師節'},
];

const restTagLabel = {green:'班間合規', amber:'班間臨界', red:'班間不足'};

function renderWeek(containerId, days){
  const el = document.getElementById(containerId);
  el.innerHTML = days.map((day, i) => {
    let barClass = 'duty-bar';
    if(day.barType === 'off') barClass += ' off';
    if(day.barType === 'split') barClass += ' split';
    if(day.barType === 'town') barClass += ' town';
    if(day.barType === 'holiday') barClass += ' holiday';

    const tagHtml = (day.tags||[]).map(t=>{
      let cls = 'grey';
      if(t==='休假日') cls='red';
      if(t==='國定假日') cls='amber';
      if(t==='工時>8.5h') cls='amber';
      if(t==='特休') cls='green';
      if(t==='破輪') cls='purple';
      if(t==='非正線勤務') cls='grey';
      return `<span class="tag ${cls}">${t}</span>`;
    }).join('');

    const timesHtml = day.off
      ? `<div class="duty-off-label ${day.barType==='holiday'?'holiday':''}">${day.off}</div>`
      : `<div class="duty-times">${day.start}<span class="arrow">→</span>${day.end}</div>
         <div class="duty-meta"><span>${day.code}</span><span>${day.dur}</span>${day.rest ? `<span style="color:var(--${day.restTag==='red'?'red':day.restTag==='amber'?'amber':'green'})">班間 ${day.rest}</span>` : ''}</div>`;

    return `
      <div class="duty-row" onclick='openDaySheet(${JSON.stringify(day)})'>
        <div class="duty-date"><div class="d mono">${day.d}</div><div class="w">${day.wd}</div></div>
        <div class="${barClass}"></div>
        <div class="duty-main">${timesHtml}</div>
        <div class="duty-tags">${tagHtml}</div>
      </div>`;
  }).join('');
}
renderWeek('week1', schedule.week1);
renderWeek('week2', schedule.week2);
renderWeek('week3', schedule.week3);

function openDaySheet(day){
  const sheet = document.getElementById('sheet');
  if(day.off){
    sheet.innerHTML = `
      <div class="sheet-handle"></div>
      <div class="sheet-title">9/${day.d}（${day.wd}）· ${day.off}</div>
      <div class="sheet-sub">${(day.tags||[]).join(' · ')}</div>
      <div style="font-size:12.5px; color:var(--dim); line-height:1.6; margin:10px 0 16px;">
        本日為排定休假，如需與他人交換休假日，可至「換假快搜」尋找同單位可交換組員。
      </div>
      <div class="sheet-actions">
        <button class="btn btn-primary" style="flex:1" onclick="closeSheet(); showTab('exchange')">前往換假快搜</button>
      </div>`;
  } else {
    const restColor = day.restTag==='red' ? '--red' : day.restTag==='amber' ? '--amber' : '--green';
    sheet.innerHTML = `
      <div class="sheet-handle"></div>
      <div class="sheet-title">9/${day.d}（${day.wd}）· ${day.code}</div>
      <div class="sheet-sub">${(day.tags||[]).join(' · ') || '一般勤務'}</div>
      <div class="sheet-big-times">${day.start}<span class="arrow">→</span>${day.end}</div>
      <div class="sheet-grid">
        <div class="sheet-stat"><div class="lbl">工時</div><div class="val">${day.dur}</div></div>
        <div class="sheet-stat"><div class="lbl">與前班間隔</div><div class="val" style="color:var(${restColor})">${day.rest || '—'}</div></div>
      </div>
      <div class="sheet-actions">
        <button class="btn btn-ghost" style="flex:1" onclick="closeSheet()">關閉</button>
        <button class="btn btn-primary" style="flex:1" onclick="closeSheet(); showTab('exchange')">尋找換班對象</button>
      </div>`;
  }
  document.getElementById('sheetOverlay').classList.add('open');
}
function closeSheet(){ document.getElementById('sheetOverlay').classList.remove('open'); }
function closeSheetOnBg(e){ if(e.target.id==='sheetOverlay') closeSheet(); }

let currentRole = '服勤員';
document.querySelectorAll('.role-tab').forEach(tab=>{
  tab.addEventListener('click', ()=>{
    document.querySelectorAll('.role-tab').forEach(t=>t.classList.remove('active'));
    tab.classList.add('active');
    currentRole = tab.dataset.role;
    document.getElementById('searchResults').innerHTML = '';
  });
});

const dateScroll = document.getElementById('dateScroll');
dateScroll.innerHTML = dateOptions.map((opt,i)=>`
  <div class="date-chip ${opt.holiday?'holiday':''} ${i===1?'active':''}" data-date="${opt.d}">
    <div class="dc-d mono">${opt.d}</div>
    <div class="dc-w">${opt.name || opt.wd}</div>
  </div>`).join('');
dateScroll.querySelectorAll('.date-chip').forEach(chip=>{
  chip.addEventListener('click', ()=>{
    dateScroll.querySelectorAll('.date-chip').forEach(c=>c.classList.remove('active'));
    chip.classList.add('active');
  });
});

function toMinutes(t){ const [h,m] = t.split(':').map(Number); return h*60+m; }

function runSearch(){
  const from = toMinutes(document.getElementById('timeFrom').value || '00:00');
  const to = toMinutes(document.getElementById('timeTo').value || '23:59');
  const pool = exchangeCandidates[currentRole] || [];
  const results = pool.filter(c => {
    const st = toMinutes(c.start);
    return st >= from && st <= to;
  });
  const container = document.getElementById('searchResults');
  if(results.length === 0){
    container.innerHTML = `
      <div class="empty-state">
        <div class="es-title">此時間窗內無可換組員</div>
        <div class="es-sub">試著放寬 Sign-in 時間窗，<br>或切換其他職位類別查詢。</div>
      </div>`;
    return;
  }
  container.innerHTML = `<div class="result-count">找到 ${results.length} 位可能人選</div>` +
    results.map(c => `
      <div class="result-card" onclick='openCandidateSheet(${JSON.stringify(c)})'>
        <div class="rc-top">
          <div>
            <div class="rc-id mono">${c.id}</div>
            <div class="rc-name">${c.name}</div>
          </div>
          <span class="tag ${c.restTag}">${restTagLabel[c.restTag]}</span>
        </div>
        <div class="rc-times">${c.start}<span class="arrow">→</span>${c.end}</div>
        <div class="rc-bottom">
          <span class="rc-streak">${c.streak}</span>
          <span style="font-size:10.5px; color:var(--dim-2);" class="mono">${c.dur}</span>
        </div>
      </div>`).join('');
}

function openCandidateSheet(c){
  const sheet = document.getElementById('sheet');
  const restColor = c.restTag==='red' ? '--red' : c.restTag==='amber' ? '--amber' : '--green';
  sheet.innerHTML = `
    <div class="sheet-handle"></div>
    <div class="sheet-title">${c.name} · ${c.id}</div>
    <div class="sheet-sub">${c.streak}</div>
    <div class="sheet-big-times">${c.start}<span class="arrow">→</span>${c.end}</div>
    <div class="sheet-grid">
      <div class="sheet-stat"><div class="lbl">工時</div><div class="val">${c.dur}</div></div>
      <div class="sheet-stat"><div class="lbl">前一班間隔</div><div class="val" style="color:var(${restColor})">${c.restBefore}</div></div>
    </div>
    <div style="font-size:11.5px; color:var(--dim-2); line-height:1.5; margin-bottom:12px;">
      點選下方可檢視該組員完整月班表，確認是否適合提出換班申請。
    </div>
    <div class="sheet-actions">
      <button class="btn btn-ghost" style="flex:1" onclick="closeSheet()">關閉</button>
      <button class="btn btn-primary" style="flex:1" onclick="closeSheet()">檢視完整月班表</button>
    </div>`;
  document.getElementById('sheetOverlay').classList.add('open');
}
runSearch();

function showTab(name){
  document.querySelectorAll('.screen').forEach(s=>s.classList.remove('active'));
  document.getElementById('screen-'+name).classList.add('active');
  document.querySelectorAll('.tab-item').forEach(t=>t.classList.toggle('active', t.dataset.tab===name));
  document.getElementById('mainContainer').scrollTop = 0;
}

function pad(n){ return String(n).padStart(2,'0'); }
function updateCountdown(){
  const now = new Date();
  const target = new Date();
  target.setHours(now.getHours()+3, now.getMinutes()+22, 15, 0);
  let diff = Math.max(0, target - now);
  const h = Math.floor(diff/3600000);
  const m = Math.floor((diff%3600000)/60000);
  const s = Math.floor((diff%60000)/1000);
  document.getElementById('cd-h').textContent = pad(h);
  document.getElementById('cd-m').textContent = pad(m);
  document.getElementById('cd-s').textContent = pad(s);
}
updateCountdown();
setInterval(updateCountdown, 1000);
</script>
</body>
</html>
"""

# 4. 渲染全視口元件
components.html(HTML_CODE, height=1000, scrolling=False)
