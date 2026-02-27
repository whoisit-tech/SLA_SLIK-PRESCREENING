import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="SLA SLIK PRE SCREENING",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; background:#050810; color:#fff; }
.stApp { background:#050810; }
.stApp::before {
    content:''; position:fixed; top:0; left:0; right:0; bottom:0;
    background: radial-gradient(ellipse 80% 50% at 20% 10%, rgba(59,130,246,0.07) 0%, transparent 60%),
                radial-gradient(ellipse 60% 40% at 80% 80%, rgba(99,102,241,0.06) 0%, transparent 60%);
    pointer-events:none; z-index:0;
}
section[data-testid="stSidebar"] { background:#080c18 !important; border-right:1px solid rgba(255,255,255,0.06); }
section[data-testid="stSidebar"] * { color:#fff !important; }
section[data-testid="stSidebar"] .stTextInput input {
    background:rgba(255,255,255,0.05) !important; border:1px solid rgba(255,255,255,0.1) !important;
    color:#fff !important; border-radius:8px !important;
}
[data-testid="metric-container"] {
    background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08);
    border-radius:16px; padding:20px 24px;
}
[data-testid="metric-container"]:hover { border-color:rgba(255,255,255,0.18); }
[data-testid="metric-container"] label {
    font-family:'Inter',sans-serif !important; font-size:11px !important; font-weight:500 !important;
    color:rgba(255,255,255,0.45) !important; letter-spacing:1.2px; text-transform:uppercase;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-family:'Syne',sans-serif !important; font-size:2rem !important;
    color:#fff !important; font-weight:700; letter-spacing:-0.5px;
}
[data-testid="metric-container"] [data-testid="stMetricDelta"] { font-size:11px !important; color:rgba(255,255,255,0.45) !important; }
.section-title {
    font-family:'Inter',sans-serif; font-size:10px; font-weight:600;
    letter-spacing:2.5px; text-transform:uppercase; color:rgba(255,255,255,0.3);
    margin:32px 0 14px; padding-bottom:8px; border-bottom:1px solid rgba(255,255,255,0.06);
}
.hero {
    background:linear-gradient(135deg,rgba(59,130,246,0.1) 0%,rgba(99,102,241,0.07) 100%);
    border:1px solid rgba(255,255,255,0.1); border-radius:20px;
    padding:36px 44px; margin-bottom:28px; position:relative; overflow:hidden;
}
.hero::after {
    content:''; position:absolute; top:-60px; right:-60px;
    width:260px; height:260px;
    background:radial-gradient(circle,rgba(99,102,241,0.12) 0%,transparent 70%);
    border-radius:50%;
}
.hero h1 { font-family:'Syne',sans-serif; font-size:2rem; font-weight:800; color:#fff; margin:0 0 8px; letter-spacing:-1px; }
.hero p { color:rgba(255,255,255,0.45); font-size:13px; margin:0; font-weight:300; }
.hero .accent { color:rgba(147,197,253,0.9); font-weight:500; }
.stTabs [data-baseweb="tab-list"] {
    background:rgba(255,255,255,0.03); border-radius:10px; padding:4px; gap:4px;
    border:1px solid rgba(255,255,255,0.06);
}
.stTabs [data-baseweb="tab"] {
    border-radius:8px !important; color:rgba(255,255,255,0.4) !important;
    font-size:12px !important; font-weight:500 !important; padding:6px 16px !important;
}
.stTabs [aria-selected="true"] { background:rgba(255,255,255,0.08) !important; color:#fff !important; }
.stDownloadButton button {
    background:rgba(255,255,255,0.05) !important; border:1px solid rgba(255,255,255,0.1) !important;
    color:#fff !important; border-radius:10px !important; font-size:12px !important;
}
::-webkit-scrollbar { width:4px; height:4px; }
::-webkit-scrollbar-track { background:transparent; }
::-webkit-scrollbar-thumb { background:rgba(255,255,255,0.1); border-radius:2px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PLOTLY THEME
# ─────────────────────────────────────────────
PL = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="rgba(255,255,255,0.6)"),
    xaxis=dict(gridcolor="rgba(255,255,255,0.05)", linecolor="rgba(255,255,255,0.06)",
               tickfont=dict(size=11, color="rgba(255,255,255,0.45)")),
    yaxis=dict(gridcolor="rgba(255,255,255,0.05)", linecolor="rgba(255,255,255,0.06)",
               tickfont=dict(size=11, color="rgba(255,255,255,0.45)")),
    margin=dict(l=0, r=0, t=36, b=0),
    legend=dict(font=dict(color="rgba(255,255,255,0.55)", size=11)),
    title_font=dict(color="rgba(255,255,255,0.8)", size=13, family="Syne"),
)

SLA_COLORS = {"≤ 1 Jam":"#34d399","1–3 Jam":"#60a5fa","3–6 Jam":"#fbbf24","6–24 Jam":"#fb923c","> 24 Jam":"#f87171","No Data":"#6b7280"}
SLA_ORDER  = ["≤ 1 Jam","1–3 Jam","3–6 Jam","6–24 Jam","> 24 Jam","No Data"]

def sla_category(h):
    if pd.isna(h):   return "No Data"
    elif h <= 1:     return "≤ 1 Jam"
    elif h <= 3:     return "1–3 Jam"
    elif h <= 6:     return "3–6 Jam"
    elif h <= 24:    return "6–24 Jam"
    else:            return "> 24 Jam"

def parse_dt(s):
    return pd.to_datetime(s, infer_datetime_format=True, errors="coerce")

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
FILE_ESCORE = "APPID ONE ME PRESCREEN ESCORE.xlsx"
FILE_PS     = "ONE ME PRE SCREENING.xlsx"
FILE_SLIK   = "SLIK.xlsx"
SHEET_ESCORE    = "Sheet1"
SHEET_PS        = "all raw"
SHEET_SLIK      = "Sheet1"
ESCORE_COL      = "APPID_ONEME_PRESCREEN"
TIMEDONE_COL    = "Timedone Hit SLIK"

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:16px 0 8px;'>
        <p style='font-family:Inter,sans-serif;font-size:10px;letter-spacing:2.5px;color:rgba(255,255,255,0.3);text-transform:uppercase;margin:0;font-weight:600;'>SLA MONITOR</p>
        <p style='font-family:Syne,sans-serif;font-size:20px;color:#fff;margin:6px 0 0;font-weight:700;letter-spacing:-0.5px;'>Pre Screening<br/>→ SLIK</p>
    </div>
    <hr style='border-color:rgba(255,255,255,0.07);margin:16px 0;'>
    """, unsafe_allow_html=True)

    st.markdown("** Config File**")
    escore_path  = st.text_input("① Master APPID (ESCORE)", value=FILE_ESCORE)
    ps_path      = st.text_input("② One Me Pre Screening",  value=FILE_PS)
    slik_path    = st.text_input("③ SLIK",                  value=FILE_SLIK)

    st.markdown("<hr style='border-color:rgba(255,255,255,0.07);margin:14px 0;'>", unsafe_allow_html=True)
    escore_sheet = st.text_input("Sheet ESCORE",   value=SHEET_ESCORE)
    ps_sheet     = st.text_input("Sheet One Me",   value=SHEET_PS)
    slik_sheet   = st.text_input("Sheet SLIK",     value=SHEET_SLIK)
    escore_col   = st.text_input("Kolom APPID ESCORE", value=ESCORE_COL)

    st.markdown("""
    <hr style='border-color:rgba(255,255,255,0.07);margin:14px 0;'>
    <p style='font-size:10px;color:rgba(255,255,255,0.2);line-height:1.8;'>
    ESCORE → ONE ME → SLIK<br/>SLA = CREATED_AT → Timedone Hit SLIK
    </p>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>SLA Dashboard</h1>
    <p><span class="accent">Pre Screening</span> → <span class="accent">SLIK</span> &nbsp;·&nbsp; Monitoring waktu proses per aplikasi</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CEK FILE
# ─────────────────────────────────────────────
missing = [f for f in [escore_path, ps_path, slik_path] if not os.path.exists(f)]
if missing:
    st.error("File tidak ditemukan: " + ", ".join(f"`{f}`" for f in missing))
    st.markdown("""
    Pastikan 3 file ini ada di root repo:
    ```
    APPID ONE ME PRESCREEN ESCORE.xlsx
    ONE ME PRE SCREENING.xlsx
    SLIK.xlsx
    ```
    """)
    st.stop()

# ─────────────────────────────────────────────
# LOAD & JOIN
# ─────────────────────────────────────────────
with st.spinner("Memuat data..."):

    # ── STEP 1: Master APPID dari ESCORE ──
    df_escore = pd.read_excel(escore_path, sheet_name=escore_sheet)
    df_escore.columns = df_escore.columns.str.strip()
    if escore_col not in df_escore.columns:
        st.error(f"Kolom '{escore_col}' tidak ada. Tersedia: {list(df_escore.columns)}"); st.stop()
    master_appids = set(pd.to_numeric(df_escore[escore_col], errors="coerce").dropna().astype(int))
    n_master = len(master_appids)

    # ── STEP 2: ONE ME → filter pakai master APPID, ambil CREATED_AT ──
    df_ps_raw = pd.read_excel(ps_path, sheet_name=ps_sheet)
    df_ps_raw.columns = df_ps_raw.columns.str.strip()
    df_ps_raw["APPID"] = pd.to_numeric(df_ps_raw["APPID"], errors="coerce")
    df_ps_raw["CREATED_AT"] = parse_dt(df_ps_raw["CREATED_AT"])
    n_ps_raw = len(df_ps_raw)

    # Filter: hanya APPID yang ada di master — TANPA dedup
    df_ps = df_ps_raw[df_ps_raw["APPID"].isin(master_appids)].copy()
    n_ps_filtered = len(df_ps)

    # ── STEP 3: SLIK ──
    df_slik = pd.read_excel(slik_path, sheet_name=slik_sheet)
    df_slik.columns = df_slik.columns.str.strip()
    df_slik["APPID"] = pd.to_numeric(df_slik["APPID"], errors="coerce")
    df_slik[TIMEDONE_COL] = parse_dt(df_slik[TIMEDONE_COL])
    if "Tanggal Hit SLIK" in df_slik.columns:
        df_slik["Tanggal Hit SLIK"] = parse_dt(df_slik["Tanggal Hit SLIK"])
    n_slik_raw = len(df_slik)

    # Rename kolom bentrok
    df_slik_j = df_slik.rename(columns={"CABANG": "CABANG_SLIK", "Product": "Product_SLIK"})

    # LEFT JOIN — TANPA dedup, semua baris ikut
    df = df_ps.merge(df_slik_j, on="APPID", how="left")

    # ── STEP 4: Hitung SLA ──
    df["_slik_found"] = df[TIMEDONE_COL].notna()
    df["SLA_Hours"]   = (df[TIMEDONE_COL] - df["CREATED_AT"]).dt.total_seconds() / 3600
    df["SLA_Minutes"] = df["SLA_Hours"] * 60
    df["SLA_Hours"]   = df["SLA_Hours"].round(2)
    df["SLA_Minutes"] = df["SLA_Minutes"].round(1)
    df["SLA_Category"] = df["SLA_Hours"].apply(sla_category)

    # Stats
    n_match    = int(df["_slik_found"].sum())
    n_nomatch  = int((~df["_slik_found"]).sum())
    df_sla     = df[df["_slik_found"]].copy()   # 2,765 baris yang punya SLA

# ─────────────────────────────────────────────
# FLOW SUMMARY
# ─────────────────────────────────────────────
match_pct = n_match / n_ps_filtered * 100 if n_ps_filtered else 0
st.markdown(f"""
<div style='display:flex;gap:8px;align-items:center;margin-bottom:24px;flex-wrap:wrap;'>
    <div style='background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.09);border-radius:10px;padding:10px 18px;font-size:12px;'>
        <span style='color:rgba(255,255,255,0.35);font-size:10px;display:block;margin-bottom:3px;letter-spacing:1px;'>① ESCORE</span>
        <span style='font-weight:700;font-size:15px;'>{n_master:,}</span><span style='color:rgba(255,255,255,0.35);font-size:11px;'> APPID</span>
    </div>
    <span style='color:rgba(255,255,255,0.15);font-size:20px;'>→</span>
    <div style='background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.09);border-radius:10px;padding:10px 18px;font-size:12px;'>
        <span style='color:rgba(255,255,255,0.35);font-size:10px;display:block;margin-bottom:3px;letter-spacing:1px;'>② ONE ME</span>
        <span style='font-weight:700;font-size:15px;'>{n_ps_filtered:,}</span><span style='color:rgba(255,255,255,0.35);font-size:11px;'> baris match</span>
    </div>
    <span style='color:rgba(255,255,255,0.15);font-size:20px;'>→</span>
    <div style='background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.09);border-radius:10px;padding:10px 18px;font-size:12px;'>
        <span style='color:rgba(255,255,255,0.35);font-size:10px;display:block;margin-bottom:3px;letter-spacing:1px;'>③ SLIK</span>
        <span style='color:#34d399;font-weight:700;font-size:15px;'>{n_match:,}</span><span style='color:rgba(255,255,255,0.35);font-size:11px;'> match &nbsp;</span>
        <span style='color:#f87171;font-weight:600;'>{n_nomatch:,}</span><span style='color:rgba(255,255,255,0.35);font-size:11px;'> tidak</span>
    </div>
    <span style='color:rgba(255,255,255,0.15);font-size:20px;'>→</span>
    <div style='background:rgba(96,165,250,0.07);border:1px solid rgba(96,165,250,0.18);border-radius:10px;padding:10px 18px;font-size:12px;'>
        <span style='color:rgba(255,255,255,0.35);font-size:10px;display:block;margin-bottom:3px;letter-spacing:1px;'>④ SLA DIHITUNG</span>
        <span style='color:#60a5fa;font-weight:700;font-size:15px;'>{n_match:,}</span><span style='color:rgba(255,255,255,0.35);font-size:11px;'> aplikasi</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# KPI
# ─────────────────────────────────────────────
st.markdown('<p class="section-title">Overview SLA</p>', unsafe_allow_html=True)

avg_sla    = df_sla["SLA_Hours"].mean()
median_sla = df_sla["SLA_Hours"].median()
min_sla    = df_sla["SLA_Hours"].min()
max_sla    = df_sla["SLA_Hours"].max()
cnt_ok     = int((df_sla["SLA_Hours"] <= 1).sum())
pct_ok     = cnt_ok / n_match * 100 if n_match else 0

k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("Total Aplikasi SLA", f"{n_match:,}")
k2.metric("Avg SLA", f"{avg_sla:.1f} Jam")
k3.metric("Median SLA", f"{median_sla:.1f} Jam")
k4.metric("Min SLA", f"{min_sla:.1f} Jam")
k5.metric("Max SLA", f"{max_sla:.1f} Jam")
k6.metric("SLA ≤ 1 Jam", f"{cnt_ok:,}", f"{pct_ok:.1f}%")

# ─────────────────────────────────────────────
# CHART: Distribusi + Kategori
# ─────────────────────────────────────────────
st.markdown('<p class="section-title">Distribusi SLA</p>', unsafe_allow_html=True)
c1, c2 = st.columns([3, 2])

with c1:
    fig_hist = px.histogram(
        df_sla[df_sla["SLA_Hours"] <= 48], x="SLA_Hours", nbins=40,
        title="Distribusi SLA (jam)", color_discrete_sequence=["#60a5fa"],
        labels={"SLA_Hours": "SLA (Jam)"}
    )
    fig_hist.update_layout(**PL)
    fig_hist.update_traces(opacity=0.8)
    st.plotly_chart(fig_hist, use_container_width=True)

with c2:
    cat = df_sla["SLA_Category"].value_counts().reindex(SLA_ORDER).dropna().reset_index()
    cat.columns = ["Kategori", "Jumlah"]
    fig_pie = go.Figure(go.Pie(
        labels=cat["Kategori"], values=cat["Jumlah"], hole=0.55,
        marker=dict(colors=[SLA_COLORS[k] for k in cat["Kategori"]]),
        textinfo="percent", textfont=dict(size=11),
    ))
    fig_pie.update_layout(**PL, title="Kategori SLA")
    fig_pie.add_annotation(text=f"<b>{n_match:,}</b>", x=0.5, y=0.5, showarrow=False,
                           font=dict(size=16, color="#fff"))
    st.plotly_chart(fig_pie, use_container_width=True)

# ─────────────────────────────────────────────
# CHART: Per Cabang
# ─────────────────────────────────────────────
if "CABANG" in df_sla.columns:
    st.markdown('<p class="section-title">SLA per Cabang</p>', unsafe_allow_html=True)
    cabang_sum = (
        df_sla.groupby("CABANG")["SLA_Hours"]
        .agg(Avg=lambda x: round(x.mean(), 2), Jumlah="count")
        .reset_index().sort_values("Avg", ascending=False).head(20)
    )
    fig_bar = px.bar(
        cabang_sum.sort_values("Avg"), x="Avg", y="CABANG", orientation="h",
        title="Avg SLA per Cabang (Top 20)", color="Avg",
        color_continuous_scale=["#34d399","#fbbf24","#f87171"],
        text="Avg", labels={"Avg": "Avg SLA (Jam)"}
    )
    fig_bar.update_traces(texttemplate="%{text:.1f}h", textposition="outside", textfont_size=10)
    fig_bar.update_layout(**PL, coloraxis_showscale=False, height=500)
    st.plotly_chart(fig_bar, use_container_width=True)

# ─────────────────────────────────────────────
# CHART: Trend Harian
# ─────────────────────────────────────────────
if df_sla["CREATED_AT"].notna().sum() > 0:
    st.markdown('<p class="section-title">Trend Harian</p>', unsafe_allow_html=True)
    daily = (
        df_sla.assign(Tanggal=df_sla["CREATED_AT"].dt.date)
        .groupby("Tanggal")["SLA_Hours"]
        .agg(Avg="mean", Count="count").reset_index()
    )
    daily["Avg"] = daily["Avg"].round(2)

    fig_trend = make_subplots(specs=[[{"secondary_y": True}]])
    fig_trend.add_trace(go.Scatter(
        x=daily["Tanggal"], y=daily["Avg"], name="Avg SLA",
        line=dict(color="#60a5fa", width=2.5), mode="lines+markers",
        marker=dict(size=5, color="#60a5fa")
    ), secondary_y=False)
    fig_trend.add_trace(go.Bar(
        x=daily["Tanggal"], y=daily["Count"], name="Jumlah Aplikasi",
        marker_color="rgba(96,165,250,0.1)", marker_line_width=0
    ), secondary_y=True)
    fig_trend.update_layout(**PL, title="Avg SLA & Volume Harian")
    fig_trend.update_yaxes(title_text="Avg SLA (Jam)", secondary_y=False, gridcolor="rgba(255,255,255,0.05)")
    fig_trend.update_yaxes(title_text="Jumlah", secondary_y=True, showgrid=False)
    st.plotly_chart(fig_trend, use_container_width=True)

# ─────────────────────────────────────────────
# TABEL
# ─────────────────────────────────────────────
st.markdown('<p class="section-title">Detail Data</p>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["SLA per APPID", "Summary per Cabang", "Duplikat APPID", "Tidak Match SLIK"])

with tab1:
    show = ["APPID","USER_NAM","CREATED_AT","CABANG","PRODUK",TIMEDONE_COL,"SLA_Hours","SLA_Minutes","SLA_Category"]
    show = [c for c in show if c in df_sla.columns]
    st.dataframe(df_sla[show].sort_values("SLA_Hours", ascending=False), use_container_width=True, hide_index=True)
    csv1 = df_sla[show].to_csv(index=False).encode()
    st.download_button(" Download SLA per APPID", csv1, "sla_per_appid.csv", "text/csv")

with tab2:
    if "CABANG" in df_sla.columns:
        summ = (
            df_sla.groupby("CABANG")["SLA_Hours"]
            .agg(Total="count", Avg=lambda x: round(x.mean(),2),
                 Median=lambda x: round(x.median(),2),
                 Min=lambda x: round(x.min(),2), Max=lambda x: round(x.max(),2))
            .reset_index().sort_values("Avg", ascending=False)
        )
        st.dataframe(summ, use_container_width=True, hide_index=True)
        csv2 = summ.to_csv(index=False).encode()
        st.download_button(" Download Summary Cabang", csv2, "summary_cabang.csv", "text/csv")

with tab3:
    # Tabel yang menunjukkan APPID dengan lebih dari 1 baris (duplikat)
    st.caption("APPID yang muncul lebih dari 1 kali di hasil join — ini yang akan hilang kalau pakai dedup")
    dup_appids = df_sla[df_sla.duplicated(subset=["APPID"], keep=False)].sort_values("APPID")
    show_dup = ["APPID","USER_NAM","CREATED_AT","CABANG",TIMEDONE_COL,"SLA_Hours","SLA_Category"]
    show_dup = [c for c in show_dup if c in dup_appids.columns]
    if len(dup_appids):
        st.info(f"{dup_appids['APPID'].nunique():,} APPID unik muncul lebih dari 1 baris ({len(dup_appids):,} baris total)")
        st.dataframe(dup_appids[show_dup], use_container_width=True, hide_index=True)

        # Perbandingan: dengan dedup vs tanpa dedup
        st.markdown("**Perbandingan hasil jika pakai dedup (ambil SLA terkecil per APPID):**")
        df_dedup = df_sla.sort_values("SLA_Hours").drop_duplicates(subset=["APPID"], keep="first")
        col_a, col_b = st.columns(2)
        col_a.metric("Tanpa Dedup (sekarang)", f"{len(df_sla):,} baris", f"Avg SLA: {df_sla['SLA_Hours'].mean():.2f} jam")
        col_b.metric("Dengan Dedup", f"{len(df_dedup):,} baris", f"Avg SLA: {df_dedup['SLA_Hours'].mean():.2f} jam")
    else:
        st.success("Tidak ada duplikat APPID — semua APPID unik.")

with tab4:
    st.caption("APPID yang ada di ONE ME tapi tidak ketemu di SLIK")
    no_match = df[~df["_slik_found"]][["APPID","USER_NAM","CREATED_AT","CABANG","PRODUK","STATUS"] if "STATUS" in df.columns else ["APPID","CREATED_AT","CABANG"]]
    no_match = no_match[[c for c in no_match.columns if c in df.columns]]
    st.info(f"{len(no_match):,} baris tidak match ke SLIK")
    st.dataframe(no_match, use_container_width=True, hide_index=True)
    csv4 = no_match.to_csv(index=False).encode()
    st.download_button(" Download Tidak Match", csv4, "tidak_match_slik.csv", "text/csv")
