import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="SLA Dashboard – Pre Screening → SLIK",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Inter:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #050810;
    color: #ffffff;
}

.stApp { background-color: #050810; }

/* Animated gradient background */
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: 
        radial-gradient(ellipse 80% 50% at 20% 10%, rgba(59,130,246,0.07) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 80%, rgba(99,102,241,0.06) 0%, transparent 60%);
    pointer-events: none;
    z-index: 0;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #080c18 !important;
    border-right: 1px solid rgba(255,255,255,0.06);
}
section[data-testid="stSidebar"] * {
    color: #ffffff !important;
}
section[data-testid="stSidebar"] .stTextInput input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    color: #ffffff !important;
    border-radius: 8px !important;
}
section[data-testid="stSidebar"] label {
    color: rgba(255,255,255,0.6) !important;
    font-size: 12px !important;
}

/* Metric cards */
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 20px 24px;
    backdrop-filter: blur(10px);
    transition: border-color 0.2s;
}
[data-testid="metric-container"]:hover {
    border-color: rgba(255,255,255,0.18);
}
[data-testid="metric-container"] label {
    font-family: 'Inter', sans-serif !important;
    font-size: 11px !important;
    font-weight: 500 !important;
    color: rgba(255,255,255,0.45) !important;
    letter-spacing: 1.2px;
    text-transform: uppercase;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.9rem !important;
    color: #ffffff !important;
    font-weight: 700;
    letter-spacing: -0.5px;
}
[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    font-size: 11px !important;
    color: rgba(255,255,255,0.5) !important;
}

/* Section headers */
.section-title {
    font-family: 'Inter', sans-serif;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: rgba(255,255,255,0.35);
    margin: 36px 0 16px 0;
    padding-bottom: 10px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}

/* Hero banner */
.hero {
    background: linear-gradient(135deg, rgba(59,130,246,0.12) 0%, rgba(99,102,241,0.08) 50%, rgba(139,92,246,0.06) 100%);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px;
    padding: 40px 48px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}
.hero::after {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 280px; height: 280px;
    background: radial-gradient(circle, rgba(99,102,241,0.15) 0%, transparent 70%);
    border-radius: 50%;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    color: #ffffff;
    margin: 0 0 10px 0;
    letter-spacing: -1px;
    line-height: 1.1;
}
.hero p {
    color: rgba(255,255,255,0.5);
    font-size: 14px;
    margin: 0;
    font-weight: 300;
    letter-spacing: 0.2px;
}
.hero .accent {
    color: rgba(147,197,253,0.9);
    font-weight: 500;
}

/* Info/warning/error boxes */
.stAlert {
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    background: rgba(255,255,255,0.03) !important;
    color: #ffffff !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.03);
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
    border: 1px solid rgba(255,255,255,0.06);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px !important;
    color: rgba(255,255,255,0.45) !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    padding: 6px 16px !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(255,255,255,0.08) !important;
    color: #ffffff !important;
}

/* Expander */
.streamlit-expanderHeader {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 12px !important;
    color: rgba(255,255,255,0.7) !important;
    font-size: 13px !important;
}
.streamlit-expanderContent {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-top: none !important;
}

/* Buttons */
.stDownloadButton button, .stButton button {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    color: #ffffff !important;
    border-radius: 10px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    transition: all 0.2s !important;
}
.stDownloadButton button:hover, .stButton button:hover {
    background: rgba(255,255,255,0.1) !important;
    border-color: rgba(255,255,255,0.2) !important;
}

/* Dataframe */
.stDataFrame {
    border-radius: 12px !important;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.07) !important;
}
[data-testid="stDataFrameResizable"] {
    background: rgba(255,255,255,0.02) !important;
}

/* Multiselect */
.stMultiSelect [data-baseweb="select"] {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
}

/* Text inputs */
.stTextInput input, .stDateInput input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    color: #ffffff !important;
    border-radius: 10px !important;
}

/* Upload area */
.upload-card {
    background: rgba(255,255,255,0.02);
    border: 1px dashed rgba(255,255,255,0.12);
    border-radius: 16px;
    padding: 28px;
    text-align: center;
}

/* Scrollbar */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.12); border-radius: 2px; }

/* Caption / small text */
.stCaption, small { color: rgba(255,255,255,0.35) !important; }

/* General text */
p, span, div { color: #ffffff; }
label { color: rgba(255,255,255,0.6) !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="rgba(255,255,255,0.75)"),
    xaxis=dict(
        gridcolor="rgba(255,255,255,0.05)",
        linecolor="rgba(255,255,255,0.08)",
        tickfont=dict(size=11, color="rgba(255,255,255,0.5)"),
        title_font=dict(color="rgba(255,255,255,0.5)")
    ),
    yaxis=dict(
        gridcolor="rgba(255,255,255,0.05)",
        linecolor="rgba(255,255,255,0.08)",
        tickfont=dict(size=11, color="rgba(255,255,255,0.5)"),
        title_font=dict(color="rgba(255,255,255,0.5)")
    ),
    margin=dict(l=0, r=0, t=40, b=0),
    legend=dict(font=dict(color="rgba(255,255,255,0.6)", size=11)),
    title_font=dict(color="rgba(255,255,255,0.85)", size=13, family="Syne"),
)
COLOR_SEQ = ["#60a5fa", "#34d399", "#a78bfa", "#fbbf24", "#f472b6", "#38bdf8", "#4ade80", "#fb923c"]


def parse_datetime(series):
    """Try multiple datetime formats."""
    for fmt in [None, "%Y-%m-%d %H:%M:%S.%f %p", "%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S %p", "%Y-%m-%d %H:%M:%S"]:
        try:
            if fmt is None:
                parsed = pd.to_datetime(series, infer_datetime_format=True, errors="coerce")
            else:
                parsed = pd.to_datetime(series, format=fmt, errors="coerce")
            if parsed.notna().sum() > 0:
                return parsed
        except Exception:
            continue
    return pd.to_datetime(series, errors="coerce")


# Kolom One Me Pre Screening
PS_COLS = ["APPID", "APPID ESCORE", "NIP_USER", "USER_NAM", "STATUS",
           "CREATED_AT", "REASON", "CABANG", "PRODUK", "NIP_CMO",
           "NAMA_COM", "PisahHarta", "namadealer",
           "FACT_HISTORICAL_ONE_ME.jenis_cluster", "sales_type"]

# Kolom SLIK
SLIK_COLS = ["APPID", "MID", "CABANG", "NIK", "Product", "EngineScoring",
             "MOName", "HitBiroKredit", "HitBiroKreditKonsumen",
             "Tanggal Hit SLIK", "Timedone Hit SLIK", "Flag",
             "DataEntryProced", "StatusMa", "MaritalStatus"]

TIMEDONE_COL = "Timedone Hit SLIK"
TANGGAL_SLIK_COL = "Tanggal Hit SLIK"

@st.cache_data(show_spinner=False)
def load_prescreening(file_path, sheet_name):
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
    df.columns = df.columns.str.strip()
    df["APPID"] = pd.to_numeric(df["APPID"], errors="coerce")
    if "CREATED_AT" in df.columns:
        df["CREATED_AT"] = parse_datetime(df["CREATED_AT"])
    # Hanya ambil kolom yang ada
    keep = [c for c in PS_COLS if c in df.columns]
    return df[keep]


@st.cache_data(show_spinner=False)
def load_slik(file_path, sheet_name):
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
    df.columns = df.columns.str.strip()
    df["APPID"] = pd.to_numeric(df["APPID"], errors="coerce")
    if TIMEDONE_COL in df.columns:
        df[TIMEDONE_COL] = parse_datetime(df[TIMEDONE_COL])
    if TANGGAL_SLIK_COL in df.columns:
        df[TANGGAL_SLIK_COL] = parse_datetime(df[TANGGAL_SLIK_COL])
    # Hanya ambil kolom yang ada
    keep = [c for c in SLIK_COLS if c in df.columns]
    return df[keep]


def sla_category(hours):
    if pd.isna(hours):
        return "No Data"
    elif hours <= 1:
        return "≤ 1 Jam"
    elif hours <= 3:
        return "1–3 Jam"
    elif hours <= 6:
        return "3–6 Jam"
    elif hours <= 24:
        return "6–24 Jam"
    else:
        return "> 24 Jam"


SLA_CAT_ORDER = ["≤ 1 Jam", "1–3 Jam", "3–6 Jam", "6–24 Jam", "> 24 Jam", "No Data"]
SLA_CAT_COLOR = {
    "≤ 1 Jam": "#34d399",
    "1–3 Jam": "#60a5fa",
    "3–6 Jam": "#fbbf24",
    "6–24 Jam": "#fb923c",
    "> 24 Jam": "#f87171",
    "No Data": "#6b7280",
}

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
# ── CONFIG PATH FILE ──
# ── Nama file (harus sama persis dengan file di repo) ──
FILE_ESCORE = "APPID ONE ME PRESCREEN ESCORE.xlsx"  # Step 1: master APPID (27k)
FILE_PS     = "ONE ME PRE SCREENING.xlsx"            # Step 2: data utama (CREATED_AT dll)
FILE_SLIK   = "SLIK.xlsx"                            # Step 3: data SLIK (Timedone)

SHEET_ESCORE   = "Sheet1"
SHEET_PS       = "all raw"
SHEET_SLIK     = "Sheet1"
ESCORE_COL     = "APPID_ONEME_PRESCREEN"   # kolom APPID di file ESCORE

with st.sidebar:
    st.markdown("""
    <div style='padding: 16px 0 8px;'>
        <p style='font-family: Inter, sans-serif; font-size: 10px; letter-spacing: 2.5px; color: rgba(255,255,255,0.35); text-transform: uppercase; margin:0; font-weight:600;'>SLA MONITOR</p>
        <p style='font-family: Syne, sans-serif; font-size: 20px; color: #ffffff; margin: 6px 0 0; font-weight:700; letter-spacing:-0.5px;'>Pre Screening<br/>→ SLIK</p>
    </div>
    <hr style='border-color: rgba(255,255,255,0.07); margin: 16px 0;'>
    """, unsafe_allow_html=True)

    st.markdown("**⚙️ Config File**")
    escore_path = st.text_input("① Master APPID (ESCORE)", value=FILE_ESCORE)
    ps_path     = st.text_input("② One Me Pre Screening", value=FILE_PS)
    slik_path   = st.text_input("③ SLIK", value=FILE_SLIK)

    st.markdown("<hr style='border-color: rgba(255,255,255,0.07); margin: 16px 0;'>", unsafe_allow_html=True)

    escore_sheet   = st.text_input("Sheet ESCORE", value=SHEET_ESCORE)
    ps_sheet       = st.text_input("Sheet One Me", value=SHEET_PS)
    slik_sheet     = st.text_input("Sheet SLIK", value=SHEET_SLIK)
    escore_col     = st.text_input("Kolom APPID di ESCORE", value=ESCORE_COL)

    st.markdown("<hr style='border-color: #1e3a5f; margin: 16px 0;'>", unsafe_allow_html=True)
    st.markdown("""
    <p style='font-family: Inter, sans-serif; font-size: 10px; color: rgba(255,255,255,0.2); letter-spacing: 0.5px; line-height: 1.8;'>
    JOIN: One Me APPID = SLIK APPID<br/>
    FILTER: APPID List (27k)<br/>
    SLA: CREATED_AT → Timedone Hit SLIK
    </p>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>SLA Dashboard</h1>
    <p>
        <span class="accent">Pre Screening</span> → <span class="accent">SLIK</span>
        &nbsp;·&nbsp; Monitoring waktu proses aplikasi per cabang &amp; produk
    </p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MAIN LOGIC
# ─────────────────────────────────────────────
import os

missing = []
if not os.path.exists(escore_path): missing.append(f"❌ `{escore_path}` — Master APPID ESCORE")
if not os.path.exists(ps_path):     missing.append(f"❌ `{ps_path}` — One Me Pre Screening")
if not os.path.exists(slik_path):   missing.append(f"❌ `{slik_path}` — SLIK")
if missing:
    st.error("File berikut tidak ditemukan di repo:")
    for m in missing:
        st.markdown(m)
    st.markdown("""
    **Pastikan 3 file ini ada di root repo GitHub (nama harus sama persis):**
    ```
    APPID ONE ME PRESCREEN ESCORE.xlsx   ← master APPID (27k)
    ONE ME PRE SCREENING.xlsx            ← data utama
    SLIK.xlsx                            ← data SLIK
    ```
    """)
    st.stop()

# ── Load data ──
with st.spinner("Memuat & memproses data..."):

    # ════════════════════════════════════════════════════════
    # STEP 1 — Baca master APPID dari ESCORE (27k)
    # ════════════════════════════════════════════════════════
    try:
        df_escore = pd.read_excel(escore_path, sheet_name=escore_sheet)
        df_escore.columns = df_escore.columns.str.strip()
        if escore_col not in df_escore.columns:
            st.error(f"Kolom '{escore_col}' tidak ada di ESCORE. Kolom tersedia: {list(df_escore.columns)}")
            st.stop()
        master_appids = set(
            pd.to_numeric(df_escore[escore_col], errors="coerce").dropna().astype(int)
        )
        n_master = len(master_appids)
    except Exception as e:
        st.error(f"Gagal baca ESCORE: {e}"); st.stop()

    # ════════════════════════════════════════════════════════
    # STEP 2 — Tabrakan master APPID ke ONE ME → dapat CREATED_AT
    #          Filter hanya APPID yang ada di master ESCORE
    #          Dedup per APPID: ambil CREATED_AT paling awal
    # ════════════════════════════════════════════════════════
    try:
        df_ps_raw    = load_prescreening(ps_path, ps_sheet)
        n_ps_raw     = len(df_ps_raw)
        # Filter: hanya APPID yang ada di master
        df_ps_filter = df_ps_raw[df_ps_raw["APPID"].isin(master_appids)].copy()
        n_ps_rows    = len(df_ps_filter)   # jumlah baris (bisa duplikat APPID)
        # Dedup per APPID — ambil CREATED_AT terkecil (paling awal)
        df_ps = (
            df_ps_filter
            .sort_values("CREATED_AT")
            .drop_duplicates(subset=["APPID"], keep="first")
            .copy()
        )
        n_ps_matched  = len(df_ps)                  # unique APPID yang ketemu di ONE ME
        n_ps_notfound = n_master - n_ps_matched      # APPID master yang tidak ada di ONE ME
    except Exception as e:
        st.error(f"Gagal baca One Me: {e}"); st.stop()

    # ════════════════════════════════════════════════════════
    # STEP 3 — Tabrakan hasil Step 2 ke SLIK → dapat Timedone
    #          Base = df_ps (ONE ME filtered), join ke SLIK
    # ════════════════════════════════════════════════════════
    try:
        df_slik = load_slik(slik_path, slik_sheet)
    except Exception as e:
        st.error(f"Gagal baca SLIK: {e}"); st.stop()

    if TIMEDONE_COL not in df_slik.columns:
        st.error(f"Kolom '{TIMEDONE_COL}' tidak ditemukan di SLIK."); st.stop()

    # Dedup SLIK per APPID — kalau 1 APPID ada banyak baris, ambil Timedone terkecil
    n_slik_raw   = len(df_slik)
    df_slik_dedup = (
        df_slik
        .dropna(subset=["APPID"])
        .sort_values(TIMEDONE_COL)
        .drop_duplicates(subset=["APPID"], keep="first")
        .copy()
    )
    n_slik_dedup = len(df_slik_dedup)

    # Rename kolom yang sama di kedua file sebelum join
    df_slik_j = df_slik_dedup.rename(columns={"CABANG": "CABANG_SLIK", "Product": "Product_SLIK"})

    # LEFT JOIN: df_ps sebagai base, ambil kolom SLIK kalau APPID ketemu
    df = df_ps.merge(df_slik_j, on="APPID", how="left")

    # ════════════════════════════════════════════════════════
    # STEP 4 — Hitung SLA per APPID
    #          SLA = Timedone Hit SLIK − CREATED_AT
    # ════════════════════════════════════════════════════════
    df["_slik_found"]  = df[TIMEDONE_COL].notna()
    df["SLA_Hours"]    = (df[TIMEDONE_COL] - df["CREATED_AT"]).dt.total_seconds() / 3600
    df["SLA_Minutes"]  = df["SLA_Hours"] * 60
    df["SLA_Hours"]    = df["SLA_Hours"].round(2)
    df["SLA_Minutes"]  = df["SLA_Minutes"].round(1)
    df["SLA_Category"] = df["SLA_Hours"].apply(sla_category)

    timedone_col = TIMEDONE_COL

    # ── Stats untuk diagnostics ──
    n_slik_match   = int(df["_slik_found"].sum())       # ONE ME yg ketemu di SLIK
    n_slik_nomatch = int((~df["_slik_found"]).sum())    # ONE ME yg TIDAK ketemu di SLIK

# ─────────────────────────────────────────────
# FILTERS
# ─────────────────────────────────────────────
with st.expander("🔽 Filter Data", expanded=False):
    col1, col2, col3 = st.columns(3)
    with col1:
        cabang_list = sorted(df["CABANG"].dropna().unique().tolist()) if "CABANG" in df.columns else []
        sel_cabang = st.multiselect("Cabang", cabang_list, default=[])
    with col2:
        prod_col = "PRODUK" if "PRODUK" in df.columns else ("Product_SLIK" if "Product_SLIK" in df.columns else None)
        if prod_col:
            prod_list = sorted(df[prod_col].dropna().unique().tolist())
            sel_prod = st.multiselect("Produk", prod_list, default=[])
        else:
            sel_prod = []
            prod_col = None
    with col3:
        date_range = st.date_input(
            "Tanggal CREATED_AT",
            value=(df["CREATED_AT"].min().date(), df["CREATED_AT"].max().date()),
            key="daterange"
        )

df_f = df.copy()
if sel_cabang:
    df_f = df_f[df_f["CABANG"].isin(sel_cabang)]
if sel_prod and prod_col and prod_col in df_f.columns:
    df_f = df_f[df_f[prod_col].isin(sel_prod)]
if len(date_range) == 2:
    df_f = df_f[
        (df_f["CREATED_AT"].dt.date >= date_range[0]) &
        (df_f["CREATED_AT"].dt.date <= date_range[1])
    ]

df_valid = df_f[df_f["SLA_Hours"].notna() & (df_f["SLA_Hours"] >= 0) & (df_f["_slik_found"] == True)]

# ─────────────────────────────────────────────
# JOIN DIAGNOSTICS
# ─────────────────────────────────────────────
st.markdown('<p class="section-title">🔗 Hasil Tabrakan Data (APPID = APPID)</p>', unsafe_allow_html=True)

# Flow summary banner
match_pct_slik = n_slik_match / n_ps_matched * 100 if n_ps_matched else 0
st.markdown(f"""
<div style='display:flex; gap:8px; align-items:center; margin-bottom:20px; flex-wrap:wrap;'>
    <div style='background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.1); border-radius:10px; padding:10px 16px; font-size:12px;'>
        <span style='color:rgba(255,255,255,0.4); font-size:10px; display:block; margin-bottom:2px;'>① ESCORE</span>
        <span style='font-weight:600;'>{n_master:,} APPID</span>
    </div>
    <span style='color:rgba(255,255,255,0.2); font-size:18px;'>→</span>
    <div style='background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.1); border-radius:10px; padding:10px 16px; font-size:12px;'>
        <span style='color:rgba(255,255,255,0.4); font-size:10px; display:block; margin-bottom:2px;'>② ONE ME</span>
        <span style='font-weight:600;'>{n_ps_matched:,} unique APPID</span>
        <span style='color:rgba(255,255,255,0.35); font-size:11px;'> dari {n_ps_rows:,} baris</span>
    </div>
    <span style='color:rgba(255,255,255,0.2); font-size:18px;'>→</span>
    <div style='background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.1); border-radius:10px; padding:10px 16px; font-size:12px;'>
        <span style='color:rgba(255,255,255,0.4); font-size:10px; display:block; margin-bottom:2px;'>③ SLIK</span>
        <span style='color:#34d399; font-weight:600;'>{n_slik_match:,} match</span>
        <span style='color:rgba(255,255,255,0.35);'> / </span>
        <span style='color:#f87171; font-weight:600;'>{n_slik_nomatch:,} tidak</span>
    </div>
    <span style='color:rgba(255,255,255,0.2); font-size:18px;'>→</span>
    <div style='background:rgba(96,165,250,0.08); border:1px solid rgba(96,165,250,0.2); border-radius:10px; padding:10px 16px; font-size:12px;'>
        <span style='color:rgba(255,255,255,0.4); font-size:10px; display:block; margin-bottom:2px;'>④ SLA</span>
        <span style='color:#60a5fa; font-weight:600;'>CREATED_AT → Timedone SLIK</span>
    </div>
</div>
""", unsafe_allow_html=True)

jc1, jc2, jc3, jc4, jc5 = st.columns(5)
jc1.metric("Master APPID (ESCORE)", f"{n_master:,}")
jc2.metric("Ketemu di ONE ME", f"{n_ps_matched:,}", f"dari {n_ps_rows:,} baris raw")
jc3.metric("SLIK (unique APPID)", f"{n_slik_dedup:,}", f"raw: {n_slik_raw:,}")
jc4.metric("✅ Match ke SLIK", f"{n_slik_match:,}", f"{match_pct_slik:.1f}%")
jc5.metric("❌ Tidak Match SLIK", f"{n_slik_nomatch:,}", f"{100-match_pct_slik:.1f}%")

# Visual bar match rate
fig_match = go.Figure()
fig_match.add_trace(go.Bar(
    x=["Match ke SLIK", "Tidak Match SLIK"],
    y=[n_slik_match, n_slik_nomatch],
    marker_color=["#34d399", "#f87171"],
    text=[f"{n_slik_match:,} ({match_pct_slik:.1f}%)", f"{n_slik_nomatch:,} ({100-match_pct_slik:.1f}%)"],
    textposition="outside",
    textfont=dict(size=12),
))
fig_match.update_layout(**PLOTLY_LAYOUT, height=220,
                         title="Join Result — Pre Screening vs SLIK",
                         title_font=dict(size=12, color="#c8d8e8"),
                         showlegend=False)
fig_match.update_yaxes(showgrid=False, showticklabels=False)

jcol1, jcol2 = st.columns([2, 3])
with jcol1:
    st.plotly_chart(fig_match, use_container_width=True)

with jcol2:
    # Tabel preview hasil join
    preview_cols = ["APPID"]
    if "USER_NAM" in df.columns: preview_cols.append("USER_NAM")
    if "CABANG" in df.columns: preview_cols.append("CABANG")
    preview_cols += ["CREATED_AT", timedone_col, "SLA_Hours", "_slik_found"]
    available_preview = [c for c in preview_cols if c in df.columns]

    tab_match, tab_nomatch = st.tabs([f"✅ Match SLIK ({n_slik_match:,})", f"❌ Tidak Match ({n_slik_nomatch:,})"])
    with tab_match:
        df_matched_preview = df[df["_slik_found"] == True][available_preview].head(200)
        st.dataframe(df_matched_preview, use_container_width=True, hide_index=True, height=180)
    with tab_nomatch:
        df_unmatched_preview = df[df["_slik_found"] == False][available_preview].head(200)
        st.dataframe(df_unmatched_preview, use_container_width=True, hide_index=True, height=180)
        if n_slik_nomatch > 0:
            csv_unmatch = df[df['_slik_found'] == False].to_csv(index=False).encode()
            st.download_button("⬇️ Download yang tidak match", csv_unmatch, "not_matched.csv", "text/csv")

# ─────────────────────────────────────────────
# KPI METRICS
# ─────────────────────────────────────────────
st.markdown('<p class="section-title">📊 Overview SLA</p>', unsafe_allow_html=True)

k1, k2, k3, k4, k5, k6 = st.columns(6)
total_filtered  = len(df_f)  # = n_ps_matched setelah filter
matched_f       = int(df_f["_slik_found"].eq(True).sum())
avg_sla         = df_valid["SLA_Hours"].mean() if len(df_valid) else 0
median_sla      = df_valid["SLA_Hours"].median() if len(df_valid) else 0
count_ok        = int((df_valid["SLA_Hours"] <= 1).sum())
pct_ok          = (count_ok / len(df_valid) * 100) if len(df_valid) else 0

k1.metric("Total APPID (filtered)", f"{total_filtered:,}")
k2.metric("Match ke SLIK", f"{matched_f:,}", f"{matched_f/total_filtered*100:.1f}%" if total_filtered else "-")
k3.metric("Avg SLA", f"{avg_sla:.2f} Jam")
k4.metric("Median SLA", f"{median_sla:.2f} Jam")
k5.metric("SLA ≤ 1 Jam", f"{count_ok:,}", f"{pct_ok:.1f}%")
k6.metric("SLA > 24 Jam", f"{int((df_valid['SLA_Hours'] > 24).sum()):,}")

# ─────────────────────────────────────────────
# CHARTS ROW 1
# ─────────────────────────────────────────────
st.markdown('<p class="section-title">📈 Distribusi SLA</p>', unsafe_allow_html=True)
c1, c2 = st.columns([3, 2])

with c1:
    # Histogram SLA
    fig_hist = px.histogram(
        df_valid[df_valid["SLA_Hours"] <= 48],
        x="SLA_Hours", nbins=50,
        title="Distribusi SLA (jam) — trimmed ≤ 48h",
        color_discrete_sequence=["#60a5fa"],
        labels={"SLA_Hours": "SLA (Jam)"}
    )
    fig_hist.update_layout(**PLOTLY_LAYOUT, title_font=dict(size=13, color="#c8d8e8"))
    fig_hist.update_traces(opacity=0.85)
    st.plotly_chart(fig_hist, use_container_width=True)

with c2:
    # Donut SLA Category
    cat_counts = df_f["SLA_Category"].value_counts().reset_index()
    cat_counts.columns = ["Kategori", "Jumlah"]
    cat_counts["Kategori"] = pd.Categorical(cat_counts["Kategori"], categories=SLA_CAT_ORDER, ordered=True)
    cat_counts = cat_counts.sort_values("Kategori")

    fig_pie = go.Figure(go.Pie(
        labels=cat_counts["Kategori"],
        values=cat_counts["Jumlah"],
        hole=0.55,
        marker=dict(colors=[SLA_CAT_COLOR.get(k, "#546e7a") for k in cat_counts["Kategori"]]),
        textinfo="percent",
        textfont=dict(size=11),
    ))
    fig_pie.update_layout(**PLOTLY_LAYOUT, title="Kategori SLA", title_font=dict(size=13, color="#c8d8e8"))
    fig_pie.add_annotation(text=f"<b>{len(df_valid):,}</b><br><span style='font-size:10'>records</span>",
                           x=0.5, y=0.5, showarrow=False, font=dict(size=14, color="#e8f4fd"))
    st.plotly_chart(fig_pie, use_container_width=True)

# ─────────────────────────────────────────────
# CHARTS ROW 2 – PER CABANG
# ─────────────────────────────────────────────
st.markdown('<p class="section-title">🏢 Analisis per Cabang</p>', unsafe_allow_html=True)

if "CABANG" in df_valid.columns:
    cabang_summary = (
        df_valid.groupby("CABANG")["SLA_Hours"]
        .agg(["mean", "median", "max", "count"])
        .reset_index()
        .rename(columns={"mean": "Avg SLA", "median": "Median SLA", "max": "Max SLA", "count": "Jumlah"})
        .sort_values("Avg SLA", ascending=False)
        .head(25)
    )
    cabang_summary[["Avg SLA", "Median SLA", "Max SLA"]] = cabang_summary[["Avg SLA", "Median SLA", "Max SLA"]].round(2)

    c3, c4 = st.columns([3, 2])
    with c3:
        fig_bar = px.bar(
            cabang_summary.sort_values("Avg SLA"),
            x="Avg SLA", y="CABANG", orientation="h",
            title="Avg SLA per Cabang (Top 25)",
            color="Avg SLA",
            color_continuous_scale=["#48c78e", "#ffb74d", "#ff5252"],
            text="Avg SLA",
            labels={"Avg SLA": "Avg SLA (Jam)"}
        )
        fig_bar.update_traces(texttemplate="%{text:.1f}h", textposition="outside", textfont_size=10)
        fig_bar.update_layout(**PLOTLY_LAYOUT, title_font=dict(size=13, color="#c8d8e8"),
                              coloraxis_showscale=False, height=600)
        st.plotly_chart(fig_bar, use_container_width=True)

    with c4:
        fig_scatter = px.scatter(
            cabang_summary,
            x="Jumlah", y="Avg SLA",
            size="Jumlah", color="Avg SLA",
            hover_name="CABANG",
            title="Volume vs Avg SLA",
            color_continuous_scale=["#48c78e", "#ffb74d", "#ff5252"],
            labels={"Jumlah": "Jumlah Aplikasi", "Avg SLA": "Avg SLA (Jam)"},
        )
        fig_scatter.update_layout(**PLOTLY_LAYOUT, title_font=dict(size=13, color="#c8d8e8"),
                                  coloraxis_showscale=False)
        st.plotly_chart(fig_scatter, use_container_width=True)

# ─────────────────────────────────────────────
# CHARTS ROW 3 – TREND
# ─────────────────────────────────────────────
st.markdown('<p class="section-title">📅 Trend Harian</p>', unsafe_allow_html=True)

if df_valid["CREATED_AT"].notna().sum() > 0:
    df_valid2 = df_valid.copy()
    df_valid2["Date"] = df_valid2["CREATED_AT"].dt.date
    daily = (
        df_valid2.groupby("Date")["SLA_Hours"]
        .agg(Avg="mean", Median="median", Count="count")
        .reset_index()
    )
    daily[["Avg", "Median"]] = daily[["Avg", "Median"]].round(2)

    fig_line = make_subplots(specs=[[{"secondary_y": True}]])
    fig_line.add_trace(go.Scatter(x=daily["Date"], y=daily["Avg"], name="Avg SLA",
                                  line=dict(color="#60a5fa", width=2.5), mode="lines+markers",
                                  marker=dict(size=5, color="#60a5fa")), secondary_y=False)
    fig_line.add_trace(go.Scatter(x=daily["Date"], y=daily["Median"], name="Median SLA",
                                  line=dict(color="#34d399", width=2, dash="dot"), mode="lines"),
                       secondary_y=False)
    fig_line.add_trace(go.Bar(x=daily["Date"], y=daily["Count"], name="Jumlah Aplikasi",
                              marker_color="rgba(96,165,250,0.12)", marker_line_width=0),
                       secondary_y=True)
    fig_line.update_layout(**PLOTLY_LAYOUT, title="Trend SLA Harian",
                           title_font=dict(size=13, color="#c8d8e8"),
                           legend=dict(orientation="h", y=1.08, font=dict(size=11)))
    fig_line.update_yaxes(title_text="SLA (Jam)", secondary_y=False, gridcolor="#1a2a3a")
    fig_line.update_yaxes(title_text="Jumlah Aplikasi", secondary_y=True, showgrid=False)
    st.plotly_chart(fig_line, use_container_width=True)

# ─────────────────────────────────────────────
# SUMMARY TABLE
# ─────────────────────────────────────────────
st.markdown('<p class="section-title">📋 Summary Tabel</p>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Per Cabang", "Per Produk", "Raw Data"])

with tab1:
    if "CABANG" in df_valid.columns:
        full_cabang = (
            df_valid.groupby("CABANG")["SLA_Hours"]
            .agg(
                Total_Record="count",
                Avg_SLA_Jam=lambda x: round(x.mean(), 2),
                Median_SLA_Jam=lambda x: round(x.median(), 2),
                Min_SLA_Jam=lambda x: round(x.min(), 2),
                Max_SLA_Jam=lambda x: round(x.max(), 2),
            )
            .reset_index()
            .sort_values("Avg_SLA_Jam", ascending=False)
        )
        full_cabang["SLA_≤1Jam"] = df_valid[df_valid["SLA_Hours"] <= 1].groupby("CABANG").size().reindex(full_cabang["CABANG"]).fillna(0).astype(int).values
        full_cabang["%_≤1Jam"] = (full_cabang["SLA_≤1Jam"] / full_cabang["Total_Record"] * 100).round(1).astype(str) + "%"
        st.dataframe(full_cabang, use_container_width=True, hide_index=True)

with tab2:
    _prod_col = "PRODUK" if "PRODUK" in df_valid.columns else ("Product_SLIK" if "Product_SLIK" in df_valid.columns else None)
    if _prod_col:
        prod_sum = (
            df_valid.groupby(_prod_col)["SLA_Hours"]
            .agg(Total_Record="count",
                 Avg_SLA_Jam=lambda x: round(x.mean(), 2),
                 Median_SLA_Jam=lambda x: round(x.median(), 2),
                 Max_SLA_Jam=lambda x: round(x.max(), 2))
            .reset_index()
            .sort_values("Avg_SLA_Jam", ascending=False)
        )
        st.dataframe(prod_sum, use_container_width=True, hide_index=True)
    else:
        st.info("Kolom PRODUK tidak ditemukan.")

with tab3:
    show_cols = [
        "APPID", "USER_NAM", "NIP_USER", "CREATED_AT",
        "CABANG", "PRODUK", "STATUS", "REASON", "sales_type",
        "FACT_HISTORICAL_ONE_ME.jenis_cluster",
        # SLIK fields
        "MID", "EngineScoring", "StatusMa", "Flag",
        TIMEDONE_COL, "Tanggal Hit SLIK",
        # Computed
        "SLA_Hours", "SLA_Minutes", "SLA_Category", "_slik_found"
    ]
    available = [c for c in show_cols if c in df_f.columns]
    st.dataframe(df_f[available].head(1000), use_container_width=True, hide_index=True)
    st.caption(f"Menampilkan 1,000 dari {len(df_f):,} baris")

# ─────────────────────────────────────────────
# DOWNLOAD
# ─────────────────────────────────────────────
st.markdown('<p class="section-title">⬇️ Export</p>', unsafe_allow_html=True)

d1, d2 = st.columns(2)
with d1:
    dl_cols = ["APPID","USER_NAM","CREATED_AT","CABANG","PRODUK","STATUS",
               "MID","EngineScoring","StatusMa",TIMEDONE_COL,
               "SLA_Hours","SLA_Minutes","SLA_Category","_slik_found"]
    csv_detail = df_f[[c for c in dl_cols if c in df_f.columns]].to_csv(index=False).encode()
    st.download_button("⬇️ Download Detail SLA (.csv)", csv_detail, "detail_sla.csv", "text/csv")

with d2:
    if "CABANG" in df_valid.columns:
        csv_summary = full_cabang.to_csv(index=False).encode()
        st.download_button("⬇️ Download Summary per Cabang (.csv)", csv_summary, "summary_cabang.csv", "text/csv")
