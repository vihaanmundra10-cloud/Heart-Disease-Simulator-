import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import streamlit as st

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Heart Disease Analyzer",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── CUSTOM CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=DM+Serif+Display:ital@0;1&display=swap');

/* ── Reset & Root ── */
*, *::before, *::after { box-sizing: border-box; }

:root {
    --bg:        #0D1117;
    --surface:   #161B22;
    --surface2:  #1E2530;
    --border:    #2A3244;
    --red:       #E53E3E;
    --red-soft:  #FC8181;
    --red-glow:  rgba(229, 62, 62, 0.15);
    --teal:      #2DD4BF;
    --teal-soft: #99F6E4;
    --teal-glow: rgba(45, 212, 191, 0.12);
    --text:      #E2E8F0;
    --muted:     #718096;
    --label:     #A0AEC0;
    --white:     #FFFFFF;
}

/* ── Global App Background ── */
.stApp, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"] { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}

/* ── Main content padding ── */
.main .block-container {
    padding: 2rem 3rem 4rem !important;
    max-width: 1100px !important;
}

/* ── Hero Banner ── */
.hero {
    background: linear-gradient(135deg, #1a0a0a 0%, #0f1a2a 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 3rem 3.5rem;
    margin-bottom: 2.5rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '🫀';
    position: absolute;
    right: 3rem;
    top: 50%;
    transform: translateY(-50%);
    font-size: 7rem;
    opacity: 0.12;
    filter: grayscale(1);
}
.hero-eyebrow {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--teal);
    margin-bottom: 0.75rem;
}
.hero h1 {
    font-family: 'DM Serif Display', serif !important;
    font-size: 2.6rem !important;
    font-weight: 400 !important;
    line-height: 1.15 !important;
    color: var(--white) !important;
    margin: 0 0 1rem !important;
    max-width: 560px;
}
.hero h1 em {
    font-style: italic;
    color: var(--red-soft);
}
.hero-sub {
    font-size: 0.95rem;
    color: var(--label);
    line-height: 1.7;
    max-width: 520px;
}
.hero-meta {
    margin-top: 1.5rem;
    display: flex;
    gap: 2rem;
}
.hero-stat {
    display: flex;
    flex-direction: column;
}
.hero-stat-num {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--teal);
}
.hero-stat-label {
    font-size: 0.7rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.1em;
}
.author-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 100px;
    padding: 0.35rem 1rem;
    font-size: 0.78rem;
    color: var(--label);
    margin-bottom: 2rem;
}
.author-badge span { color: var(--teal); font-weight: 600; }

/* ── Section Headers ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin: 2.5rem 0 1.25rem;
}
.section-header-line {
    flex: 1;
    height: 1px;
    background: var(--border);
}
.section-title {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--muted);
    white-space: nowrap;
}

/* ── Metric Cards ── */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin: 1.25rem 0 2rem;
}
.metric-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    position: relative;
    overflow: hidden;
}
.metric-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 12px 12px 0 0;
}
.metric-card.red::after  { background: var(--red); }
.metric-card.teal::after { background: var(--teal); }
.metric-card.gold::after { background: #F6AD55; }
.metric-label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.5rem;
}
.metric-value {
    font-size: 1.9rem;
    font-weight: 700;
    color: var(--white);
    line-height: 1;
}
.metric-sub {
    font-size: 0.75rem;
    color: var(--muted);
    margin-top: 0.3rem;
}

/* ── Risk Breakdown ── */
.risk-row {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.75rem 0;
    border-bottom: 1px solid var(--border);
}
.risk-row:last-child { border-bottom: none; }
.risk-label { font-size: 0.85rem; color: var(--label); width: 200px; flex-shrink: 0; }
.risk-bar-wrap { flex: 1; background: var(--surface2); border-radius: 4px; height: 8px; }
.risk-bar { height: 8px; border-radius: 4px; }
.risk-pct { font-size: 0.85rem; font-weight: 600; color: var(--text); width: 45px; text-align: right; }

/* ── Data Table ── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}
[data-testid="stDataFrame"] table {
    background: var(--surface) !important;
    color: var(--text) !important;
}
[data-testid="stDataFrame"] th {
    background: var(--surface2) !important;
    color: var(--teal) !important;
    font-size: 0.72rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    border-bottom: 1px solid var(--border) !important;
}
[data-testid="stDataFrame"] td {
    border-color: var(--border) !important;
    color: var(--label) !important;
    font-size: 0.82rem !important;
}

/* ── Tabs ── */
[data-testid="stTabs"] [role="tablist"] {
    border-bottom: 1px solid var(--border) !important;
    gap: 0 !important;
}
[data-testid="stTabs"] [role="tab"] {
    background: transparent !important;
    color: var(--muted) !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    padding: 0.6rem 1.5rem !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
    transition: all 0.2s !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    color: var(--teal) !important;
    border-bottom: 2px solid var(--teal) !important;
}
[data-testid="stTabs"] [role="tab"]:hover {
    color: var(--text) !important;
}
[data-testid="stTabContent"] {
    padding-top: 1.5rem !important;
}

/* ── Number Inputs ── */
[data-testid="stNumberInput"] label {
    color: var(--label) !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
}
[data-testid="stNumberInput"] input {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-size: 0.95rem !important;
}
[data-testid="stNumberInput"] input:focus {
    border-color: var(--teal) !important;
    box-shadow: 0 0 0 3px var(--teal-glow) !important;
}

/* ── Simulator Card ── */
.sim-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 2rem;
    margin-top: 1.5rem;
}
.sim-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.3rem;
    color: var(--white);
    margin-bottom: 0.4rem;
}
.sim-desc {
    font-size: 0.82rem;
    color: var(--muted);
    margin-bottom: 1.75rem;
}

/* Risk result display */
.risk-result {
    background: var(--surface2);
    border-radius: 12px;
    padding: 1.75rem;
    margin-top: 1.5rem;
    text-align: center;
    border: 1px solid var(--border);
}
.risk-result-pct {
    font-size: 3.5rem;
    font-weight: 800;
    line-height: 1;
}
.risk-result-label {
    font-size: 0.78rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
    margin-top: 0.4rem;
}
.risk-result-tier {
    display: inline-block;
    margin-top: 0.75rem;
    padding: 0.3rem 1rem;
    border-radius: 100px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.tier-low    { background: rgba(45,212,191,0.15); color: var(--teal); }
.tier-medium { background: rgba(246,173,85,0.15); color: #F6AD55; }
.tier-high   { background: rgba(229,62,62,0.15);  color: var(--red-soft); }

/* ── Matplotlib theme override ── */
.stPlotlyChart, [data-testid="stImage"] { border-radius: 10px; overflow: hidden; }

/* ── Caution box ── */
.caution {
    background: var(--surface2);
    border-left: 3px solid #F6AD55;
    border-radius: 0 8px 8px 0;
    padding: 0.9rem 1.25rem;
    font-size: 0.8rem;
    color: var(--muted);
    margin: 2rem 0;
    line-height: 1.6;
}
.caution strong { color: #F6AD55; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--muted); }

/* ── Write / st.write text ── */
p, .stMarkdown p { color: var(--label) !important; font-size: 0.88rem !important; line-height: 1.7 !important; }

/* ── Expander ── */
[data-testid="stExpander"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
}
[data-testid="stExpander"] summary { color: var(--label) !important; }
</style>
""", unsafe_allow_html=True)


# ─── MATPLOTLIB DARK THEME ──────────────────────────────────────────────────────
plt.rcParams.update({
    'figure.facecolor':  '#161B22',
    'axes.facecolor':    '#161B22',
    'axes.edgecolor':    '#2A3244',
    'axes.labelcolor':   '#A0AEC0',
    'axes.titlecolor':   '#E2E8F0',
    'xtick.color':       '#718096',
    'ytick.color':       '#718096',
    'text.color':        '#E2E8F0',
    'grid.color':        '#2A3244',
    'grid.alpha':        0.5,
    'axes.spines.top':   False,
    'axes.spines.right': False,
    'font.family':       'sans-serif',
})
ACCENT_RED  = '#E53E3E'
ACCENT_TEAL = '#2DD4BF'
ACCENT_GOLD = '#F6AD55'


# ─── LOAD DATA ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv('cleveland_data.csv')
    df.columns = [
        "age", "sex", "cp", "trestbps", "chol", "fbs", "restecg",
        "thalach", "exang", "oldpeak", "slope", "ca", "thal", "target"
    ]
    df = df.replace('?', np.nan).dropna().apply(pd.to_numeric).drop_duplicates()
    return df

df = load_data()


# ─── HERO ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="author-badge">
    <span>Vihaan Mundra</span> · Heart Disease Research Project
</div>
<div class="hero">
    <div class="hero-eyebrow">UCI Cleveland Dataset · 303 Patients · 14 Variables</div>
    <h1>Fundamental <em>Heart Disease</em> Simulator &amp; Analysis</h1>
    <p class="hero-sub">
        Exploring how age, cholesterol, and peak cardiac stress-test heart rate 
        interact with heart disease risk — with an interactive risk simulator built 
        from real clinical data.
    </p>
    <div class="hero-meta">
        <div class="hero-stat">
            <span class="hero-stat-num">303</span>
            <span class="hero-stat-label">Patients</span>
        </div>
        <div class="hero-stat">
            <span class="hero-stat-num">14</span>
            <span class="hero-stat-label">Variables</span>
        </div>
        <div class="hero-stat">
            <span class="hero-stat-num">3</span>
            <span class="hero-stat-label">Key Predictors</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ─── DATASET PREVIEW ────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <span class="section-title">Dataset</span>
    <div class="section-header-line"></div>
</div>
""", unsafe_allow_html=True)
st.markdown(
    "<p>Raw data sourced from the <a href='https://archive.ics.uci.edu/dataset/45/heart+disease' "
    "style='color:#2DD4BF;'>UCI Heart Disease Repository</a>. "
    "Rows with missing values were dropped; numeric conversion applied throughout.</p>",
    unsafe_allow_html=True
)
with st.expander("View full dataset"):
    st.dataframe(df, use_container_width=True)


# ─── KEY METRICS ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <span class="section-title">Key Metrics</span>
    <div class="section-header-line"></div>
</div>
""", unsafe_allow_html=True)

total       = len(df)
hd_count    = (df['target'] >= 1).sum()
hd_pct      = hd_count / total * 100
mean_age_hd = df.loc[df['target'] >= 1, 'age'].mean()
mean_chol   = df.loc[df['target'] >= 1, 'chol'].mean()
mean_hr     = df.loc[df['target'] >= 1, 'thalach'].mean()

st.markdown(f"""
<div class="metric-grid">
    <div class="metric-card red">
        <div class="metric-label">HD Prevalence</div>
        <div class="metric-value">{hd_pct:.0f}%</div>
        <div class="metric-sub">{hd_count} of {total} patients</div>
    </div>
    <div class="metric-card teal">
        <div class="metric-label">Mean Age (HD+)</div>
        <div class="metric-value">{mean_age_hd:.1f}</div>
        <div class="metric-sub">Years old</div>
    </div>
    <div class="metric-card gold">
        <div class="metric-label">Avg Cholesterol (HD+)</div>
        <div class="metric-value">{mean_chol:.0f}</div>
        <div class="metric-sub">mg/dL</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ─── TABS: ANALYSIS ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <span class="section-title">Analysis</span>
    <div class="section-header-line"></div>
</div>
""", unsafe_allow_html=True)

tab_summary, tab_age, tab_chol, tab_hr = st.tabs(["Summary", "Age", "Cholesterol", "Heart Rate"])

# ── SUMMARY TAB ──
with tab_summary:
    st.markdown("""
    <p>Three factors are examined as primary predictors of heart disease risk in this dataset.
    Each is analyzed independently before being combined in the simulator.</p>
    """, unsafe_allow_html=True)

    young_hd_pct  = (df[df['age'] < 40]['target'] >= 1).mean() * 100
    middle_hd_pct = (df[(df['age'] >= 40) & (df['age'] < 60)]['target'] >= 1).mean() * 100
    old_hd_pct    = (df[df['age'] >= 60]['target'] >= 1).mean() * 100
    high_chol_hd  = (df[df['chol'] > 240]['target'] >= 1).mean() * 100
    low_hr_hd     = (df[df['thalach'] < 130]['target'] >= 1).mean() * 100

    st.markdown(f"""
    <div class="risk-row">
        <div class="risk-label">Young patients (&lt;40)</div>
        <div class="risk-bar-wrap"><div class="risk-bar" style="width:{young_hd_pct:.0f}%;background:#2DD4BF;"></div></div>
        <div class="risk-pct">{young_hd_pct:.0f}%</div>
    </div>
    <div class="risk-row">
        <div class="risk-label">Middle-aged (40–60)</div>
        <div class="risk-bar-wrap"><div class="risk-bar" style="width:{middle_hd_pct:.0f}%;background:#F6AD55;"></div></div>
        <div class="risk-pct">{middle_hd_pct:.0f}%</div>
    </div>
    <div class="risk-row">
        <div class="risk-label">Older patients (&gt;60)</div>
        <div class="risk-bar-wrap"><div class="risk-bar" style="width:{old_hd_pct:.0f}%;background:#E53E3E;"></div></div>
        <div class="risk-pct">{old_hd_pct:.0f}%</div>
    </div>
    <div class="risk-row">
        <div class="risk-label">High cholesterol (&gt;240 mg/dL)</div>
        <div class="risk-bar-wrap"><div class="risk-bar" style="width:{high_chol_hd:.0f}%;background:#E53E3E;"></div></div>
        <div class="risk-pct">{high_chol_hd:.0f}%</div>
    </div>
    <div class="risk-row">
        <div class="risk-label">Low stress-test HR (&lt;130 bpm)</div>
        <div class="risk-bar-wrap"><div class="risk-bar" style="width:{low_hr_hd:.0f}%;background:#E53E3E;"></div></div>
        <div class="risk-pct">{low_hr_hd:.0f}%</div>
    </div>
    """, unsafe_allow_html=True)

# ── AGE TAB ──
with tab_age:
    age_hd = df.loc[df["target"] >= 1, "age"]
    total_hd = len(age_hd)
    pct_y = (age_hd < 40).sum() / total_hd * 100
    pct_m = ((age_hd >= 40) & (age_hd < 60)).sum() / total_hd * 100
    pct_o = (age_hd >= 60).sum() / total_hd * 100

    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots(figsize=(5, 3.5))
        groups = ["Young\n(<40)", "Middle\n(40–60)", "Old\n(>60)"]
        vals   = [pct_y, pct_m, pct_o]
        colors = [ACCENT_TEAL, ACCENT_GOLD, ACCENT_RED]
        bars = ax.bar(groups, vals, color=colors, width=0.55, zorder=3)
        ax.grid(axis='y', zorder=0)
        ax.set_ylabel("% of HD patients")
        ax.set_title("Heart Disease by Age Group", pad=12)
        for bar, v in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.8,
                    f"{v:.1f}%", ha='center', va='bottom', fontsize=9, color='#A0AEC0')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with col2:
        young_g  = df[df['age'] < 40]
        middle_g = df[(df['age'] >= 40) & (df['age'] < 60)]
        old_g    = df[df['age'] >= 60]
        hd_pcts  = [
            (young_g['target']  >= 1).mean() * 100,
            (middle_g['target'] >= 1).mean() * 100,
            (old_g['target']    >= 1).mean() * 100,
        ]
        fig, ax = plt.subplots(figsize=(5, 3.5))
        bars = ax.bar(groups, hd_pcts, color=colors, width=0.55, zorder=3)
        ax.grid(axis='y', zorder=0)
        ax.set_ylabel("% with Heart Disease")
        ax.set_title("HD Rate Within Each Age Group", pad=12)
        for bar, v in zip(bars, hd_pcts):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.8,
                    f"{v:.1f}%", ha='center', va='bottom', fontsize=9, color='#A0AEC0')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    st.markdown(f"""
    <p>The mean age of patients with heart disease is <strong style='color:#E2E8F0'>{age_hd.mean():.1f} years</strong>.
    HD risk climbs steeply with age — though younger patients still make up 
    <strong style='color:#2DD4BF'>{pct_y:.1f}%</strong> of the disease group, 
    highlighting the importance of early screening.</p>
    """, unsafe_allow_html=True)

# ── CHOLESTEROL TAB ──
with tab_chol:
    low   = df[df['chol'] < 200]
    medium = df[(df['chol'] >= 200) & (df['chol'] <= 239)]
    high  = df[df['chol'] > 240]

    pct_low  = (low['target']    >= 1).mean() * 100
    pct_med  = (medium['target'] >= 1).mean() * 100
    pct_high = (high['target']   >= 1).mean() * 100

    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots(figsize=(5, 3.5))
        cats = ["Low\n(<200)", "Medium\n(200–239)", "High\n(>240)"]
        vals = [pct_low, pct_med, pct_high]
        bars = ax.bar(cats, vals, color=[ACCENT_TEAL, ACCENT_GOLD, ACCENT_RED], width=0.55, zorder=3)
        ax.grid(axis='y', zorder=0)
        ax.set_ylabel("% with Heart Disease")
        ax.set_title("HD Rate by Cholesterol Level", pad=12)
        for bar, v in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.6,
                    f"{v:.1f}%", ha='center', va='bottom', fontsize=9, color='#A0AEC0')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with col2:
        fig, ax = plt.subplots(figsize=(5, 3.5))
        ax.hist(df[df['target'] == 0]['chol'], bins=20, color='#2DD4BF', alpha=0.7,
                label='No HD', zorder=3)
        ax.hist(df[df['target'] >= 1]['chol'], bins=20, color='#E53E3E', alpha=0.7,
                label='HD+', zorder=3)
        ax.grid(axis='y', zorder=0)
        ax.set_xlabel("Cholesterol (mg/dL)")
        ax.set_ylabel("Count")
        ax.set_title("Cholesterol Distribution", pad=12)
        ax.legend(fontsize=8)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    avg_chol_hd = df[df['target'] >= 1]['chol'].mean()
    st.markdown(f"""
    <p>Average cholesterol among HD patients: <strong style='color:#E2E8F0'>{avg_chol_hd:.0f} mg/dL</strong>. 
    Interestingly, cholesterol alone is a weak predictor in this dataset — 
    the separation between healthy and diseased groups is modest, 
    suggesting cholesterol works best as one factor in a multivariate model.</p>
    """, unsafe_allow_html=True)

# ── HEART RATE TAB ──
with tab_hr:
    mean_hr_hd     = df.loc[df['target'] >= 1, 'thalach'].mean()
    mean_hr_severe = df.loc[df['target'] >= 3, 'thalach'].mean()
    mean_hr_mild   = df.loc[df['target'].isin([1, 2]), 'thalach'].mean()
    mean_hr_none   = df.loc[df['target'] == 0, 'thalach'].mean()

    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots(figsize=(5, 3.5))
        ax.hist(df[df['target'] == 0]['thalach'], bins=20, color=ACCENT_TEAL, alpha=0.7,
                label='No HD', zorder=3)
        ax.hist(df[df['target'] >= 1]['thalach'], bins=20, color=ACCENT_RED, alpha=0.7,
                label='HD+', zorder=3)
        ax.grid(axis='y', zorder=0)
        ax.set_xlabel("Max Heart Rate (bpm)")
        ax.set_ylabel("Count")
        ax.set_title("Stress-Test HR Distribution", pad=12)
        ax.legend(fontsize=8)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with col2:
        labels = ['No HD', 'Mild HD\n(1–2)', 'Severe HD\n(3–4)']
        vals   = [mean_hr_none, mean_hr_mild, mean_hr_severe]
        colors = [ACCENT_TEAL, ACCENT_GOLD, ACCENT_RED]
        fig, ax = plt.subplots(figsize=(5, 3.5))
        bars = ax.bar(labels, vals, color=colors, width=0.55, zorder=3)
        ax.set_ylim(min(vals) - 10, max(vals) + 10)
        ax.grid(axis='y', zorder=0)
        ax.set_ylabel("Mean Max HR (bpm)")
        ax.set_title("Mean Stress-Test HR by Severity", pad=12)
        for bar, v in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    f"{v:.0f}", ha='center', va='bottom', fontsize=9, color='#A0AEC0')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    st.markdown(f"""
    <p>A <strong style='color:#E53E3E'>lower peak heart rate</strong> during a cardiac stress test is 
    associated with higher disease severity — indicating a reduced cardiovascular reserve. 
    Mean HR drops from <strong style='color:#E2E8F0'>{mean_hr_none:.0f} bpm</strong> in healthy 
    patients to <strong style='color:#E2E8F0'>{mean_hr_severe:.0f} bpm</strong> in severe cases.</p>
    """, unsafe_allow_html=True)


# ─── SIMULATOR ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <span class="section-title">Risk Simulator</span>
    <div class="section-header-line"></div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="sim-card">
<div class="sim-title">Personal Risk Estimator</div>
<div class="sim-desc">
    Enter your values below. The simulator uses scoring weights derived from the 
    Cleveland dataset's observed HD rates across age, cholesterol, and peak cardiac heart rate bands.
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    sim_age  = st.number_input("Age", min_value=0, max_value=120, value=50)
with c2:
    sim_chol = st.number_input("Cholesterol (mg/dL)", min_value=0, max_value=1000, value=200)
with c3:
    sim_hr   = st.number_input("Peak stress-test heart rate (bpm)", min_value=0, max_value=250, value=150)

def heart_disease_risk(age, chol, thalach):
    score = 0
    if age >= 60:         score += 200
    elif age >= 40:       score += 125
    else:                 score += 50
    if chol >= 240:       score += 50
    elif chol >= 200:     score += 25
    else:                 score += 5
    if thalach >= 170:    score += 100
    elif thalach >= 150:  score += 200
    elif thalach >= 130:  score += 300
    else:                 score += 400
    return (score / 750) * 100

risk_pct = heart_disease_risk(sim_age, sim_chol, sim_hr)

if risk_pct < 40:
    tier_cls, tier_label, color = "tier-low",    "Low Risk",    "#2DD4BF"
elif risk_pct < 65:
    tier_cls, tier_label, color = "tier-medium", "Moderate Risk", "#F6AD55"
else:
    tier_cls, tier_label, color = "tier-high",   "Elevated Risk", "#FC8181"

st.markdown(f"""
<div class="risk-result">
    <div class="risk-result-pct" style="color:{color}">{risk_pct:.1f}%</div>
    <div class="risk-result-label">Estimated Heart Disease Risk Score</div>
    <span class="risk-result-tier {tier_cls}">{tier_label}</span>
</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)  # close sim-card

st.markdown("""
<div class="caution">
    <strong>⚠ Educational use only.</strong> This simulator is a simplified scoring model built 
    from a 303-patient dataset for academic purposes. It is not a clinical diagnostic tool and 
    should not replace advice from a qualified healthcare professional.
</div>
""", unsafe_allow_html=True)
