import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import plotly.graph_objects as go

# ══════════════════════════════════════════════════════════════════════════
#  1. PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="MarketSense · Global Tech Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════════════════
#  2. CONSTANTS
# ══════════════════════════════════════════════════════════════════════════
COUNTRY_MAP = {
    "at": "Austria",    "au": "Australia",   "be": "Belgium",
    "br": "Brazil",     "ca": "Canada",      "ch": "Switzerland",
    "de": "Germany",    "es": "Spain",       "fr": "France",
    "gb": "United Kingdom", "in": "India",   "it": "Italy",
    "mx": "Mexico",     "nl": "Netherlands", "nz": "New Zealand",
    "pl": "Poland",     "sg": "Singapore",   "us": "United States",
    "za": "South Africa",
}
COUNTRY_FLAGS = {
    "us": "🇺🇸", "gb": "🇬🇧", "in": "🇮🇳", "au": "🇦🇺", "ca": "🇨🇦",
    "de": "🇩🇪", "fr": "🇫🇷", "sg": "🇸🇬", "nl": "🇳🇱", "ch": "🇨🇭",
    "br": "🇧🇷", "pl": "🇵🇱", "es": "🇪🇸", "nz": "🇳🇿", "za": "🇿🇦",
    "it": "🇮🇹", "at": "🇦🇹", "be": "🇧🇪", "mx": "🇲🇽",
}
TECH_ROLES = [
    "Data Engineer", "Data Scientist", "Data Analyst",
    "Software Engineer", "Machine Learning Engineer", "DevOps Engineer",
]
SKILL_KEYWORDS = [
    "Python", "SQL", "AWS", "Azure", "Docker",
    "Kubernetes", "Spark", "React", "Tableau", "Snowflake", "Java",
]

# ══════════════════════════════════════════════════════════════════════════
#  3. DESIGN SYSTEM — Dark Intelligence Terminal
# ══════════════════════════════════════════════════════════════════════════
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600&display=swap');

/* ── Root tokens ─────────────────────────────────────────────────── */
:root {
    --bg-deep:    #070B14;
    --bg-surface: #0D1321;
    --bg-card:    #111827;
    --bg-raised:  #1A2236;
    --border:     rgba(99,102,241,0.18);
    --border-dim: rgba(255,255,255,0.07);
    --indigo:     #6366F1;
    --violet:     #8B5CF6;
    --cyan:       #22D3EE;
    --emerald:    #10B981;
    --amber:      #F59E0B;
    --rose:       #F43F5E;
    --text-primary:   #F1F5F9;
    --text-secondary: #94A3B8;
    --text-muted:     #475569;
    --glow-indigo: 0 0 40px rgba(99,102,241,0.25);
    --glow-violet: 0 0 40px rgba(139,92,246,0.2);
}

/* ── Global reset ────────────────────────────────────────────────── */
html, body, [class*="css"], [class*="st-"], .stMarkdown, p, h1, h2, h3, li, span {
    font-family: 'DM Sans', sans-serif !important;
    color: var(--text-primary);
}

/* ── App background ──────────────────────────────────────────────── */
.stApp {
    background:
        radial-gradient(ellipse 80% 50% at 10% -10%, rgba(99,102,241,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 90% 110%, rgba(139,92,246,0.1) 0%, transparent 60%),
        var(--bg-deep);
    min-height: 100vh;
}

/* ── Hide sidebar toggle ─────────────────────────────────────────── */
[data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none; }

/* ── Main content padding ────────────────────────────────────────── */
.main .block-container { padding: 0 3rem 4rem 3rem; max-width: 1600px; }

/* ══════════════════════════════════════════════════════════════════
   HERO HEADER
══════════════════════════════════════════════════════════════════ */
.hero-wrap {
    position: relative;
    width: 100%;
    display: block;
    padding: 56px 0 44px;
    text-align: center;
    overflow: hidden;
}
.hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(99,102,241,0.12);
    border: 1px solid rgba(99,102,241,0.28);
    border-radius: 99px;
    padding: 6px 18px;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #818CF8;
    margin-bottom: 24px;
}
.hero-eyebrow .dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--emerald);
    box-shadow: 0 0 8px var(--emerald);
    animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.5; transform: scale(0.7); }
}
.hero-title {
    font-family: 'Syne', sans-serif !important;
    font-size: 5.5rem;
    font-weight: 800;
    letter-spacing: -4px;
    line-height: 0.95;
    margin: 0 0 20px 0;
    background: linear-gradient(135deg, #E2E8F0 0%, #818CF8 50%, #C4B5FD 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 1rem;
    color: var(--text-secondary);
    letter-spacing: 0.3px;
    font-weight: 400;
    max-width: 500px;
    margin: 0 auto;
    line-height: 1.65;
}
/* Decorative grid lines */
.hero-wrap::before {
    content: '';
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(rgba(99,102,241,0.06) 1px, transparent 1px),
        linear-gradient(90deg, rgba(99,102,241,0.06) 1px, transparent 1px);
    background-size: 48px 48px;
    mask-image: radial-gradient(ellipse 70% 60% at 50% 50%, black, transparent);
    pointer-events: none;
}

/* ══════════════════════════════════════════════════════════════════
   DIVIDER
══════════════════════════════════════════════════════════════════ */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 0 0 32px;
}

/* ══════════════════════════════════════════════════════════════════
   FILTER PANEL
══════════════════════════════════════════════════════════════════ */
.filter-header {
    font-family: 'Syne', sans-serif !important;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--indigo);
    margin-bottom: 18px;
}
.filter-panel {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 28px 36px 22px;
    margin-bottom: 32px;
    box-shadow: var(--glow-indigo), inset 0 1px 0 rgba(255,255,255,0.04);
    position: relative;
    overflow: hidden;
}
.filter-panel::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--indigo), var(--violet), var(--cyan));
    border-radius: 20px 20px 0 0;
}

/* Streamlit widget overrides for dark theme */
[data-testid="stMultiSelect"] > div,
[data-testid="stSelectbox"] > div {
    background: var(--bg-raised) !important;
    border: 1px solid var(--border-dim) !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
}
[data-testid="stMultiSelect"] [data-baseweb="tag"] {
    background: rgba(99,102,241,0.25) !important;
    border: 1px solid rgba(99,102,241,0.4) !important;
    border-radius: 6px !important;
    color: #A5B4FC !important;
}
[data-testid="stRadio"] label { color: var(--text-secondary) !important; }
[data-testid="stRadio"] [data-testid="stMarkdownContainer"] p {
    color: var(--text-secondary) !important;
    font-size: 0.85rem !important;
}
/* Labels */
[data-testid="stMultiSelect"] label,
[data-testid="stSelectbox"] label,
[data-testid="stRadio"] > label {
    color: var(--text-muted) !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
}

/* ── Dropdown popover / listbox (fixes white-on-white) ───────────── */
[data-baseweb="popover"],
[data-baseweb="popover"] > div,
[data-baseweb="menu"],
ul[data-baseweb="menu"] {
    background: #1A2236 !important;
    border: 1px solid rgba(99,102,241,0.25) !important;
    border-radius: 12px !important;
    box-shadow: 0 12px 40px rgba(0,0,0,0.5) !important;
}
[role="option"],
li[role="option"],
[data-baseweb="menu"] li,
[data-baseweb="select"] li {
    background: transparent !important;
    color: #94A3B8 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.85rem !important;
}
[role="option"]:hover,
li[role="option"]:hover,
[data-baseweb="menu"] li:hover {
    background: rgba(99,102,241,0.15) !important;
    color: #F1F5F9 !important;
}
[aria-selected="true"][role="option"] {
    background: rgba(99,102,241,0.22) !important;
    color: #A5B4FC !important;
}
[data-baseweb="select"] input {
    color: #F1F5F9 !important;
    caret-color: #6366F1 !important;
}
[data-testid="stSelectbox"] [data-baseweb="select"] span {
    color: #F1F5F9 !important;
}
[data-baseweb="menu"]::-webkit-scrollbar { width: 4px; }
[data-baseweb="menu"]::-webkit-scrollbar-thumb {
    background: rgba(99,102,241,0.35);
    border-radius: 99px;
}
/* ── DEEP portal overrides: target every nested div/li inside popover ── */
[data-baseweb="popover"] [data-baseweb="block"],
[data-baseweb="popover"] [data-baseweb="block"] > div,
[data-baseweb="popover"] ul,
[data-baseweb="popover"] li {
    background-color: #1A2236 !important;
    color: #94A3B8 !important;
}
[data-baseweb="popover"] li:hover,
[data-baseweb="popover"] li[aria-selected="true"] {
    background-color: rgba(99,102,241,0.2) !important;
    color: #E2E8F0 !important;
}
/* Override any inline style="background: white" Streamlit injects */
[data-baseweb="popover"] * { color: #94A3B8; }
[data-baseweb="popover"] [role="option"] { background: #1A2236 !important; }
[data-baseweb="popover"] [role="option"]:hover { background: rgba(99,102,241,0.18) !important; color: #F1F5F9 !important; }

/* Generate Button */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%) !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    color: white !important;
    height: 3em !important;
    padding: 0 32px !important;
    margin-top: 24px !important;
    box-shadow: 0 4px 20px rgba(99,102,241,0.45) !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(99,102,241,0.6) !important;
}

/* ══════════════════════════════════════════════════════════════════
   KPI STRIP
══════════════════════════════════════════════════════════════════ */
.kpi-strip { display: flex; gap: 16px; margin-bottom: 28px; }

.kpi-card {
    flex: 1;
    background: var(--bg-card);
    border: 1px solid var(--border-dim);
    border-radius: 16px;
    padding: 22px 24px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.25s, transform 0.25s;
}
.kpi-card:hover {
    border-color: var(--border);
    transform: translateY(-3px);
}
.kpi-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
    border-radius: 0 0 16px 16px;
}
.kpi-indigo::after  { background: var(--indigo); }
.kpi-violet::after  { background: var(--violet); }
.kpi-cyan::after    { background: var(--cyan); }
.kpi-emerald::after { background: var(--emerald); }

.kpi-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 10px;
}
.kpi-value {
    font-family: 'Syne', sans-serif !important;
    font-size: 2.1rem;
    font-weight: 700;
    line-height: 1;
    color: var(--text-primary);
    letter-spacing: -1px;
}
.kpi-sub {
    font-size: 0.75rem;
    color: var(--text-muted);
    margin-top: 8px;
    font-weight: 400;
}
.kpi-icon {
    position: absolute;
    top: 20px; right: 20px;
    font-size: 1.4rem;
    opacity: 0.3;
}

/* ══════════════════════════════════════════════════════════════════
   TABS
══════════════════════════════════════════════════════════════════ */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-dim) !important;
    border-radius: 14px !important;
    padding: 6px !important;
    gap: 4px !important;
    margin-bottom: 28px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 10px !important;
    color: var(--text-secondary) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    padding: 10px 24px !important;
    border: none !important;
    transition: all 0.2s !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(99,102,241,0.25), rgba(139,92,246,0.15)) !important;
    color: #A5B4FC !important;
    border: 1px solid rgba(99,102,241,0.3) !important;
    font-weight: 600 !important;
}
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }
.stTabs [data-baseweb="tab-border"]    { display: none !important; }

/* ══════════════════════════════════════════════════════════════════
   REPORT CARDS
══════════════════════════════════════════════════════════════════ */
.report-card {
    background: var(--bg-card);
    border: 1px solid var(--border-dim);
    border-radius: 20px;
    padding: 32px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.25s;
}
.report-card:hover { border-color: var(--border); }
.report-card-accent {
    position: absolute;
    top: 0; left: 0;
    width: 4px;
    height: 100%;
    border-radius: 20px 0 0 20px;
    background: linear-gradient(180deg, var(--indigo), var(--violet));
}
.report-badge {
    display: inline-block;
    background: rgba(99,102,241,0.15);
    border: 1px solid rgba(99,102,241,0.25);
    color: #818CF8;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 99px;
    margin-bottom: 10px;
}
.report-title {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.35rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0 0 6px;
    letter-spacing: -0.5px;
}
.report-desc {
    font-size: 0.82rem;
    color: var(--text-muted);
    margin: 0 0 24px;
    line-height: 1.6;
}

/* ══════════════════════════════════════════════════════════════════
   NARRATIVE BOX
══════════════════════════════════════════════════════════════════ */
.narrative-box {
    background: rgba(99,102,241,0.07);
    border: 1px solid rgba(99,102,241,0.15);
    border-left: 3px solid var(--indigo);
    border-radius: 0 12px 12px 0;
    padding: 14px 20px;
    font-size: 0.82rem;
    color: var(--text-secondary);
    line-height: 1.65;
    margin-top: 16px;
}

/* ══════════════════════════════════════════════════════════════════
   JOB EXPLORER
══════════════════════════════════════════════════════════════════ */
.explorer-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
}
.explorer-count {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--text-muted);
}
.explorer-count span {
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.5px;
    margin-right: 6px;
}

/* Job card */
.job-card {
    background: var(--bg-card);
    border: 1px solid var(--border-dim);
    border-radius: 16px;
    padding: 22px 28px;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 24px;
    transition: all 0.22s ease;
    position: relative;
    overflow: hidden;
}
.job-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    background: linear-gradient(180deg, var(--indigo), var(--violet));
    opacity: 0;
    transition: opacity 0.22s;
}
.job-card:hover {
    border-color: rgba(99,102,241,0.35);
    background: var(--bg-raised);
    transform: translateX(4px);
    box-shadow: var(--glow-indigo);
}
.job-card:hover::before { opacity: 1; }

.job-logo {
    width: 52px; height: 52px;
    border-radius: 14px;
    background: var(--bg-raised);
    border: 1px solid var(--border-dim);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.3rem;
    flex-shrink: 0;
}
.job-info { flex: 1; min-width: 0; }
.job-title {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0 0 5px;
    letter-spacing: -0.3px;
}
.job-meta {
    font-size: 0.8rem;
    color: var(--indigo);
    font-weight: 500;
    margin: 0 0 4px;
}
.job-location { font-size: 0.78rem; color: var(--text-muted); }

.salary-pill {
    background: rgba(16,185,129,0.1);
    border: 1px solid rgba(16,185,129,0.2);
    border-radius: 10px;
    padding: 10px 18px;
    text-align: center;
    flex-shrink: 0;
}
.salary-label { font-size: 0.6rem; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: var(--emerald); opacity: 0.7; }
.salary-value { font-family: 'Syne', sans-serif; font-size: 0.9rem; font-weight: 700; color: var(--emerald); white-space: nowrap; }

.apply-link {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: linear-gradient(135deg, #6366F1, #8B5CF6);
    color: white !important;
    padding: 10px 22px;
    border-radius: 11px;
    text-decoration: none !important;
    font-family: 'DM Sans', sans-serif;
    font-weight: 600;
    font-size: 0.8rem;
    letter-spacing: 0.3px;
    box-shadow: 0 4px 16px rgba(99,102,241,0.4);
    flex-shrink: 0;
    transition: all 0.2s;
    white-space: nowrap;
}
.apply-link:hover {
    box-shadow: 0 6px 24px rgba(99,102,241,0.6);
    transform: translateY(-1px);
}

/* No-salary variant */
.salary-na {
    background: rgba(71,85,105,0.2);
    border: 1px solid var(--border-dim);
}
.salary-na .salary-label, .salary-na .salary-value { color: var(--text-muted); }

/* ══════════════════════════════════════════════════════════════════
   EMPTY / ERROR STATES
══════════════════════════════════════════════════════════════════ */
.empty-state {
    text-align: center;
    padding: 80px 40px;
    color: var(--text-muted);
}
.empty-state .icon { font-size: 3rem; margin-bottom: 16px; opacity: 0.4; }
.empty-state h3 {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text-secondary);
    margin-bottom: 8px;
}

/* ══════════════════════════════════════════════════════════════════
   FOOTER
══════════════════════════════════════════════════════════════════ */
.footer {
    text-align: center;
    padding: 40px 0 20px;
    font-size: 0.72rem;
    color: var(--text-muted);
    border-top: 1px solid var(--border-dim);
    margin-top: 48px;
    letter-spacing: 0.5px;
}

/* ── Misc. Streamlit chrome ─────────────────────────────────────── */
[data-testid="stVerticalBlock"] > div { gap: 0 !important; }
.stSpinner > div { border-top-color: var(--indigo) !important; }
[data-testid="stExpander"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-dim) !important;
    border-radius: 12px !important;
}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
#  4. PLOTLY DARK THEME (shared across all charts)
# ══════════════════════════════════════════════════════════════════════════
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color="#94A3B8"),
    margin=dict(t=20, b=20, l=10, r=10),
    legend=dict(
        bgcolor="rgba(17,24,39,0.7)",
        bordercolor="rgba(99,102,241,0.2)",
        borderwidth=1,
        font=dict(color="#94A3B8"),
    ),
)
PLOTLY_AXIS = dict(
    gridcolor="rgba(255,255,255,0.04)",
    linecolor="rgba(255,255,255,0.06)",
    zerolinecolor="rgba(255,255,255,0.06)",
    tickfont=dict(color="#475569", size=11),
    title_font=dict(color="#475569"),
)
CHART_COLORS = ["#6366F1", "#8B5CF6", "#22D3EE", "#10B981", "#F59E0B", "#F43F5E",
                "#A78BFA", "#34D399", "#60A5FA", "#FB923C", "#E879F9"]


# ══════════════════════════════════════════════════════════════════════════
#  5. DATA LAYER
#  ↓ Swap the try-block with your real Supabase / SQLAlchemy call.
# ══════════════════════════════════════════════════════════════════════════
@st.cache_data(ttl=3600)
def load_data() -> pd.DataFrame:
    try:
        engine = create_engine(st.secrets["DATABASE_URL"])
        df = pd.read_sql("SELECT * FROM tech_jobs", engine)
        df["salary_min"] = pd.to_numeric(df["salary_min"], errors="coerce").fillna(0)
        df["salary_max"] = pd.to_numeric(df["salary_max"], errors="coerce").fillna(0)
        df["country_code"] = df["country"].str.lower()
        df["country_name"] = df["country_code"].map(COUNTRY_MAP).fillna(df["country_code"].str.upper())
        df["avg_salary"] = (df["salary_min"] + df["salary_max"]) / 2
        return df
    except Exception:
        return pd.DataFrame()


raw_df = load_data()

# ══════════════════════════════════════════════════════════════════════════
#  6. HERO HEADER
# ══════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-wrap">
    <div style="display:block; width:100%; text-align:center;">
        <div class="hero-eyebrow" style="display:inline-flex;">
            <div class="dot"></div>
            Live Intelligence · 19 Markets
        </div>
        <h1 class="hero-title" style="display:block;">MarketSense</h1>
        <p class="hero-sub" style="display:block; margin-left:auto; margin-right:auto;">
            Real-time salary benchmarks, skill demand signals, and job discovery
            across the global technology market.
        </p>
    </div>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════
#  7. MAIN APP FLOW
# ══════════════════════════════════════════════════════════════════════════
if "triggered" not in st.session_state:
    st.session_state.triggered = False

if raw_df.empty:
    st.markdown("""
    <div class="empty-state">
        <div class="icon">⚡</div>
        <h3>Engine Disconnected</h3>
        <p>Unable to reach the database. Check your DATABASE_URL secret and retry.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── FILTER PANEL ──────────────────────────────────────────────────────────
st.markdown('<div class="filter-panel"><div class="filter-header">◈ Intelligence Parameters</div>', unsafe_allow_html=True)

col_region, col_role, col_cur, col_btn = st.columns([3, 2, 1, 1.2])

with col_region:
    all_countries = sorted(raw_df["country_name"].unique().tolist())
    sel_regions = st.multiselect(
        "Target Regions",
        options=all_countries,
        default=all_countries[:3],
        placeholder="Select one or more regions…",
    )

with col_role:
    sel_role = st.selectbox(
        "Role Filter",
        options=["All Tech Roles"] + TECH_ROLES,
    )

with col_cur:
    sel_currency = st.radio("Currency", ["USD", "INR"], horizontal=False)
    rate = 83.5 if sel_currency == "INR" else 1.0
    cur_symbol = "₹" if sel_currency == "INR" else "$"

with col_btn:
    if st.button("Generate Report", type="primary"):
        st.session_state.triggered = True

st.markdown("</div>", unsafe_allow_html=True)

# ── FILTERED DATA ─────────────────────────────────────────────────────────
if not st.session_state.triggered:
    st.markdown("""
    <div class="empty-state" style="padding:60px 40px;">
        <div class="icon" style="font-size:2.5rem; opacity:0.25;">◈</div>
        <h3 style="color:#475569;">Configure Parameters Above</h3>
        <p style="font-size:0.82rem;">Select regions, a role filter, and click Generate Report to run analysis.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

res_df = raw_df[raw_df["country_name"].isin(sel_regions)].copy()
if sel_role != "All Tech Roles":
    res_df = res_df[res_df["title"].str.contains(sel_role, case=False, na=False)]

sal_df = res_df[res_df["salary_min"] > 0].copy()
sal_df["salary_min_c"] = sal_df["salary_min"] * rate
sal_df["salary_max_c"] = sal_df["salary_max"] * rate
sal_df["avg_salary_c"] = (sal_df["salary_min_c"] + sal_df["salary_max_c"]) / 2


# ── KPI STRIP ─────────────────────────────────────────────────────────────
total_jobs   = len(res_df)
avg_sal      = sal_df["avg_salary_c"].mean() if not sal_df.empty else 0
top_country  = res_df["country_name"].value_counts().idxmax() if not res_df.empty else "—"
top_company  = res_df["company"].value_counts().idxmax() if not res_df.empty else "—"

def fmt_salary(v):
    if sel_currency == "INR":
        if v >= 1e7: return f"₹{v/1e7:.1f}Cr"
        if v >= 1e5: return f"₹{v/1e5:.1f}L"
        return f"₹{v:,.0f}"
    return f"${v/1000:.0f}K" if v >= 1000 else f"${v:,.0f}"

st.markdown(f"""
<div class="kpi-strip">
    <div class="kpi-card kpi-indigo">
        <div class="kpi-label">Total Roles</div>
        <div class="kpi-value">{total_jobs:,}</div>
        <div class="kpi-sub">across {res_df['country_name'].nunique()} markets</div>
        <div class="kpi-icon">💼</div>
    </div>
    <div class="kpi-card kpi-violet">
        <div class="kpi-label">Avg. Benchmark Salary</div>
        <div class="kpi-value">{fmt_salary(avg_sal) if avg_sal else "N/A"}</div>
        <div class="kpi-sub">midpoint across {len(sal_df)} disclosed roles</div>
        <div class="kpi-icon">📈</div>
    </div>
    <div class="kpi-card kpi-cyan">
        <div class="kpi-label">Top Hiring Market</div>
        <div class="kpi-value">{top_country}</div>
        <div class="kpi-sub">{res_df['country_name'].value_counts().iloc[0] if not res_df.empty else 0} open positions</div>
        <div class="kpi-icon">🌍</div>
    </div>
    <div class="kpi-card kpi-emerald">
        <div class="kpi-label">Most Active Employer</div>
        <div class="kpi-value" style="font-size:1.4rem; letter-spacing:-0.5px;">{top_company}</div>
        <div class="kpi-sub">{res_df['company'].value_counts().iloc[0] if not res_df.empty else 0} listings</div>
        <div class="kpi-icon">🏢</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
#  8. TABS
# ══════════════════════════════════════════════════════════════════════════
tab1, tab2 = st.tabs(["  📊  Market Analysis  ", "  🔍  Live Job Explorer  "])


# ─────────────────────────────────────────────────────────────────────────
#  TAB 1: MARKET ANALYSIS
# ─────────────────────────────────────────────────────────────────────────
with tab1:

    # ── REPORT 1: Salary Distribution ────────────────────────────────────
    st.markdown("""
    <div class="report-card">
        <div class="report-card-accent"></div>
        <div class="report-badge">REPORT 01</div>
        <div class="report-title">Regional Salary Variance</div>
        <div class="report-desc">Statistical distribution of base salary floors across selected geographies, revealing market-specific compensation norms.</div>
    """, unsafe_allow_html=True)

    if not sal_df.empty:
        fig1 = px.box(
            sal_df, x="country_name", y="salary_min_c",
            color="country_name",
            color_discrete_sequence=CHART_COLORS,
            labels={"salary_min_c": f"Base Salary ({sel_currency})", "country_name": ""},
        )
        fig1.update_traces(
            hovertemplate="<b>%{x}</b><br>Salary: " + cur_symbol + "%{y:,.0f}<extra></extra>",
            marker_size=4, line_width=1.5,
        )
        fig1.update_layout(**PLOTLY_LAYOUT, height=320, showlegend=False)
        fig1.update_xaxes(**PLOTLY_AXIS, tickangle=-20)
        fig1.update_yaxes(**PLOTLY_AXIS)
        st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})
        st.markdown(f"""<div class="narrative-box">Median baseline compensation ranges from <strong>{fmt_salary(sal_df['salary_min_c'].min())}</strong> to <strong>{fmt_salary(sal_df['salary_min_c'].max())}</strong> across the selected markets, a variance that reflects cost-of-living differentials, local talent scarcity, and employer compensation strategy.</div>""", unsafe_allow_html=True)
    else:
        st.markdown('<div class="empty-state"><div class="icon">📊</div><h3>No salary data for this selection</h3></div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ── REPORT 2 + 3 side by side ────────────────────────────────────────
    col_a, col_b = st.columns(2, gap="medium")

    with col_a:
        st.markdown("""
        <div class="report-card" style="height:100%;">
            <div class="report-card-accent"></div>
            <div class="report-badge">REPORT 02</div>
            <div class="report-title">Global Hub Market Share</div>
            <div class="report-desc">Vacancy density across regions — identifying where talent demand is most concentrated.</div>
        """, unsafe_allow_html=True)

        country_counts = res_df["country_name"].value_counts().reset_index()
        country_counts.columns = ["Country", "Jobs"]
        fig2 = go.Figure(go.Pie(
            labels=country_counts["Country"],
            values=country_counts["Jobs"],
            hole=0.6,
            marker=dict(colors=CHART_COLORS, line=dict(color="#070B14", width=2)),
            hovertemplate="<b>%{label}</b><br>%{value} roles · %{percent}<extra></extra>",
            textinfo="none",
        ))
        fig2.add_annotation(
            text=f"<b>{total_jobs}</b><br><span style='font-size:10px'>Total</span>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=20, color="#E2E8F0", family="Syne"),
        )
        _layout_no_legend = {k: v for k, v in PLOTLY_LAYOUT.items() if k != "legend"}
        fig2.update_layout(**_layout_no_legend, height=290,
                           legend=dict(**PLOTLY_LAYOUT["legend"], orientation="v", x=1.05))
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
        st.markdown('<div class="narrative-box">Market concentration reveals where hiring activity clusters, informing geographic sourcing and competitive talent acquisition strategy.</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        <div class="report-card" style="height:100%;">
            <div class="report-card-accent"></div>
            <div class="report-badge">REPORT 03</div>
            <div class="report-title">Technical Skill Demand Pulse</div>
            <div class="report-desc">Frequency analysis of skill mentions across all job descriptions, mapping the current demand landscape.</div>
        """, unsafe_allow_html=True)

        all_desc = " ".join(res_df["description"].fillna("").tolist()).lower()
        skill_counts = {s: all_desc.count(s.lower()) for s in SKILL_KEYWORDS}
        skill_df = pd.DataFrame(list(skill_counts.items()), columns=["Skill", "Mentions"]).sort_values("Mentions", ascending=False)

        fig3 = go.Figure()
        fig3.add_trace(go.Scatterpolar(
            r=skill_df["Mentions"],
            theta=skill_df["Skill"],
            fill="toself",
            fillcolor="rgba(99,102,241,0.18)",
            line=dict(color="#6366F1", width=2),
            hovertemplate="<b>%{theta}</b><br>Mentions: %{r}<extra></extra>",
            name="",
        ))
        fig3.update_layout(
            **PLOTLY_LAYOUT, height=290,
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(
                    visible=True,
                    gridcolor="rgba(255,255,255,0.05)",
                    linecolor="rgba(255,255,255,0.05)",
                    tickfont=dict(color="#475569", size=9),
                ),
                angularaxis=dict(
                    gridcolor="rgba(255,255,255,0.05)",
                    linecolor="rgba(255,255,255,0.05)",
                    tickfont=dict(color="#94A3B8", size=11),
                ),
            ),
        )
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

        top_skill = skill_df.iloc[0]["Skill"] if not skill_df.empty else "—"
        st.markdown(f'<div class="narrative-box"><strong>{top_skill}</strong> surfaces as the most-referenced technology across job descriptions, with the radar surface area reflecting relative competitive weight of each skill in the current market.</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── REPORT 4: Avg Salary by Role (bar) ───────────────────────────────
    if not sal_df.empty:
        role_sal = (
            sal_df.groupby("title")["avg_salary_c"]
            .mean()
            .reset_index()
            .rename(columns={"title": "Role", "avg_salary_c": "Avg Salary"})
            .sort_values("Avg Salary", ascending=True)
            .tail(12)
        )
        st.markdown("""
        <div class="report-card">
            <div class="report-card-accent"></div>
            <div class="report-badge">REPORT 04</div>
            <div class="report-title">Compensation Ladder by Role</div>
            <div class="report-desc">Average total compensation benchmark ranked by role title — reveals which positions command the greatest market premium.</div>
        """, unsafe_allow_html=True)

        fig4 = px.bar(
            role_sal, y="Role", x="Avg Salary", orientation="h",
            color="Avg Salary",
            color_continuous_scale=["#4338CA", "#6366F1", "#8B5CF6", "#A78BFA", "#C4B5FD"],
            labels={"Avg Salary": f"Avg. Salary ({sel_currency})", "Role": ""},
        )
        fig4.update_traces(
            hovertemplate="<b>%{y}</b><br>" + cur_symbol + "%{x:,.0f}<extra></extra>",
            marker_line_width=0,
        )
        fig4.update_layout(**PLOTLY_LAYOUT, height=340, coloraxis_showscale=False)
        _axis_no_tick = {k: v for k, v in PLOTLY_AXIS.items() if k != "tickfont"}
        fig4.update_xaxes(**PLOTLY_AXIS)
        fig4.update_yaxes(**_axis_no_tick, tickfont=dict(color="#94A3B8", size=11))
        st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────
#  TAB 2: LIVE JOB EXPLORER
# ─────────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown(f"""
    <div class="explorer-header">
        <div class="explorer-count"><span>{len(res_df):,}</span> Positions Found</div>
    </div>
    """, unsafe_allow_html=True)

    if res_df.empty:
        st.markdown('<div class="empty-state"><div class="icon">🔍</div><h3>No roles match your filters</h3></div>', unsafe_allow_html=True)
    else:
        for _, row in res_df.iterrows():
            flag   = COUNTRY_FLAGS.get(str(row.get("country_code", "")).lower(), "📍")
            co_ini = "".join(w[0] for w in str(row.get("company", "?")).split()[:2]).upper()

            if row["salary_min"] > 0:
                s_min = fmt_salary(row["salary_min"] * rate)
                s_max = fmt_salary(row["salary_max"] * rate)
                salary_html = f"""
                <div class="salary-pill">
                    <div class="salary-label">Benchmark</div>
                    <div class="salary-value">{s_min} — {s_max}</div>
                </div>"""
            else:
                salary_html = """
                <div class="salary-pill salary-na">
                    <div class="salary-label">Salary</div>
                    <div class="salary-value">On Application</div>
                </div>"""

            st.markdown(f"""
            <div class="job-card">
                <div class="job-logo">{flag}</div>
                <div class="job-info">
                    <div class="job-title">{row.get('title','Unknown Role')}</div>
                    <div class="job-meta">{row.get('company','—')}</div>
                    <div class="job-location">{row.get('location','—')} · {row.get('country_name', '')}</div>
                </div>
                {salary_html}
                <a href="{row.get('url','#')}" target="_blank" class="apply-link">
                    Apply Now ↗
                </a>
            </div>
            """, unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    MarketSense · Global Tech Intelligence · Data refreshed every hour via Adzuna ETL pipeline
</div>
""", unsafe_allow_html=True)
