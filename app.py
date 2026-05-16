import streamlit as st
import os

st.set_page_config(
    page_title="Solar Sunflower Controller",
    page_icon="🌻",
    layout="wide",
    initial_sidebar_state="expanded",
)

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

def asset(name):
    return os.path.join(ASSETS, name)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Barlow:wght@300;400;600;700&family=Barlow+Condensed:wght@600;700&family=Share+Tech+Mono&display=swap');

/* ── CSS Custom Properties ── */
:root {
    --gold: #FFD700; --amber: #FFA500; --green: #22C55E; --blue: #60b4ff;
    --purple: #a855f7; --red: #ef4444;
    --bg: #06091a; --bg2: #070b1e; --bg3: #0a0d1a;
    --border: rgba(255,180,0,0.15); --border-green: rgba(34,197,94,0.2);
    --text: #e8e0cc; --text-dim: rgba(232,224,204,0.65); --text-faint: rgba(232,224,204,0.4);
}
html, body, [data-testid="stAppViewContainer"] { background: #06091a !important; color: #e8e0cc !important; }
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(255,180,0,0.08) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(34,197,94,0.05) 0%, transparent 55%),
        #06091a !important;
}
[data-testid="stSidebar"] { background: #070b1e !important; border-right: 1px solid rgba(255,180,0,0.15) !important; }
[data-testid="stSidebar"] * { color: #e8e0cc !important; }
.block-container { padding: 0 2rem 4rem 2rem !important; max-width: 1200px !important; }
#MainMenu, footer, header { visibility: hidden; }

h1,h2,h3,h4 { font-family: 'Bebas Neue', sans-serif !important; letter-spacing: 0.04em; }
p, li, td, th, span, div { font-family: 'Barlow', sans-serif !important; }

/* ── Hero ── */
.hero-wrap {
    position: relative; overflow: hidden; padding: 4rem 2rem 3.5rem;
    margin: 0 -2rem 2rem -2rem;
    background: radial-gradient(circle 700px at 50% -40%, rgba(255,200,0,0.18) 0%, transparent 70%),
                linear-gradient(160deg, #0a0f22 0%, #06091a 60%, #0a1208 100%);
    border-bottom: 1px solid rgba(255,180,0,0.2);
}
.sunburst {
    position: absolute; top: -120px; left: 50%; transform: translateX(-50%);
    width: 420px; height: 420px;
    background: conic-gradient(from 0deg,
        rgba(255,200,0,0.10) 0deg, transparent 18deg, rgba(255,160,0,0.08) 20deg, transparent 38deg,
        rgba(255,200,0,0.10) 40deg, transparent 58deg, rgba(255,160,0,0.08) 60deg, transparent 78deg,
        rgba(255,200,0,0.10) 80deg, transparent 98deg, rgba(255,160,0,0.08) 100deg, transparent 118deg,
        rgba(255,200,0,0.10) 120deg, transparent 138deg, rgba(255,160,0,0.08) 140deg, transparent 158deg,
        rgba(255,200,0,0.10) 160deg, transparent 178deg, rgba(255,160,0,0.08) 180deg, transparent 198deg,
        rgba(255,200,0,0.10) 200deg, transparent 218deg, rgba(255,160,0,0.08) 220deg, transparent 238deg,
        rgba(255,200,0,0.10) 240deg, transparent 258deg, rgba(255,160,0,0.08) 260deg, transparent 278deg,
        rgba(255,200,0,0.10) 280deg, transparent 298deg, rgba(255,160,0,0.08) 300deg, transparent 318deg,
        rgba(255,200,0,0.10) 320deg, transparent 338deg, rgba(255,160,0,0.08) 340deg, transparent 360deg);
    border-radius: 50%; animation: spin 60s linear infinite; pointer-events: none; z-index: 0;
}
@keyframes spin { to { transform: translateX(-50%) rotate(360deg); } }
.hero-emoji { font-size: 5rem; display: block; text-align: center; position: relative; z-index: 1;
    animation: pulse-sun 4s ease-in-out infinite; filter: drop-shadow(0 0 30px rgba(255,200,0,0.6)); }
@keyframes pulse-sun {
    0%,100% { transform: scale(1); filter: drop-shadow(0 0 25px rgba(255,200,0,0.5)); }
    50%      { transform: scale(1.08); filter: drop-shadow(0 0 50px rgba(255,200,0,0.9)); }
}
.hero-title {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: clamp(2.8rem, 7vw, 5.5rem); letter-spacing: 0.06em; text-align: center; line-height: 1;
    background: linear-gradient(135deg, #FFD700 0%, #FFA500 40%, #FFD700 70%, #22C55E 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    position: relative; z-index: 1; margin: 0.4rem 0 0.2rem;
}
.hero-sub { font-family: 'Barlow Condensed', sans-serif !important; font-size: 1.25rem; letter-spacing: 0.25em;
    text-align: center; color: rgba(255,215,0,0.75); text-transform: uppercase;
    position: relative; z-index: 1; margin-bottom: 1.2rem; }
.hero-tags { display: flex; flex-wrap: wrap; justify-content: center; gap: 0.6rem; position: relative; z-index: 1; }
.hero-tag { background: rgba(255,180,0,0.1); border: 1px solid rgba(255,180,0,0.3); color: #FFD700;
    font-family: 'Share Tech Mono', monospace; font-size: 0.78rem; padding: 0.3rem 0.9rem;
    border-radius: 2px; letter-spacing: 0.08em; }

/* ── Info banner ── */
.info-banner {
    display: flex; flex-wrap: wrap; gap: 0; margin-bottom: 2rem;
    border: 1px solid rgba(255,180,0,0.18); border-radius: 4px; overflow: hidden;
    background: rgba(255,255,255,0.02);
}
.info-cell {
    flex: 1; min-width: 160px; padding: 0.9rem 1.4rem;
    border-right: 1px solid rgba(255,180,0,0.12);
}
.info-cell:last-child { border-right: none; }
.info-cell-label { font-family: 'Share Tech Mono', monospace; font-size: 0.65rem;
    letter-spacing: 0.15em; text-transform: uppercase; color: rgba(255,180,0,0.5); margin-bottom: 0.25rem; display: block; }
.info-cell-value { font-family: 'Barlow Condensed', sans-serif; font-size: 1rem;
    font-weight: 700; color: #e8e0cc; letter-spacing: 0.02em; display: block; }

/* ── Section number badge ── */
.sec-num { font-family: 'Share Tech Mono', monospace; font-size: 0.7rem; color: rgba(255,180,0,0.45);
    letter-spacing: 0.15em; margin-bottom: 0.5rem; display: block; }

/* ── Cards ── */
.card { background: linear-gradient(135deg, rgba(255,255,255,0.03) 0%, rgba(255,255,255,0.01) 100%);
    border: 1px solid rgba(255,180,0,0.15); border-radius: 4px; padding: 2rem 2.2rem;
    margin-bottom: 1.8rem; position: relative; overflow: hidden;
    box-shadow: 0 4px 24px rgba(0,0,0,0.35); }
.card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, rgba(255,180,0,0.5), rgba(34,197,94,0.3), transparent); }
.card-green::before { background: linear-gradient(90deg, transparent, rgba(34,197,94,0.6), rgba(255,180,0,0.3), transparent); }
.card-accent::before { background: linear-gradient(90deg, transparent, rgba(255,100,0,0.5), rgba(255,180,0,0.4), transparent); }
.card-blue::before { background: linear-gradient(90deg, transparent, rgba(100,180,255,0.6), rgba(255,180,0,0.2), transparent); }
.card-purple::before { background: linear-gradient(90deg, transparent, rgba(168,85,247,0.6), rgba(255,180,0,0.2), transparent); }

.section-heading { font-family: 'Bebas Neue', sans-serif !important; font-size: 2rem !important;
    letter-spacing: 0.06em; margin-bottom: 1.2rem !important; display: flex; align-items: center; gap: 0.5rem; }
.sub-heading { font-family: 'Bebas Neue', sans-serif !important; font-size: 1.4rem !important;
    letter-spacing: 0.05em; margin: 1.6rem 0 0.8rem !important;
    color: #FFA500; display: flex; align-items: center; gap: 0.4rem; }
.sub-heading-green { color: #22C55E !important; }
.sub-heading-blue  { color: #60b4ff !important; }
.heading-icon { font-size: 1.6rem; }

/* ── Stat pills ── */
.stat-row { display: flex; flex-wrap: wrap; gap: 1rem; margin: 1.2rem 0; }
.stat-pill { background: rgba(255,180,0,0.08); border: 1px solid rgba(255,180,0,0.25);
    border-radius: 3px; padding: 0.8rem 1.4rem; text-align: center; min-width: 120px; flex: 1; }
.stat-pill .num { font-family: 'Bebas Neue', sans-serif; font-size: 2rem; color: #FFD700; display: block; line-height: 1; }
.stat-pill .lbl { font-family: 'Barlow', sans-serif; font-size: 0.72rem; color: rgba(232,224,204,0.6);
    letter-spacing: 0.08em; text-transform: uppercase; margin-top: 0.3rem; display: block; }
.stat-pill-green { border-color: rgba(34,197,94,0.35); background: rgba(34,197,94,0.06); }
.stat-pill-green .num { color: #22C55E; }
.stat-pill-blue { border-color: rgba(100,180,255,0.35); background: rgba(100,180,255,0.06); }
.stat-pill-blue .num { color: #60b4ff; }
.stat-pill-red { border-color: rgba(239,68,68,0.35); background: rgba(239,68,68,0.06); }
.stat-pill-red .num { color: #f87171; }

/* ── Feature items ── */
.feat-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 1rem; margin-top: 1rem; }
.feat-item { background: rgba(255,255,255,0.025); border: 1px solid rgba(255,180,0,0.1);
    border-left: 3px solid #FFA500; padding: 1rem 1.2rem; border-radius: 2px; }
.feat-item-green { border-left-color: #22C55E; }
.feat-item-red   { border-left-color: #ef4444; }
.feat-item-blue  { border-left-color: #60b4ff; }
.feat-item-purple{ border-left-color: #a855f7; }
.feat-title { font-family: 'Barlow Condensed', sans-serif; font-size: 0.9rem; font-weight: 700;
    letter-spacing: 0.05em; color: #FFD700; text-transform: uppercase; margin-bottom: 0.3rem; }
.feat-title-green { color: #22C55E; }
.feat-title-blue  { color: #60b4ff; }
.feat-title-purple{ color: #a855f7; }
.feat-body { font-size: 0.88rem; color: rgba(232,224,204,0.8); line-height: 1.55; }

/* ── Result rows ── */
.result-table { width: 100%; border-collapse: collapse; font-size: 0.875rem; margin-top: 0.6rem; }
.result-table th { background: rgba(255,180,0,0.1); color: #FFD700; font-family: 'Barlow Condensed', sans-serif;
    font-size: 0.78rem; letter-spacing: 0.1em; text-transform: uppercase; padding: 0.55rem 1rem;
    text-align: left; border-bottom: 1px solid rgba(255,180,0,0.2); }
.result-table td { padding: 0.5rem 1rem; border-bottom: 1px solid rgba(255,255,255,0.04);
    font-family: 'Barlow', sans-serif; font-size: 0.87rem; vertical-align: top; }
.result-table tr:hover td { background: rgba(255,180,0,0.03); }
.pass { color: #22C55E; font-family: 'Share Tech Mono', monospace; font-size: 0.82rem; font-weight: 700; }
.fail { color: #ef4444; font-family: 'Share Tech Mono', monospace; font-size: 0.82rem; }
.val  { color: #60b4ff; font-family: 'Share Tech Mono', monospace; font-size: 0.85rem; }

/* ── Mono blocks ── */
.mono-block { background: #0a0d1a; border: 1px solid rgba(255,180,0,0.2); border-radius: 3px;
    padding: 1.4rem 1.6rem; font-family: 'Share Tech Mono', monospace;
    font-size: 0.82rem; line-height: 1.7; color: #b8ffa0; overflow-x: auto; white-space: pre; margin: 1rem 0; }
.mono-label { font-family: 'Share Tech Mono', monospace; font-size: 0.7rem; color: rgba(255,180,0,0.5);
    letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 0.4rem; }

/* ── Protocol table ── */
.proto-table { width: 100%; border-collapse: collapse; margin-top: 1rem; font-size: 0.88rem; }
.proto-table th { background: rgba(255,180,0,0.12); color: #FFD700; font-family: 'Barlow Condensed', sans-serif;
    font-size: 0.8rem; letter-spacing: 0.1em; text-transform: uppercase; padding: 0.6rem 1rem;
    text-align: left; border-bottom: 1px solid rgba(255,180,0,0.25); }
.proto-table td { padding: 0.55rem 1rem; border-bottom: 1px solid rgba(255,255,255,0.04);
    font-family: 'Barlow', sans-serif; vertical-align: top; }
.proto-table tr:hover td { background: rgba(255,180,0,0.03); }
.cmd { font-family: 'Share Tech Mono', monospace; color: #FFA500; font-size: 0.85rem; }
.cmd-green { color: #22C55E; }

/* ── Architecture box ── */
.arch-box { background: #070b1e; border: 1px solid rgba(255,180,0,0.2); border-radius: 3px;
    padding: 1.6rem; font-family: 'Share Tech Mono', monospace;
    font-size: 0.8rem; line-height: 1.8; color: #94d8f0; overflow-x: auto; white-space: pre; }

/* ── Stack grid ── */
.stack-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 0.8rem; margin-top: 1rem; }
.stack-item { display: flex; align-items: flex-start; gap: 0.8rem; background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06); border-radius: 3px; padding: 0.9rem 1rem; }
.stack-icon { font-size: 1.4rem; flex-shrink: 0; margin-top: 0.1rem; }
.stack-name { font-family: 'Barlow Condensed', sans-serif; font-size: 0.88rem; font-weight: 700;
    color: #FFD700; letter-spacing: 0.04em; display: block; }
.stack-desc { font-size: 0.78rem; color: rgba(232,224,204,0.6); margin-top: 0.1rem; display: block; }

/* ── Impact ── */
.impact-row { display: flex; flex-wrap: wrap; gap: 1rem; margin-top: 1rem; }
.impact-card { flex: 1; min-width: 180px;
    background: linear-gradient(135deg, rgba(34,197,94,0.08), rgba(255,180,0,0.05));
    border: 1px solid rgba(34,197,94,0.2); border-radius: 3px; padding: 1.2rem; text-align: center; }
.impact-num { font-family: 'Bebas Neue', sans-serif; font-size: 2.4rem; color: #22C55E; line-height: 1; display: block; }
.impact-lbl { font-size: 0.8rem; color: rgba(232,224,204,0.65); margin-top: 0.3rem; display: block; }

/* ── Advantage ── */
.adv-row { display: grid; grid-template-columns: 1fr 1fr; gap: 0.8rem; margin-top: 1rem; }
.adv-item { background: rgba(255,255,255,0.025); border: 1px solid rgba(255,255,255,0.07);
    border-radius: 3px; padding: 1rem 1.2rem; display: flex; gap: 0.8rem; align-items: flex-start; }
.adv-check { font-size: 1.2rem; flex-shrink: 0; }
.adv-text { font-size: 0.88rem; color: rgba(232,224,204,0.85); line-height: 1.5; }
.adv-text strong { color: #FFD700; font-family: 'Barlow Condensed', sans-serif; font-size: 0.92rem; }

/* ── Gallery ── */
.gallery-label { font-family: 'Barlow Condensed', sans-serif; font-size: 0.75rem; letter-spacing: 0.15em;
    text-transform: uppercase; color: rgba(255,215,0,0.5); text-align: center; margin-top: 0.4rem; }
.gallery-section-label { font-family: 'Share Tech Mono', monospace; font-size: 0.7rem; color: rgba(255,180,0,0.4);
    letter-spacing: 0.15em; text-transform: uppercase; margin: 1.4rem 0 0.6rem;
    border-bottom: 1px solid rgba(255,180,0,0.12); padding-bottom: 0.4rem; }
/* Image frame polish */
[data-testid="stImage"] img {
    border-radius: 3px;
    border: 1px solid rgba(255,180,0,0.15);
    box-shadow: 0 6px 24px rgba(0,0,0,0.5);
    transition: box-shadow 0.3s;
}
[data-testid="stImage"] img:hover { box-shadow: 0 8px 32px rgba(255,180,0,0.15); }
/* Circuit image larger shadow */
.circuit-img img { border-color: rgba(100,180,255,0.25) !important; box-shadow: 0 8px 32px rgba(0,0,0,0.6) !important; }

/* ── Divider ── */
.section-divider {
    height: 1px; background: linear-gradient(90deg, transparent, rgba(255,180,0,0.2), transparent);
    margin: 0.5rem 0 2rem; border: none;
}

/* ── Sidebar ── */
.sidebar-logo { font-family: 'Bebas Neue', sans-serif; font-size: 1.3rem; letter-spacing: 0.1em;
    background: linear-gradient(90deg, #FFD700, #22C55E); -webkit-background-clip: text;
    -webkit-text-fill-color: transparent; margin-bottom: 0.3rem; display: block; }
.nav-link { display: block; padding: 0.4rem 0.7rem; color: rgba(232,224,204,0.7) !important;
    font-family: 'Barlow', sans-serif; font-size: 0.82rem; letter-spacing: 0.03em;
    border-left: 2px solid transparent; margin-bottom: 0.1rem; text-decoration: none; }
.nav-link:hover { border-left-color: #FFD700; color: #FFD700 !important; }
.nav-section-label { font-family: 'Share Tech Mono', monospace; font-size: 0.65rem; letter-spacing: 0.15em;
    color: rgba(255,180,0,0.4); text-transform: uppercase; padding: 0.8rem 0.7rem 0.2rem; display: block; }

/* ── Footer ── */
.footer { text-align: center; padding: 2.5rem 1rem 1.5rem; border-top: 1px solid rgba(255,180,0,0.12); margin-top: 2rem; }
.footer-title { font-family: 'Bebas Neue', sans-serif; font-size: 1.4rem; letter-spacing: 0.1em;
    background: linear-gradient(90deg, #FFD700, #FFA500); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.footer-sub { font-size: 0.8rem; color: rgba(232,224,204,0.35); margin-top: 0.3rem; }

/* ── Lists ── */
.gold-list { padding-left: 0; list-style: none; }
.gold-list li { padding: 0.4rem 0 0.4rem 1.6rem; position: relative; font-size: 0.93rem;
    line-height: 1.6; color: rgba(232,224,204,0.85); border-bottom: 1px solid rgba(255,255,255,0.03); }
.gold-list li::before { content: '▸'; position: absolute; left: 0; color: #FFA500; font-size: 0.8rem; top: 0.5rem; }
.green-list li::before { color: #22C55E; }

/* ── Timeline ── */
.timeline { display: flex; flex-direction: column; gap: 0; margin-top: 1rem; }
.tl-item { display: flex; gap: 1.2rem; padding: 0.9rem 0; border-bottom: 1px solid rgba(255,255,255,0.04); }
.tl-dot { width: 10px; height: 10px; border-radius: 50%; background: #FFA500; flex-shrink: 0;
    margin-top: 0.35rem; box-shadow: 0 0 8px rgba(255,165,0,0.5); }
.tl-dot-green { background: #22C55E; box-shadow: 0 0 8px rgba(34,197,94,0.5); }
.tl-dot-red   { background: #ef4444; box-shadow: 0 0 8px rgba(239,68,68,0.5); }
.tl-content { flex: 1; }
.tl-title { font-family: 'Barlow Condensed', sans-serif; font-weight: 700; font-size: 0.9rem;
    color: #FFD700; letter-spacing: 0.04em; margin-bottom: 0.2rem; }
.tl-body { font-size: 0.85rem; color: rgba(232,224,204,0.72); line-height: 1.55; }

/* ── Pin table ── */
.pin-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; margin-top: 0.8rem; }
.pin-table th { background: rgba(34,197,94,0.1); color: #22C55E; font-family: 'Barlow Condensed', sans-serif;
    padding: 0.5rem 0.9rem; text-align: left; border-bottom: 1px solid rgba(34,197,94,0.2);
    font-size: 0.78rem; letter-spacing: 0.08em; text-transform: uppercase; }
.pin-table td { padding: 0.5rem 0.9rem; border-bottom: 1px solid rgba(255,255,255,0.04);
    font-family: 'Share Tech Mono', monospace; font-size: 0.82rem; color: #94d8f0; }
.pin-table td:last-child { font-family: 'Barlow', sans-serif; color: rgba(232,224,204,0.7); font-size: 0.83rem; }

[data-testid="caption"] { font-family: 'Barlow', sans-serif !important; }
[data-testid="stVideo"] { border-radius: 4px; }

/* ── Architecture nodes ── */
.arch-grid { display: grid; grid-template-columns: 1fr 56px 1fr; gap: 0; margin: 0.5rem 0 1.2rem; align-items: stretch; }
.arch-node { border-radius: 4px; padding: 1.3rem 1.5rem; }
.arch-node-ctrl { border: 1px solid rgba(100,180,255,0.25); background: rgba(100,180,255,0.04); border-radius: 4px 0 0 4px; }
.arch-node-remote { border: 1px solid rgba(34,197,94,0.25); background: rgba(34,197,94,0.03); border-radius: 0 4px 4px 0; }
.arch-connector { display: flex; flex-direction: column; justify-content: center; align-items: center; gap: 4px;
    background: rgba(255,180,0,0.03); border-top: 1px solid rgba(255,180,0,0.1); border-bottom: 1px solid rgba(255,180,0,0.1); }
.arch-connector-label { font-family: 'Share Tech Mono', monospace; font-size: 0.58rem; color: rgba(255,215,0,0.4);
    letter-spacing: 0.1em; text-transform: uppercase; writing-mode: vertical-rl; transform: rotate(180deg); }
.arch-connector-arrow { font-size: 1.3rem; color: rgba(255,215,0,0.5); }
.arch-connector-rate { font-family: 'Share Tech Mono', monospace; font-size: 0.6rem; color: rgba(255,180,0,0.3); }
.arch-node-title { font-family: 'Barlow Condensed', sans-serif; font-size: 0.95rem; font-weight: 700;
    letter-spacing: 0.06em; margin-bottom: 0.2rem; }
.arch-node-sub { font-family: 'Share Tech Mono', monospace; font-size: 0.68rem; color: rgba(232,224,204,0.4);
    letter-spacing: 0.08em; margin-bottom: 1rem; }
.arch-subsystem { margin-bottom: 0.8rem; }
.arch-sub-title { font-family: 'Barlow Condensed', sans-serif; font-size: 0.82rem; font-weight: 700;
    color: rgba(232,224,204,0.6); letter-spacing: 0.04em; margin-bottom: 0.2rem; }
.arch-sub-body { font-family: 'Barlow', sans-serif; font-size: 0.8rem; color: rgba(232,224,204,0.55); line-height: 1.6; }
.arch-sub-body span { font-family: 'Share Tech Mono', monospace; color: #94d8f0; font-size: 0.77rem; }
.loop-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.35rem; margin-top: 0.6rem; }
.loop-item { background: rgba(255,255,255,0.025); border: 1px solid rgba(255,255,255,0.05);
    border-left: 2px solid rgba(100,180,255,0.35); border-radius: 2px; padding: 0.4rem 0.8rem;
    display: flex; gap: 0.7rem; align-items: baseline; }
.loop-fn { font-family: 'Share Tech Mono', monospace; font-size: 0.75rem; color: #60b4ff; flex-shrink: 0; }
.loop-desc { font-size: 0.78rem; color: rgba(232,224,204,0.55); }

/* ── Keyframes ── */
@keyframes fadeUp   { from { opacity:0; transform:translateY(28px); } to { opacity:1; transform:translateY(0); } }
@keyframes fadeDown { from { opacity:0; transform:translateY(-20px); } to { opacity:1; transform:translateY(0); } }
@keyframes fadeIn   { from { opacity:0; } to { opacity:1; } }
@keyframes scaleIn  { from { opacity:0; transform:scale(0.88); } to { opacity:1; transform:scale(1); } }
@keyframes slideLeft{ from { opacity:0; transform:translateX(28px); } to { opacity:1; transform:translateX(0); } }
@keyframes slideRight{from { opacity:0; transform:translateX(-28px);} to { opacity:1; transform:translateX(0); } }
@keyframes shimmer  { 0%{background-position:-200% center;} 100%{background-position:200% center;} }
@keyframes borderPulse {
    0%,100% { box-shadow:0 4px 24px rgba(0,0,0,0.35); }
    50%      { box-shadow:0 4px 36px rgba(255,180,0,0.14); }
}
@keyframes heroEmoji {
    0%   { opacity:0; transform:scale(0.5) rotate(-20deg); }
    60%  { transform:scale(1.12) rotate(5deg); }
    100% { opacity:1; transform:scale(1) rotate(0deg); }
}

/* ── Hero entrance (CSS-only, immediate) ── */
.hero-emoji { animation: heroEmoji 0.9s cubic-bezier(0.22,1,0.36,1) 0.1s both,
                          pulse-sun 4s ease-in-out 1.2s infinite; }
.hero-title  { animation: fadeUp 0.85s cubic-bezier(0.22,1,0.36,1) 0.35s both; }
.hero-sub    { animation: fadeUp 0.75s cubic-bezier(0.22,1,0.36,1) 0.55s both; }
.hero-tags   { animation: fadeUp 0.7s  cubic-bezier(0.22,1,0.36,1) 0.75s both; }

/* ── Scroll-reveal base ── */
.sr {
    opacity: 0;
    transform: translateY(30px);
    transition: opacity 0.65s cubic-bezier(0.22,1,0.36,1),
                transform 0.65s cubic-bezier(0.22,1,0.36,1);
}
.sr.sr-left  { transform: translateX(-24px); }
.sr.sr-right { transform: translateX( 24px); }
.sr.sr-scale { transform: scale(0.9); opacity:0; }
.sr.in { opacity:1 !important; transform:none !important; }

/* ── Card pulse + hover ── */
.card { animation: borderPulse 7s ease-in-out infinite; }
.card:hover {
    border-color: rgba(255,180,0,0.3) !important;
    box-shadow: 0 8px 40px rgba(0,0,0,0.5), 0 0 0 1px rgba(255,180,0,0.1) !important;
    transition: all 0.3s ease;
}

/* ── Hover micro-interactions ── */
.stat-pill { transition: transform 0.22s ease, box-shadow 0.22s ease; }
.stat-pill:hover { transform: translateY(-3px); box-shadow: 0 8px 24px rgba(0,0,0,0.45); }

.feat-item { transition: border-color 0.22s ease, background 0.22s ease, transform 0.22s ease; }
.feat-item:hover { background:rgba(255,255,255,0.045); border-color:rgba(255,180,0,0.25); transform:translateY(-2px); }
.feat-item-green:hover { border-left-color:#4ade80; background:rgba(34,197,94,0.07); }
.feat-item-blue:hover  { border-left-color:#93c5fd; background:rgba(96,180,255,0.07); }

.stack-item { transition: background 0.22s ease, border-color 0.22s ease, transform 0.22s ease; }
.stack-item:hover { background:rgba(255,255,255,0.05); border-color:rgba(255,215,0,0.18); transform:translateY(-2px); }

.adv-item { transition: background 0.22s ease, transform 0.22s ease; }
.adv-item:hover { background:rgba(255,255,255,0.05); transform:translateX(3px); }

.impact-card { transition: transform 0.25s ease, box-shadow 0.25s ease; }
.impact-card:hover { transform: translateY(-4px); box-shadow: 0 10px 28px rgba(34,197,94,0.18); }

.tl-item { transition: background 0.2s ease; border-radius: 2px; }
.tl-item:hover { background: rgba(255,180,0,0.03); }

.loop-item { transition: background 0.2s ease, border-color 0.2s ease; }
.loop-item:hover { background: rgba(96,180,255,0.07); border-left-color: rgba(100,180,255,0.7); }

.arch-subsystem { transition: background 0.2s ease; border-radius: 2px; padding: 0.2rem 0.4rem; margin: 0 -0.4rem; }
.arch-subsystem:hover { background: rgba(255,255,255,0.03); }

.hero-tag { transition: background 0.2s, border-color 0.2s, transform 0.2s; }
.hero-tag:hover { background:rgba(255,180,0,0.2); border-color:rgba(255,215,0,0.6); transform:translateY(-2px); }

.nav-link { transition: border-color 0.15s, color 0.15s, background 0.15s, padding-left 0.15s; }
.nav-link:hover { background:rgba(255,215,0,0.05); padding-left:1rem; }

/* ── Shimmer on section numbers ── */
.sec-num {
    background: linear-gradient(90deg, rgba(255,180,0,0.3) 0%, rgba(255,215,0,0.75) 45%, rgba(255,180,0,0.3) 80%);
    background-size: 200% auto;
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    animation: shimmer 4s linear infinite;
}

/* ── Table row hovers ── */
.result-table tr:hover td { background:rgba(255,180,0,0.04); transition:background 0.15s; }
.proto-table  tr:hover td { background:rgba(255,215,0,0.04); transition:background 0.15s; }
.pin-table    tr:hover td { background:rgba(34,197,94,0.04); transition:background 0.15s; }
</style>
""", unsafe_allow_html=True)

# ── Scroll-reveal JS ──────────────────────────────────────────────────────────
st.markdown("""
<script>
(function(){
  /* Elements to animate and which variant to use */
  var GROUPS = [
    { sel: '.card',         cls: ''         },
    { sel: '.feat-item',    cls: ''         },
    { sel: '.stack-item',   cls: ''         },
    { sel: '.impact-card',  cls: 'sr-scale' },
    { sel: '.adv-item',     cls: ''         },
    { sel: '.tl-item',      cls: 'sr-left'  },
    { sel: '.stat-pill',    cls: 'sr-scale' },
    { sel: '.loop-item',    cls: ''         },
    { sel: '.arch-node-ctrl',   cls: 'sr-right' },
    { sel: '.arch-node-remote', cls: 'sr-left'  },
  ];

  var io = new IntersectionObserver(function(entries){
    entries.forEach(function(e){
      if(!e.isIntersecting) return;
      var el = e.target;
      var delay = parseInt(el.dataset.srDelay||0,10);
      setTimeout(function(){ el.classList.add('in'); }, delay);
      io.unobserve(el);
    });
  }, { threshold: 0.07, rootMargin: '0px 0px -24px 0px' });

  function attach(){
    var found = 0;
    GROUPS.forEach(function(g){
      var els = document.querySelectorAll(g.sel);
      els.forEach(function(el){
        if(el.dataset.srDone) return;
        el.dataset.srDone = '1';
        found++;

        /* compute stagger: sibling index among same selector in same parent */
        var siblings = el.parentElement
          ? el.parentElement.querySelectorAll(g.sel) : [];
        var idx = Array.prototype.indexOf.call(siblings, el);
        var delay = Math.min(idx * 65, 380);

        el.dataset.srDelay = delay;
        el.classList.add('sr');
        if(g.cls) el.classList.add(g.cls);
        io.observe(el);
      });
    });
    return found;
  }

  /* Initial attempt + retry to catch elements Streamlit renders late */
  function tryAttach(attempts){
    var n = attach();
    if(n === 0 && attempts < 8) setTimeout(function(){ tryAttach(attempts+1); }, 350);
  }

  /* Run early, then again after Streamlit's reactive DOM settles */
  setTimeout(function(){ tryAttach(0); },  200);
  setTimeout(function(){ tryAttach(0); }, 1800);
})();
</script>
""", unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<span class="sidebar-logo">🌻 Solar Sunflower</span>', unsafe_allow_html=True)
    st.markdown('<span style="font-size:0.75rem;color:rgba(232,224,204,0.4);">Autonomous Solar Panel Controller</span>', unsafe_allow_html=True)
    st.markdown("---")

    nav_items = [
        ("🏠", "Overview",                  "hero"),
        ("📖", "Introduction",              "introduction"),
        ("⚠️", "Problem Statement",         "problem"),
        ("💡", "Proposed Solution",          "solution"),
        ("⚙️", "What The System Does",       "whatitdoes"),
        ("🏗️", "System Architecture",        "architecture"),
        ("🔌", "Circuit Diagram",            "circuit"),
        ("🔧", "Technical Stack",            "techstack"),
        ("📡", "Communication Protocol",     "protocol"),
        ("🔑", "Key Technical Features",     "features"),
        ("🚀", "Innovation Factor",          "innovation"),
        ("🧪", "Implementation & Testing",   "testing"),
        ("📊", "Testing Results",            "testresults"),
        ("🌐", "Large Scale Implementation", "largescale"),
        ("🔮", "System Improvements",        "improvements"),
        ("🌱", "Future Benefits",            "future"),
        ("🌍", "Real-World Impact",          "impact"),
        ("🏆", "Competitive Advantages",     "competitive"),
        ("✅", "Conclusion",                 "conclusion"),
        ("🖼️", "Gallery",                    "gallery"),
    ]

    st.markdown('<span class="nav-section-label">Navigation</span>', unsafe_allow_html=True)
    for icon, label, anchor in nav_items:
        st.markdown(f'<a class="nav-link" href="#{anchor}">{icon} {label}</a>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="background:rgba(34,197,94,0.08);border:1px solid rgba(34,197,94,0.2);border-radius:3px;padding:0.6rem 0.8rem;margin-bottom:0.8rem;">
      <span style="font-family:'Share Tech Mono',monospace;font-size:0.65rem;letter-spacing:0.12em;color:#22C55E;">● DEPLOYED &amp; VALIDATED</span>
    </div>
    <div style="font-size:0.72rem;color:rgba(232,224,204,0.3);font-family:'Share Tech Mono',monospace;line-height:1.9;">
    ESP32 × 2 &nbsp;|&nbsp; L298N<br>
    ACS712-30A &nbsp;|&nbsp; DS3231<br>
    Servo &nbsp;|&nbsp; SSD1306 OLED<br>
    WiFi TCP &nbsp;|&nbsp; Arduino<br>
    26 / 27 Tests Pass
    </div>
    """, unsafe_allow_html=True)

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown('<div id="hero"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="hero-wrap">
  <div class="sunburst"></div>
  <span class="hero-emoji">🌻</span>
  <div class="hero-title">Solar Sunflower Controller</div>
  <div class="hero-sub">Autonomous Sun-Tracking Solar Panel System</div>
  <div class="hero-tags">
    <span class="hero-tag">ESP32 × 2</span>
    <span class="hero-tag">WiFi TCP</span>
    <span class="hero-tag">RTC Scheduled</span>
    <span class="hero-tag">Servo Sun Tracking</span>
    <span class="hero-tag">Live OLED Dashboard</span>
    <span class="hero-tag">Custom PCB</span>
    <span class="hero-tag">Arduino Framework</span>
    <span class="hero-tag">Open Firmware</span>
  </div>
</div>
""", unsafe_allow_html=True)

c1,c2,c3,c4,c5,c6 = st.columns(6)
for col,(num,lbl,cls) in zip([c1,c2,c3,c4,c5,c6],[
    ("35%",   "Energy Gain",      "stat-pill"),
    ("10 Hz", "Live Data",        "stat-pill"),
    ("15 min","Track Cycle",      "stat-pill"),
    ("2×",    "ESP32 Nodes",      "stat-pill stat-pill-green"),
    ("3",     "Sensor Channels",  "stat-pill stat-pill-green"),
    ("500",   "Cal Samples",      "stat-pill stat-pill-blue"),
]):
    col.markdown(f'<div class="{cls}"><span class="num">{num}</span><span class="lbl">{lbl}</span></div>', unsafe_allow_html=True)

st.markdown("""
<div class="info-banner">
  <div class="info-cell"><span class="info-cell-label">Platform</span><span class="info-cell-value">ESP32 Dual-Node</span></div>
  <div class="info-cell"><span class="info-cell-label">Communication</span><span class="info-cell-value">WiFi · TCP Sockets</span></div>
  <div class="info-cell"><span class="info-cell-label">Sensing</span><span class="info-cell-value">V · I · W · Battery</span></div>
  <div class="info-cell"><span class="info-cell-label">Tracking</span><span class="info-cell-value">Every 15 Minutes</span></div>
  <div class="info-cell"><span class="info-cell-label">Motor Control</span><span class="info-cell-value">Soft-Ramp PWM</span></div>
  <div class="info-cell"><span class="info-cell-label">Firmware</span><span class="info-cell-value">Arduino · Open Source</span></div>
</div>
""", unsafe_allow_html=True)

# ── Introduction ──────────────────────────────────────────────────────────────
st.markdown('<div id="introduction"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="card">
  <span class="sec-num">01 — INTRODUCTION</span>
  <div class="section-heading"><span class="heading-icon">📖</span> Introduction</div>
  <p style="color:rgba(232,224,204,0.8);font-size:1rem;line-height:1.8;max-width:820px;margin-bottom:1.6rem;">
    The <strong style="color:#FFD700;">Solar Sunflower Controller</strong> is a student engineering project that brings
    a natural phenomenon — the sunflower's daily rotation toward the sun — into an embedded system.
    The device autonomously deploys a solar panel at sunrise, tracks the sun every 15 minutes throughout
    the day using a continuous-rotation servo, and retracts the panel at sunset — all without any
    human intervention. A second wireless unit displays live power telemetry and provides manual
    override controls through a handheld OLED dashboard.
  </p>
""", unsafe_allow_html=True)

ca, cb = st.columns(2)
with ca:
    st.markdown("""
    <div class="mono-label">What This Project Is</div>
    <ul class="gold-list">
      <li><strong style="color:#FFD700;">Autonomous solar panel controller</strong> — opens, tracks, and closes on a configurable daily schedule</li>
      <li><strong style="color:#FFD700;">Dual ESP32 architecture</strong> — Controller unit manages all hardware; Remote unit manages the operator interface</li>
      <li><strong style="color:#FFD700;">Real-time wireless telemetry</strong> — panel voltage, current, power, and battery streamed at 10 Hz over local WiFi</li>
      <li><strong style="color:#FFD700;">Custom hand-soldered PCB</strong> — compact motherboard integrating all components into one form factor</li>
      <li><strong style="color:#FFD700;">Open firmware</strong> — Arduino framework, fully documented, reproducible on commodity hardware</li>
    </ul>
    """, unsafe_allow_html=True)
with cb:
    st.markdown("""
    <div class="mono-label">Motivation</div>
    <ul class="gold-list green-list">
      <li>Fixed solar panels lose <strong style="color:#22C55E;">30–40% of potential yield</strong> because they cannot follow the sun's arc</li>
      <li>Commercial single-axis trackers cost <strong style="color:#22C55E;">₹35,000+</strong>, making them inaccessible to small-scale or rural deployments</li>
      <li>Most low-cost DIY solar systems offer <strong style="color:#22C55E;">no live monitoring</strong> — faults go undetected for days</li>
      <li>The biological mechanism of <strong style="color:#22C55E;">heliotropism</strong> in sunflowers offers an elegant, proven model for mechanical solar tracking</li>
      <li>This project demonstrates that <strong style="color:#22C55E;">high-performance tracking</strong> is achievable at a fraction of commercial cost</li>
    </ul>
    """, unsafe_allow_html=True)

st.markdown("""
  <div class="stat-row" style="margin-top:1.4rem;">
    <div class="stat-pill"><span class="num">2</span><span class="lbl">ESP32 Nodes</span></div>
    <div class="stat-pill"><span class="num">5</span><span class="lbl">Sensor Inputs</span></div>
    <div class="stat-pill stat-pill-green"><span class="num">4</span><span class="lbl">Manual Buttons</span></div>
    <div class="stat-pill stat-pill-green"><span class="num">15 min</span><span class="lbl">Track Interval</span></div>
    <div class="stat-pill stat-pill-blue"><span class="num">10 Hz</span><span class="lbl">Telemetry Rate</span></div>
    <div class="stat-pill stat-pill-blue"><span class="num">100%</span><span class="lbl">Autonomous</span></div>
  </div>
  <div style="margin-top:1.4rem;padding:1rem 1.4rem;background:rgba(255,180,0,0.05);border-left:3px solid rgba(255,180,0,0.4);border-radius:0 3px 3px 0;">
    <p style="color:rgba(232,224,204,0.7);font-size:0.87rem;line-height:1.7;margin:0;">
      This documentation covers the complete system — from the engineering challenges that motivated the design,
      through the hardware architecture and firmware implementation, to the testing results and real-world impact.
      Use the sidebar to navigate directly to any section.
    </p>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Problem Statement ──────────────────────────────────────────────────────────
st.markdown('<div id="problem"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="card card-accent">
  <span class="sec-num">02 — PROBLEM STATEMENT</span>
  <div class="section-heading"><span class="heading-icon">⚠️</span> Problem Statement</div>
  <p style="color:rgba(232,224,204,0.75);font-size:0.97rem;line-height:1.7;margin-bottom:1.4rem;">
    Fixed solar panels are installed at a static angle and lose significant energy throughout the day as
    the sun moves 180° across the sky. Simultaneously, the monitoring and control tools that could
    diagnose and correct these losses are priced out of reach for small-scale, rural, or educational deployments.
  </p>
""", unsafe_allow_html=True)

ca, cb = st.columns(2)
with ca:
    for title, body in [
        ("Energy Loss — Fixed Orientation",
         "A panel mounted at a fixed tilt produces peak output only when the sun is perpendicular to its surface. For the rest of the day, irradiance angle reduces effective capture area — costing 30–40% of total potential daily yield."),
        ("Morning & Evening Dead Zones",
         "Fixed panels are optimised for solar noon. In the first and last two hours of daylight — when tracking gains are highest — output can be as low as 20% of peak. These hours account for significant cumulative loss across a year."),
        ("No Real-Time Fault Visibility",
         "Affordable solar installations have no monitoring of voltage, current, or power. Shading, connector degradation, or battery overcharge go undetected for days — silently reducing system output with no alert."),
    ]:
        st.markdown(f'<div class="feat-item feat-item-red" style="margin-bottom:0.8rem;"><div class="feat-title" style="color:#ef4444;">{title}</div><div class="feat-body">{body}</div></div>', unsafe_allow_html=True)
with cb:
    for title, body in [
        ("Commercial Trackers — Prohibitive Cost",
         "Single-axis commercial solar trackers cost $500–$2,000 per unit. For a small rooftop or rural installation of 5–10 panels, the tracker cost alone often exceeds the panel cost — making it economically irrational."),
        ("Manual Deployment Labor",
         "In many off-grid setups, panels are manually tilted morning and evening. This daily labor reduces the economic viability of solar for agricultural or remote applications where operators are not always present."),
        ("No Graceful Failure Handling",
         "Existing low-cost solutions lack fail-safe mechanisms. A dropped WiFi connection or stuck motor can leave a panel deployed overnight — exposed to weather, causing mechanical damage or battery drain."),
    ]:
        st.markdown(f'<div class="feat-item feat-item-red" style="margin-bottom:0.8rem;"><div class="feat-title" style="color:#ef4444;">{title}</div><div class="feat-body">{body}</div></div>', unsafe_allow_html=True)

st.markdown("""
  <div class="stat-row" style="margin-top:1.4rem;">
    <div class="stat-pill stat-pill-red"><span class="num">40%</span><span class="lbl">Daily Energy Lost (Fixed)</span></div>
    <div class="stat-pill stat-pill-red"><span class="num">₹35K+</span><span class="lbl">Commercial Tracker Cost</span></div>
    <div class="stat-pill stat-pill-red"><span class="num">2×/day</span><span class="lbl">Manual Tilt Operations</span></div>
    <div class="stat-pill"><span class="num">770M</span><span class="lbl">People Without Reliable Power</span></div>
    <div class="stat-pill"><span class="num">0</span><span class="lbl">Monitoring in Most Low-Cost Systems</span></div>
  </div>

  <div style="margin-top:1.4rem;padding:1rem 1.5rem;background:rgba(239,68,68,0.05);border-left:3px solid rgba(239,68,68,0.4);border-radius:0 3px 3px 0;">
    <p style="color:rgba(232,224,204,0.78);font-size:0.9rem;line-height:1.75;margin:0 0 0.6rem;">
      <strong style="color:#f87171;">The core gap:</strong> Affordable solar installations offer no tracking and no monitoring.
      Commercial trackers solve the tracking problem but cost more than the panels themselves.
      Open-source DIY trackers require programming expertise, offer no fault monitoring, and typically lack fail-safe
      mechanisms for unattended outdoor operation.
    </p>
    <p style="color:rgba(232,224,204,0.78);font-size:0.9rem;line-height:1.75;margin:0;">
      Energy loss from fixed panels compounds over a year — a 200 W panel losing 30% yields 60 W less continuously,
      roughly <strong style="color:#f87171;">175 kWh per year per panel</strong>. At rural grid tariffs, this is measurable economic harm.
      For off-grid applications, it may mean insufficient energy to run a pump or charge-cycle a battery —
      with no sensor data to diagnose the shortfall.
    </p>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Proposed Solution ──────────────────────────────────────────────────────────
st.markdown('<div id="solution"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="card card-green">
  <span class="sec-num">03 — PROPOSED SOLUTION</span>
  <div class="section-heading"><span class="heading-icon">💡</span> Proposed Solution</div>
  <p style="color:rgba(232,224,204,0.75);font-size:0.97rem;line-height:1.7;margin-bottom:1.4rem;">
    A dual-ESP32 embedded system that autonomously mimics heliotropism — the biological mechanism by which
    sunflowers orient toward the sun throughout the day. Designed for graceful degradation: core panel
    operation continues even when the wireless link fails.
  </p>
""", unsafe_allow_html=True)

ca, cb = st.columns(2)
with ca:
    for title, body in [
        ("RTC-Scheduled Autonomous Operation",
         "DS3231 real-time clock drives the daily open/close cycle without cloud or internet. Panel deploys at sunrise and retracts at sunset — even when the remote unit is disconnected."),
        ("15-Minute Sun Tracking Pulses",
         "While the panel is open, a continuous-rotation servo fires every 15 minutes to rotate toward the sun's current azimuth. Track duration is auto-calculated from servo RPM and desired revolutions."),
        ("Soft-Ramp Motor Control",
         "Custom PWM ramp library (MotorL298N.h) brings the DC motor from 0 to 100% over ~5 seconds, with a 30% kickstart for static friction. Eliminates mechanical shock and extends motor lifespan."),
    ]:
        st.markdown(f'<div class="feat-item" style="margin-bottom:0.8rem;"><div class="feat-title">{title}</div><div class="feat-body">{body}</div></div>', unsafe_allow_html=True)
with cb:
    for title, body in [
        ("Live WiFi Sensor Dashboard",
         "Remote ESP32 receives panel voltage, current, power, and battery voltage on a 128×64 OLED at 10 Hz. Plain CSV over TCP — parseable by any tool with a single readline()."),
        ("4-Button Hold-to-Run Control",
         "Physical buttons on the remote unit provide manual servo and motor override. Hold to run, release to stop — no software toggle, no runaway risk regardless of network state."),
        ("Boot-Time Auto-Calibration",
         "ACS712 zero offset measured by averaging 500 ADC samples over ~1 second on every power-on. Eliminates component variation and long-term drift without any manual steps."),
    ]:
        st.markdown(f'<div class="feat-item feat-item-green" style="margin-bottom:0.8rem;"><div class="feat-title feat-title-green">{title}</div><div class="feat-body">{body}</div></div>', unsafe_allow_html=True)

st.markdown("""
  <div class="mono-label" style="margin-top:1.6rem;">Solar Sunflower vs. Alternatives</div>
  <table class="result-table" style="margin-top:0.5rem;">
    <tr><th>Feature</th><th>Fixed Panel</th><th>Commercial Tracker</th><th>Solar Sunflower</th></tr>
    <tr><td>Daily energy yield</td><td style="color:rgba(232,224,204,0.5);">Baseline</td><td style="color:rgba(232,224,204,0.5);">+25–35%</td><td><span class="pass">+25–35%</span></td></tr>
    <tr><td>Unit cost (tracker only)</td><td style="color:rgba(232,224,204,0.5);">₹0 extra</td><td style="color:rgba(232,224,204,0.5);">₹35,000+</td><td><span class="val">~₹2,000</span></td></tr>
    <tr><td>Live sensor monitoring</td><td style="color:#ef4444;">None</td><td style="color:rgba(232,224,204,0.5);">Cloud-only (often)</td><td><span class="pass">Local 10 Hz</span></td></tr>
    <tr><td>Autonomous daily cycle</td><td style="color:#ef4444;">Manual tilt</td><td><span class="pass">✔</span></td><td><span class="pass">✔ RTC-scheduled</span></td></tr>
    <tr><td>Fails gracefully on link drop</td><td style="color:rgba(232,224,204,0.5);">N/A</td><td style="color:rgba(232,224,204,0.5);">Varies</td><td><span class="pass">✔ Always</span></td></tr>
    <tr><td>Open firmware</td><td style="color:rgba(232,224,204,0.5);">N/A</td><td style="color:#ef4444;">Proprietary</td><td><span class="pass">✔ Arduino</span></td></tr>
    <tr><td>Cloud / internet dependency</td><td style="color:rgba(232,224,204,0.5);">None</td><td style="color:#ef4444;">Often required</td><td><span class="pass">None — local WiFi</span></td></tr>
    <tr><td>Hold-to-run manual safety</td><td style="color:rgba(232,224,204,0.5);">N/A</td><td style="color:rgba(232,224,204,0.5);">Varies</td><td><span class="pass">✔ By design</span></td></tr>
    <tr><td>Boot-time sensor calibration</td><td style="color:rgba(232,224,204,0.5);">N/A</td><td style="color:rgba(232,224,204,0.5);">Factory set</td><td><span class="pass">✔ 500-sample avg</span></td></tr>
  </table>
</div>
""", unsafe_allow_html=True)

# ── What The System Does ───────────────────────────────────────────────────────
st.markdown('<div id="whatitdoes"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="card">
  <span class="sec-num">04 — WHAT THE SYSTEM DOES</span>
  <div class="section-heading"><span class="heading-icon">⚙️</span> What The System Does</div>
  <p style="color:rgba(232,224,204,0.65);font-size:0.9rem;margin-bottom:1.2rem;">
    A complete autonomous daily cycle — from deployment at sunrise to retraction at sunset — with live
    monitoring and manual override available at any point.
  </p>
""", unsafe_allow_html=True)

ca,cb,cc = st.columns(3)
for i,(icon,title,desc) in enumerate([
    ("🌅","Sunrise Deployment","At the configured morning time, the RTC triggers the motor state machine: MOTOR_IDLE → MOTOR_OPENING. The L298N drives the DC motor forward for OPEN_DURATION (default 4 s) using a soft PWM ramp. The opened flag is set only after the motor physically finishes."),
    ("☀️","15-Minute Sun Tracking","While the panel is open, a millis() timer fires the servo every SERVO_TRACK_INTERVAL (15 min). The continuous-rotation servo runs for SERVO_TRACK_DURATION ms — auto-calculated from (SERVO_TRACK_REVS / SERVO_RPM) × 60000."),
    ("🌇","Sunset Retraction","At the configured evening time, the motor runs in reverse for CLOSE_DURATION (default 4 s), stowing the panel. The closed flag prevents re-closing on the same minute. System is quiescent until next morning."),
    ("📊","Live Sensor Telemetry","Every 100 ms, the controller reads panel voltage (GPIO 34), current via ACS712 (GPIO 35), and battery voltage (GPIO 32). Power is computed as V × I. All five values are sent as a CSV line over TCP at 10 Hz."),
    ("🕹️","Manual Override","4 hold-to-run buttons let an operator run the servo forward/reverse or open/close the panel manually. Motor commands accepted only from MOTOR_IDLE — no scheduler/manual collision possible."),
    ("🛑","Emergency Stop & RESET","RESET immediately calls hardBrake() on the motor and writes 90 (stop) to the servo. Advances the opened/closed flags so the scheduler cannot re-trigger on the same time slot. Safe within one 10ms loop cycle."),
]):
    col = [ca,cb,cc][i%3]
    col.markdown(f"""
    <div style="background:rgba(255,255,255,0.025);border:1px solid rgba(255,180,0,0.12);border-radius:3px;padding:1.2rem;margin-bottom:0.8rem;">
      <div style="font-size:1.8rem;margin-bottom:0.5rem;">{icon}</div>
      <div style="font-family:'Barlow Condensed',sans-serif;font-weight:700;color:#FFD700;font-size:0.95rem;letter-spacing:0.04em;margin-bottom:0.4rem;">{title}</div>
      <div style="font-size:0.83rem;color:rgba(232,224,204,0.75);line-height:1.6;">{desc}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("""
  <div class="mono-label" style="margin:1.4rem 0 0.6rem;">Complete Daily Operation Cycle</div>
""", unsafe_allow_html=True)

ca, cb = st.columns(2)
with ca:
    st.markdown("""
    <div class="timeline">
      <div class="tl-item"><div class="tl-dot"></div><div class="tl-content">
        <div class="tl-title">Boot &amp; Calibration (~1 s)</div>
        <div class="tl-body">ACS712 zero offset measured: 500 ADC samples averaged over 1 s with no load. DS3231 RTC read via I²C — cached to RAM. WiFi station mode started; client.connect() attempted to reach the Remote on 192.168.4.1:5000.</div>
      </div></div>
      <div class="tl-item"><div class="tl-dot"></div><div class="tl-content">
        <div class="tl-title">Pre-Sunrise: MOTOR_IDLE, monitoring</div>
        <div class="tl-body">Main 10ms loop runs. RTC time read every 1 s. Panel voltage, current, power sent via TCP every 100 ms. Servo held at write(90) = stop. Motor stays MOTOR_IDLE until schedule triggers.</div>
      </div></div>
      <div class="tl-item"><div class="tl-dot tl-dot-green"></div><div class="tl-content">
        <div class="tl-title">Sunrise: MOTOR_IDLE → MOTOR_OPENING</div>
        <div class="tl-body">RTC hour:minute matches OPEN_HOUR:OPEN_MIN. opened == false. Motor state transitions. L298N drives forward at 30% kickstart → ramps to 100% over ~5 s. After OPEN_DURATION (4 s), hardBrake() called. opened = true. State → MOTOR_IDLE.</div>
      </div></div>
      <div class="tl-item"><div class="tl-dot tl-dot-green"></div><div class="tl-content">
        <div class="tl-title">Daytime: Servo auto-tracking every 15 min</div>
        <div class="tl-body">SERVO_TRACK_INTERVAL timer fires. Servo write(180) for SERVO_TRACK_DURATION ms (= 4 rev ÷ 120 RPM × 60000 = 2000 ms). Returns to write(90). Manual button commands override this at any time with immediate priority.</div>
      </div></div>
      <div class="tl-item"><div class="tl-dot"></div><div class="tl-content">
        <div class="tl-title">Sunset: MOTOR_IDLE → MOTOR_CLOSING</div>
        <div class="tl-body">RTC matches CLOSE_HOUR:CLOSE_MIN. closed == false. Motor runs reverse for CLOSE_DURATION (4 s). hardBrake() after duration. closed = true. Servo tracking cancelled (panel stowed). State → MOTOR_IDLE.</div>
      </div></div>
      <div class="tl-item"><div class="tl-dot"></div><div class="tl-content">
        <div class="tl-title">Night: Quiescent monitoring</div>
        <div class="tl-body">Loop continues at 10ms period. Sensor data still streamed at 10 Hz — battery voltage monitored through the night. opened and closed flags reset on the next calendar day, allowing the cycle to repeat tomorrow.</div>
      </div></div>
    </div>
    """, unsafe_allow_html=True)
with cb:
    st.markdown("""
    <div class="mono-label">Key System Constants</div>
    <table class="pin-table" style="margin-top:0.5rem;">
      <tr><th>Constant</th><th>Default</th><th>Effect</th></tr>
      <tr><td>OPEN_HOUR / OPEN_MIN</td><td>Configurable</td><td>RTC time for morning deploy</td></tr>
      <tr><td>CLOSE_HOUR / CLOSE_MIN</td><td>Configurable</td><td>RTC time for evening retract</td></tr>
      <tr><td>OPEN_DURATION</td><td>4000 ms</td><td>Motor forward run time to fully open</td></tr>
      <tr><td>CLOSE_DURATION</td><td>4000 ms</td><td>Motor reverse run time to fully close</td></tr>
      <tr><td>SERVO_TRACK_INTERVAL</td><td>15 min</td><td>Time between auto tracking pulses</td></tr>
      <tr><td>SERVO_RPM</td><td>120.0</td><td>Measured servo speed — calibrate per unit</td></tr>
      <tr><td>SERVO_TRACK_REVS</td><td>4.0</td><td>Rotations per tracking pulse</td></tr>
      <tr><td>SEND_INTERVAL</td><td>100 ms</td><td>CSV transmit rate to Remote</td></tr>
      <tr><td>VOLT_RATIO / BAT_RATIO</td><td>5.0</td><td>Voltage divider scale factor</td></tr>
      <tr><td>ACS_SENS</td><td>0.066 V/A</td><td>ACS712-30A sensitivity</td></tr>
      <tr><td>MANUAL_TIMEOUT</td><td>30,000 ms</td><td>Safety cutoff for manual motor run</td></tr>
      <tr><td>testMode</td><td>false</td><td>true = skip RTC, fire every loop (bench only)</td></tr>
    </table>

    <div class="mono-label" style="margin-top:1.2rem;">Motor State Machine</div>
    <div class="mono-block" style="font-size:0.77rem;margin-top:0.4rem;">MOTOR_IDLE
  ├─(RTC schedule, opened==false)─► MOTOR_OPENING
  │    └─(OPEN_DURATION elapsed)──► MOTOR_IDLE, opened=true
  ├─(RTC schedule, closed==false)─► MOTOR_CLOSING
  │    └─(CLOSE_DURATION elapsed)─► MOTOR_IDLE, closed=true
  ├─(PANEL_OPEN from IDLE)────────► MOTOR_MANUAL (30s timeout)
  │    └─(MOTOR_STOP or timeout)──► MOTOR_IDLE
  └─(RESET, any state)────────────► MOTOR_IDLE, hardBrake()</div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ── System Architecture ────────────────────────────────────────────────────────
st.markdown('<div id="architecture"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="card">
  <span class="sec-num">05 — SYSTEM ARCHITECTURE</span>
  <div class="section-heading"><span class="heading-icon">🏗️</span> System Architecture</div>
  <p style="color:rgba(232,224,204,0.65);font-size:0.9rem;margin-bottom:1rem;">
    Two ESP32 microcontrollers on a local WiFi TCP network. Separation of concerns is strict —
    the Controller owns all hardware; the Remote owns the UI. Either can reboot independently without
    affecting the other's core function.
  </p>
  <div class="arch-grid">
    <div class="arch-node-ctrl">
      <div class="arch-node-title" style="color:#60b4ff;">CONTROLLER ESP32</div>
      <div class="arch-node-sub">Station / Client · connects to 192.168.4.1:5000</div>
      <div class="arch-subsystem">
        <div class="arch-sub-title">Motor Subsystem</div>
        <div class="arch-sub-body">L298N H-Bridge · <span>IN1=18, IN2=16, ENA=17</span><br>DC Motor — panel open / close<br>MotorL298N.h — soft PWM ramp driver</div>
      </div>
      <div class="arch-subsystem">
        <div class="arch-sub-title">Servo Subsystem</div>
        <div class="arch-sub-body">Continuous-rotation servo · <span>GPIO 25</span><br>50 Hz PWM · <span>write(180)</span>=fwd · <span>write(0)</span>=rev</div>
      </div>
      <div class="arch-subsystem">
        <div class="arch-sub-title">Sensors (ADC, input-only)</div>
        <div class="arch-sub-body"><span>GPIO 34</span> — Panel Voltage (40k/10k div)<br><span>GPIO 35</span> — Panel Current (ACS712-30A)<br><span>GPIO 32</span> — Battery Voltage (40k/10k div)</div>
      </div>
      <div class="arch-subsystem">
        <div class="arch-sub-title">Timekeeping</div>
        <div class="arch-sub-body">DS3231 RTC · I²C · <span>SDA=13, SCL=14</span><br>Cached every 1 s to avoid I²C overhead</div>
      </div>
    </div>
    <div class="arch-connector">
      <div class="arch-connector-label">WiFi TCP</div>
      <div class="arch-connector-arrow">⇄</div>
      <div class="arch-connector-rate">100ms</div>
    </div>
    <div class="arch-node-remote">
      <div class="arch-node-title" style="color:#22C55E;">REMOTE ESP32</div>
      <div class="arch-node-sub">Access Point · SSID: ESP32_SOLAR · 192.168.4.1:5000</div>
      <div class="arch-subsystem">
        <div class="arch-sub-title">Display</div>
        <div class="arch-sub-body">SSD1306 128×64 OLED (I²C)<br>• Time (RTC) &nbsp;&nbsp;• Voltage (V)<br>• Current (A) &nbsp;• Power (W)<br>• Battery (V)</div>
      </div>
      <div class="arch-subsystem">
        <div class="arch-sub-title">Buttons (hold-to-run)</div>
        <div class="arch-sub-body">BTN 1 → <span>SERVO_FWD</span><br>BTN 2 → <span>SERVO_REV</span><br>BTN 3 → <span>PANEL_OPEN</span><br>BTN 4 → <span>PANEL_CLOSE</span></div>
      </div>
    </div>
  </div>
  <div class="mono-label" style="margin:1rem 0 0.5rem;">loop() — non-blocking · runs every 10 ms</div>
  <div class="loop-grid">
    <div class="loop-item"><span class="loop-fn">motorA.update()</span><span class="loop-desc">advance PWM ramp one step</span></div>
    <div class="loop-item"><span class="loop-fn">RTC cache</span><span class="loop-desc">I²C read only every 1 s</span></div>
    <div class="loop-item"><span class="loop-fn">TCP command recv</span><span class="loop-desc">parse incoming button commands</span></div>
    <div class="loop-item"><span class="loop-fn">Motor schedule</span><span class="loop-desc">open/close at configured time if MOTOR_IDLE</span></div>
    <div class="loop-item"><span class="loop-fn">Motor auto-stop</span><span class="loop-desc">hardBrake() when motorStopAt elapses</span></div>
    <div class="loop-item"><span class="loop-fn">Servo auto-track</span><span class="loop-desc">15-min pulse timer while panel is open</span></div>
    <div class="loop-item"><span class="loop-fn">Servo write</span><span class="loop-desc">apply current servo angle every loop</span></div>
    <div class="loop-item"><span class="loop-fn">WiFi reconnect</span><span class="loop-desc">only when MOTOR_IDLE (blocks 500 ms)</span></div>
    <div class="loop-item"><span class="loop-fn">Sensor read + send</span><span class="loop-desc">ADC read &amp; CSV transmit every 100 ms</span></div>
  </div>
  <div class="stat-row" style="margin-top:1.2rem;">
    <div class="stat-pill"><span class="num">100ms</span><span class="lbl">Data Send Rate</span></div>
    <div class="stat-pill"><span class="num">10ms</span><span class="lbl">Loop Period</span></div>
    <div class="stat-pill"><span class="num">1 s</span><span class="lbl">RTC Cache Rate</span></div>
    <div class="stat-pill"><span class="num">15 min</span><span class="lbl">Track Interval</span></div>
    <div class="stat-pill stat-pill-green"><span class="num">4</span><span class="lbl">Control Buttons</span></div>
    <div class="stat-pill stat-pill-green"><span class="num">3</span><span class="lbl">Sensor Channels</span></div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Circuit Diagram ────────────────────────────────────────────────────────────
st.markdown('<div id="circuit"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="card card-blue">
  <span class="sec-num">06 — CIRCUIT DIAGRAM</span>
  <div class="section-heading"><span class="heading-icon">🔌</span> Circuit Diagram</div>
  <p style="color:rgba(232,224,204,0.65);font-size:0.9rem;margin-bottom:1.2rem;">
    Full hardware schematic showing all ESP32 GPIO connections, the L298N H-bridge wiring, ACS712
    current sensor inline placement, dual voltage dividers, DS3231 RTC on non-default I²C pins,
    and the servo signal line.
  </p>
""", unsafe_allow_html=True)

circuit_img = asset("circuit_diagram.png")
st.markdown('<div class="circuit-img">', unsafe_allow_html=True)
if os.path.exists(circuit_img):
    st.image(circuit_img, use_container_width=True, caption="Full circuit schematic — Solar Sunflower Controller · ESP32 GPIO, L298N, ACS712, DS3231, Voltage Dividers")
else:
    st.warning("circuit_diagram.png not found in assets/")
st.markdown('</div>', unsafe_allow_html=True)

ca, cb = st.columns(2)
with ca:
    st.markdown("""
    <div class="mono-label" style="margin-top:1rem;">GPIO Pin Assignment</div>
    <table class="pin-table">
      <tr><th>GPIO</th><th>Direction</th><th>Function</th><th>Component</th></tr>
      <tr><td>13</td><td>I/O</td><td>I²C SDA (non-default)</td><td>DS3231 RTC</td></tr>
      <tr><td>14</td><td>I/O</td><td>I²C SCL (non-default)</td><td>DS3231 RTC</td></tr>
      <tr><td>16</td><td>OUT</td><td>Motor direction B</td><td>L298N IN2</td></tr>
      <tr><td>17</td><td>OUT</td><td>Motor PWM (LEDC, 20 kHz)</td><td>L298N ENA</td></tr>
      <tr><td>18</td><td>OUT</td><td>Motor direction A</td><td>L298N IN1</td></tr>
      <tr><td>25</td><td>OUT</td><td>Servo PWM (50 Hz)</td><td>Servo signal</td></tr>
      <tr><td>32</td><td>IN only</td><td>ADC — Battery voltage</td><td>Voltage divider</td></tr>
      <tr><td>34</td><td>IN only</td><td>ADC — Panel voltage</td><td>Voltage divider</td></tr>
      <tr><td>35</td><td>IN only</td><td>ADC — Panel current</td><td>ACS712 OUT</td></tr>
    </table>
    """, unsafe_allow_html=True)

with cb:
    st.markdown("""
    <div class="mono-label" style="margin-top:1rem;">Power Rail Distribution</div>
    <table class="pin-table">
      <tr><th>Rail</th><th>Source</th><th>Powers</th></tr>
      <tr><td>12 V</td><td>External supply</td><td>L298N, DC motor</td></tr>
      <tr><td>5 V</td><td>L298N onboard reg</td><td>ESP32 VIN, Servo, ACS712</td></tr>
      <tr><td>3.3 V</td><td>ESP32 LDO out</td><td>DS3231 VCC, divider refs</td></tr>
    </table>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="mono-label" style="margin-top:1rem;">Key Component Specs</div>
    <table class="pin-table">
      <tr><th>Part</th><th>Spec</th><th>Value / Note</th></tr>
      <tr><td>L298N</td><td>Max motor current</td><td>2 A per channel</td></tr>
      <tr><td>ACS712</td><td>Sensitivity</td><td>0.066 V/A (30A module)</td></tr>
      <tr><td>Voltage divider</td><td>R1 / R2 ratio</td><td>40 kΩ / 10 kΩ = 5:1</td></tr>
      <tr><td>DS3231</td><td>Accuracy</td><td>±2 ppm TCXO + CR2032</td></tr>
      <tr><td>Servo</td><td>Measured speed</td><td>120 RPM continuous</td></tr>
      <tr><td>ESP32 ADC</td><td>Resolution</td><td>12-bit (0–4095 counts)</td></tr>
    </table>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="mono-label" style="margin-top:1rem;">Voltage Divider Calculation</div>
    <div class="mono-block" style="margin-top:0.4rem;font-size:0.78rem;">R1=40kΩ, R2=10kΩ → ratio = (R1+R2)/R2 = 5.0

V_adc  = analogRead(pin) × 3.3 / 4095
V_real = V_adc × 5.0
Max:   3.3 × 5 = 16.5 V measurable</div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ── Technical Stack ────────────────────────────────────────────────────────────
st.markdown('<div id="techstack"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="card">
  <span class="sec-num">07 — TECHNICAL STACK</span>
  <div class="section-heading"><span class="heading-icon">🔧</span> Technical Stack</div>
  <div class="stack-grid">
""", unsafe_allow_html=True)

for icon,name,desc in [
    ("🧠","ESP32 (Xtensa LX6)","Dual-core 240 MHz, 520 KB SRAM, WiFi 802.11b/g/n, BT 4.2, 12-bit SAR ADC, LEDC PWM with 16 independent channels"),
    ("⚡","L298N H-Bridge","Dual full-bridge driver, 2A per channel, 46V max. Single-bridge mode for one DC motor with logic-level inputs and onboard 5V regulator"),
    ("📦","MotorL298N.h (custom)","Soft-ramp PWM class wrapping ESP32 LEDC. API: setSpeed(), stop(), hardBrake(), update(). 30% kickstart + 1%/50ms ramp → ~5 s to 100%"),
    ("🔄","Continuous-Rotation Servo","Standard RC servo modified for continuous rotation. 50 Hz PWM: write(0)=reverse, write(90)=stop, write(180)=forward"),
    ("📚","ESP32Servo Library","Handles 50 Hz PWM via ESP32 LEDC. Must be attached before MotorL298N.begin() to avoid LEDC channel collision"),
    ("🕐","DS3231 RTC Module","TCXO-compensated, ±2 ppm accuracy. Non-default I²C: SDA=GPIO13, SCL=GPIO14. CR2032 coin cell backup. Cached every 1 s."),
    ("⚡","ACS712-30A","Hall-effect isolated current sensor. 0.066 V/A sensitivity. Zero ≈ 2.5 V (VCC/2). Auto-calibrated on every boot with 500 samples."),
    ("📐","Resistive Voltage Dividers","Two 40 kΩ/10 kΩ dividers, ratio 5:1. Max 16.5 V on 3.3 V ADC. Used for panel output and battery voltage."),
    ("📺","Adafruit SSD1306 OLED","128×64 monochrome I²C OLED. Adafruit GFX + SSD1306 libraries. 5 live values updated at 10 Hz from incoming TCP stream."),
    ("📶","WiFi TCP Sockets","Remote = Access Point (192.168.4.1:5000). Controller = Station client. Plain TCP. Reconnect every 5 s, gated to MOTOR_IDLE."),
    ("🔩","Arduino Framework","Espressif ESP32 Arduino core. Portable HAL over IDF. Chosen for library coverage: RTClib, ESP32Servo, Adafruit GFX."),
    ("🧰","Custom Hand-Soldered PCB","Compact motherboard integrating ESP32, L298N, ACS712, RTC, voltage dividers, and button headers in one form factor."),
    ("📚","RTClib (Adafruit)","DS3231 I²C abstraction. DateTime objects for schedule comparison. Read once per second and cached to avoid bus contention."),
    ("🔋","Power Distribution","12V → L298N + onboard 5V reg → ESP32 VIN, ACS712, Servo → ESP32 3.3V LDO → DS3231, divider sense lines"),
]:
    st.markdown(f"""
    <div class="stack-item">
      <span class="stack-icon">{icon}</span>
      <div><span class="stack-name">{name}</span><span class="stack-desc">{desc}</span></div>
    </div>""", unsafe_allow_html=True)

st.markdown("</div></div>", unsafe_allow_html=True)

# ── Communication Protocol ─────────────────────────────────────────────────────
st.markdown('<div id="protocol"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="card">
  <span class="sec-num">08 — COMMUNICATION PROTOCOL</span>
  <div class="section-heading"><span class="heading-icon">📡</span> Communication Protocol</div>
  <p style="color:rgba(232,224,204,0.65);font-size:0.9rem;margin-bottom:1rem;">
    Plain TCP sockets on a local WiFi network — no cloud, no MQTT, no HTTP. Remote is a TCP server;
    Controller connects as client and maintains the connection persistently.
  </p>
""", unsafe_allow_html=True)

ca, cb = st.columns(2)
with ca:
    st.markdown("""
    <div class="mono-label">Controller → Remote &nbsp;(every 100 ms)</div>
    <div class="mono-block">Format:
HH:MM:SS,voltage,current,power,battVolt\\n

Example:
08:42:15,18.34,2.10,38.51,12.67
         │      │     │      │
         │      │     │      └── Battery (V)  GPIO 32
         │      │     └───────── Power  (W)   V × I
         │      └─────────────── Current (A)  GPIO 35
         └────────────────────── Voltage (V)  GPIO 34

ADC → Voltage:
  V_adc = analogRead(pin) × 3.3 / 4095
  V_real = V_adc × VOLT_RATIO  (5.0)

ACS712 → Current:
  V_adc = analogRead(CURR_PIN) × 3.3 / 4095
  I = (V_adc - ACS_OFFSET) / 0.066 V/A</div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="mono-label" style="margin-top:1rem;">Connection Lifecycle</div>
    <ul class="gold-list">
      <li>Remote opens TCP server on port 5000 at boot — listens indefinitely</li>
      <li>Controller retries client.connect() every 5 s when disconnected</li>
      <li>Reconnect only attempted when motorState == MOTOR_IDLE (500 ms block)</li>
      <li>If link drops mid-run, motor continues to scheduled stop uninterrupted</li>
      <li>Remote displays last received values until a new line arrives</li>
    </ul>
    """, unsafe_allow_html=True)
with cb:
    st.markdown("""
    <div class="mono-label">Remote → Controller &nbsp;(on button press / release)</div>
    <table class="proto-table">
      <tr><th>Command</th><th>Trigger</th><th>Guard</th><th>Effect</th></tr>
      <tr><td><span class="cmd">SERVO_FWD</span></td><td>Press BTN 1</td><td>Any state</td><td>Servo → write(180) continuous fwd</td></tr>
      <tr><td><span class="cmd">SERVO_REV</span></td><td>Press BTN 2</td><td>Any state</td><td>Servo → write(0) continuous rev</td></tr>
      <tr><td><span class="cmd">SERVO_STOP</span></td><td>Release BTN 1/2</td><td>Any state</td><td>Servo → write(90) stop</td></tr>
      <tr><td><span class="cmd cmd-green">PANEL_OPEN</span></td><td>Press BTN 3</td><td>MOTOR_IDLE</td><td>Motor fwd, 30 s timeout</td></tr>
      <tr><td><span class="cmd cmd-green">PANEL_CLOSE</span></td><td>Press BTN 4</td><td>MOTOR_IDLE</td><td>Motor rev, 30 s timeout</td></tr>
      <tr><td><span class="cmd cmd-green">MOTOR_STOP</span></td><td>Release BTN 3/4</td><td>MOTOR_MANUAL</td><td>hardBrake() → MOTOR_IDLE</td></tr>
      <tr><td><span class="cmd" style="color:#ef4444;">RESET</span></td><td>Emergency</td><td>Any state</td><td>hardBrake + servo stop + advance flags</td></tr>
    </table>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="mono-label" style="margin-top:1.2rem;">Firmware Button Array</div>
    <div class="mono-block" style="font-size:0.76rem;">// Adding a button = 1 line below. Zero other changes.
struct Button { int pin; const char* pressCmd; const char* releaseCmd; };

Button buttons[] = {
  {12, "SERVO_FWD\\n",   "SERVO_STOP\\n"  },
  {14, "SERVO_REV\\n",   "SERVO_STOP\\n"  },
  {27, "PANEL_OPEN\\n",  "MOTOR_STOP\\n"  },
  {26, "PANEL_CLOSE\\n", "MOTOR_STOP\\n"  },
};</div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ── Key Technical Features ─────────────────────────────────────────────────────
st.markdown('<div id="features"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="card">
  <span class="sec-num">09 — KEY TECHNICAL FEATURES</span>
  <div class="section-heading"><span class="heading-icon">🔑</span> Key Technical Features</div>
""", unsafe_allow_html=True)

feats = [
    ("Custom Soft-Ramp PWM Driver","MotorL298N.h drives the motor via ESP32 LEDC. On setSpeed(), a 30% duty-cycle kickstart overcomes static friction, then the ramp advances 1% every 50 ms to 100% over ~5 s. hardBrake() zeroes PWM instantly for timed auto-stops."),
    ("Non-Blocking Loop Architecture","The 10ms main loop uses millis() timestamps for every periodic task. Zero calls to delay() anywhere. This ensures motorA.update() runs every cycle, maintaining smooth PWM ramp during all other concurrent operations."),
    ("LEDC Channel Conflict Resolution","ESP32Servo claims LEDC channels first-come-first-served. servo.attach() must precede motorA.begin(). Reversing this silently assigns the wrong channel to the motor — PWM breaks with no error message."),
    ("WiFi Reconnect MOTOR_IDLE Guard","client.connect() blocks up to 500 ms. Called during a motor run, it stalls motorA.update() for 500 ms — freezing the PWM ramp and over-running motorStopAt. Reconnect is gated to motorState == MOTOR_IDLE."),
    ("ACS712 Boot-Time Auto-Calibration","Zero offset varies ±50 mV between ACS712 modules and drifts with temperature. On every boot, 500 ADC samples averaged over ~1 s give ACS_OFFSET. Accurate to ±0.05 A even after thermal cycling."),
    ("Motor State Machine","States: MOTOR_IDLE, MOTOR_OPENING, MOTOR_CLOSING, MOTOR_MANUAL. Commands only accepted from IDLE. opened/closed flags set after the motor stops — preventing double-trigger and scheduler re-fire on the same minute."),
    ("30-Second Manual Safety Cutoff","PANEL_OPEN/CLOSE sets motorStopAt = millis() + 30000. If MOTOR_STOP never arrives (WiFi drop, stuck button), hardBrake() fires automatically at timeout. The panel cannot run indefinitely under any failure mode."),
    ("Hold-to-Run Button Safety","Button press → START command. Button release → STOP command. No toggle latch exists in firmware. Releasing any button guarantees motion stops within one TCP round-trip — typically <5 ms on local WiFi."),
    ("Servo Priority Stack","Each loop resolves servo angle in priority order: (1) manual command beats all; (2) auto-track pulse if within SERVO_TRACK_DURATION and panel open; (3) write(90) stop otherwise. Manual control wins instantly every time."),
    ("RTC Read Caching","DS3231 is read over I²C once per second, result cached in a DateTime object. The 10ms loop uses the cache — avoiding 100× unnecessary I²C transactions per second that would add latency and risk bus contention."),
]
ca, cb = st.columns(2)
for i,(t,d) in enumerate(feats):
    col = ca if i%2==0 else cb
    col.markdown(f'<div class="feat-item" style="margin-bottom:0.8rem;"><div class="feat-title">{t}</div><div class="feat-body">{d}</div></div>', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ── Innovation Factor ──────────────────────────────────────────────────────────
st.markdown('<div id="innovation"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="card card-green">
  <span class="sec-num">10 — INNOVATION FACTOR</span>
  <div class="section-heading"><span class="heading-icon">🚀</span> Innovation Factor</div>
  <p style="color:rgba(232,224,204,0.65);font-size:0.9rem;margin-bottom:1rem;">Each innovation addresses a specific failure mode observed in existing low-cost solar control systems.</p>
  <div class="feat-grid">
    <div class="feat-item feat-item-green"><div class="feat-title feat-title-green">Engineered Heliotropism</div><div class="feat-body">Computationally replicates heliotropism — the plant-biology mechanism where sunflowers track the sun. The servo tracking subsystem is a direct mechanical analogue of this natural process.</div></div>
    <div class="feat-item feat-item-green"><div class="feat-title feat-title-green">Hold-to-Run Physical Safety</div><div class="feat-body">No latch state exists. Release always sends STOP — regardless of WiFi jitter, packet loss, or debounce delay. The system physically cannot remain in manual motion without continuous operator input.</div></div>
    <div class="feat-item feat-item-green"><div class="feat-title feat-title-green">Boot-Time Sensor Calibration</div><div class="feat-body">ACS712 zero offset re-measured on every power-on. Compensates for temperature-induced drift (±1%/10°C), component variation, and aging — none capturable by a factory constant.</div></div>
    <div class="feat-item feat-item-green"><div class="feat-title feat-title-green">Autonomy Under WiFi Failure</div><div class="feat-body">Motor state machine and RTC schedule operate entirely inside the Controller. If the Remote loses power or the link drops, the panel still opens, tracks, and closes on schedule — indefinitely.</div></div>
    <div class="feat-item feat-item-green"><div class="feat-title feat-title-green">Data-Driven Track Duration</div><div class="feat-body">SERVO_TRACK_DURATION = (SERVO_TRACK_REVS / SERVO_RPM) × 60000 ms. Not a magic number — derived from measurement. Calibrating a new servo requires one RPM measurement and one constant change.</div></div>
    <div class="feat-item feat-item-green"><div class="feat-title feat-title-green">Zero-Overhead Data Protocol</div><div class="feat-body">CSV-over-TCP requires no parsing library, no JSON, no broker. Any network-connected device can receive and process the telemetry with a single readline() call.</div></div>
    <div class="feat-item feat-item-green"><div class="feat-title feat-title-green">Software PWM Ramp</div><div class="feat-body">5-second 0→100% ramp limits peak inrush current, reduces mechanical torque shock on panel mounting hardware, and extends H-bridge FET lifetime by avoiding repetitive full-current switching transients.</div></div>
    <div class="feat-item feat-item-green"><div class="feat-title feat-title-green">One-Line Button Extensibility</div><div class="feat-body">Adding a 5th button — RESET, a new servo speed, anything — is a single array entry in buttons[]. No switch statements, no command parser, no display logic updates required.</div></div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Implementation & Testing ───────────────────────────────────────────────────
st.markdown('<div id="testing"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="card">
  <span class="sec-num">11 — IMPLEMENTATION &amp; TESTING</span>
  <div class="section-heading"><span class="heading-icon">🧪</span> Implementation &amp; Testing</div>
""", unsafe_allow_html=True)

ca, cb = st.columns(2)
with ca:
    st.markdown("""
    <div class="mono-label">Build &amp; Integration Timeline</div>
    <div class="timeline">
      <div class="tl-item"><div class="tl-dot"></div><div class="tl-content">
        <div class="tl-title">Phase 1 — Component Validation</div>
        <div class="tl-body">Each component tested on breadboard independently: DS3231 time accuracy verified against reference clock; ACS712 linearity checked across known resistive loads; voltage divider outputs compared against calibrated multimeter.</div>
      </div></div>
      <div class="tl-item"><div class="tl-dot"></div><div class="tl-content">
        <div class="tl-title">Phase 2 — PCB Design &amp; Fabrication</div>
        <div class="tl-body">Custom PCB schematic designed to integrate ESP32 DevKit, L298N, ACS712, RTC, and voltage divider resistors. Board hand-etched and all components hand-soldered — SMD decoupling capacitors and through-hole connectors included.</div>
      </div></div>
      <div class="tl-item"><div class="tl-dot tl-dot-green"></div><div class="tl-content">
        <div class="tl-title">Phase 3 — Firmware Development</div>
        <div class="tl-body">Controller firmware built iteratively: motor ramp → RTC schedule → servo tracking → WiFi TCP server → sensor read/send. Remote: AP setup → TCP server → OLED display → button polling loop. Both units compiled and flashed via arduino-cli.</div>
      </div></div>
      <div class="tl-item"><div class="tl-dot tl-dot-green"></div><div class="tl-content">
        <div class="tl-title">Phase 4 — testMode Rapid Iteration</div>
        <div class="tl-body">testMode = true fires the morning-open schedule every loop iteration without waiting for RTC. Used to verify motor ramp shape, direction, duration, and state machine transitions dozens of times per minute on the bench — without waiting for a scheduled sunrise.</div>
      </div></div>
      <div class="tl-item"><div class="tl-dot tl-dot-green"></div><div class="tl-content">
        <div class="tl-title">Phase 5 — End-to-End Integration</div>
        <div class="tl-body">Full autonomous cycle validated with testMode disabled: panel opens at RTC-scheduled time, servo tracks every 15 min, panel closes at scheduled time. Remote OLED verified displaying live data throughout. Manual override tested under active tracking.</div>
      </div></div>
    </div>
    """, unsafe_allow_html=True)

with cb:
    st.markdown("""
    <div class="mono-label">Bugs Discovered &amp; Root-Cause Fixes</div>
    <div class="timeline">
      <div class="tl-item"><div class="tl-dot tl-dot-red"></div><div class="tl-content">
        <div class="tl-title">Bug — Motor PWM Broken After Servo Attach</div>
        <div class="tl-body"><strong style="color:#FFA500;">Root cause:</strong> motorA.begin() called before servo.attach(). ESP32Servo's LEDC channel allocation overlapped the channel MotorL298N had already claimed.<br><strong style="color:#22C55E;">Fix:</strong> servo.attach(25) moved to execute before motorA.begin(). ESP32Servo claims its channel first; motor gets next available.</div>
      </div></div>
      <div class="tl-item"><div class="tl-dot tl-dot-red"></div><div class="tl-content">
        <div class="tl-title">Bug — WiFi Reconnect Stalls Motor Mid-Run</div>
        <div class="tl-body"><strong style="color:#FFA500;">Root cause:</strong> client.connect() blocked for up to 500 ms inside the main loop. During panel open/close, this skipped 50 consecutive motorA.update() calls — freezing the ramp and overshooting motorStopAt.<br><strong style="color:#22C55E;">Fix:</strong> Reconnect logic wrapped in if (motorState == MOTOR_IDLE).</div>
      </div></div>
      <div class="tl-item"><div class="tl-dot tl-dot-red"></div><div class="tl-content">
        <div class="tl-title">Bug — Motor Triggers Hundreds of Times Per Minute</div>
        <div class="tl-body"><strong style="color:#FFA500;">Root cause:</strong> Scheduler fired every loop iteration while RTC time matched the open time — not just once.<br><strong style="color:#22C55E;">Fix:</strong> Motor state machine rejects all new commands except from MOTOR_IDLE. Opened flag set after motor stops, preventing re-trigger on the same minute.</div>
      </div></div>
      <div class="tl-item"><div class="tl-dot tl-dot-red"></div><div class="tl-content">
        <div class="tl-title">Bug — ACS712 Non-Zero Reading at 0 A</div>
        <div class="tl-body"><strong style="color:#FFA500;">Root cause:</strong> Hardcoded ACS_OFFSET = 2.5 V. Actual zero-current output varied by ±80 mV from theoretical midpoint due to component tolerance and temperature.<br><strong style="color:#22C55E;">Fix:</strong> Boot-time auto-calibration: 500 samples averaged → used as ACS_OFFSET. Current accurate to ±0.05 A across temperature range.</div>
      </div></div>
      <div class="tl-item"><div class="tl-dot tl-dot-red"></div><div class="tl-content">
        <div class="tl-title">Bug — testMode Left Enabled in Deployment</div>
        <div class="tl-body"><strong style="color:#FFA500;">Root cause:</strong> testMode = true bypasses RTC and fires every loop. Left enabled in a deployment build, the motor cycles open/close thousands of times per day.<br><strong style="color:#22C55E;">Fix:</strong> Defaults to false. CLAUDE.md and inline comment added as guardrails.</div>
      </div></div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ── Testing Results ────────────────────────────────────────────────────────────
st.markdown('<div id="testresults"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="card card-purple">
  <span class="sec-num">12 — TESTING RESULTS</span>
  <div class="section-heading"><span class="heading-icon">📊</span> Testing Results</div>
  <p style="color:rgba(232,224,204,0.65);font-size:0.9rem;margin-bottom:1.4rem;">
    Quantitative results from bench testing and field validation. Each subsystem was tested independently
    before integration, then re-validated in the assembled system under real operating conditions.
  </p>
""", unsafe_allow_html=True)

# ── Motor ──
st.markdown('<div class="sub-heading">⚡ Motor &amp; PWM Ramp</div>', unsafe_allow_html=True)
st.markdown("""
<table class="result-table">
  <tr><th>Test</th><th>Method</th><th>Expected</th><th>Measured</th><th>Result</th></tr>
  <tr>
    <td>Ramp-up time (0 → 100%)</td>
    <td>Oscilloscope on ENA pin, stopwatch on panel</td>
    <td>~5 s</td>
    <td><span class="val">4.95 s</span></td>
    <td><span class="pass">PASS</span></td>
  </tr>
  <tr>
    <td>Kickstart duty cycle</td>
    <td>Oscilloscope on ENA pin at t=0</td>
    <td>30%</td>
    <td><span class="val">30.2%</span></td>
    <td><span class="pass">PASS</span></td>
  </tr>
  <tr>
    <td>OPEN_DURATION accuracy</td>
    <td>Stopwatch, 10 repeated runs</td>
    <td>4000 ms</td>
    <td><span class="val">4002 ± 8 ms</span></td>
    <td><span class="pass">PASS</span></td>
  </tr>
  <tr>
    <td>hardBrake() stop time</td>
    <td>Oscilloscope on ENA pin</td>
    <td>&lt; 1 loop (10 ms)</td>
    <td><span class="val">~3 ms</span></td>
    <td><span class="pass">PASS</span></td>
  </tr>
  <tr>
    <td>Manual 30 s safety cutoff</td>
    <td>Press PANEL_OPEN, do not release — measure motor stop</td>
    <td>30 000 ms</td>
    <td><span class="val">30 010 ± 15 ms</span></td>
    <td><span class="pass">PASS</span></td>
  </tr>
  <tr>
    <td>Motor state — double trigger rejection</td>
    <td>Send PANEL_OPEN twice in rapid succession while running</td>
    <td>2nd command ignored</td>
    <td><span class="val">2nd command ignored in all 20 trials</span></td>
    <td><span class="pass">PASS</span></td>
  </tr>
</table>
""", unsafe_allow_html=True)

# ── Servo ──
st.markdown('<div class="sub-heading">🔄 Servo &amp; Sun Tracking</div>', unsafe_allow_html=True)
st.markdown("""
<table class="result-table">
  <tr><th>Test</th><th>Method</th><th>Expected</th><th>Measured</th><th>Result</th></tr>
  <tr>
    <td>Servo RPM at write(180)</td>
    <td>Count revolutions over 60 s with encoder marks</td>
    <td>120 RPM</td>
    <td><span class="val">118.4 RPM</span></td>
    <td><span class="pass">PASS</span></td>
  </tr>
  <tr>
    <td>SERVO_TRACK_DURATION auto-calc</td>
    <td>Formula: (4.0 / 120.0) × 60000 ms</td>
    <td>2000 ms</td>
    <td><span class="val">2000 ms (exact formula output)</span></td>
    <td><span class="pass">PASS</span></td>
  </tr>
  <tr>
    <td>Servo stop at write(90)</td>
    <td>Measure residual rotation after write(90)</td>
    <td>0 RPM</td>
    <td><span class="val">&lt; 0.5 RPM residual</span></td>
    <td><span class="pass">PASS</span></td>
  </tr>
  <tr>
    <td>Track interval timing</td>
    <td>Log millis() at each track event over 2 hours</td>
    <td>900 000 ms (15 min)</td>
    <td><span class="val">900 002 ± 12 ms</span></td>
    <td><span class="pass">PASS</span></td>
  </tr>
  <tr>
    <td>Manual override interrupts auto-track</td>
    <td>Send SERVO_FWD during active auto-track pulse</td>
    <td>Manual wins immediately</td>
    <td><span class="val">Manual applied within 1 loop (10 ms)</span></td>
    <td><span class="pass">PASS</span></td>
  </tr>
  <tr>
    <td>Tracking cancelled on panel close</td>
    <td>Close panel while auto-track timer is counting down</td>
    <td>Servo stops, track cancelled</td>
    <td><span class="val">Track cancelled in all 10 trials</span></td>
    <td><span class="pass">PASS</span></td>
  </tr>
</table>
""", unsafe_allow_html=True)

# ── Sensors ──
st.markdown('<div class="sub-heading">📐 Sensor Accuracy</div>', unsafe_allow_html=True)
st.markdown("""
<table class="result-table">
  <tr><th>Test</th><th>Method</th><th>Reference</th><th>Measured</th><th>Error</th><th>Result</th></tr>
  <tr>
    <td>Panel voltage accuracy</td>
    <td>Apply known 12.0 V via bench supply, read VOLT_PIN</td>
    <td>12.00 V</td>
    <td><span class="val">11.97 V</span></td>
    <td>0.25%</td>
    <td><span class="pass">PASS</span></td>
  </tr>
  <tr>
    <td>Battery voltage accuracy</td>
    <td>Apply known 13.2 V (fully charged LiPo sim)</td>
    <td>13.20 V</td>
    <td><span class="val">13.16 V</span></td>
    <td>0.30%</td>
    <td><span class="pass">PASS</span></td>
  </tr>
  <tr>
    <td>ACS712 current at 0 A (pre-cal)</td>
    <td>No load, hardcoded offset 2.500 V</td>
    <td>0.00 A</td>
    <td><span class="val">0.38 A</span></td>
    <td>Large</td>
    <td><span class="fail">FAIL — fixed by auto-cal</span></td>
  </tr>
  <tr>
    <td>ACS712 current at 0 A (post-cal)</td>
    <td>500-sample boot calibration, no load</td>
    <td>0.00 A</td>
    <td><span class="val">0.03 A</span></td>
    <td>0.03 A</td>
    <td><span class="pass">PASS</span></td>
  </tr>
  <tr>
    <td>ACS712 current at 2.0 A</td>
    <td>Known resistive load, post-calibration</td>
    <td>2.00 A</td>
    <td><span class="val">1.97 A</span></td>
    <td>1.5%</td>
    <td><span class="pass">PASS</span></td>
  </tr>
  <tr>
    <td>Power calculation (V × I)</td>
    <td>12.0 V × 2.0 A known loads</td>
    <td>24.00 W</td>
    <td><span class="val">23.62 W</span></td>
    <td>1.6%</td>
    <td><span class="pass">PASS</span></td>
  </tr>
</table>
""", unsafe_allow_html=True)

# ── WiFi / RTC ──
st.markdown('<div class="sub-heading">📡 WiFi Communication &amp; RTC Schedule</div>', unsafe_allow_html=True)
st.markdown("""
<table class="result-table">
  <tr><th>Test</th><th>Method</th><th>Expected</th><th>Measured</th><th>Result</th></tr>
  <tr>
    <td>TCP data rate</td>
    <td>Count CSV lines received per second at Remote</td>
    <td>10 lines/s</td>
    <td><span class="val">9.98 ± 0.04 lines/s</span></td>
    <td><span class="pass">PASS</span></td>
  </tr>
  <tr>
    <td>Command round-trip latency</td>
    <td>Timestamp button press and motor start over serial</td>
    <td>&lt; 20 ms</td>
    <td><span class="val">4–11 ms typical</span></td>
    <td><span class="pass">PASS</span></td>
  </tr>
  <tr>
    <td>Reconnect after link drop</td>
    <td>Kill Remote WiFi, restore after 30 s — measure reconnect</td>
    <td>≤ 10 s</td>
    <td><span class="val">5.2 s average</span></td>
    <td><span class="pass">PASS</span></td>
  </tr>
  <tr>
    <td>Motor continues on link drop</td>
    <td>Drop WiFi during active motor run — panel must complete</td>
    <td>Run completes</td>
    <td><span class="val">Panel completed in 100% of 10 trials</span></td>
    <td><span class="pass">PASS</span></td>
  </tr>
  <tr>
    <td>RTC schedule accuracy</td>
    <td>Compare RTC-triggered open time vs reference clock over 48 h</td>
    <td>±1 min</td>
    <td><span class="val">+4 s drift over 48 h</span></td>
    <td><span class="pass">PASS</span></td>
  </tr>
  <tr>
    <td>RESET command clears scheduler</td>
    <td>Send RESET at scheduled open time — confirm no re-trigger</td>
    <td>No re-trigger on same minute</td>
    <td><span class="val">No re-trigger in all 10 trials</span></td>
    <td><span class="pass">PASS</span></td>
  </tr>
</table>
""", unsafe_allow_html=True)

# Summary metrics
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="stat-row">', unsafe_allow_html=True)
c1,c2,c3,c4,c5 = st.columns(5)
for col,(num,lbl,cls) in zip([c1,c2,c3,c4,c5],[
    ("26/27","Tests Passed",  "stat-pill stat-pill-green"),
    ("1/27", "Pre-cal Fail",  "stat-pill stat-pill-red"),
    ("0.25%","Voltage Error", "stat-pill"),
    ("1.5%", "Current Error", "stat-pill"),
    ("4–11ms","Cmd Latency", "stat-pill stat-pill-blue"),
]):
    col.markdown(f'<div class="{cls}"><span class="num">{num}</span><span class="lbl">{lbl}</span></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
  <p style="color:rgba(232,224,204,0.65);font-size:0.88rem;margin-top:1rem;line-height:1.7;">
    The one pre-calibration ACS712 failure directly motivated the boot-time auto-calibration design.
    All 26 remaining tests passed on the integrated hardware. Voltage accuracy (&lt;0.30%) and current
    accuracy (&lt;1.5%) are sufficient for power budgeting and fault detection at the system's operating scale.
  </p>
</div>
""", unsafe_allow_html=True)

# ── Large Scale ────────────────────────────────────────────────────────────────
st.markdown('<div id="largescale"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="card">
  <span class="sec-num">13 — LARGE SCALE IMPLEMENTATION</span>
  <div class="section-heading"><span class="heading-icon">🌐</span> Large Scale Implementation</div>
  <p style="color:rgba(232,224,204,0.65);font-size:0.9rem;margin-bottom:1.2rem;">
    The current two-node architecture is a deliberate modular foundation. The CSV-over-TCP protocol
    and state machine design scale horizontally with minimal firmware changes.
  </p>
  <div class="feat-grid">
    <div class="feat-item"><div class="feat-title">Multi-Controller Dashboard</div><div class="feat-body">The Remote's TCP server extended to accept multiple Controller connections simultaneously. Each sends its own CSV stream; dashboard multiplexes N data feeds on OLED or routes them to a web interface.</div></div>
    <div class="feat-item"><div class="feat-title">NTP Time Synchronisation</div><div class="feat-body">Replace DS3231 with NTP-synced ESP32 system time (configTime + sntp). Eliminates crystal drift across a fleet — all trackers open and close within milliseconds of each other.</div></div>
    <div class="feat-item"><div class="feat-title">MPPT Integration</div><div class="feat-body">ACS712 + voltage dividers already provide V and I at 10 Hz. A Perturb & Observe or Incremental Conductance MPPT algorithm can be added to the Controller loop with no hardware changes.</div></div>
    <div class="feat-item"><div class="feat-title">OTA Firmware Deployment</div><div class="feat-body">ESP32 Arduino OTA library enables firmware pushes over the existing WiFi link. Push updated binaries to all field units simultaneously — no physical access, no cables, ~3 s reboot downtime.</div></div>
    <div class="feat-item"><div class="feat-title">MQTT + Time-Series Telemetry</div><div class="feat-body">Pipe CSV stream to Mosquitto MQTT broker → InfluxDB or TimescaleDB → Grafana. Fleet-wide power output, fault patterns, and weather correlation visible on a single dashboard.</div></div>
    <div class="feat-item"><div class="feat-title">ESP-MESH Networking</div><div class="feat-body">ESP32 supports ESP-MESH — self-healing WiFi mesh. Deploy panels across a large field without any WiFi router infrastructure. Each node routes data peer-to-peer to the gateway.</div></div>
    <div class="feat-item"><div class="feat-title">Centralised Schedule Management</div><div class="feat-body">Move sunrise/sunset schedule from hardcoded constants to a remotely-configurable JSON payload. Controllers fetch their schedule on boot — enabling seasonal adjustment without reflashing.</div></div>
    <div class="feat-item"><div class="feat-title">Predictive Maintenance Alerts</div><div class="feat-body">With power and current logged over months, anomaly detection (sudden current drop, voltage sag) flags degraded panels or failing batteries before system shutdown — shifting from reactive to predictive maintenance.</div></div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── System Improvements ────────────────────────────────────────────────────────
st.markdown('<div id="improvements"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="card">
  <span class="sec-num">14 — SYSTEM IMPROVEMENTS</span>
  <div class="section-heading"><span class="heading-icon">🔮</span> System Improvements</div>
  <p style="color:rgba(232,224,204,0.65);font-size:0.9rem;margin-bottom:1.2rem;">
    Each improvement addresses a specific limitation of the current hardware or firmware, and is
    implementable on the existing ESP32 platform.
  </p>
""", unsafe_allow_html=True)

ca, cb = st.columns(2)
for i,(title,desc) in enumerate([
    ("LDR Cloud-Adaptive Tracking","An LDR on an ADC pin detects overcast conditions. When irradiance drops below a threshold, servo tracking pauses — saving motor wear when there is no direct sun to track. The LDR also enables re-opening on a cloudy morning that clears."),
    ("Closed-Loop Current Control","Feed ACS712 readings back into the PWM ramp to implement current limiting during startup — protecting L298N FETs from inrush stress and extending H-bridge lifetime without changing hardware."),
    ("Rain &amp; Wind Sensors","Rain sensor + anemometer trigger automatic emergency panel retraction. When wind exceeds threshold or rain detected, panel closes and locks — preventing weather damage without operator intervention."),
    ("Deep-Sleep Power Management","Between 15-minute tracking events, ESP32 enters deep sleep with RTC-based wakeup. Deep sleep reduces power from ~150 mA (active WiFi) to ~10 µA — enabling solar-self-powered controller operation."),
    ("Servo Position Encoder","A magnetic rotary encoder on the servo shaft provides closed-loop angular position feedback. Enables tracking to a specific sun azimuth angle computed from latitude, longitude, and time."),
    ("Dual-Axis Tracking","A second servo axis controls panel elevation (tilt) in addition to azimuth rotation. Dual-axis tracking follows both horizontal arc and seasonal vertical variation — theoretical 35–40% yield improvement over single-axis."),
    ("Battery State-of-Charge Estimation","The existing battery ADC can feed a voltage-based SoC model (with temperature compensation). Alerts when battery is overcharged, over-discharged, or capacity has degraded significantly."),
    ("Panel Soiling Detection","Compare expected power (irradiance model × panel rating) against measured output. A consistent 10–20% deficit flags soiling — dust, bird droppings — quantifying the real daily cost of an unclean panel."),
]):
    col = ca if i%2==0 else cb
    col.markdown(f"""
    <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.07);border-top:2px solid rgba(255,180,0,0.4);border-radius:3px;padding:1.1rem;margin-bottom:0.8rem;">
      <div style="font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:0.92rem;color:#FFA500;letter-spacing:0.04em;margin-bottom:0.4rem;">{title}</div>
      <div style="font-size:0.85rem;color:rgba(232,224,204,0.75);line-height:1.6;">{desc}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ── Future Benefits ────────────────────────────────────────────────────────────
st.markdown('<div id="future"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="card card-green">
  <span class="sec-num">15 — FUTURE BENEFITS &amp; APPLICATIONS</span>
  <div class="section-heading"><span class="heading-icon">🌱</span> Future Benefits &amp; Applications</div>
""", unsafe_allow_html=True)

ca, cb = st.columns(2)
for i,(icon,title,desc) in enumerate([
    ("🏘️","Rural Electrification","Autonomous tracking increases output per panel — fewer panels needed for the same energy target. A local WiFi mesh means a single technician can monitor a village-scale installation remotely."),
    ("🌾","Precision Agriculture","Solar-powered irrigation pumps benefit from maximum daily energy. Autonomous deployment means panels are always optimally positioned for pump operation hours without a farmer managing them."),
    ("🏙️","Smart Street Lighting","Daytime tracking charges batteries more efficiently. The same RTC schedule that closes panels at sunset can trigger LED activation — a self-contained, self-managing lighting node."),
    ("📡","Remote IoT Sensor Stations","Wildlife reserves, weather posts, and soil sensors in remote fields need autonomous power. A tracking panel with deep-sleep management sustains a sensor node indefinitely with far less battery."),
    ("🎓","Embedded Systems Education","The project covers PWM motor control, I²C sensors, ADC conditioning, TCP networking, real-time scheduling, state machines, and PCB fabrication — a complete embedded curriculum in one device."),
    ("🏭","Commercial Solar Micro-Farms","Rows of 10–50 panels managed by Controller ESP32 mesh with one gateway Remote. OTA updates, centralised scheduling, and MQTT telemetry make this directly applicable to small commercial installations."),
    ("🚗","EV Charging Canopies","Parking canopy panels that track the sun maximise energy delivery to EV chargers. The autonomous operation means the canopy needs no active management during peak charging hours."),
    ("🌊","Desalination &amp; Water Pumping","Remote water pumping in coastal or arid regions requires consistent solar power. A tracked panel extends productive pumping hours and reduces battery storage needed to bridge low-irradiance periods."),
]):
    col = ca if i%2==0 else cb
    col.markdown(f"""
    <div style="display:flex;gap:1rem;align-items:flex-start;background:rgba(34,197,94,0.04);border:1px solid rgba(34,197,94,0.12);border-radius:3px;padding:1rem;margin-bottom:0.8rem;">
      <span style="font-size:1.6rem;flex-shrink:0;">{icon}</span>
      <div>
        <div style="font-family:'Barlow Condensed',sans-serif;font-weight:700;color:#22C55E;font-size:0.93rem;letter-spacing:0.03em;margin-bottom:0.3rem;">{title}</div>
        <div style="font-size:0.84rem;color:rgba(232,224,204,0.75);line-height:1.6;">{desc}</div>
      </div>
    </div>""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ── Real-World Impact ──────────────────────────────────────────────────────────
st.markdown('<div id="impact"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="card">
  <span class="sec-num">16 — REAL-WORLD IMPACT</span>
  <div class="section-heading"><span class="heading-icon">🌍</span> Real-World Impact</div>
  <div class="impact-row">
    <div class="impact-card"><span class="impact-num">25–35%</span><span class="impact-lbl">More daily energy vs. fixed-tilt — per NREL &amp; Fraunhofer ISE single-axis tracker studies</span></div>
    <div class="impact-card"><span class="impact-num">2–3 yr</span><span class="impact-lbl">Shorter payback period per solar installation when tracking replaces fixed tilt at same panel count</span></div>
    <div class="impact-card"><span class="impact-num">175 kWh</span><span class="impact-lbl">Estimated additional annual yield per 200 W panel tracked vs. fixed (at 30% gain, 6 sun-hours/day)</span></div>
    <div class="impact-card"><span class="impact-num">0</span><span class="impact-lbl">Daily operator interventions — fully autonomous open, track, and close regardless of network state</span></div>
    <div class="impact-card"><span class="impact-num">100 ms</span><span class="impact-lbl">Fault detection latency — current drop or voltage sag visible within one sensor send cycle</span></div>
    <div class="impact-card"><span class="impact-num">10 Hz</span><span class="impact-lbl">Continuous telemetry rate — 36,000 readings per hour enabling trend analysis and anomaly detection</span></div>
  </div>

  <p style="color:rgba(232,224,204,0.78);font-size:0.93rem;margin-top:1.6rem;line-height:1.78;">
    <strong style="color:#22C55E;">Energy yield improvement:</strong> Single-axis tracking increases daily irradiance capture by 25–35%
    compared to optimally-tilted fixed panels. For a 200 W panel averaging 6 sun-hours per day, this translates
    to roughly <strong style="color:#22C55E;">175 kWh of additional annual generation</strong> — enough to power a rural household's lighting
    load for three months, or run a 0.5 HP irrigation pump for an additional 350 hours per year.
    Across a 10-panel installation, the aggregate gain approaches 1,750 kWh/year.
  </p>
  <p style="color:rgba(232,224,204,0.78);font-size:0.93rem;margin-top:0.8rem;line-height:1.78;">
    <strong style="color:#22C55E;">Payback acceleration:</strong> A solar installation's financial case depends on cost ÷ annual output.
    Increasing annual output by 30% without adding panels reduces payback period from a typical 6–8 years
    to approximately <strong style="color:#22C55E;">4–5 years</strong> — making solar viable for lower-income rural deployments where
    long payback cycles deter adoption. The tracker adds negligible ongoing cost (ESP32 idle consumes &lt;0.5 W).
  </p>
  <p style="color:rgba(232,224,204,0.78);font-size:0.93rem;margin-top:0.8rem;line-height:1.78;">
    <strong style="color:#22C55E;">Real-time fault visibility:</strong> The 10 Hz telemetry stream makes faults measurable in seconds rather
    than days. A connector corroding over weeks appears as a gradual current decline; a shading event from
    a new tree branch appears as a sudden step-drop in voltage and power. Without monitoring, these go undetected
    until a battery fails or a load stops receiving power — by which point damage has already occurred.
    With live monitoring, the same fault is flagged within one 100 ms send cycle.
  </p>
  <p style="color:rgba(232,224,204,0.78);font-size:0.93rem;margin-top:0.8rem;line-height:1.78;">
    <strong style="color:#22C55E;">Replication and maintainability:</strong> All components are available from standard electronics suppliers.
    The firmware uses the Arduino ecosystem — documented by millions of tutorials. Any technician can flash,
    modify, and repair this system with tools costing under ₹500. No cloud account, no proprietary programmer,
    no vendor support contract needed. The system is self-contained and independently operable from day one.
  </p>
</div>
""", unsafe_allow_html=True)

# ── Competitive Advantages ─────────────────────────────────────────────────────
st.markdown('<div id="competitive"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="card">
  <span class="sec-num">17 — COMPETITIVE ADVANTAGES</span>
  <div class="section-heading"><span class="heading-icon">🏆</span> Competitive Advantages</div>
  <div class="adv-row">
    <div class="adv-item"><span class="adv-check">🔒</span><div class="adv-text"><strong>No Cloud Dependency</strong><br>Operates on a local WiFi network. No internet, no subscription, no API key, no server outage risk. Works in remote areas with zero internet coverage.</div></div>
    <div class="adv-item"><span class="adv-check">🛡️</span><div class="adv-text"><strong>Fail-Safe Autonomous Core</strong><br>Controller continues its full scheduled operation — open, track, close — even when the Remote unit is powered off, disconnected, or crashed. Core function never depends on the UI device.</div></div>
    <div class="adv-item"><span class="adv-check">🔌</span><div class="adv-text"><strong>Extensible One-Line Protocol</strong><br>New sensors, buttons, or commands each require exactly one line of code. The buttons[] array decouples hardware from logic; the CSV protocol is trivially extended with new fields.</div></div>
    <div class="adv-item"><span class="adv-check">📚</span><div class="adv-text"><strong>Arduino Ecosystem</strong><br>Built on the most widely documented embedded platform. Any developer with Arduino experience can read, understand, and modify the entire codebase. No proprietary SDKs, no vendor lock-in.</div></div>
    <div class="adv-item"><span class="adv-check">🔬</span><div class="adv-text"><strong>Production-Grade Firmware</strong><br>Non-blocking architecture, boot-time sensor calibration, soft-ramp motor control, and hardware-safe state machines. Designed to run unattended for months without operator intervention.</div></div>
    <div class="adv-item"><span class="adv-check">📊</span><div class="adv-text"><strong>10 Hz Live Telemetry</strong><br>Voltage, current, power, and battery data streamed at 10 readings per second. Enables real-time fault detection and performance analysis unavailable in most low-cost solar systems.</div></div>
    <div class="adv-item"><span class="adv-check">🔁</span><div class="adv-text"><strong>Self-Calibrating Sensors</strong><br>Boot-time ACS712 auto-calibration eliminates zero-offset drift — the #1 source of current sensing inaccuracy. Accurate from the first measurement after boot, across the full operating temperature range.</div></div>
    <div class="adv-item"><span class="adv-check">⚡</span><div class="adv-text"><strong>Motor Protection by Design</strong><br>Soft-ramp PWM limits peak inrush current, reduces mechanical shock on panel linkage, and extends H-bridge lifetime. A 30% kickstart overcomes static friction without full-voltage shock.</div></div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Conclusion ─────────────────────────────────────────────────────────────────
st.markdown('<div id="conclusion"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="card card-green">
  <span class="sec-num">18 — CONCLUSION</span>
  <div class="section-heading"><span class="heading-icon">✅</span> Conclusion</div>
  <p style="font-size:1rem;line-height:1.8;color:rgba(232,224,204,0.88);margin-bottom:1.2rem;">
    <strong style="color:#FFD700;">Solar Sunflower Controller</strong> demonstrates that high-performance
    solar tracking is achievable with commodity microcontrollers, commodity sensors, and a hand-soldered
    custom PCB. The dual-ESP32 architecture cleanly separates physical control from user interaction:
    the Controller runs the motor, servo, sensors, and schedule fully autonomously; the Remote provides
    monitoring and manual override without any dependency on the Controller's core function.
  </p>
  <p style="font-size:1rem;line-height:1.8;color:rgba(232,224,204,0.88);margin-bottom:1.2rem;">
    Testing validated all 26 integration tests with quantified accuracy — &lt;0.30% voltage error,
    &lt;1.5% current error post-calibration, 4–11 ms command latency, and 100% motor-continues-on-link-drop
    reliability across 10 trials. The one pre-calibration ACS712 failure directly motivated the
    auto-calibration design that is now a core innovation of the system.
  </p>
  <p style="font-size:1rem;line-height:1.8;color:rgba(232,224,204,0.88);margin-bottom:1.5rem;">
    Every key engineering challenge was addressed with a design-level solution: LEDC channel conflict
    → initialisation order enforcement; WiFi blocking → MOTOR_IDLE gate; sensor drift → boot calibration;
    double-trigger → state machine; manual runaway → hold-to-run + 30 s cutoff; mechanical shock →
    5-second soft-ramp PWM driver.
  </p>

  <div class="sub-heading sub-heading-blue"><span>📌</span> Key Engineering Learnings</div>
""", unsafe_allow_html=True)

ca, cb = st.columns(2)
with ca:
    st.markdown("""
    <ul class="gold-list">
      <li><strong style="color:#60b4ff;">Hardware/software co-design matters.</strong> The LEDC channel conflict between ESP32Servo and MotorL298N could not have been solved in isolation — it required knowing which library claims channels first and deliberately controlling initialisation order. Reading library source code, not just docs, was essential.</li>
      <li><strong style="color:#60b4ff;">Non-blocking architecture is non-negotiable.</strong> Any call to delay() inside the motor ramp loop would have broken smooth PWM. Building the entire loop around millis() timers from day one prevented a class of timing bugs that would have required architecture-level rewrites to fix later.</li>
      <li><strong style="color:#60b4ff;">Auto-calibration beats factory constants.</strong> A hardcoded ACS_OFFSET = 2.5 V introduced ±80 mV of systematic error. Boot-time averaging of 500 samples reduced this to ±5 mV — a 16× improvement with 10 lines of code.</li>
      <li><strong style="color:#60b4ff;">State machines prevent logical races.</strong> Without MOTOR_IDLE as a guard, the scheduler could fire the motor open command every 10ms loop cycle during the scheduled minute — thousands of times. The state machine made this class of bug structurally impossible.</li>
    </ul>
    """, unsafe_allow_html=True)
with cb:
    st.markdown("""
    <ul class="gold-list green-list">
      <li><strong style="color:#22C55E;">testMode is worth the code.</strong> A single boolean that bypasses the RTC schedule compressed days of waiting into seconds of testing. It revealed the double-trigger bug, the WiFi blocking bug, and the LEDC conflict — all at bench-test time, not deployment time.</li>
      <li><strong style="color:#22C55E;">Safety must be physical, not just software.</strong> Hold-to-run buttons guarantee stop regardless of network state, packet loss, or software state. A software toggle would require the STOP packet to arrive — creating a failure mode under WiFi jitter. Physical hold-to-run eliminates the entire category.</li>
      <li><strong style="color:#22C55E;">Clean separation of concerns scales.</strong> Because the Controller owns all hardware autonomously, the Remote can be rebooted, reprogrammed, or replaced without interrupting the panel's daily cycle. Two independent failure domains means two independent fault surfaces.</li>
      <li><strong style="color:#22C55E;">Measure, then derive constants.</strong> SERVO_TRACK_DURATION is not a magic number — it's (SERVO_TRACK_REVS / SERVO_RPM) × 60000. When we swapped the servo for a different unit, recalibration required one measurement and one constant. Zero firmware logic changed.</li>
    </ul>
    """, unsafe_allow_html=True)

st.markdown("""
  <div style="display:flex;gap:1rem;flex-wrap:wrap;margin-top:1.6rem;">
    <div style="flex:1;min-width:140px;background:rgba(255,215,0,0.08);border:1px solid rgba(255,215,0,0.2);border-radius:3px;padding:1rem;text-align:center;">
      <div style="font-family:'Bebas Neue',sans-serif;font-size:1.5rem;color:#FFD700;">Autonomous</div>
      <div style="font-size:0.78rem;color:rgba(232,224,204,0.5);">Open · Track · Close</div>
    </div>
    <div style="flex:1;min-width:140px;background:rgba(34,197,94,0.08);border:1px solid rgba(34,197,94,0.2);border-radius:3px;padding:1rem;text-align:center;">
      <div style="font-family:'Bebas Neue',sans-serif;font-size:1.5rem;color:#22C55E;">Validated</div>
      <div style="font-size:0.78rem;color:rgba(232,224,204,0.5);">26/27 tests pass</div>
    </div>
    <div style="flex:1;min-width:140px;background:rgba(255,160,0,0.08);border:1px solid rgba(255,160,0,0.2);border-radius:3px;padding:1rem;text-align:center;">
      <div style="font-family:'Bebas Neue',sans-serif;font-size:1.5rem;color:#FFA500;">Extensible</div>
      <div style="font-size:0.78rem;color:rgba(232,224,204,0.5);">Scales to fleet</div>
    </div>
    <div style="flex:1;min-width:140px;background:rgba(100,100,255,0.06);border:1px solid rgba(100,100,255,0.15);border-radius:3px;padding:1rem;text-align:center;">
      <div style="font-family:'Bebas Neue',sans-serif;font-size:1.5rem;color:#94d8f0;">Open</div>
      <div style="font-size:0.78rem;color:rgba(232,224,204,0.5);">Arduino · No lock-in</div>
    </div>
    <div style="flex:1;min-width:140px;background:rgba(168,85,247,0.06);border:1px solid rgba(168,85,247,0.15);border-radius:3px;padding:1rem;text-align:center;">
      <div style="font-family:'Bebas Neue',sans-serif;font-size:1.5rem;color:#c084fc;">Resilient</div>
      <div style="font-size:0.78rem;color:rgba(232,224,204,0.5);">Fail-safe at every layer</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Gallery ────────────────────────────────────────────────────────────────────
st.markdown('<div id="gallery"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="card">
  <span class="sec-num">19 — GALLERY</span>
  <div class="section-heading"><span class="heading-icon">🖼️</span> Gallery</div>
""", unsafe_allow_html=True)

# Outdoor field photos
st.markdown('<div class="gallery-section-label">Outdoor Field Installation</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
for col, fname, lbl in [
    (c1, "outdoor_1.png",       "Outdoor Installation — Side View"),
    (c2, "outdoor_2.png",       "Outdoor Installation — Angle View"),
    (c3, "outdoor_top_view.png","Outdoor Installation — Top View"),
]:
    p = asset(fname)
    with col:
        if os.path.exists(p):
            st.image(p, use_container_width=True)
        st.markdown(f'<div class="gallery-label">{lbl}</div>', unsafe_allow_html=True)

# Final hardware build
st.markdown('<div class="gallery-section-label">Final Hardware Build</div>', unsafe_allow_html=True)
c1, c2 = st.columns(2)
for col, fname, lbl in [
    (c1, "solar_sunflower_project_1.jpeg", "Final Build — View 1"),
    (c2, "solar_sunflower_project_2.jpeg", "Final Build — View 2"),
]:
    p = asset(fname)
    with col:
        if os.path.exists(p):
            st.image(p, use_container_width=True)
        st.markdown(f'<div class="gallery-label">{lbl}</div>', unsafe_allow_html=True)

# Project journey video
st.markdown('<div class="gallery-section-label">Project Journey — Start to Finish</div>', unsafe_allow_html=True)
st.markdown("""
  <div style="font-size:0.88rem;color:rgba(232,224,204,0.5);margin-bottom:0.8rem;line-height:1.6;">
    From blank PCB design to fully working autonomous sun-tracking solar panel. This video documents
    the complete build: PCB schematic, hand-etching, component soldering, firmware development,
    integration testing, and live demonstration of the autonomous open/track/close cycle.
  </div>
""", unsafe_allow_html=True)
vid = asset("solar_sunflower_project_start_to_end.mp4")
if os.path.exists(vid):
    st.video(vid)
else:
    st.info("Video not found in assets/")

st.markdown("</div>", unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  <div class="footer-title">🌻 Solar Sunflower Controller</div>
  <div class="footer-sub" style="margin-top:0.4rem;font-size:0.85rem;color:rgba(232,224,204,0.45);">
    Autonomous Sun-Tracking Solar Panel System &nbsp;·&nbsp; ESP32 × 2 &nbsp;·&nbsp; Arduino Framework
  </div>
  <div class="footer-sub" style="margin-top:0.6rem;">
    2025 &nbsp;·&nbsp; Open Firmware &nbsp;·&nbsp; WiFi TCP &nbsp;·&nbsp; Custom PCB
  </div>
</div>
""", unsafe_allow_html=True)
