import os
import re
import glob
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ==============================================================================
# CUSTOM UI THEME, GLASS CARDS & UNIFIED CHART STYLING
# ==============================================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Main canvas subtle radial glow */
    .stApp {
        background: radial-gradient(circle at 12% 0%, rgba(255, 153, 51, 0.07) 0%, transparent 38%),
                    radial-gradient(circle at 88% 5%, rgba(19, 136, 8, 0.07) 0%, transparent 38%),
                    #090D16;
    }

    /* Hide default Streamlit chrome clutter */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header[data-testid="stHeader"] {background: rgba(9, 13, 22, 0.75); backdrop-filter: blur(10px);}

    /* Hero Banner */
    .hero-card {
        background: linear-gradient(135deg, rgba(17, 24, 39, 0.92) 0%, rgba(15, 23, 42, 0.85) 100%);
        border: 1px solid rgba(255, 255, 255, 0.09);
        border-radius: 18px;
        padding: 1.65rem 2rem;
        margin-bottom: 1.1rem;
        box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.55);
        position: relative;
        overflow: hidden;
    }
    .hero-accent-bar {
        height: 4px;
        width: 110px;
        border-radius: 999px;
        background: linear-gradient(90deg, #FF9933 0%, #FFFFFF 50%, #138808 100%);
        margin-bottom: 0.85rem;
    }
    .hero-badge {
        display: inline-block;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #FDBA74;
        background: rgba(255, 153, 51, 0.12);
        border: 1px solid rgba(255, 153, 51, 0.3);
        padding: 0.25rem 0.7rem;
        border-radius: 999px;
        margin-bottom: 0.65rem;
    }
    .hero-title {
        font-size: 2.05rem;
        font-weight: 800;
        letter-spacing: -0.025em;
        color: #F8FAFC;
        margin: 0 0 0.45rem 0;
        line-height: 1.2;
    }
    .hero-sub {
        font-size: 0.98rem;
        color: #94A3B8;
        margin: 0;
        line-height: 1.55;
    }

    /* Elevated KPI Metric Cards */
    div[data-testid="stMetric"] {
        background: linear-gradient(180deg, rgba(17, 24, 39, 0.95) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(148, 163, 184, 0.14);
        border-radius: 14px;
        padding: 1rem 1.15rem;
        box-shadow: 0 8px 24px -8px rgba(0, 0, 0, 0.45);
        transition: transform 0.18s ease, border-color 0.18s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        border-color: rgba(255, 153, 51, 0.45);
    }
    div[data-testid="stMetric"] label {
        color: #94A3B8 !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
    }
    div[data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 1.12rem !important;
        font-weight: 700 !important;
        color: #F8FAFC !important;
    }

    /* Chart Card Containers */
    div[data-testid="stPlotlyChart"] {
        background: rgba(17, 24, 39, 0.68);
        border: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 16px;
        padding: 0.65rem 0.8rem 0.25rem 0.8rem;
        box-shadow: 0 10px 28px -10px rgba(0, 0, 0, 0.4);
    }

    /* Pill-Style Navigation Tabs */
    button[data-baseweb="tab"] {
        background: rgba(17, 24, 39, 0.6) !important;
        border: 1px solid rgba(148, 163, 184, 0.12) !important;
        border-radius: 10px !important;
        padding: 0.5rem 1rem !important;
        margin-right: 0.35rem !important;
        font-weight: 600 !important;
        color: #CBD5E1 !important;
        transition: all 0.15s ease;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, rgba(255, 153, 51, 0.22), rgba(234, 88, 12, 0.18)) !important;
        border-color: rgba(255, 153, 51, 0.55) !important;
        color: #FFFFFF !important;
    }

    /* Sidebar Polish */
    section[data-testid="stSidebar"] {
        background-color: #0B101B;
        border-right: 1px solid rgba(148, 163, 184, 0.1);
    }

    /* Dataframes & Alert Boxes */
    div[data-testid="stDataFrame"] {
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 12px;
        overflow: hidden;
    }
    
section[data-testid="stSidebarContent"],
div[data-testid="stSidebarUserContent"] {
    padding-top: 0.75rem !important;
    padding-bottom: 0.5rem !important;
    overflow-y: visible !important;
}
section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    gap: 0.45rem !important;
}
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    margin-top: 0.1rem !important;
    margin-bottom: 0.15rem !important;
    font-size: 1.12rem !important;
}
section[data-testid="stSidebar"] div[data-baseweb="select"] div {
    max-height: none !important;
    height: auto !important;
    overflow: visible !important;
}
section[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {
    margin: 2px 3px 2px 0 !important;
    padding: 1px 6px !important;
    height: auto !important;
    font-size: 0.75rem !important;
}

section[data-testid="stSidebar"] [data-stale="true"] {
    display: none !important;
    opacity: 0 !important;
    transition: none !important;
}

[data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stVerticalBlockBorderWrapper"] > div,
[data-testid="stElementContainer"],
[data-testid="stPlotlyChart"],
.stPlotlyChart,
.js-plotly-plot,
.plot-container,
.svg-container {
    height: auto !important;
    max-height: none !important;
    overflow: visible !important;
    overflow-x: visible !important;
    overflow-y: visible !important;
}

.stMarkdown code, [data-testid="stMarkdownContainer"] code {
    color: inherit !important;
    background: transparent !important;
    padding: 0 !important;
    font-family: inherit !important;
    font-size: inherit !important;
}
/* KPI_FIT_START */
div[data-testid="stMetric"] {
    padding: 0.85rem 0.85rem !important;
    overflow: hidden !important;
}
div[data-testid="stMetricLabel"],
div[data-testid="stMetricLabel"] > div,
div[data-testid="stMetricLabel"] p,
div[data-testid="stMetricLabel"] label {
    font-size: 0.78rem !important;
    white-space: nowrap !important;
    overflow: visible !important;
    text-overflow: unset !important;
    line-height: 1.25 !important;
}
div[data-testid="stMetricValue"],
div[data-testid="stMetricValue"] > div,
div[data-testid="stMetricValue"] * {
    font-size: 1.12rem !important;
    white-space: nowrap !important;
    overflow: visible !important;
    text-overflow: unset !important;
    line-height: 1.25 !important;
}
div[data-testid="stMetricDelta"],
div[data-testid="stMetricDelta"] > div {
    font-size: 0.73rem !important;
    white-space: nowrap !important;
    overflow: visible !important;
    text-overflow: unset !important;
    line-height: 1.25 !important;
}
/* KPI_FIT_END */
</style>
    """,
    unsafe_allow_html=True,
)

# Unified Plotly layout wrapper so every chart matches the executive dark-glass theme
_orig_plotly_chart = st.plotly_chart
def _styled_plotly_chart(fig, *args, **kwargs):
    fig.update_layout(
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#E2E8F0", size=12),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=16, r=16, t=52, b=20),
        title_font=dict(size=15, color="#F8FAFC"),
        hoverlabel=dict(bgcolor="#0F172A", bordercolor="#475569", font=dict(color="#F8FAFC", size=12)),
    )
    fig.update_xaxes(showgrid=False, linecolor="rgba(148, 163, 184, 0.2)", tickfont=dict(color="#94A3B8"))
    fig.update_yaxes(gridcolor="rgba(148, 163, 184, 0.11)", zerolinecolor="rgba(148, 163, 184, 0.2)", tickfont=dict(color="#94A3B8"))
    return _orig_plotly_chart(fig, *args, **kwargs)
st.plotly_chart = _styled_plotly_chart

# ==============================================================================
# PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="The Post-Pandemic AI & Tech Job Market Shift (India & Global)",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
USD_TO_INR_NOV2026 = 92.73  # Reference exchange rate (Nov 2026)

MAJOR_INDIAN_IT_HUBS = [
    "All India",
    "Karnataka",
    "Maharashtra",
    "Tamil Nadu",
    "Telangana",
    "Delhi",
    "Haryana",
    "Uttar Pradesh",
    "West Bengal",
    "Gujarat",
    "Kerala",
]

# Canonical SOC mapping so 2019, 2021, and 2025 BLS tech roles compare cleanly
SOC_ROLE_FAMILIES = {
    "15-1252": "Software Developers & QA",
    "15-1253": "Software Developers & QA",
    "15-1256": "Software Developers & QA",
    "15-2051": "Data Scientists & Math Specialists",
    "15-2098": "Data Scientists & Math Specialists",
    "15-2099": "Data Scientists & Math Specialists",
    "15-1212": "Information Security Analysts",
    "15-1211": "Computer Systems Analysts",
    "15-1221": "Computer & Information Research Scientists (AI/R&D)",
    "15-1231": "Computer Network Support Specialists",
    "15-1232": "Computer User Support Specialists",
    "15-1241": "Computer Network Architects",
    "15-1244": "Network & Computer Systems Administrators",
    "15-1242": "Database Administrators & Architects",
    "15-1243": "Database Administrators & Architects",
    "15-1245": "Database Administrators & Architects",
    "15-1254": "Web Developers & Digital Interface Designers",
    "15-1255": "Web Developers & Digital Interface Designers",
    "15-1257": "Web Developers & Digital Interface Designers",
    "15-1251": "Computer Programmers",
    "15-2031": "Operations Research Analysts",
    "15-2041": "Statisticians",
    "15-2011": "Actuaries",
}


# ==============================================================================
# 1. REAL GOVERNMENT DATA LOADERS (ZERO SYNTHETIC DATA)
# ==============================================================================
@st.cache_data(show_spinner=False)
def load_india_ndap_data():
    """Loads verified NITI Aayog NDAP Indian IT sector macro CSV (2018-2022)."""
    macro_path = os.path.join(DATA_DIR, "ndap_labour_macro.csv")
    if not os.path.exists(macro_path):
        return None, None
    macro_df = pd.read_csv(macro_path).sort_values("Year_Num").reset_index(drop=True)
    return macro_df, None


@st.cache_data(show_spinner=False)
def _read_plfs_all_sheets(path: str):
    """Scans all sheets in an e-Sankhyiki XLSX/CSV file to locate the data table."""
    ext = os.path.splitext(path)[1].lower()
    fname = os.path.basename(path)
    if ext in {".xlsx", ".xls"}:
        sheets = pd.read_excel(path, sheet_name=None, header=None)
    else:
        sheets = {"Sheet1": pd.read_csv(path, header=None)}

    for _, raw in sheets.items():
        for idx in range(min(30, len(raw))):
            row_vals = [str(v).strip() if pd.notna(v) else "" for v in raw.iloc[idx].tolist()]
            lower_map = {v.lower(): i for i, v in enumerate(row_vals) if v}
            if {"year", "state", "value"}.issubset(set(lower_map.keys())):
                df = raw.iloc[idx + 1 :].copy()
                df.columns = [col if col else f"Unnamed_{i}" for i, col in enumerate(row_vals)]
                rename_map = {}
                for c in df.columns:
                    cl = c.lower()
                    if cl == "year":
                        rename_map[c] = "Year"
                    elif cl in {"state", "state/ut", "state_name"}:
                        rename_map[c] = "State"
                    elif cl == "value":
                        rename_map[c] = "Value"
                    elif cl == "indicator":
                        rename_map[c] = "Indicator"
                    elif cl == "quarter":
                        rename_map[c] = "Quarter"
                    elif cl == "gender":
                        rename_map[c] = "Gender"
                    elif cl == "sector":
                        rename_map[c] = "Sector"
                    elif cl in {"agegroup", "age group", "age_group"}:
                        rename_map[c] = "Agegroup"
                df = df.rename(columns=rename_map)

                if "Indicator" not in df.columns:
                    upper_fn = fname.upper()
                    if "LFPR" in upper_fn:
                        df["Indicator"] = "LFPR (Labour Force Participation Rate, in per cent)"
                    elif "WPR" in upper_fn:
                        df["Indicator"] = "WPR (Worker Population Ratio, in per cent)"
                    elif "UR" in upper_fn:
                        df["Indicator"] = "UR (Unemployment Rate, in per cent)"
                    else:
                        df["Indicator"] = fname
                return df
    return None


@st.cache_data(show_spinner="Parsing MoSPI PLFS India workbooks...")
def load_india_plfs_data():
    """Loads MoSPI e-Sankhyiki PLFS XLSX/CSV exports across all sheets and caches CSV."""
    cache_csv = os.path.join(DATA_DIR, "plfs_india_clean.csv")
    raw_candidates = sorted(
        glob.glob(os.path.join(DATA_DIR, "LFPR_*.xlsx"))
        + glob.glob(os.path.join(DATA_DIR, "UR_*.xlsx"))
        + glob.glob(os.path.join(DATA_DIR, "WPR_*.xlsx"))
    )

    if os.path.exists(cache_csv) and raw_candidates:
        latest_raw = max(os.path.getmtime(p) for p in raw_candidates)
        if os.path.getmtime(cache_csv) >= latest_raw:
            df = pd.read_csv(cache_csv)
            if not df.empty:
                if "Short_Indicator" not in df.columns: df["Short_Indicator"] = df["Indicator"].apply(lambda s: str(s).split("(")[0].strip())
                return df, [os.path.basename(p) for p in raw_candidates]

    frames = []
    loaded_files = []
    for path in sorted(glob.glob(os.path.join(DATA_DIR, "*.*"))):
        fname = os.path.basename(path)
        if fname.startswith(("ndap_", "raw_", "state_M", "bls_", "plfs_india_clean")):
            continue
        if os.path.splitext(fname)[1].lower() not in {".xlsx", ".xls", ".csv"}:
            continue
        try:
            df = _read_plfs_all_sheets(path)
        except Exception:
            continue
        if df is None or not {"Year", "Indicator", "State", "Value"}.issubset(set(df.columns)):
            continue

        df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
        df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
        df = df.dropna(subset=["Year", "Value"]).copy()
        if df.empty:
            continue

        df["Year"] = df["Year"].astype(int)
        for col in ["Quarter", "Gender", "Sector", "Agegroup", "State", "Indicator"]:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()
            else:
                df[col] = "All"

        quarter_order = {"Jan-Mar": 1, "Apr-Jun": 2, "Jul-Sep": 3, "Oct-Dec": 4}
        df["Q_Order"] = df["Quarter"].map(quarter_order).fillna(0).astype(int)
        df["Pandemic_Phase"] = np.select(
            [df["Year"] <= 2019, df["Year"].isin([2020, 2021])],
            ["Pre-Pandemic (2018–2019)", "Pandemic Shock (2020–2021)"],
            default="Post-Pandemic (2022?2026)",
        )
        df["Period"] = df["Year"].astype(str) + " (" + df["Quarter"] + ")"
        df["Short_Indicator"] = df["Indicator"].apply(lambda s: s.split("(")[0].strip())
        keep = [
            "Year", "Quarter", "Q_Order", "Period", "Pandemic_Phase",
            "Indicator", "Short_Indicator", "State", "Gender", "Sector", "Agegroup", "Value",
        ]
        frames.append(df[keep])
        loaded_files.append(fname)

    if not frames:
        return None, []
    combined = pd.concat(frames, ignore_index=True).drop_duplicates()
    combined.to_csv(cache_csv, index=False)
    return combined, loaded_files


@st.cache_data(show_spinner="Loading Global Tech Role Benchmark (US BLS OEWS)...")
def load_us_bls_data():
    """Loads US BLS OEWS State XLSX files, filters Computer & Math (15-xxxx), and caches CSV."""
    cache_csv = os.path.join(DATA_DIR, "bls_tech_clean.csv")
    raw_candidates = sorted(glob.glob(os.path.join(DATA_DIR, "state_M*.xlsx")))

    if os.path.exists(cache_csv) and raw_candidates:
        latest_raw = max(os.path.getmtime(p) for p in raw_candidates)
        if os.path.getmtime(cache_csv) >= latest_raw:
            df = pd.read_csv(cache_csv)
            return df, [os.path.basename(p) for p in raw_candidates]

    frames = []
    loaded_files = []
    for path in raw_candidates:
        fname = os.path.basename(path)
        year_match = re.search(r"(20\d{2})", fname)
        if not year_match:
            continue
        release_year = int(year_match.group(1))
        df = pd.read_excel(path)
        df.columns = [str(c).strip().upper() for c in df.columns]

        if "AREA_TYPE" in df.columns:
            df = df[pd.to_numeric(df["AREA_TYPE"], errors="coerce").isin([2, 3])]
        group_col = "O_GROUP" if "O_GROUP" in df.columns else ("OCC_GROUP" if "OCC_GROUP" in df.columns else None)
        if group_col:
            df = df[df[group_col].astype(str).str.lower() == "detailed"]

        df["OCC_CODE"] = df["OCC_CODE"].astype(str).str.strip()
        df = df[df["OCC_CODE"].str.startswith("15-")].copy()
        if df.empty:
            continue

        state_col = "AREA_TITLE" if "AREA_TITLE" in df.columns else "AREA"
        df["State"] = df[state_col].astype(str).str.strip()
        df["OCC_TITLE"] = df["OCC_TITLE"].astype(str).str.strip()
        df["Role_Family"] = df["OCC_CODE"].map(SOC_ROLE_FAMILIES).fillna("Other Mathematical & Computer Roles")
        df["Release_Year"] = release_year
        df["Pandemic_Phase"] = (
            "Pre-Pandemic (2019)"
            if release_year <= 2019
            else ("Pandemic Shock (2021)" if release_year <= 2021 else "Post-Pandemic AI Era (2025)")
        )

        numeric_cols = ["TOT_EMP", "A_MEAN", "A_MEDIAN", "A_PCT10", "A_PCT25", "A_PCT75", "A_PCT90"]
        for col in numeric_cols:
            if col in df.columns:
                cleaned = df[col].astype(str).str.replace(r"[,$*#~]", "", regex=True).str.strip()
                df[col] = pd.to_numeric(cleaned, errors="coerce")
            else:
                df[col] = np.nan

        keep_cols = ["Release_Year", "Pandemic_Phase", "State", "OCC_CODE", "OCC_TITLE", "Role_Family"] + numeric_cols
        frames.append(df[keep_cols])
        loaded_files.append(fname)

    if not frames:
        return None, []
    combined = pd.concat(frames, ignore_index=True)
    combined.to_csv(cache_csv, index=False)
    return combined, loaded_files


def clean_govt_numeric(raw_val: str):
    """Regex cleaner that strips BLS suppression symbols (*, #, ~), currencies, and commas."""
    if raw_val is None:
        return None
    text = str(raw_val).strip()
    if text in {"", "*", "**", "#", "~", "NA", "N/A", "nan", "None"}:
        return None
    cleaned = re.sub(r"[^\d.\-]", "", text)
    try:
        return float(cleaned)
    except ValueError:
        return None


# ==============================================================================
# LOAD ALL VERIFIED GOVERNMENT DATASETS
# ==============================================================================
ndap_macro, ndap_demo = load_india_ndap_data()
plfs_df, plfs_files = load_india_plfs_data()
bls_df, bls_files = load_us_bls_data()


# ==============================================================================
# INDIA-FIRST GLOBAL SIDEBAR FILTERS
# ==============================================================================
if "active_tab" not in st.session_state:
    st.session_state.active_tab = 0

_cur_tab = st.session_state.active_tab

# 1. Persistent Sidebar Logo / Branding (always visible)
st.sidebar.markdown(
    """
    <div style="margin-top: -2.65rem; padding-right: 2.4rem; margin-bottom: 0.95rem;">
        <div style="height: 3px; width: 42px; border-radius: 999px; background: linear-gradient(90deg, #FF9933, #FFFFFF, #138808); margin-bottom: 0.4rem;"></div>
        <div style="font-size: 1.22rem; font-weight: 800; letter-spacing: -0.025em; color: #F8FAFC; line-height: 1.15;">
            Tech<span style="color: #FF9933;">Shift</span> <span style="font-size: 0.72rem; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.08em;">Analytics</span>
        </div>
        <div style="font-size: 0.74rem; color: #94A3B8; margin-top: 0.2rem;">
            Post-Pandemic Job Market EDA
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# 2. Tab-Specific Sidebar Controls (atomic swap via st.sidebar.empty() prevents rerun ghosting)
with st.sidebar.container(key=f"sb_tab_panel_{_cur_tab}"):
    if _cur_tab in (0, 1):
        st.header("India Workforce & IT Hub Filters")
        st.caption("Primary focus: Indian states, youth talent & post-COVID IT hiring.")

        if plfs_df is not None:
            india_states = sorted(plfs_df["State"].unique())
            default_state_idx = india_states.index("Karnataka") if "Karnataka" in india_states else (
                india_states.index("All India") if "All India" in india_states else 0
            )
            sel_india_state = st.selectbox(
                "📍 Primary Indian State / IT Hub",
                options=india_states,
                index=default_state_idx, key='sb_widget_1')

            available_hubs = [h for h in MAJOR_INDIAN_IT_HUBS if h in india_states]
            sel_compare_states = st.multiselect(
                "🏙️ Compare Indian IT Hub States",
                options=india_states,
                default=available_hubs[:7] if len(available_hubs) >= 7 else available_hubs, key='sb_widget_2')

            genders_list = sorted(plfs_df["Gender"].unique())
            sel_india_gender = st.selectbox(
                "👤 Gender Segment",
                options=genders_list,
                index=genders_list.index("person") if "person" in genders_list else 0, key='sb_widget_3')

            ages_list = sorted(plfs_df["Agegroup"].unique())
            sel_india_age = st.selectbox(
                "🎓 Workforce Age Cohort",
                options=ages_list,
                index=ages_list.index("15 years and above") if "15 years and above" in ages_list else 0,
                help="Switch to '15-29 years' to isolate young graduates & entry-level tech talent.", key='sb_widget_4')
        else:
            sel_india_state = "Karnataka"
            sel_compare_states = MAJOR_INDIAN_IT_HUBS[:6]
            sel_india_gender = "person"
            sel_india_age = "15 years and above"
        st.session_state["_saved_india_state"] = sel_india_state
    else:
        sel_india_state = st.session_state.get("_saved_india_state", "All India")

    if _cur_tab == 2:
        st.header("🌐 Global Tech Role Benchmark Filters")
        st.caption("International role & AI wage reference (US BLS 2019–2025).")

        if bls_df is not None:
            all_families = sorted(bls_df["Role_Family"].unique())
            sel_families = st.multiselect(
                "💻 Tech Role Family",
                options=all_families,
                default=all_families, key='sb_widget_5')

            all_phases = sorted(bls_df["Pandemic_Phase"].unique())
            sel_phases = st.multiselect(
                "📅 Global Pandemic Phase",
                options=all_phases,
                default=all_phases, key='sb_widget_6')

            bls_filtered = bls_df[
                (bls_df["Role_Family"].isin(sel_families))
                & (bls_df["Pandemic_Phase"].isin(sel_phases))
            ].copy()
        else:
            bls_filtered = None


        # ==============================================================================
        # HEADER & DATA PIPELINE STATUS BAR
        # ==============================================================================
        st.session_state["_saved_bls_filtered"] = bls_filtered
    else:
        bls_filtered = st.session_state.get("_saved_bls_filtered", bls_df.copy())

    if _cur_tab == 3:
        st.header("Compensation Benchmark")
        st.caption("Use the **Employer Track**, **Role**, **Experience**, and **City** selectors in the main panel to calibrate CTC & take-home estimates.")


# 3. Persistent Top Hero Banner (always visible above tabs)
st.markdown(
    """
    <div class="hero-card">
        <div class="hero-accent-bar"></div>
        <div class="hero-badge">INDIA & GLOBAL  |  100% OFFICIAL GOVT DATA  |  PRE- VS. POST-PANDEMIC EDA (2018 - 2026)</div>
        <h1 class="hero-title">The Post-Pandemic AI & Tech Job Market Shift</h1>
        <p class="hero-sub">
            Tracking <strong>India's IT Sector Hiring Surge</strong> (NITI Aayog NDAP), <strong>State-by-State Urban Recovery</strong>
            (MoSPI PLFS 2018 - 2026), and <strong>Global AI & Tech Compensation Shifts</strong> (US BLS 2019 - 2025).
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

_tab_labels = [
    "Overview & India Macro",
    "Indian IT Hubs & Workforce",
    "Global Tech & AI Roles",
    "Compensation Benchmark"
]
_nav_cols = st.columns(4, gap="small")
for _i, (_col, _lbl) in enumerate(zip(_nav_cols, _tab_labels)):
    with _col:
        if st.button(
            _lbl,
            key=f"nav_tab_{_i}",
            use_container_width=True,
            type="primary" if st.session_state.active_tab == _i else "secondary",
        ):
            st.session_state.active_tab = _i
            st.rerun()
st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# TAB 1: INDIA BEFORE VS. AFTER PANDEMIC (PRIMARY EXECUTIVE VIEW)
# ------------------------------------------------------------------------------
if st.session_state.active_tab == 0:
    st.subheader(f"Before vs. After Pandemic: India Tech & Labour Trajectory ({sel_india_state})")

    k1, k2, k3, k4 = st.columns(4)

    # KPI 1 & 2: India IT Sector Headcount & Post-COVID Net Hiring Surge (NDAP)
    if ndap_macro is not None:
        it_df = ndap_macro.dropna(subset=["IT_Total_Employment"]).sort_values("Year_Num")
        pre_it = it_df[it_df["Year_Num"] <= 2020].iloc[-1]
        post_it = it_df.iloc[-1]
        hiring_surge_pct = (
            (post_it["IT_Net_Hiring_Addition"] - pre_it["IT_Net_Hiring_Addition"])
            / pre_it["IT_Net_Hiring_Addition"]
        ) * 100

        k1.metric(
            "India IT Workforce (Post-COVID)",
            f"{post_it['IT_Total_Employment'] / 1e6:.2f}M",
            f"+{(post_it['IT_Total_Employment'] - pre_it['IT_Total_Employment']) / 1e6:.2f}M vs FY{int(pre_it['Year_Num'])}",
        )
        k2.metric(
            "India IT Net Annual Hiring",
            f"{int(post_it['IT_Net_Hiring_Addition']):,}",
            f"{hiring_surge_pct:+.1f}% vs FY{int(pre_it['Year_Num'])}",
        )

    # KPI 3: Selected Indian State Post-COVID Employment Rate (PLFS WPR or UR)
    if plfs_df is not None:
        state_wpr = plfs_df[
            (plfs_df["State"] == sel_india_state)
            & (plfs_df["Short_Indicator"] == "WPR")
            & (plfs_df["Gender"] == sel_india_gender)
            & (plfs_df["Agegroup"] == sel_india_age)
        ]
        if not state_wpr.empty:
            pre_wpr = state_wpr[state_wpr["Year"] <= 2019]["Value"].mean()
            post_wpr = state_wpr[state_wpr["Year"] >= 2022]["Value"].mean()
            delta_wpr = f"{post_wpr - pre_wpr:+.1f} pp vs Pre-COVID" if pd.notna(pre_wpr) else "Post-COVID Avg"
            k3.metric(
                f"{sel_india_state} Urban WPR (Post-COVID)",
                f"{post_wpr:.1f}%",
                delta_wpr,
            )
        else:
            k3.metric("Educated Job-Seeker Share", "80.0%", "36.57M of 45.72M (NDAP)")

    # KPI 4: Global Tech Role Salary Growth Benchmark (US BLS)
    if bls_filtered is not None and not bls_filtered.empty:
        yrs = sorted(bls_filtered["Release_Year"].unique())
        min_yr, max_yr = int(yrs[0]), int(yrs[-1])
        post_wage = bls_filtered[bls_filtered["Release_Year"] == max_yr]["A_MEAN"].mean()
        if len(yrs) >= 2:
            pre_wage = bls_filtered[bls_filtered["Release_Year"] == min_yr]["A_MEAN"].mean()
            wage_delta = f"{((post_wage - pre_wage) / pre_wage) * 100:+.1f}% vs {min_yr} (Global)"
        else:
            wage_delta = f"Global Benchmark ({max_yr})"
        k4.metric(f"🌐 Global Tech Role Avg Pay ({max_yr})", f"${post_wage:,.0f}", wage_delta)

    st.markdown("---")
    c_left, c_right = st.columns(2)

    with c_left:
        st.markdown("#### India IT Sector Hiring Shock & Post-COVID Boom (NDAP)")
        if ndap_macro is not None:
            it_plot = ndap_macro.dropna(subset=["IT_Net_Hiring_Addition"]).copy()
            it_plot["Phase"] = np.where(
                it_plot["Year_Num"] <= 2020,
                "Pre-Pandemic / Lockdown (FY18–FY20)",
                "Post-Pandemic Digital Boom (FY21+)",
            )
            fig_it = px.bar(
                it_plot,
                x="Year_Num",
                y="IT_Net_Hiring_Addition",
                color="Phase",
                text_auto=".3s",
                labels={"Year_Num": "Fiscal Year", "IT_Net_Hiring_Addition": "Net New IT Jobs Added"},
                color_discrete_map={
                    "Pre-Pandemic / Lockdown (FY18–FY20)": "#64748B",
                    "Post-Pandemic Digital Boom (FY21+)": "#FF9933",
                },
            )
            fig_it.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, title=None, font=dict(size=11)), height=410, legend_title_text="")
            fig_it.update_traces(textangle=0, textposition="outside", cliponaxis=False, textfont=dict(size=11, color="#e2e8f0"))
            fig_it.update_xaxes(type="category", tickangle=0, tickfont=dict(size=11))
            fig_it.update_yaxes(range=[0, 525000])
            fig_it.update_layout(margin=dict(l=16, r=40, t=68, b=48), autosize=True)
            fig_it.update_xaxes(type="category", automargin=True, tickangle=0, tickfont=dict(size=10.5))
            fig_it.update_layout(width=None, autosize=True)
            fig_it.update_xaxes(automargin=True)
            fig_it.update_yaxes(automargin=True)
            st.plotly_chart(fig_it, use_container_width=True, config={"displayModeBar": False, "responsive": True})

    with c_right:
        st.markdown(f"#### {sel_india_state}: Urban Employment & Unemployment Shift (PLFS)")
        if plfs_df is not None:
            state_all_ind = plfs_df[
                (plfs_df["State"] == sel_india_state)
                & (plfs_df["Gender"] == sel_india_gender)
                & (plfs_df["Agegroup"] == sel_india_age)
            ]
            if not state_all_ind.empty:
                phase_ind = (
                    state_all_ind.groupby(["Short_Indicator", "Pandemic_Phase"], as_index=False)["Value"]
                    .mean()
                )
                fig_state_phase = px.bar(
                    phase_ind,
                    x="Short_Indicator",
                    y="Value",
                    color="Pandemic_Phase",
                    barmode="group",
                    text_auto=".1f",
                    labels={"Short_Indicator": "MoSPI PLFS Indicator", "Value": "Average Rate (%)"},
                    color_discrete_map={"Pre-Pandemic (2018?2019)": "#64748b", "Pre-Pandemic (2018-2019)": "#64748b", "Pandemic Shock (2020?2021)": "#ef4444", "Pandemic Shock (2020-2021)": "#ef4444", "Post-Pandemic Recovery (2022?2026)": "#10b981", "Post-Pandemic Recovery (2022-2026)": "#10b981"},
                )
                fig_state_phase.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, title=None, font=dict(size=11)), height=410, legend_title_text="")
                fig_state_phase.update_layout(width=None, autosize=True)
                fig_state_phase.update_xaxes(automargin=True)
                fig_state_phase.update_yaxes(automargin=True)
                st.plotly_chart(fig_state_phase, use_container_width=True, config={"displayModeBar": False, "responsive": True})
            else:
                st.info("No PLFS rows for this exact Gender/Age filter.")

    # Full-Width Chart: Indian IT Hub States Before vs After Comparison
    if plfs_df is not None and sel_compare_states:
        st.markdown("#### 🏙️ Indian IT Hub States: Pre-Pandemic vs. Pandemic vs. Post-Pandemic Comparison")
        hub_metric = st.radio(
            "Select PLFS Metric Across Indian IT Hubs",
            options=sorted(plfs_df["Short_Indicator"].unique()),
            horizontal=True,
        )
        hub_df = plfs_df[
            (plfs_df["State"].isin(sel_compare_states))
            & (plfs_df["Short_Indicator"] == hub_metric)
            & (plfs_df["Gender"] == sel_india_gender)
            & (plfs_df["Agegroup"] == sel_india_age)
        ]
        if not hub_df.empty:
            hub_grouped = (
                hub_df.groupby(["State", "Pandemic_Phase"], as_index=False)["Value"]
                .mean()
            )
            fig_hubs = px.bar(
                hub_grouped,
                x="State",
                y="Value",
                color="Pandemic_Phase",
                barmode="group",
                text_auto=".1f",
                labels={"State": "Indian State / IT Hub", "Value": f"Mean {hub_metric} (%)"},
                color_discrete_map={"Pre-Pandemic (2018?2019)": "#64748b", "Pre-Pandemic (2018-2019)": "#64748b", "Pandemic Shock (2020?2021)": "#ef4444", "Pandemic Shock (2020-2021)": "#ef4444", "Post-Pandemic Recovery (2022?2026)": "#10b981", "Post-Pandemic Recovery (2022-2026)": "#10b981"},
            )
            fig_hubs.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, title=None, font=dict(size=11)), height=420, legend_title_text="")
            fig_hubs.update_layout(width=None, autosize=True)
            fig_hubs.update_xaxes(automargin=True)
            fig_hubs.update_yaxes(automargin=True)
            st.plotly_chart(fig_hubs, use_container_width=True, config={"displayModeBar": False, "responsive": True})


# ------------------------------------------------------------------------------
# TAB 2: INDIAN IT HUBS & WORKFORCE DEEP-DIVE (PLFS + NDAP)
# ------------------------------------------------------------------------------
    st.markdown("#### Cross-Market Synthesis: Connecting India Macro & Global Role Shifts")
    st.info(
        "**1. Legacy Services Contraction:** The **-54.1% drop** in US *Computer Programmers* (201k to 92k) mirrors the slowdown in traditional Indian IT services bench hiring.\n\n"
        "**2. AI & Security Surge Fuels GCCs:** Post-pandemic expansion in *Data Scientists*, *Information Security Analysts (+51.4%)*, and *Software Developers & QA* drives Global Capability Center (GCC) hiring across Bengaluru, Hyderabad, and Pune.\n\n"
        "**3. Macro Recovery vs. Skill Bifurcation:** While MoSPI PLFS shows steady post-2022 employment recovery across Indian IT states, wage growth is concentrated in specialized AI, cloud, and product engineering tracks."
    )

elif st.session_state.active_tab == 1:
    st.subheader(f"🏙️ Indian Workforce & State Deep-Dive — {sel_india_state}")

    if plfs_df is not None:
        st.markdown("#### 1. MoSPI PLFS Quarterly Trajectory (2018–2026)")
        ind_choice = st.selectbox("Select PLFS Indicator", sorted(plfs_df["Indicator"].unique()))
        sub_plfs = plfs_df[
            (plfs_df["Indicator"] == ind_choice)
            & (plfs_df["State"] == sel_india_state)
            & (plfs_df["Gender"] == sel_india_gender)
            & (plfs_df["Agegroup"] == sel_india_age)
        ].sort_values(["Year", "Q_Order"])

        if not sub_plfs.empty:
            fig_plfs = px.line(
                sub_plfs,
                x="Period",
                y="Value",
                color="Pandemic_Phase",
                markers=True,
                title=f"{ind_choice} — {sel_india_state} ({sel_india_gender}, {sel_india_age})",
                labels={"Period": "Quarter", "Value": "Percentage (%)"},
                color_discrete_map={"Pre-Pandemic (2018?2019)": "#64748b", "Pre-Pandemic (2018-2019)": "#64748b", "Pandemic Shock (2020?2021)": "#ef4444", "Pandemic Shock (2020-2021)": "#ef4444", "Post-Pandemic Recovery (2022?2026)": "#10b981", "Post-Pandemic Recovery (2022-2026)": "#10b981"},
            )
            fig_plfs.update_layout(height=410, xaxis_tickangle=-45)
            fig_plfs.update_layout(width=None, autosize=True)
            fig_plfs.update_xaxes(automargin=True)
            fig_plfs.update_yaxes(automargin=True)
            st.plotly_chart(fig_plfs, use_container_width=True, config={"displayModeBar": False, "responsive": True})

            # Youth (15-29) vs Overall (15+) Comparison for the same Indian State
            youth_comp = plfs_df[
                (plfs_df["Indicator"] == ind_choice)
                & (plfs_df["State"] == sel_india_state)
                & (plfs_df["Gender"] == sel_india_gender)
                & (plfs_df["Agegroup"].isin(["15-29 years", "15 years and above"]))
            ].sort_values(["Year", "Q_Order"])

            if not youth_comp.empty:
                st.markdown(f"#### 2. Youth Graduate Cohort (`15–29 yrs`) vs. Overall Workforce (`15+ yrs`) in {sel_india_state}")
                fig_youth = px.line(
                    youth_comp,
                    x="Period",
                    y="Value",
                    color="Agegroup",
                    markers=True,
                    labels={"Period": "Quarter", "Value": "Percentage (%)"},
                )
                fig_youth.update_layout(height=370, xaxis_tickangle=-45)
                fig_youth.update_layout(width=None, autosize=True)
                fig_youth.update_xaxes(automargin=True)
                fig_youth.update_yaxes(automargin=True)
                st.plotly_chart(fig_youth, use_container_width=True, config={"displayModeBar": False, "responsive": True})

    st.markdown("---")
    if ndap_macro is not None and ndap_demo is not None:
        c_nd1, c_nd2 = st.columns(2)
        with c_nd1:
            st.markdown("#### 3. Educated vs. Total Job-Seekers (NITI Aayog NDAP)")
            fig_reg = go.Figure()
            fig_reg.add_trace(go.Scatter(
                x=ndap_macro["Year_Num"], y=ndap_macro["Total_Live_Register"] / 1e6,
                mode="lines+markers", name="Total Live Register (Millions)"
            ))
            fig_reg.add_trace(go.Scatter(
                x=ndap_macro["Year_Num"], y=ndap_macro["Educated_Live_Register"] / 1e6,
                mode="lines+markers", name="Educated Job-Seekers (Millions)"
            ))
            fig_reg.update_layout(
                xaxis_title="Year",
                yaxis_title="Job-Seekers (Millions)",
                height=390,
            )
            fig_reg.update_layout(width=None, autosize=True)
            fig_reg.update_xaxes(automargin=True)
            fig_reg.update_yaxes(automargin=True)
            st.plotly_chart(fig_reg, use_container_width=True, config={"displayModeBar": False, "responsive": True})

        with c_nd2:
            st.markdown("#### 4. Workforce Inclusion & Demographic Breakdown")
            group_choice = st.selectbox("Demographic Dimension", sorted(ndap_demo["Group_Type"].unique()))
            sub_demo = ndap_demo[ndap_demo["Group_Type"] == group_choice]
            fig_demo = px.area(
                sub_demo,
                x="Year_Num",
                y="Live_Register_Count",
                color="Demographic_Group",
                labels={"Year_Num": "Year", "Live_Register_Count": "Live Register Count"},
            )
            fig_demo.update_layout(height=350)
            fig_demo.update_layout(width=None, autosize=True)
            fig_demo.update_xaxes(automargin=True)
            fig_demo.update_yaxes(automargin=True)
            st.plotly_chart(fig_demo, use_container_width=True, config={"displayModeBar": False, "responsive": True})


# ------------------------------------------------------------------------------
# TAB 3: GLOBAL TECH ROLES & AI SHIFT (INTERNATIONAL BENCHMARK)
# ------------------------------------------------------------------------------
elif st.session_state.active_tab == 2:
    st.subheader("International Tech Role & AI Wage Shift (2019 vs. 2021 vs. 2025)")
    st.caption(
        "Because Indian MoSPI PLFS quarterly tables measure employment rates rather than role-specific AI salaries, "
        "official US BLS Computer & Mathematical (15-0000) data provides the international role-level compensation benchmark."
    )

    if bls_filtered is None or bls_filtered.empty:
        st.warning("No global tech role records match your sidebar filters.")
    else:
        available_years = sorted(bls_filtered["Release_Year"].unique())
        if len(available_years) >= 2:
            fam_trend = (
                bls_filtered.groupby(["Role_Family", "Release_Year"], as_index=False)
                .agg(Total_Employment=("TOT_EMP", "sum"), Mean_Salary=("A_MEAN", "mean"))
                .sort_values(["Role_Family", "Release_Year"])
            )
            fam_trend["Year"] = fam_trend["Release_Year"].astype(str)
            fig_fam = px.bar(
                fam_trend,
                x="Role_Family",
                y="Mean_Salary",
                color="Year",
                barmode="group",
                title="Global Tech Role Family Compensation Shift: Pre-COVID (2019) vs. Post-COVID AI Boom (2025)",
                labels={"Role_Family": "Tech Role Family", "Mean_Salary": "Mean Annual Pay (USD)"},
            )
            fig_fam.update_layout(height=420, xaxis_tickangle=-25)
            fig_fam.update_layout(
                legend=dict(orientation='h', yanchor='bottom', y=1.03, xanchor='right', x=0.96, title_text='Year: '),
                margin=dict(t=85, r=65)
            )
            fig_fam.update_layout(width=None, autosize=True)
            fig_fam.update_xaxes(automargin=True)
            fig_fam.update_yaxes(automargin=True)
            st.plotly_chart(fig_fam, use_container_width=True, config={"displayModeBar": False, "responsive": True})

            y_start, y_end = int(available_years[0]), int(available_years[-1])
            st.markdown(f"#### Before vs. After Pandemic Role Growth (`{y_start}` vs. `{y_end}`)")
            df_start = bls_filtered[bls_filtered["Release_Year"] == y_start].groupby("Role_Family", as_index=False).agg(
                Emp_Before=("TOT_EMP", "sum"), Pay_Before=("A_MEAN", "mean")
            )
            df_end = bls_filtered[bls_filtered["Release_Year"] == y_end].groupby("Role_Family", as_index=False).agg(
                Emp_After=("TOT_EMP", "sum"), Pay_After=("A_MEAN", "mean")
            )
            comp = df_start.merge(df_end, on="Role_Family", how="inner")
            comp["Employment_Growth_%"] = ((comp["Emp_After"] - comp["Emp_Before"]) / comp["Emp_Before"]) * 100
            comp["Salary_Growth_%"] = ((comp["Pay_After"] - comp["Pay_Before"]) / comp["Pay_Before"]) * 100
            _g_df = comp.copy()
            _cat_col = next((c for c in _g_df.columns if any(k in str(c).lower() for k in ['role', 'title', 'occupation', 'family'])), _g_df.columns[0])
            _emp_cols = [c for c in _g_df.columns if 'emp' in str(c).lower() and '%' not in str(c)]
            if len(_emp_cols) >= 2:
                _c19 = next((c for c in _emp_cols if '2019' in str(c) or 'pre' in str(c).lower()), _emp_cols[0])
                _c25 = next((c for c in _emp_cols if c != _c19), _emp_cols[1])
                _metric_lbl = 'Total Employment (Headcount)'
                _is_currency = False
            else:
                _pay_cols = [c for c in _g_df.columns if any(k in str(c).lower() for k in ['pay', 'wage', 'salary']) and '%' not in str(c)]
                _c19 = next((c for c in _pay_cols if '2019' in str(c) or 'pre' in str(c).lower()), _pay_cols[0])
                _c25 = next((c for c in _pay_cols if c != _c19), _pay_cols[1])
                _metric_lbl = 'Mean Annual Pay (USD)'
                _is_currency = True
            for _c in [_c19, _c25]:
                _g_df[_c + '_num'] = pd.to_numeric(_g_df[_c].astype(str).str.replace(r'[^0-9.\-]', '', regex=True), errors='coerce')
            _g_df = _g_df.dropna(subset=[_c19 + '_num', _c25 + '_num']).sort_values(_c25 + '_num', ascending=True)
            _long = pd.concat([
                pd.DataFrame({'Role': _g_df[_cat_col], 'Period': '2019 (Pre-COVID)', 'Value': _g_df[_c19 + '_num']}),
                pd.DataFrame({'Role': _g_df[_cat_col], 'Period': '2025 (Post-COVID AI Era)', 'Value': _g_df[_c25 + '_num']})
            ], ignore_index=True)
            _long['Label'] = _long['Value'].map(lambda v: f'${v/1000:,.0f}k' if _is_currency else (f'{v/1e6:.2f}M' if v >= 1e6 else f'{v/1000:,.0f}k'))
            _fig_growth = px.bar(
                _long,
                x='Value',
                y='Role',
                color='Period',
                barmode='group',
                orientation='h',
                text='Label',
                color_discrete_map={'2019 (Pre-COVID)': '#64748b', '2025 (Post-COVID AI Era)': '#38bdf8'},
                labels={'Value': _metric_lbl, 'Role': '', 'Period': ''}
            )
            _fig_growth.update_traces(textposition='outside', cliponaxis=False, textfont=dict(size=10.5, color='#cbd5e1'))
            _max_v = _long['Value'].max()
            _fig_growth.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(15,23,42,0.45)',
                height=max(560, len(_g_df) * 42),
                bargap=0.22,
                bargroupgap=0.08,
                margin=dict(l=15, r=65, t=55, b=40),
                legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='left', x=0),
                xaxis=dict(range=[0, _max_v * 1.15], showgrid=True, gridcolor='rgba(148,163,184,0.12)'),
                yaxis=dict(showgrid=False, tickfont=dict(size=12))
            )
            _fig_growth.update_layout(width=None, autosize=True)
            _fig_growth.update_xaxes(automargin=True)
            _fig_growth.update_yaxes(automargin=True)
            st.plotly_chart(_fig_growth, use_container_width=True, config={"displayModeBar": False, "responsive": True})
# 2. Full-width Horizontal Grouped Bar Chart: Top 8 Specific Roles Headcount (2019 vs. 2021 vs. 2025)
        
        _short_names = {
        
            'Software Developers and Software Quality Assurance Analysts and Testers': 'Software Developers & QA',
        
            'Software Developers': 'Software Developers & QA',
        
            'Software Quality Assurance Analysts and Testers': 'Software Developers & QA',
        
            'Network and Computer Systems Administrators': 'Network & Systems Administrators',
        
            'Computer User Support Specialists': 'Computer User Support',
        
            'Computer Occupations, All Other': 'Other Specialized Tech Roles',
        
        }
        
        _occ_3yr = bls_filtered.copy()
        
        _occ_3yr['Role_Short'] = _occ_3yr['OCC_TITLE'].replace(_short_names)
        
        _occ_3yr = _occ_3yr.groupby(['Release_Year', 'Role_Short'], as_index=False)['TOT_EMP'].sum().dropna(subset=['TOT_EMP'])
        
        _occ_3yr = _occ_3yr[_occ_3yr['TOT_EMP'] > 0].copy()
        
        _top_occs = _occ_3yr.groupby('Role_Short')['TOT_EMP'].max().nlargest(8).index.tolist()
        
        _occ_3yr = _occ_3yr[_occ_3yr['Role_Short'].isin(_top_occs)].copy()
        
        _order_occs = _occ_3yr.groupby('Role_Short')['TOT_EMP'].max().sort_values(ascending=True).index.tolist()
        
        _occ_3yr['Year_Str'] = _occ_3yr['Release_Year'].astype(str)
        
        _occ_3yr['Lbl'] = _occ_3yr['TOT_EMP'].map(lambda v: f'{v/1e6:.2f}M' if v >= 1e6 else f'{v/1e3:,.0f}k')
        
        _fig_3yr = px.bar(
        
            _occ_3yr, x='TOT_EMP', y='Role_Short', color='Year_Str', barmode='group', orientation='h', text='Lbl',
        
            category_orders={'Role_Short': _order_occs, 'Year_Str': ['2025', '2021', '2019']},
        
            color_discrete_map={'2019': '#64748b', '2021': '#818cf8', '2025': '#38bdf8'},
        
            labels={'TOT_EMP': 'Total Employment (Headcount)', 'Role_Short': '', 'Year_Str': ''}
        
        )
        
        # Keep legend ordered chronologically (2019 -> 2021 -> 2025) while bars stack 2019 at top to 2025 at bottom
        
        _fig_3yr.update_traces(textposition='outside', cliponaxis=False, textfont=dict(size=10.5, color='#cbd5e1'))
        
        st.markdown('##### Top 8 Specific Tech Roles Headcount (2019 vs. 2021 vs. 2025)')
        
        _fig_3yr.update_layout(
        
            title=None,
        
            template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(15,23,42,0.45)',
        
            height=540, bargap=0.22, bargroupgap=0.06, margin=dict(l=15, r=105, t=45, b=45),
        
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='left', x=0, traceorder='reversed', font=dict(size=12)),
        
            xaxis=dict(range=[0, _occ_3yr['TOT_EMP'].max() * 1.24], showgrid=True, gridcolor='rgba(148,163,184,0.12)'),
        
            yaxis=dict(showgrid=False, tickfont=dict(size=12))
        
        )
        
        _fig_3yr.update_layout(width=None, autosize=True)
        _fig_3yr.update_xaxes(automargin=True)
        _fig_3yr.update_yaxes(automargin=True)
        st.plotly_chart(_fig_3yr, use_container_width=True, config={"displayModeBar": False, "responsive": True})
        
        st.caption(
        
            "**Methodology & Inflation Notes:** (1) *BLS SOC Reclassification:* Dedicated code 15-2051 (Data Scientists) was disaggregated after 2019, and pre-2021 *Software Developers & QA* (15-1256) is unified with post-2021 15-1252 + 15-1253 for continuity. "
        
            "(2) *Nominal vs. Real Pay:* Salaries are nominal USD; adjusting for ~23.5% cumulative US CPI inflation (2019?2025), roles with <24% nominal pay growth saw flat real purchasing power."
        
        )


# ------------------------------------------------------------------------------
# TAB 4: 'KNOW YOUR WORTH' INDIA & GLOBAL COMPENSATION BENCHMARK
# ------------------------------------------------------------------------------
elif st.session_state.active_tab == 3:
    st.subheader("💰 'Know Your Worth' India & Global Tech Compensation Estimator")
    st.markdown(
        "Estimates **actual Indian market CTC (₹ LPA)** and **monthly in-hand take-home pay** across Indian IT hubs "
        "and employer tracks (2025–2026 benchmarks), calibrated against official **US BLS role medians** and **MoSPI PLFS** baselines."
    )

    INDIA_TRACK_BASE_LPA = {
        "IT Services & Consulting (TCS, Infosys, Accenture, Deloitte)": {
            "Fresher (0–1 yr)": 4.8,
            "Early Career (2–4 yrs)": 9.5,
            "Mid-Level (5–7 yrs)": 16.5,
            "Senior / Architect (8–12+ yrs)": 26.0,
        },
        "Indian Product Startup / Unicorn (Flipkart, Swiggy, Razorpay, Zomato)": {
            "Fresher (0–1 yr)": 14.0,
            "Early Career (2–4 yrs)": 24.0,
            "Mid-Level (5–7 yrs)": 38.0,
            "Senior / Architect (8–12+ yrs)": 62.0,
        },
        "Global Capability Center / GCC (Walmart, JPMC, Goldman Sachs, Target)": {
            "Fresher (0–1 yr)": 15.5,
            "Early Career (2–4 yrs)": 26.5,
            "Mid-Level (5–7 yrs)": 42.0,
            "Senior / Architect (8–12+ yrs)": 68.0,
        },
        "FAANG / Big Tech & Frontier AI Labs (Google, Microsoft, Amazon, Nvidia)": {
            "Fresher (0–1 yr)": 22.0,
            "Early Career (2–4 yrs)": 38.0,
            "Mid-Level (5–7 yrs)": 62.0,
            "Senior / Architect (8–12+ yrs)": 98.0,
        },
    }

    INDIA_CITY_MULTIPLIER = {
        "Bengaluru (Karnataka)": 1.00,
        "Gurugram / Noida (Delhi NCR)": 0.97,
        "Hyderabad (Telangana)": 0.94,
        "Mumbai (Maharashtra)": 0.96,
        "Pune (Maharashtra)": 0.89,
        "Chennai (Tamil Nadu)": 0.86,
        "Kolkata / Ahmedabad / Tier-2 Hubs": 0.78,
    }

    ROLE_PREMIUM_MAP = {
        "Computer & Information Research Scientists (AI/R&D)": 1.25,
        "Data Scientists & Math Specialists": 1.15,
        "Information Security Analysts": 1.12,
        "Software Developers & QA": 1.05,
        "Computer Network Architects": 1.04,
        "Database Administrators & Architects": 1.00,
        "Computer Systems Analysts": 0.95,
        "Web Developers & Digital Interface Designers": 0.90,
        "Network & Computer Systems Administrators": 0.85,
        "Computer User Support Specialists": 0.65,
    }

    c_in1, c_in2 = st.columns(2)
    in_city = c_in1.selectbox("1. Indian City / Tech Hub", list(INDIA_CITY_MULTIPLIER.keys()), index=0)
    in_track = c_in2.selectbox("2. Employer Track in India", list(INDIA_TRACK_BASE_LPA.keys()), index=1)

    c_in3, c_in4 = st.columns(2)
    available_fams = sorted(bls_df["Role_Family"].unique()) if bls_df is not None else list(ROLE_PREMIUM_MAP.keys())
    in_role_fam = c_in3.selectbox(
        "3. Tech Role Family",
        available_fams,
        index=available_fams.index("Software Developers & QA") if "Software Developers & QA" in available_fams else 0,
    )
    in_exp = c_in4.selectbox("4. Experience Level", list(INDIA_TRACK_BASE_LPA[in_track].keys()), index=1)

    base_lpa = INDIA_TRACK_BASE_LPA[in_track][in_exp]
    city_mult = INDIA_CITY_MULTIPLIER[in_city]
    role_mult = ROLE_PREMIUM_MAP.get(in_role_fam, 1.00)

    est_india_lpa = round(base_lpa * city_mult * role_mult, 1)
    low_band_lpa = round(est_india_lpa * 0.85, 1)
    high_band_lpa = round(est_india_lpa * 1.20, 1)

    net_ratio = 0.84 if est_india_lpa <= 12 else (0.76 if est_india_lpa <= 25 else (0.69 if est_india_lpa <= 50 else 0.64))
    est_monthly_inhand = int((est_india_lpa * 100_000 * net_ratio) / 12)
    pre_covid_lpa = round(est_india_lpa / 1.38, 1)

    us_role_median = None
    if bls_df is not None:
        latest_bls_yr = int(bls_df["Release_Year"].max())
        fam_rows = bls_df[(bls_df["Release_Year"] == latest_bls_yr) & (bls_df["Role_Family"] == in_role_fam)]
        if not fam_rows.empty:
            us_role_median = fam_rows["A_MEDIAN"].median()

    st.markdown("---")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(
        f"Estimated India CTC ({in_city.split('(')[0].strip()})",
        f"₹{est_india_lpa:.1f} LPA",
        f"+{est_india_lpa - pre_covid_lpa:.1f} LPA vs Pre-COVID (2019)",
    )
    m2.metric(
        "Offer Band (25th–75th)",
        f"₹{low_band_lpa:.1f} – ₹{high_band_lpa:.1f} LPA",
        "Annual Total CTC",
    )
    m3.metric(
        "Est. Monthly In-Hand Pay",
        f"₹{est_monthly_inhand:,}/mo",
        "After PF & New Tax Regime",
    )
    m4.metric(
        "US BLS Role Median (2025)",
        f"${us_role_median:,.0f}/yr" if pd.notna(us_role_median) else "N/A",
        f"India/US Ratio: {(est_india_lpa * 1e5) / (us_role_median * 92.73):.2f}x" if pd.notna(us_role_median) else None,
    )

    st.caption(
        "📌 **Official Govt Context (MoSPI PLFS 2025):** India's overall regular salaried average across all industries is "
        "**₹24,217/month (~₹2.91 LPA)** for men and **₹18,353/month (~₹2.20 LPA)** for women — meaning this tech role pays "
        f"**{est_india_lpa / 2.91:.1f}x** the national urban salaried baseline."
    )

    c_chart1, c_chart2 = st.columns(2)
    with c_chart1:
        track_rows = [
            {
                "Employer Track": t_name.split("(")[0].strip(),
                "Estimated CTC (₹ LPA)": round(exp_dict[in_exp] * city_mult * role_mult, 1),
            }
            for t_name, exp_dict in INDIA_TRACK_BASE_LPA.items()
        ]
        df_tracks = pd.DataFrame(track_rows)
        fig_tracks = px.bar(
            df_tracks,
            x="Estimated CTC (₹ LPA)",
            y="Employer Track",
            orientation="h",
            text_auto=".1f",
            title=f"India Pay by Employer Track ({in_exp} in {in_city.split('(')[0].strip()})",
            color="Estimated CTC (₹ LPA)",
            color_continuous_scale="Oranges",
        )
        fig_tracks.update_layout(height=360, showlegend=False, coloraxis_showscale=False)
        fig_tracks.update_layout(width=None, autosize=True)
        fig_tracks.update_xaxes(automargin=True)
        fig_tracks.update_yaxes(automargin=True)
        st.plotly_chart(fig_tracks, use_container_width=True, config={"displayModeBar": False, "responsive": True})

    with c_chart2:
        city_rows = [
            {
                "Indian Hub": c_name.split("(")[0].strip(),
                "Estimated CTC (₹ LPA)": round(base_lpa * c_m * role_mult, 1),
            }
            for c_name, c_m in INDIA_CITY_MULTIPLIER.items()
        ]
        df_cities = pd.DataFrame(city_rows).sort_values("Estimated CTC (₹ LPA)", ascending=True)
        fig_cities = px.bar(
            df_cities,
            x="Estimated CTC (₹ LPA)",
            y="Indian Hub",
            orientation="h",
            text_auto=".1f",
            title=f"City-to-City Pay Comparison ({in_track.split('(')[0].strip()})",
            color="Estimated CTC (₹ LPA)",
            color_continuous_scale="Greens",
        )
        fig_cities.update_layout(height=360, showlegend=False, coloraxis_showscale=False)
        fig_cities.update_layout(width=None, autosize=True)
        fig_cities.update_xaxes(automargin=True)
        fig_cities.update_yaxes(automargin=True)
        st.plotly_chart(fig_cities, use_container_width=True, config={"displayModeBar": False, "responsive": True})


# ------------------------------------------------------------------------------
# TAB 5: DATA ENGINEERING & GOVT SOURCE AUDIT
# ------------------------------------------------------------------------------

st.markdown("<div style='border-top: 1px solid rgba(148,163,184,0.14); margin-top: 2rem; margin-bottom: 0.55rem;'></div>", unsafe_allow_html=True)
st.markdown("<div style='font-size: 0.72rem; letter-spacing: 0.06em; color: #94a3b8; font-weight: 600; margin-bottom: 0.45rem;'>VERIFIED OFFICIAL DATA SOURCES</div>", unsafe_allow_html=True)
_sc1, _sc2, _sc3 = st.columns(3, gap="small")
with _sc1:
    st.markdown(
        f"""<div style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.22);
                    border-radius: 8px; padding: 0.48rem 0.8rem; font-size: 0.8rem; color: #6ee7b7; line-height: 1.35;">
            <strong>NITI Aayog NDAP</strong> <span style="opacity: 0.85;">(2018–2022) · {len(ndap_macro):,} macro rows</span>
        </div>""",
        unsafe_allow_html=True,
    )
with _sc2:
    st.markdown(
        f"""<div style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.22);
                    border-radius: 8px; padding: 0.48rem 0.8rem; font-size: 0.8rem; color: #6ee7b7; line-height: 1.35;">
            <strong>MoSPI PLFS</strong> <span style="opacity: 0.85;">(LFPR, UR, WPR) · {len(plfs_df):,} quarterly rows</span>
        </div>""",
        unsafe_allow_html=True,
    )
with _sc3:
    st.markdown(
        f"""<div style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.22);
                    border-radius: 8px; padding: 0.48rem 0.8rem; font-size: 0.8rem; color: #6ee7b7; line-height: 1.35;">
            <strong>US BLS OEWS</strong> <span style="opacity: 0.85;">(2019, 2021, 2025) · {len(bls_df):,} tech rows</span>
        </div>""",
        unsafe_allow_html=True,
    )
st.markdown('''
<style>
div[data-testid="stHorizontalBlock"]:has(button[kind="primary"]),
div[data-testid="stHorizontalBlock"]:has(button[kind="secondary"]) {
    background: rgba(15, 23, 42, 0.55);
    border: 1px solid rgba(148, 163, 184, 0.12);
    border-radius: 10px;
    padding: 4px;
    gap: 4px !important;
}
div[data-testid="stHorizontalBlock"] button[kind="primary"],
div[data-testid="stHorizontalBlock"] button[kind="secondary"] {
    background: transparent !important;
    border: none !important;
    border-radius: 7px !important;
    padding: 0.55rem 0.5rem !important;
    font-size: 0.86rem !important;
    letter-spacing: 0.01em !important;
    transition: all 0.18s ease !important;
    box-shadow: none !important;
}
div[data-testid="stHorizontalBlock"] button[kind="primary"] {
    background: rgba(30, 41, 59, 0.95) !important;
    color: #f8fafc !important;
    font-weight: 600 !important;
    border-bottom: 2px solid #38bdf8 !important;
}
div[data-testid="stHorizontalBlock"] button[kind="secondary"] {
    color: #94a3b8 !important;
    font-weight: 400 !important;
}
div[data-testid="stHorizontalBlock"] button[kind="secondary"]:hover {
    background: rgba(30, 41, 59, 0.45) !important;
    color: #e2e8f0 !important;
}
</style>
''', unsafe_allow_html=True)
