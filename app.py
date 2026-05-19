import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from io import BytesIO
import base64
import os

# ─────────────────────────────────────────────
# SHINGDA BRAND DESIGN SYSTEM
# Sunshine Yellow: #f3d03e  (Pantone 129 C)
# Dark Grey:       #707372  (Pantone 424 C)
# Black:           #1a1a1a  (Process Black C)
# Font: Helvetica Neue / Arial
# ─────────────────────────────────────────────
BRAND_YELLOW   = "#f3d03e"
BRAND_GREY     = "#707372"
BRAND_BLACK    = "#1a1a1a"
BRAND_YELLOW_D = "#d4b900"   # darker gold for contrast / hover
BRAND_YELLOW_L = "#fffbea"   # light yellow for card backgrounds
BRAND_PALETTE  = [
    BRAND_YELLOW, BRAND_GREY, BRAND_BLACK,
    BRAND_YELLOW_D, "#a8a8a8", "#8c7a00", "#5a5a5a", "#fef5c0",
]

pio.templates["shingda"] = go.layout.Template(
    layout=go.Layout(
        colorway=BRAND_PALETTE,
        font=dict(family="Helvetica Neue, Arial, sans-serif", color=BRAND_BLACK),
        paper_bgcolor="white",
        plot_bgcolor="white",
    )
)
pio.templates.default = "plotly_white+shingda"

# ── Load company logo images ──
def _load_img_b64(filename):
    """Load an image from the same folder as app.py and return base64 string."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    for name in [filename, filename.lower(), filename.upper()]:
        path = os.path.join(base_dir, name)
        if os.path.exists(path):
            with open(path, "rb") as f:
                return base64.b64encode(f.read()).decode()
    return None

# Top.png  — full vertical logo (S-mark + SHINGDA 昇達 + GROUP OF COMPANIES)
LOGO_B64   = _load_img_b64("Top.png")   or _load_img_b64("Logo.png")
# Bottom.png — horizontal division strip (all subsidiaries)
BOTTOM_B64 = _load_img_b64("Bottom.png")

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Diesel Consumption Dashboard",
    page_icon="⛽",
    layout="wide",
)

# ─────────────────────────────────────────────
# WEBSITE DESIGN THEME — SHINGDA BRAND
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ═══════════════════════════════════════════════════════════
   SHINGDA DIESEL DASHBOARD — CORPORATE WEBSITE DESIGN THEME
   Sunshine Yellow #f3d03e | Dark Grey #707372 | Black #1a1a1a
   ═══════════════════════════════════════════════════════════ */

/* Global font — targeted only, avoids breaking Streamlit icon rendering */
html, body, [class*="css"] {
    font-family: 'Helvetica Neue', Arial, sans-serif !important;
}
.stMarkdown, .stText, p, h1, h2, h3, h4, h5,
[data-testid="stMetricLabel"], [data-testid="stMetricValue"],
[data-testid="stMetricDelta"] {
    font-family: 'Helvetica Neue', Arial, sans-serif !important;
}

/* ── Page background: warm corporate off-white ── */
.stApp {
    background-color: #edeae4 !important;
}
.main .block-container {
    padding-top: 0 !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    padding-bottom: 3rem !important;
    max-width: 100% !important;
}

/* ── Tabs: dark nav-bar style with yellow active ── */
.stTabs [data-baseweb="tab-list"] {
    background: #2a2a2a !important;
    border-radius: 8px 8px 0 0 !important;
    padding: 0 12px !important;
    gap: 2px !important;
    border-bottom: none !important;
}
.stTabs [data-baseweb="tab"] {
    color: #909090 !important;
    padding: 10px 15px !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 0.4px !important;
    border-radius: 5px 5px 0 0 !important;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    background: #f3d03e !important;
    color: #1a1a1a !important;
}
.stTabs [data-baseweb="tab-highlight"] {
    background: transparent !important;
    height: 0 !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: white !important;
    border-radius: 0 0 8px 8px !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.09) !important;
}
.stTabs [data-baseweb="tab-panel"] > div {
    padding: 24px !important;
}

/* ── Metric cards: white with yellow top accent ── */
[data-testid="metric-container"] {
    background: white !important;
    border: none !important;
    border-top: 3px solid #f3d03e !important;
    border-radius: 6px !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.09) !important;
    padding: 14px 18px 12px 18px !important;
}
[data-testid="stMetricLabel"] p {
    color: #707372 !important;
    font-size: 10px !important;
    letter-spacing: 0.8px !important;
    text-transform: uppercase !important;
    font-weight: 600 !important;
}
[data-testid="stMetricValue"] {
    color: #1a1a1a !important;
    font-weight: 700 !important;
}

/* ── Sidebar: clean white with shadow ── */
[data-testid="stSidebar"] {
    background: white !important;
    border-right: none !important;
    box-shadow: 4px 0 24px rgba(0,0,0,0.13) !important;
}
[data-testid="stSidebar"] > div:first-child {
    border-top: 4px solid #f3d03e !important;
}

/* ── Upload boxes ── */
[data-testid="stFileUploader"] {
    background: white !important;
    border-radius: 8px !important;
    padding: 8px 14px !important;
    box-shadow: 0 1px 6px rgba(0,0,0,0.07) !important;
}

/* ── Upload section background ── */
.stMarkdown + div [data-testid="stVerticalBlock"] {
    background: white;
}

/* ── Download buttons → brand yellow ── */
.stDownloadButton > button {
    background-color: #f3d03e !important;
    color: #1a1a1a !important;
    border: none !important;
    font-weight: 700 !important;
    border-radius: 6px !important;
    letter-spacing: 0.3px !important;
    padding: 8px 22px !important;
    box-shadow: 0 2px 6px rgba(243,208,62,0.4) !important;
}
.stDownloadButton > button:hover {
    background-color: #d4b900 !important;
    box-shadow: 0 4px 12px rgba(243,208,62,0.5) !important;
}

/* ── Info / success / warning banners ── */
[data-testid="stAlert"] {
    border-radius: 6px !important;
    border-left-width: 4px !important;
}

/* ── Dividers ── */
hr {
    border: none !important;
    border-top: 1px solid #d6d2cc !important;
    margin: 20px 0 !important;
    opacity: 1 !important;
}

/* ── Subheaders ── */
h1, h2, h3, h4 {
    color: #1a1a1a !important;
    letter-spacing: 0.3px !important;
}

/* ── Dataframes ── */
[data-testid="stDataFrame"] {
    border-radius: 8px !important;
    overflow: hidden !important;
    box-shadow: 0 1px 6px rgba(0,0,0,0.07) !important;
}

/* ── Expanders (sidebar filters) ── */
.streamlit-expanderHeader {
    background: #f8f6f2 !important;
    border-radius: 6px !important;
}

/* ── Number inputs, selectboxes ── */
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input {
    border-radius: 6px !important;
    border-color: #d6d2cc !important;
}
</style>
""", unsafe_allow_html=True)

# ── Website-style nav bar (dark, full-width, with logo) ───────────────────────
if LOGO_B64:
    _nav_logo_html = (
        f'<img src="data:image/png;base64,{LOGO_B64}" '
        f'style="height:130px;width:auto;object-fit:contain;display:block;">'
    )
else:
    _nav_logo_html = (
        '<div style="font-size:26px;font-weight:900;color:#1a1a1a;letter-spacing:3px;">'
        'SHINGDA</div>'
    )

st.markdown(f"""
<div style="margin:0 -2rem 0 -2rem;display:flex;height:160px;
            box-shadow:0 4px 20px rgba(0,0,0,0.25);border-bottom:3px solid #f3d03e;">
    <div style="background:white;padding:0 32px;display:flex;align-items:center;
                justify-content:center;flex-shrink:0;">
        {_nav_logo_html}
    </div>
    <div style="background:white;flex:1;padding:0 36px;display:flex;align-items:center;">
        <div style="font-family:'Helvetica Neue',Arial,sans-serif;">
            <div style="font-size:22px;font-weight:700;color:#1a1a1a;
                        letter-spacing:2px;line-height:1.2;">
                SHINGDA GROUP OF COMPANIES
            </div>
            <div style="font-size:11px;color:#707372;margin-top:6px;letter-spacing:0.3px;">
                Fleet Management &nbsp;&middot;&nbsp; Fuel Analysis &nbsp;&middot;&nbsp; KM/L Efficiency
            </div>
        </div>
        <div style="margin-left:auto;display:flex;align-items:center;gap:8px;flex-shrink:0;">
            <div style="width:8px;height:8px;background:#f3d03e;border-radius:50%;
                        box-shadow:0 0 8px rgba(243,208,62,0.6);"></div>
            <span style="font-size:10px;color:#707372;letter-spacing:1.5px;
                         font-family:'Helvetica Neue',Arial,sans-serif;font-weight:600;">
                LIVE DASHBOARD
            </span>
        </div>
    </div>
</div>

<!-- Hero band below nav -->
<div style="
    margin: 0 -2rem 28px -2rem;
    padding: 18px 40px 18px 40px;
    background: #f3d03e;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 3px 10px rgba(243,208,62,0.3);
">
    <div style="font-family:'Helvetica Neue',Arial,sans-serif;">
        <div style="font-size:16px;font-weight:700;letter-spacing:0.5px;color:#1a1a1a;">
            ⛽ Diesel Consumption Dashboard
        </div>
        <div style="font-size:13px;color:#5a4a00;margin-top:2px;letter-spacing:0.3px;">
            ⛽ &nbsp;Upload your reports below to begin analysis
        </div>
    </div>
    <div style="font-family:'Helvetica Neue',Arial,sans-serif;text-align:right;">
        <div style="font-size:10px;letter-spacing:2px;color:#5a4a00;text-transform:uppercase;
                    font-weight:600;">
            FLEET FUEL INTELLIGENCE
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# STEP 1: FILE SOURCES
# Priority: 1) Local/Network folder  2) OneDrive  3) Manual upload
# ─────────────────────────────────────────────

import glob as _glob

# ── File-type detection (shared by local + OneDrive modes) ────────────────
_SLOT_LABELS = {
    "diesel":   "⛽ Diesel (Transactions)",
    "job":      "📋 Job List (SELPL)",
    "vehicle":  "🚗 Vehicle List",
    "bowser":   "🚰 Bowser / Fuel Records",
    "odometer": "📍 Odometer Detail",
}

def _detect_slot(filename: str) -> str | None:
    n = filename.lower()
    if "transaction" in n:                                      return "diesel"
    if "job list" in n or ("selpl" in n and "vehicle" in n):   return "job"
    if "vehicle" in n and "job" not in n and "odometer" not in n: return "vehicle"
    if "fuel record" in n or "燃油记录" in filename:           return "bowser"
    if "odometer" in n:                                         return "odometer"
    return None

# Named subfolders for each report slot.
# Place each report type in its own subfolder under the root folder.
_SLOT_FOLDERS = {
    "diesel":   "Transactions",
    "job":      "Job List",
    "vehicle":  "Vehicle List",
    "bowser":   "Fuel Records",
    "odometer": "Odometer",
}

def _scan_folder_slot(folder_path: str, slot: str) -> list:
    """Scan one subfolder and return all Excel/CSV files as slot entries."""
    import os
    exts    = ("*.xlsx", "*.xls", "*.xlsm", "*.csv")
    entries = []
    for ext in exts:
        for fpath in _glob.glob(os.path.join(folder_path, ext)):
            fname = os.path.basename(fpath)
            try:
                with open(fpath, "rb") as f:
                    raw_bytes = f.read()
                mtime = pd.Timestamp(
                    os.path.getmtime(fpath), unit="s"
                ).strftime("%Y-%m-%d %H:%M")
                entries.append({"bytes": raw_bytes, "name": fname,
                                 "modified": mtime, "subfolder": _SLOT_FOLDERS[slot]})
            except Exception:
                continue
    entries.sort(key=lambda x: x["modified"], reverse=True)
    return entries

def _scan_local_folder(folder: str) -> dict:
    """
    Scan the root folder for report files.

    PRIMARY MODE — named subfolders:
        Looks for one subfolder per report type (Transactions/, Job List/, etc.).
        Every Excel file inside a subfolder belongs to that slot — no keyword
        guessing needed.  New months just go into the matching subfolder.

    FALLBACK MODE — flat folder:
        If none of the named subfolders exist, falls back to scanning the root
        folder and detecting file types by keyword (original behaviour).

    Returns { slot: [{"bytes": bytes, "name": str, "modified": str}] }
    """
    import os
    slots = {k: [] for k in _SLOT_LABELS}

    # Check whether at least one named subfolder exists
    any_subfolder = any(
        os.path.isdir(os.path.join(folder, sub))
        for sub in _SLOT_FOLDERS.values()
    )

    if any_subfolder:
        # ── Subfolder mode ────────────────────────────────────────────────
        for slot, subfolder_name in _SLOT_FOLDERS.items():
            sub_path = os.path.join(folder, subfolder_name)
            if os.path.isdir(sub_path):
                slots[slot] = _scan_folder_slot(sub_path, slot)
    else:
        # ── Flat fallback mode ────────────────────────────────────────────
        exts = ("*.xlsx", "*.xls", "*.xlsm", "*.csv")
        for ext in exts:
            for fpath in _glob.glob(os.path.join(folder, ext)):
                fname = os.path.basename(fpath)
                slot  = _detect_slot(fname)
                if slot is None:
                    continue
                try:
                    with open(fpath, "rb") as f:
                        raw_bytes = f.read()
                    mtime = pd.Timestamp(
                        os.path.getmtime(fpath), unit="s"
                    ).strftime("%Y-%m-%d %H:%M")
                    slots[slot].append({"bytes": raw_bytes, "name": fname,
                                         "modified": mtime, "subfolder": None})
                except Exception:
                    continue
        for k in slots:
            slots[k].sort(key=lambda x: x["modified"], reverse=True)

    return slots

def _show_slot_status(reports: dict, loaded_at: str) -> None:
    lines = []
    for slot, label in _SLOT_LABELS.items():
        found = reports.get(slot, [])
        subfolder = _SLOT_FOLDERS.get(slot, "")
        if found:
            count = len(found)
            names = ", ".join(f["name"] for f in found)
            mod   = found[0]["modified"]
            folder_tag = f"`{subfolder}\\`  " if subfolder else ""
            file_word  = "file" if count == 1 else "files"
            lines.append(
                f"✅ **{label}** — {folder_tag}{count} {file_word}  "
                f"*(latest: {found[0]['name']}, {mod})*"
            )
        else:
            folder_tag = f"`{subfolder}\\` " if subfolder else ""
            lines.append(f"⚠️ **{label}** — {folder_tag}no files found")
    st.info(f"**Last scanned: {loaded_at}**\n\n" + "\n\n".join(lines))

def _make_buf(entry: dict):
    """Create a fresh BytesIO (always at position 0) from a stored bytes entry."""
    import io as _io
    buf = _io.BytesIO(entry["bytes"])
    buf.name = entry["name"]   # needed by pandas and load_* functions
    return buf

def _wire_files(reports: dict) -> tuple:
    """
    Build fresh file-like objects from the stored raw bytes on every call.
    Fresh BytesIO objects are always at position 0, so @st.cache_data
    content-hashing works correctly and pandas never reads from EOF.
    """
    d_entries = reports.get("diesel",   [])
    j_entries = reports.get("job",      [])
    d_files   = [_make_buf(e) for e in d_entries]
    j_files   = [_make_buf(e) for e in j_entries]
    _v = reports.get("vehicle",  []);  v_file = _make_buf(_v[0]) if _v else None
    _b = reports.get("bowser",   []);  b_file = _make_buf(_b[0]) if _b else None
    _o = reports.get("odometer", []);  o_file = _make_buf(_o[0]) if _o else None
    return d_files, (d_files[0] if d_files else None), j_files, (j_files[0] if j_files else None), v_file, b_file, o_file

# ══════════════════════════════════════════════════════════════════
# MODE 1 — LOCAL / NETWORK FOLDER  (I: drive or any mapped path)
# ══════════════════════════════════════════════════════════════════
import os as _os

# Folder path can be set in the sidebar so users can point to any subfolder.
# Default shows the Operations I: drive root; adjust as needed.
st.sidebar.markdown("---")
st.sidebar.markdown("**📂 Network Folder**")
_default_path = r"I:\Fleet\Diesel Report\Diesel Consumption"
_folder_input = st.sidebar.text_input(
    "Folder path on I: drive",
    value=st.session_state.get("local_folder", _default_path.strip()),
    key="local_folder_input",
    help="Paste the full path to the folder containing your Excel reports, e.g.  I:\\Operations\\Diesel",
).strip()
st.session_state["local_folder"] = _folder_input
_local_folder_valid = _os.path.isdir(_folder_input)

if _local_folder_valid:
    # ── Local folder scan ─────────────────────────────────────────────────
    hdr_col, btn_col = st.columns([5, 1])
    with hdr_col:
        st.subheader("📂 Auto-Scanning Network Folder")
        st.caption(f"Folder: `{_folder_input}`")
    with btn_col:
        st.write("")
        _refresh_local = st.button("🔄 Refresh", use_container_width=True, key="local_refresh")

    _cache_key    = f"local_reports_{_folder_input}"
    _cache_ts_key = f"local_loaded_at_{_folder_input}"

    if _cache_key not in st.session_state or _refresh_local:
        with st.spinner("Scanning folder for the latest reports…"):
            st.session_state[_cache_key]    = _scan_local_folder(_folder_input)
            st.session_state[_cache_ts_key] = pd.Timestamp.now().strftime("%d %b %Y  %H:%M")

    _reports   = st.session_state[_cache_key]
    _loaded_at = st.session_state.get(_cache_ts_key, "—")
    _show_slot_status(_reports, _loaded_at)
    diesel_files, diesel_file, job_files, job_file, veh_file, bowser_file, odometer_file = _wire_files(_reports)

    if diesel_file is None:
        st.warning(
            f"⚠️ No Diesel / Transactions file found in `{_folder_input}`.  "
            "Make sure a file with **'Transaction'** in its name is saved in "
            "`I:\\Fleet\\Diesel Report\\Diesel Consumption`."
        )
        st.stop()

# ══════════════════════════════════════════════════════════════════
# MODE 2 — ONEDRIVE  (when Azure credentials are in secrets.toml)
# ══════════════════════════════════════════════════════════════════
else:
    _od = st.secrets.get("onedrive", {}) if hasattr(st, "secrets") else {}
    USE_ONEDRIVE = all(k in _od for k in (
        "tenant_id", "client_id", "client_secret", "user_or_site", "folder_path"
    ))

    if USE_ONEDRIVE:
        import onedrive_loader
        hdr_col, btn_col = st.columns([5, 1])
        with hdr_col:
            st.subheader("📡 Auto-Loading from OneDrive")
        with btn_col:
            st.write("")
            _refresh_od = st.button("🔄 Refresh", use_container_width=True, key="od_refresh")

        if "od_reports" not in st.session_state or _refresh_od:
            with st.spinner("Scanning OneDrive folder for the latest reports…"):
                try:
                    st.session_state["od_reports"] = onedrive_loader.load_reports_from_onedrive(
                        tenant_id     = _od["tenant_id"],
                        client_id     = _od["client_id"],
                        client_secret = _od["client_secret"],
                        user_or_site  = _od["user_or_site"],
                        folder_path   = _od["folder_path"],
                    )
                    st.session_state["od_loaded_at"] = pd.Timestamp.now().strftime("%d %b %Y  %H:%M")
                except Exception as _e:
                    st.error(f"❌ Could not connect to OneDrive: {_e}")
                    st.stop()

        _reports   = st.session_state["od_reports"]
        _loaded_at = st.session_state.get("od_loaded_at", "—")
        _show_slot_status(_reports, _loaded_at)
        diesel_files, diesel_file, job_files, job_file, veh_file, bowser_file, odometer_file = _wire_files(_reports)

        if diesel_file is None:
            st.warning("⚠️ No Diesel / Transactions file found in the OneDrive folder.")
            st.stop()

    # ══════════════════════════════════════════════════════════════════
    # MODE 3 — MANUAL UPLOAD  (fallback when no folder/OneDrive configured)
    # ══════════════════════════════════════════════════════════════════
    else:
        st.subheader("📂 Upload Files")
        st.caption("💡 Tip: enter a folder path in the sidebar to auto-load files instead of uploading.")
        col_up1, col_up2, col_up3 = st.columns(3)

        with col_up1:
            st.markdown("**Report 1 — Diesel Top-Up Record(s)**")
            st.caption("You can upload multiple months at once for compare mode")
            diesel_files = st.file_uploader(
                "Upload Diesel/Transaction file(s)", type=["xlsx", "xls", "csv"],
                key="diesel", accept_multiple_files=True
            )
            diesel_file = diesel_files[0] if diesel_files else None

        with col_up2:
            st.markdown("**Report 2 — Job List (Site / Project Info)**")
            st.caption("You can upload multiple months at once")
            job_files = st.file_uploader(
                "Upload Job List file(s)", type=["xlsx", "xls", "csv"],
                key="job", accept_multiple_files=True
            )
            job_file = job_files[0] if job_files else None

        with col_up3:
            st.markdown("**Report 3 — Vehicle Master List (Model & Type)**")
            veh_file = st.file_uploader(
                "Upload Vehicle List file", type=["xlsx", "xlsm", "xls", "csv"], key="veh"
            )

        col_up4, col_up5, _ = st.columns(3)
        with col_up4:
            st.markdown("**Report 4 — Bowser Dispensing Log (YP9421D-T)**")
            bowser_file = st.file_uploader(
                "Upload Bowser Fuel Records file", type=["xlsx", "xls", "csv"], key="bowser"
            )
        with col_up5:
            st.markdown("**Report 5 — Odometer Detail (KM/L Calculation)**")
            odometer_file = st.file_uploader(
                "Upload Odometer Detail file", type=["xlsx", "xls", "csv"], key="odometer"
            )

        if diesel_file is None:
            st.info("Please upload at least the Diesel Top-Up file to continue.")
            st.stop()

    if diesel_file is None:
        st.info("Please upload at least the Diesel Top-Up file to continue.")
        st.stop()

# ─────────────────────────────────────────────
# STEP 2: LOAD FILES
# ─────────────────────────────────────────────
# Custom hasher for BytesIO objects.
# Streamlit's default hashing calls os.path.getmtime(f.name), which fails when
# .name is a virtual name (not a real disk path). Hash by content instead so
# caching works for both UploadedFile and BytesIO from local/OneDrive auto-load.
import hashlib as _hashlib, io as _io

def _hash_file(f):
    pos = f.tell(); f.seek(0)
    digest = _hashlib.md5(f.read()).hexdigest()
    f.seek(pos)
    return digest

_FILE_HASH = {_io.BytesIO: _hash_file}

@st.cache_data(hash_funcs=_FILE_HASH)
def load_diesel(file):
    return pd.read_csv(file) if file.name.endswith(".csv") else pd.read_excel(file)

def load_job(file):
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
        df.columns = df.columns.str.strip()
        return df

    import io as _io2

    # ── Read 1: detect which row is the real header ───────────────────────
    # Use a fresh copy of the bytes so the original BytesIO is untouched.
    raw_bytes = file.read()
    file.seek(0)                                    # reset for Read 2
    probe = pd.read_excel(_io2.BytesIO(raw_bytes), header=None)

    _veh_kw = {"vehicle no", "veh no", "plate no", "reg no",
               "vehicle number", "veh number", "registration", "vehicle"}
    header_row = 0
    for i, row in probe.iterrows():
        lv = {str(v).strip().lower() for v in row.values}
        if "date" in lv and bool(lv & _veh_kw):
            header_row = i
            break

    # ── Read 2: read with correct header — gets proper dtypes (dates, ints) ─
    df = pd.read_excel(_io2.BytesIO(raw_bytes), header=header_row)
    df.columns = df.columns.str.strip()
    return df

@st.cache_data(hash_funcs=_FILE_HASH)
def load_vehicle_list(file):
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file, engine="openpyxl")
    df.columns = df.columns.str.strip()

    # Rename vehicle number column — handle all common variations
    veh_col_map = {
        "veh number":  "Vehicle No",
        "vehicle no":  "Vehicle No",
        "vehicle no.": "Vehicle No",
        "plate":       "Vehicle No",
        "plate no":    "Vehicle No",
        "reg no":      "Vehicle No",
    }
    for col in df.columns:
        if col.strip().lower() in veh_col_map:
            df.rename(columns={col: "Vehicle No"}, inplace=True)
            break

    if "Vehicle No" not in df.columns:
        st.warning("Vehicle List: cannot find vehicle number column. Expected 'Veh Number' or 'Vehicle No'.")
        return pd.DataFrame(columns=["Vehicle No", "Model", "Type"])

    df["Vehicle No"] = df["Vehicle No"].astype(str).str.strip().str.upper()
    # Drop blank/NaN vehicle numbers
    df = df[df["Vehicle No"].notna() & (df["Vehicle No"] != "NAN") & (df["Vehicle No"] != "")]
    keep = [c for c in ["Vehicle No", "Model", "Type"] if c in df.columns]
    return df[keep]

@st.cache_data(hash_funcs=_FILE_HASH)
def load_bowser(file):
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)
    df.columns = df.columns.str.strip()

    # Standardise column names
    df.rename(columns={
        "Date 日期":                          "Date",
        "Equipment ID 机械编号":              "Equipment ID",
        "Qty Litres 公升数量":               "Qty Litres",
        "Remarks 备注":                       "Remarks",
        "Project/Location 工程/位置":         "Project",
        "Employee ID 员工证号":               "Employee ID",
        "Foreman/Operator ID 工头/操作员证号":"Foreman ID",
    }, inplace=True)

    df["Date"]      = pd.to_datetime(df["Date"], errors="coerce")
    df["Qty Litres"] = pd.to_numeric(df["Qty Litres"], errors="coerce").fillna(0)
    df.dropna(subset=["Date"], inplace=True)

    # Flag record type
    df["Record Type"] = df["Remarks"].apply(
        lambda x: "Office Top-Up (IN)" if isinstance(x, str) and "office top up" in x.lower()
        else "Dispensed to Vehicle (OUT)"
    )
    df["Equipment ID"] = df["Equipment ID"].astype(str).str.strip()
    return df

@st.cache_data(hash_funcs=_FILE_HASH)
def load_odometer(file):
    """
    Parse the multi-block odometer report.
    Each block: REGISTRATION row → vehicle no + model → Date/Start/End/Distance rows.
    Returns a flat DataFrame: Vehicle No, Model, Date, Start KM, End KM, Distance KM
    """
    if file.name.endswith(".csv"):
        raw = pd.read_csv(file, header=None)
    else:
        raw = pd.read_excel(file, header=None, engine="openpyxl")

    records = []
    current_veh   = None
    current_model = None
    in_data       = False

    for i, row in raw.iterrows():
        vals = [str(v).strip() for v in row.values]

        # Detect REGISTRATION header → next row has vehicle info
        if vals[0] == "REGISTRATION":
            in_data = False
            # vehicle info is on the NEXT row — guard against last-row edge case
            if i + 1 < len(raw):
                next_row = raw.iloc[i + 1]
                next_vals = [str(v).strip() for v in next_row.values if str(v).strip() not in ["nan",""]]
                if next_vals:
                    current_veh   = next_vals[0].upper()
                    current_model = next_vals[1] if len(next_vals) > 1 else "Unknown"
            continue

        # Detect data header row
        if vals[0] == "Date" and "Start Odometer" in vals:
            in_data = True
            continue

        # Skip total row
        if vals[0].lower().startswith("total"):
            in_data = False
            continue

        # Parse data rows
        if in_data and current_veh:
            try:
                date     = pd.to_datetime(vals[0], errors="coerce")
                start_km = float(vals[1]) if vals[1] not in ["nan",""] else None
                end_km   = float(vals[2]) if vals[2] not in ["nan",""] else None
                distance = float(vals[3]) if vals[3] not in ["nan",""] else None
                if pd.notna(date) and distance is not None:
                    records.append({
                        "Vehicle No": current_veh,
                        "Model":      current_model,
                        "Date":       date,
                        "Start KM":   start_km,
                        "End KM":     end_km,
                        "Distance KM": distance,
                    })
            except (ValueError, IndexError):
                continue

    df = pd.DataFrame(records)
    if not df.empty:
        df["Date_Only"] = df["Date"].dt.normalize()
        df["Month"]     = df["Date"].dt.strftime("%Y-%m")
        df["Month_Label"] = df["Date"].dt.strftime("%b %Y")
    return df

# ── Load ALL diesel files combined as the primary source ─────────────────────
# This ensures all months are always available. The sidebar month selector
# (shown when >1 file) lets users filter to specific months.
# Using all files prevents the "wrong month loaded" bug caused by OS mtime.
@st.cache_data(show_spinner=False)
def load_all_diesel(file_tuples: tuple):
    """Load multiple diesel files from (name, bytes) tuples, tag each with its filename."""
    import io as _io
    frames = []
    for fname, raw_bytes in file_tuples:
        try:
            buf = _io.BytesIO(raw_bytes)
            raw = pd.read_csv(buf) if fname.endswith(".csv") else pd.read_excel(buf)
            raw["_source_file"] = fname
            frames.append(raw)
        except Exception as e:
            st.warning(f"Could not load {fname}: {e}")
    if frames:
        return pd.concat(frames, ignore_index=True)
    return pd.DataFrame()

_diesel_tuples = tuple((f.name, f.read()) for f in diesel_files)
for _f in diesel_files: _f.seek(0)

# Always combine all files — single file just produces a one-entry combined df
_combined_raw = load_all_diesel(_diesel_tuples)
if not _combined_raw.empty:
    diesel_raw = _combined_raw
else:
    diesel_raw = load_diesel(diesel_file)        # ultimate fallback
    diesel_raw["_source_file"] = diesel_file.name

all_diesel_raw = _combined_raw if len(diesel_files) > 1 else pd.DataFrame()

# Load and combine all job list files
job_raw = None  # placeholder — defined after clean_job
veh_raw      = load_vehicle_list(veh_file)  if veh_file      else None
bowser_raw   = load_bowser(bowser_file)     if bowser_file   else None
odometer_raw = load_odometer(odometer_file) if odometer_file else None

# ─────────────────────────────────────────────
# STEP 3: CLEAN DIESEL REPORT
# ─────────────────────────────────────────────
def clean_diesel(df):
    df = df.copy()
    df.columns = df.columns.str.strip()  # guard against Excel headers with trailing spaces
    rename_map = {
        "Date/time":    "Date",
        "LicensePlate": "Vehicle No",
        "Station":      "Fuel Station",
        "Quantity":     "Diesel Litre",
        "Odometer":     "KM Reading",
        "Article":      "Fuel Type",
        "Driver":       "Driver",
        "Vehicle No.":  "Vehicle No",
        "Veh No":       "Vehicle No",
        "Litres":       "Diesel Litre",
        "Litre":        "Diesel Litre",
        "Km Reading":   "KM Reading",
    }
    df.rename(columns=rename_map, inplace=True)

    # ── Fallback: if Vehicle No is missing/empty, try other common columns ──
    # Some fleet systems put the plate in LicensePlate (already mapped above),
    # others use Customer, Vehicle, or Plate columns.
    if "Vehicle No" not in df.columns or df["Vehicle No"].isna().all():
        for _try in ["Customer", "Vehicle", "Plate", "Reg No", "Registration"]:
            if _try in df.columns and df[_try].notna().any():
                df["Vehicle No"] = df[_try]
                break

    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df.dropna(subset=["Date"], inplace=True)

    if "Fuel Type" in df.columns:
        df["Fuel Type"] = df["Fuel Type"].astype(str).str.strip()
        df["Fuel Type"] = df["Fuel Type"].str.replace(r"^\[\d+\]\s*", "", regex=True)

    if "Fuel Station" in df.columns:
        df["Fuel Station"] = df["Fuel Station"].astype(str).str.strip()
        df["Fuel Station"] = df["Fuel Station"].str.replace(r"^\[\d+\]\s*", "", regex=True)

    for col in ["Diesel Litre", "KM Reading"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "Vehicle No" in df.columns:
        # strip + upper + remove ALL internal spaces so "SHD 1234 A" == "SHD1234A"
        df["Vehicle No"] = (df["Vehicle No"].astype(str)
                            .str.strip().str.upper()
                            .str.replace(r"\s+", "", regex=True))

    if "Diesel Litre" in df.columns:
        df.dropna(subset=["Diesel Litre"], inplace=True)
        df = df[df["Diesel Litre"] > 0]

    df["Date_Only"]   = df["Date"].dt.normalize()
    df["Day"]         = df["Date"].dt.strftime("%b %d").str.replace(" 0", " ", regex=False)
    df["Day_Sort"]    = df["Date"].dt.date
    df["Month"]       = df["Date"].dt.strftime("%Y-%m")
    df["Month_Label"] = df["Date"].dt.strftime("%b %Y")
    df["Year"]        = df["Date"].dt.strftime("%Y")
    return df

# ─────────────────────────────────────────────
# STEP 4: CLEAN JOB LIST
# ─────────────────────────────────────────────
def clean_job(df):
    df = df.copy()
    df.columns = df.columns.str.strip()

    # ── Normalise Vehicle No column ──────────────────────────────────────
    _veh_aliases = [
        "vehicle no", "vehicle no.", "veh no", "veh no.", "veh number",
        "vehicle number", "plate no", "plate no.", "reg no", "reg no.",
        "registration", "vehicle", "車號", "车号",
    ]
    for col in df.columns:
        if col.strip().lower() in _veh_aliases:
            df.rename(columns={col: "Vehicle No"}, inplace=True)
            break

    # ── Normalise Site / Project column ──────────────────────────────────
    _site_aliases = [
        "site", "project", "project / site", "project/site", "location",
        "job site", "job location", "description", "site name",
        "project name", "work site", "工地", "项目", "地点",
    ]
    for col in df.columns:
        if col.strip().lower() in _site_aliases and col != "Vehicle No":
            df.rename(columns={col: "Site"}, inplace=True)
            break

    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df.dropna(subset=["Date"], inplace=True)
    if "Vehicle No" in df.columns:
        # Match exact normalisation used in clean_diesel so the merge works
        df["Vehicle No"] = (df["Vehicle No"].astype(str)
                            .str.strip().str.upper()
                            .str.replace(r"\s+", "", regex=True))
    if "Site" in df.columns:
        df["Site"] = df["Site"].astype(str).str.strip()
        # Strip shift suffixes: "CR3026 ( NIGHT SHIFT )" → "CR3026"
        df["Site"] = df["Site"].str.replace(
            r"\s*\(\s*(DAY SHIFT|NIGHT SHIFT|AM|PM|SHIFT\s*\d*)\s*\)\s*$",
            "", regex=True, flags=0
        ).str.strip()

    keep = [c for c in ["Date", "Vehicle No", "Site"] if c in df.columns]
    df = df[keep].copy()

    if "Date" not in df.columns or df.empty:
        return df
    df["Date_Only"] = df["Date"].dt.normalize()
    return df

# ─────────────────────────────────────────────
# LOAD ALL JOB FILES (defined here so clean_job is available)
# ─────────────────────────────────────────────
def load_all_jobs(file_tuples: tuple):
    """Load all job list files from (name, bytes) tuples."""
    import io as _io
    frames = []
    for fname, raw_bytes in file_tuples:
        try:
            buf      = _io.BytesIO(raw_bytes); buf.name = fname
            raw      = load_job(buf)
            cleaned  = clean_job(raw)
            frames.append(cleaned)
        except Exception as e:
            st.warning(f"Could not load {fname}: {e}")
    if frames:
        combined = pd.concat(frames, ignore_index=True)
        combined.drop_duplicates(subset=["Vehicle No", "Date_Only", "Site"], inplace=True)
        return combined
    return None

_job_tuples = tuple((f.name, f.read()) for f in job_files) if job_files else ()
for _f in (job_files or []): _f.seek(0)   # reset so individual load_job() calls still work
job_raw = load_all_jobs(_job_tuples) if _job_tuples else None

# ─────────────────────────────────────────────
# STEP 5: MERGE
# ─────────────────────────────────────────────
def merge_reports(diesel_df, job_df):
    if job_df is None:
        diesel_df["Project"] = "No Job List Uploaded"
        return diesel_df

    site_map = (
        job_df.groupby(["Vehicle No", "Date_Only"])["Site"]
        .agg(lambda x: x.mode()[0])
        .reset_index()
        .rename(columns={"Site": "Project"})
    )
    merged = diesel_df.merge(site_map, on=["Vehicle No", "Date_Only"], how="left")

    # Vehicles that exist in job list but have no entry on that specific date
    # (e.g. topped up diesel on a rest day or before/after their shift)
    all_job_vehicles = set(job_df["Vehicle No"].unique())

    def label_unmatched(row):
        if pd.notna(row["Project"]):
            return row["Project"]
        if row["Vehicle No"] in all_job_vehicles:
            return "Off-day / No Schedule"   # vehicle known but no job on that date
        return "Vehicle Not in Job List"      # vehicle never appears in job list

    merged["Project"] = merged.apply(label_unmatched, axis=1)
    return merged

diesel_df = clean_diesel(diesel_raw)
job_df    = clean_job(job_raw) if job_raw is not None else None
df        = merge_reports(diesel_df, job_df)

# Merge vehicle model & type from Vehicle List
if veh_raw is not None and not veh_raw.empty:
    df = df.merge(veh_raw, on="Vehicle No", how="left")
    matched   = df["Model"].notna().sum()
    unmatched = df["Model"].isna().sum()
    df["Model"] = df["Model"].fillna("Not in Vehicle List")
    df["Type"]  = df["Type"].fillna("Not in Vehicle List")
    st.sidebar.caption(f"🚛 Vehicle List: {matched} matched, {unmatched} unmatched")
else:
    df["Model"] = "No Vehicle List"
    df["Type"]  = "No Vehicle List"

# ─────────────────────────────────────────────
# STEP 6: SIDEBAR — REPORT TOGGLES + FILTERS
# ─────────────────────────────────────────────
st.sidebar.header("🔍 Filters")

# ── Job list debug (temporary — remove once matching works) ──────────────────
if job_df is not None:
    with st.sidebar.expander("🔬 Job List Debug", expanded=True):
        st.caption(f"job_df rows: {len(job_df)}")
        st.caption(f"job_df cols: {list(job_df.columns)}")
        if "Date_Only" in job_df.columns:
            jd = job_df["Date_Only"].dropna()
            st.caption(f"Job dates: {jd.min()} → {jd.max()} ({len(jd)} rows)")
            st.caption(f"Date type: {jd.dtype}")
        if "Date_Only" in df.columns:
            dd = df["Date_Only"].dropna()
            st.caption(f"Diesel dates: {dd.min()} → {dd.max()}")
            st.caption(f"Date type: {dd.dtype}")
        if "Vehicle No" in job_df.columns:
            jv = sorted(job_df["Vehicle No"].dropna().unique())[:5]
            st.caption(f"Job vehs: {jv}")
        if "Vehicle No" in df.columns:
            dv = sorted(df["Vehicle No"].dropna().unique())[:5]
            st.caption(f"Diesel vehs: {dv}")
        if "Site" in job_df.columns:
            js = sorted(job_df["Site"].dropna().unique())[:5]
            st.caption(f"Sites: {js}")
else:
    st.sidebar.caption("⚠️ job_df is None")

# ── Active Reports panel ─────────────────────────────────────────────────────
# Each loaded report can be toggled on/off independently.
# Toggling a report OFF removes its contribution from the analysis
# without unloading the file — useful for focused single-report views.
st.sidebar.markdown("**📋 Active Reports**")

_rep_col1, _rep_col2 = st.sidebar.columns(2)

with _rep_col1:
    _use_job = st.checkbox(
        "📋 Job List",
        value=(job_raw is not None),
        disabled=(job_raw is None),
        key="toggle_job",
        help="Show/hide project & site analysis"
    )
    _use_bowser = st.checkbox(
        "🚰 Fuel Records",
        value=(bowser_raw is not None),
        disabled=(bowser_raw is None),
        key="toggle_bowser",
        help="Show/hide Bowser tab"
    )

with _rep_col2:
    _use_vehicle = st.checkbox(
        "🚗 Vehicle List",
        value=(veh_raw is not None),
        disabled=(veh_raw is None),
        key="toggle_vehicle",
        help="Show/hide model & type columns"
    )
    _use_odometer = st.checkbox(
        "📍 Odometer",
        value=(odometer_raw is not None),
        disabled=(odometer_raw is None),
        key="toggle_odometer",
        help="Show/hide KM/L analysis"
    )

# Apply toggles — treat deactivated reports as if not loaded
if not _use_job:      job_df       = None
if not _use_vehicle:  veh_raw      = None
if not _use_bowser:   bowser_raw   = None
if not _use_odometer: odometer_raw = None

# Re-apply vehicle model/type merge if vehicle list was toggled on after initial load
if _use_vehicle and veh_raw is not None and "Model" not in df.columns:
    df = df.merge(veh_raw, on="Vehicle No", how="left")
    df["Model"] = df["Model"].fillna("Not in Vehicle List")
    df["Type"]  = df["Type"].fillna("Not in Vehicle List")
elif not _use_vehicle:
    df["Model"] = "Report Off"
    df["Type"]  = "Report Off"

# Re-apply project merge if job list was toggled on/off
if _use_job and job_df is not None:
    _site_map2 = (
        job_df.groupby(["Vehicle No", "Date_Only"])["Site"]
        .agg(lambda x: x.mode()[0]).reset_index()
        .rename(columns={"Site": "Project"})
    )
    df = df.drop(columns=["Project"], errors="ignore")
    df = df.merge(_site_map2, on=["Vehicle No", "Date_Only"], how="left")
    _all_job_v = set(job_df["Vehicle No"].unique())
    def _relabel(row):
        if pd.notna(row["Project"]): return row["Project"]
        return "Off-day / No Schedule" if row["Vehicle No"] in _all_job_v else "Vehicle Not in Job List"
    df["Project"] = df.apply(_relabel, axis=1)
elif not _use_job:
    df["Project"] = "Job List Off"

st.sidebar.divider()

# ── Job List merge diagnostics (shown when job_df loaded) ────────────────────
if job_df is not None and not job_df.empty:
    _matched   = df[df["Project"].notna() & ~df["Project"].isin(
        ["No Job List Uploaded", "Off-day / No Schedule", "Vehicle Not in Job List"]
    )].shape[0]
    _total     = len(df)
    _pct       = _matched / _total * 100 if _total else 0
    _match_col = "🟢" if _pct > 60 else ("🟡" if _pct > 20 else "🔴")

    with st.sidebar.expander(f"{_match_col} Job List Match — {_pct:.0f}%", expanded=(_pct < 60)):
        st.caption(f"**{_matched} / {_total}** diesel rows matched a project site.")

        if _pct < 60:
            # Show date range comparison
            _d_dates = pd.to_datetime(df["Date"]).dt.date
            _j_dates = pd.to_datetime(job_df["Date"]).dt.date if "Date" in job_df.columns else None
            st.markdown("**Diesel file dates:**")
            st.caption(f"{_d_dates.min()} → {_d_dates.max()}")
            if _j_dates is not None:
                st.markdown("**Job list dates:**")
                st.caption(f"{_j_dates.min()} → {_j_dates.max()}")

            # Show vehicle number format samples
            _d_vehs = sorted(df["Vehicle No"].dropna().unique())[:5]
            _j_vehs = sorted(job_df["Vehicle No"].dropna().unique())[:5] \
                      if "Vehicle No" in job_df.columns else []
            st.markdown("**Diesel vehicle sample:**")
            st.caption("  ".join(_d_vehs))
            if _j_vehs:
                st.markdown("**Job list vehicle sample:**")
                st.caption("  ".join(_j_vehs))
            st.info("If the date ranges or vehicle formats look different above, "
                    "that's why projects aren't matching.")


# ── Report Period Mode ──
st.sidebar.markdown("**📆 Report Period**")
view_mode = st.sidebar.selectbox(
    "View By", ["Monthly", "Yearly"], key="view_mode"
)
# ── Global Price per Litre ──
st.sidebar.markdown("**💰 Fuel Price**")
price_per_litre = st.sidebar.number_input(
    "Price per Litre (SGD)", min_value=0.01, value=2.15,
    step=0.05, format="%.2f", key="global_price"
)
st.sidebar.divider()

# ── File / Month selector (shown when multiple files are in the folder) ──
if len(diesel_files) > 1:
    st.sidebar.markdown("**📂 Report Files**")
    _all_file_names = [f.name for f in diesel_files]
    # Build friendly month labels where possible (e.g. "Apr 2026 — Transactions.xls -Apr 26")
    def _friendly(fname):
        import re
        m = re.search(r"(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s*(\d{2,4})", fname, re.I)
        if m:
            mon, yr = m.group(1).capitalize(), m.group(2)
            yr_full = f"20{yr}" if len(yr) == 2 else yr
            return f"{mon} {yr_full}  —  {fname}"
        return fname
    _labels    = [_friendly(n) for n in _all_file_names]
    _label_map = dict(zip(_labels, _all_file_names))   # label → real filename
    sel_labels = st.sidebar.multiselect(
        "Select month(s) to view", _labels, default=_labels, key="sel_source_files"
    )
    sel_files = [_label_map[l] for l in sel_labels] if sel_labels else _all_file_names
    df = df[df["_source_file"].isin(sel_files)]
    st.sidebar.caption(f"{len(sel_files)} of {len(_all_file_names)} file(s) shown")
    st.sidebar.divider()

if "Date" in df.columns:
    _valid_dates = df["Date"].dropna()
    if _valid_dates.empty:
        st.warning(
            "⚠️ No valid dates found in the Diesel Transactions file. "
            "Check that the file has a Date or Date/time column and the "
            "rows are not all blank."
        )
        st.stop()
    min_date = _valid_dates.min().date()
    max_date = _valid_dates.max().date()
    date_from, date_to = st.sidebar.date_input(
        "Date Range", value=(min_date, max_date),
        min_value=min_date, max_value=max_date,
    )
    df = df[(df["Date"].dt.date >= date_from) & (df["Date"].dt.date <= date_to)]

# ── All filters inside collapsible expanders ──

# 1. Vehicle Model
if "Model" in df.columns:
    real_models = sorted([
        m for m in df["Model"].dropna().unique()
        if m not in ["N/A","No Vehicle List","Not in Vehicle List","Unknown Model"]
    ])
    if real_models:
        with st.sidebar.expander("🚗 Vehicle Model", expanded=False):
            sel_model = st.multiselect(
                "Select models", real_models, default=real_models, key="sel_model",
                label_visibility="collapsed"
            )
        if sel_model:
            df = df[df["Model"].isin(sel_model) | df["Model"].isin(
                ["N/A","No Vehicle List","Not in Vehicle List","Unknown Model"]
            )]

# 2. Vehicle Type
if "Type" in df.columns:
    real_types = sorted([
        t for t in df["Type"].dropna().unique()
        if t not in ["N/A","No Vehicle List","Not in Vehicle List","Unknown Type"]
    ])
    if real_types:
        with st.sidebar.expander("🚛 Vehicle Type", expanded=False):
            sel_type = st.multiselect(
                "Select types", real_types, default=real_types, key="sel_type",
                label_visibility="collapsed"
            )
        if sel_type:
            df = df[df["Type"].isin(sel_type) | df["Type"].isin(
                ["N/A","No Vehicle List","Not in Vehicle List","Unknown Type"]
            )]

# 3. Vehicle No
if "Vehicle No" in df.columns:
    vehicles = sorted(df["Vehicle No"].dropna().unique())
    with st.sidebar.expander("🔢 Vehicle No", expanded=False):
        sel_veh = st.multiselect(
            "Select vehicles", vehicles, default=vehicles, key="sel_veh",
            label_visibility="collapsed"
        )
    df = df[df["Vehicle No"].isin(sel_veh)]

# 4. Project / Site
if "Project" in df.columns:
    projects = sorted(df["Project"].dropna().unique())
    with st.sidebar.expander("🏗️ Project / Site", expanded=False):
        sel_proj = st.multiselect(
            "Select sites", projects, default=projects, key="sel_proj",
            label_visibility="collapsed"
        )
    df = df[df["Project"].isin(sel_proj)]

# 5. Fuel Type
if "Fuel Type" in df.columns:
    fuels = sorted(df["Fuel Type"].dropna().unique())
    with st.sidebar.expander("⛽ Fuel Type", expanded=False):
        sel_fuels = st.multiselect(
            "Select fuel types", fuels, default=fuels, key="sel_fuels",
            label_visibility="collapsed"
        )
    df = df[df["Fuel Type"].isin(sel_fuels)]

# ─────────────────────────────────────────────
# PERIOD HELPER — switches between Monthly / Yearly
# ─────────────────────────────────────────────
def get_period_col(dataframe, mode):
    """Return the right grouping column and label based on view mode."""
    if mode == "Yearly":
        if "Year" not in dataframe.columns:
            dataframe["Year"] = pd.to_datetime(dataframe["Date"]).dt.strftime("%Y")
        return "Year", "Year"
    else:
        if "Month" not in dataframe.columns:
            dataframe["Month"] = pd.to_datetime(dataframe["Date"]).dt.strftime("%Y-%m")
        if "Month_Label" not in dataframe.columns:
            dataframe["Month_Label"] = pd.to_datetime(dataframe["Date"]).dt.strftime("%b %Y")
        return "Month_Label", "Month"

# Apply period to main df
period_label, period_sort = get_period_col(df, view_mode)

# ─────────────────────────────────────────────
# STEP 7: COMPUTE SUMMARY STATS
# ─────────────────────────────────────────────
total_diesel  = df["Diesel Litre"].sum()
try:
    num_days = max((df["Date"].dt.date.max() - df["Date"].dt.date.min()).days + 1, 1)
except Exception:
    num_days = 1
avg_per_day   = total_diesel / num_days
total_veh     = df["Vehicle No"].nunique()
total_proj    = df["Project"].nunique() if "Project" in df.columns else 0

# Guard: if df is empty after filters, show empty state
if df.empty:
    st.warning("⚠️ No data matches the current filters. Please adjust your selections.")
    st.stop()

# Peak day / peak month depending on view mode
if view_mode == "Yearly":
    peak_sum     = df.groupby("Month_Label")["Diesel Litre"].sum()
    peak_day_str = peak_sum.idxmax() if not peak_sum.empty else "N/A"
    peak_day_val = peak_sum.max()    if not peak_sum.empty else 0
else:
    daily_sum     = df.groupby("Day_Sort")["Diesel Litre"].sum()
    peak_day_date = daily_sum.idxmax() if not daily_sum.empty else None
    peak_day_val  = daily_sum.max()    if not daily_sum.empty else 0
    peak_day_str  = peak_day_date.strftime("%b %d").replace(" 0", " ") if peak_day_date else "N/A"

# Top project & vehicle
proj_sum    = df.groupby("Project")["Diesel Litre"].sum() if "Project" in df.columns else pd.Series()
top_project = proj_sum.idxmax() if not proj_sum.empty else "N/A"
veh_sum     = df.groupby("Vehicle No")["Diesel Litre"].sum()
top_vehicle = veh_sum.idxmax() if not veh_sum.empty else "N/A"

if view_mode == "Yearly":
    years = sorted(df["Year"].unique())
    period_str = f"Year(s): {', '.join(years)}"
else:
    period_str = (
        f"{df['Date'].min().strftime('%b %d, %Y').replace(' 0', ' ')} to "
        f"{df['Date'].max().strftime('%b %d, %Y').replace(' 0', ' ')} ({num_days} days)"
    )

# ─────────────────────────────────────────────
# STEP 8: TOP SUMMARY BAR  (matches PDF header)
# ─────────────────────────────────────────────
st.divider()
st.markdown(f"**Period: {period_str}**")

total_cost = total_diesel * price_per_litre

c1, c2, c3, c4, c5, c6, c7, c8 = st.columns(8)
c1.metric("⛽ Total Diesel (L)", f"{total_diesel:,.0f}")
c2.metric("💵 Total Cost (SGD)",  f"${total_cost:,.0f}")
c3.metric("📅 Avg / Day" if view_mode=="Monthly" else "📅 Avg / Month",
          f"{avg_per_day:,.0f}" if view_mode=="Monthly"
          else f"{total_diesel/max(df['Month'].nunique(),1):,.0f}")
c4.metric("📈 Peak Day" if view_mode=="Monthly" else "📈 Peak Month", peak_day_str)
c5.metric("🔝 Peak Total",  f"{peak_day_val:,.0f}")
c6.metric("🏗️ Top Project",     top_project)
c7.metric("🚛 Top Vehicle",     top_vehicle)
c8.metric("📊 Projects / Veh",  f"{total_proj} / {total_veh}")

st.divider()

# ─────────────────────────────────────────────
# STEP 9: FOUR TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "🏗️ 1. Diesel by Project",
    "📅 2. Daily Diesel Trend",
    "🚛 3. Diesel by Vehicle",
    "🚰 4. Bowser (YP9421D-T)",
    "📊 5. Compare Mode",
    "⚡ 6. KM/L Analysis",
    "🖨️ 7. Vehicle Proof Sheet",
    "🚨 8. No Job Alert",
    "📋 9. Full Data & Export",
])

# ══════════════════════════════════════════════
# TAB 1 — DIESEL BY PROJECT
# ══════════════════════════════════════════════
with tab1:
    st.subheader("🏗️ Diesel by Project")

    proj_df = (
        df.groupby("Project")
        .agg(
            Total_Diesel = ("Diesel Litre", "sum"),
            Vehicles     = ("Vehicle No",   "nunique"),
        )
        .reset_index()
        .sort_values("Total_Diesel", ascending=False)
        .reset_index(drop=True)
    )
    proj_df.index += 1
    proj_df["% of Total"]      = (proj_df["Total_Diesel"] / proj_df["Total_Diesel"].sum() * 100).round(1)
    proj_df["Avg / Day"]       = (proj_df["Total_Diesel"] / num_days).round(1)
    proj_df["Total Cost (SGD)"] = (proj_df["Total_Diesel"] * price_per_litre).round(2)

    # Project share — donut chart (distinct from the bar chart below)
    st.markdown(f"#### Diesel Share by Project — {view_mode}")
    proj_share = (
        df.groupby("Project")["Diesel Litre"]
        .sum().reset_index()
        .sort_values("Diesel Litre", ascending=False)
    )
    # Group small projects (<1%) into "Others" to keep chart readable
    _total_share = proj_share["Diesel Litre"].sum()
    proj_share["_pct"] = proj_share["Diesel Litre"] / _total_share * 100
    _main   = proj_share[proj_share["_pct"] >= 1].copy()
    _others = proj_share[proj_share["_pct"] <  1].copy()
    if not _others.empty:
        _main = pd.concat([
            _main,
            pd.DataFrame([{"Project": f"Others ({len(_others)} sites)",
                           "Diesel Litre": _others["Diesel Litre"].sum(), "_pct": _others["_pct"].sum()}])
        ], ignore_index=True)

    fig_proj_period = px.pie(
        _main,
        names="Project", values="Diesel Litre",
        hole=0.42,
        title=f"Project Share of Total Diesel — {view_mode}",
        color_discrete_sequence=BRAND_PALETTE,
    )
    fig_proj_period.update_traces(
        textposition="outside",
        textinfo="label+percent",
        textfont_size=11,
    )
    fig_proj_period.update_layout(
        height=480,
        legend=dict(orientation="v", x=1.02, y=0.5),
        margin=dict(l=20, r=180, t=60, b=20),
    )
    st.plotly_chart(fig_proj_period, use_container_width=True)

    # Chart
    fig_proj = px.bar(
        proj_df.sort_values("Total_Diesel"),
        x="Total_Diesel", y="Project", orientation="h",
        title="Diesel by Project (Litres)",
        labels={"Total_Diesel": "Litres", "Project": "Project"},
        color_discrete_sequence=[BRAND_YELLOW],
        text="Total_Diesel",
    )
    fig_proj.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
    fig_proj.update_layout(height=max(300, len(proj_df) * 35), margin=dict(l=10, r=80))
    st.plotly_chart(fig_proj, use_container_width=True)

    # Table
    st.markdown("#### Project Summary Table")
    display_proj = proj_df[["Project", "Total_Diesel", "% of Total", "Vehicles", "Avg / Day", "Total Cost (SGD)"]].copy()
    display_proj.columns = ["Project", "Total Diesel (L)", "% of Total", "Vehicles", "Avg / Day", "Total Cost (SGD)"]
    display_proj["Total Diesel (L)"] = display_proj["Total Diesel (L)"].map("{:,.2f}".format)
    display_proj["% of Total"]       = display_proj["% of Total"].map("{:.1f}%".format)
    display_proj["Avg / Day"]        = display_proj["Avg / Day"].map("{:,.1f}".format)
    display_proj["Total Cost (SGD)"] = display_proj["Total Cost (SGD)"].map("${:,.2f}".format)
    st.dataframe(display_proj, use_container_width=True, hide_index=False)

# ══════════════════════════════════════════════
# TAB 2 — DAILY DIESEL TREND
# ══════════════════════════════════════════════
with tab2:
    st.subheader("📅 Daily Diesel Trend")

    daily_df = (
        df.groupby(["Day_Sort", "Day"])["Diesel Litre"]
        .sum()
        .reset_index()
        .sort_values("Day_Sort")
        .rename(columns={"Diesel Litre": "Daily Total"})
    )

    # Line + bar chart
    fig_daily = px.bar(
        daily_df, x="Day", y="Daily Total",
        title="Daily Diesel Consumption (Litres)",
        labels={"Daily Total": "Litres", "Day": "Date"},
        color_discrete_sequence=[BRAND_YELLOW],
        text="Daily Total",
    )
    fig_daily.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
    fig_daily.update_layout(
        xaxis_tickangle=-45,
        height=460,
        xaxis=dict(tickmode="array", tickvals=daily_df["Day"].tolist()),
    )
    st.plotly_chart(fig_daily, use_container_width=True)

    # Daily table — two columns side by side for compact view
    st.markdown("#### Daily Total Table")
    daily_display = daily_df[["Day", "Daily Total"]].copy()
    daily_display["Daily Total"] = daily_display["Daily Total"].map("{:,.1f}".format)
    daily_display.columns = ["Date", "Daily Total (L)"]
    daily_display = daily_display.reset_index(drop=True)
    daily_display.index += 1

    # Split into two halves for side-by-side display
    half = len(daily_display) // 2 + len(daily_display) % 2
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.dataframe(daily_display.iloc[:half], use_container_width=True)
    with col_d2:
        st.dataframe(daily_display.iloc[half:], use_container_width=True)

# ══════════════════════════════════════════════
# TAB 3 — DIESEL BY VEHICLE
# ══════════════════════════════════════════════
with tab3:
    st.subheader("🚛 Diesel by Vehicle")

    # Per vehicle: total diesel, avg/day, # projects, project names
    veh_proj = (
        df.groupby("Vehicle No")["Project"]
        .agg(lambda x: sorted(x.dropna().unique()))
        .reset_index()
    )
    veh_proj["# Projects"]    = veh_proj["Project"].apply(len)
    veh_proj["Project Names"] = veh_proj["Project"].apply(lambda x: ", ".join(x))
    veh_proj.drop(columns=["Project"], inplace=True)

    # Add Model & Type per vehicle
    veh_model = df.drop_duplicates("Vehicle No")[["Vehicle No", "Model", "Type"]]

    veh_df = (
        df.groupby("Vehicle No")["Diesel Litre"]
        .sum()
        .reset_index()
        .rename(columns={"Diesel Litre": "Total Diesel"})
        .sort_values("Total Diesel", ascending=False)
        .reset_index(drop=True)
    )
    veh_df.index += 1
    veh_df["% of Total"]       = (veh_df["Total Diesel"] / veh_df["Total Diesel"].sum() * 100).round(1)
    avg_label = "Avg / Day" if view_mode == "Monthly" else "Avg / Month"
    avg_divisor = num_days if view_mode == "Monthly" else max(df["Month"].nunique(), 1)
    veh_df[avg_label]          = (veh_df["Total Diesel"] / avg_divisor).round(1)
    veh_df["Total Cost (SGD)"] = (veh_df["Total Diesel"] * price_per_litre).round(2)
    veh_df = veh_df.merge(veh_proj, on="Vehicle No", how="left")
    veh_df = veh_df.merge(veh_model, on="Vehicle No", how="left")

    # Period breakdown per vehicle (top 10)
    st.markdown(f"#### Top 10 Vehicles — {view_mode} Breakdown")
    top10_vehs = veh_df.head(10)["Vehicle No"].tolist()
    veh_period = (
        df[df["Vehicle No"].isin(top10_vehs)]
        .groupby(["Vehicle No", period_label])["Diesel Litre"]
        .sum().reset_index()
    )
    fig_vp = px.bar(
        veh_period, x=period_label, y="Diesel Litre",
        color="Vehicle No", barmode="group",
        title=f"Top 10 Vehicles Diesel by {view_mode}",
        labels={"Diesel Litre":"Litres", period_label: view_mode},
        text="Diesel Litre",
    )
    fig_vp.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
    fig_vp.update_layout(height=420, xaxis_tickangle=-30, xaxis=dict(type="category"))
    st.plotly_chart(fig_vp, use_container_width=True)

    # Top 15 chart
    top15 = veh_df.head(15).sort_values("Total Diesel")
    fig_veh = px.bar(
        top15, x="Total Diesel", y="Vehicle No", orientation="h",
        title="Top 15 Vehicles by Diesel Usage",
        labels={"Total Diesel": "Litres", "Vehicle No": "Vehicle"},
        color_discrete_sequence=[BRAND_YELLOW],
        text="Total Diesel",
    )
    fig_veh.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
    fig_veh.update_layout(height=500, margin=dict(r=80))
    st.plotly_chart(fig_veh, use_container_width=True)

    # Full vehicle table
    st.markdown("#### Vehicle Summary Table")
    avg_col = avg_label  # "Avg / Day" or "Avg / Month"
    display_veh = veh_df[["Vehicle No", "Model", "Type", "Total Diesel", "% of Total",
                            avg_col, "Total Cost (SGD)", "# Projects", "Project Names"]].copy()
    display_veh.columns = ["Vehicle", "Model", "Type", "Total Diesel (L)", "% of Total",
                             avg_col, "Total Cost (SGD)", "# Projects", "Project Names"]
    display_veh["Total Diesel (L)"] = display_veh["Total Diesel (L)"].map("{:,.2f}".format)
    display_veh["% of Total"]       = display_veh["% of Total"].map("{:.1f}%".format)
    display_veh[avg_col]            = display_veh[avg_col].map("{:,.1f}".format)
    display_veh["Total Cost (SGD)"] = display_veh["Total Cost (SGD)"].map("${:,.2f}".format)
    st.dataframe(display_veh, use_container_width=True, height=500, hide_index=False)

# ══════════════════════════════════════════════
# TAB 4 — BOWSER (YP9421D-T)
# ══════════════════════════════════════════════
with tab4:
    st.subheader("🚰 Bowser Tracker — YP9421D-T")

    if bowser_raw is None:
        st.info("Please upload the Bowser Dispensing Log (Report 4) to see this section.")
    else:
        # ── Filter to selected date range ──
        bdf = bowser_raw.copy()
        bdf = bdf[(bdf["Date"].dt.date >= date_from) & (bdf["Date"].dt.date <= date_to)]

        # ── Split IN vs OUT ──
        b_in  = bdf[bdf["Record Type"] == "Office Top-Up (IN)"]
        b_out = bdf[bdf["Record Type"] == "Dispensed to Vehicle (OUT)"]

        # ── Also get YP9421D-T top-ups from transaction file (pump station IN) ──
        pump_in = df[df["Vehicle No"] == "YP9421D-T"][["Date", "Diesel Litre"]].copy()
        pump_in["Source"] = "Pump Station (Transaction File)"
        pump_in_total = pump_in["Diesel Litre"].sum()

        office_in_total = b_in["Qty Litres"].sum()
        total_out       = b_out["Qty Litres"].sum()
        # Official balance uses system record (transaction file) as IN
        total_in        = pump_in_total  # system record is official

        # ── Balance uses Transaction file as official IN ──
        official_balance   = pump_in_total - total_out
        manual_vs_system   = pump_in_total - office_in_total  # how much they differ

        # ── KPI Cards ──
        st.markdown("#### Bowser Fuel Balance")
        st.caption("📌 Official IN = Transaction file (system record). Office Top-Up is manual reference only.")

        bk1, bk2, bk3, bk4, bk5 = st.columns(5)
        bk1.metric("📟 System IN — Transaction (L)",  f"{pump_in_total:,.1f}",
                   help="Official figure from the diesel transaction system (YP9421D-T top-ups)")
        bk2.metric("📝 Manual IN — Office Log (L)",   f"{office_in_total:,.1f}",
                   help="Manual entry in dispensing log — for reference/verification only")
        bk3.metric("🔍 System vs Manual Diff (L)",
                   f"{manual_vs_system:,.1f}",
                   delta=f"{manual_vs_system:,.1f}",
                   delta_color="off",
                   help="Difference between system record and manual record. Should be close to 0.")
        bk4.metric("📤 Total Dispensed OUT (L)",      f"{total_out:,.1f}")
        bk5.metric(
            "⚖️ Balance (System IN − OUT) (L)",
            f"{official_balance:,.1f}",
            delta=f"{official_balance:,.1f}",
            delta_color="normal" if official_balance >= 0 else "inverse",
            help="System IN minus Dispensed OUT. Positive = fuel still in bowser. Negative = over-dispensed."
        )

        # Status messages
        if abs(manual_vs_system) > 200:
            st.warning(
                f"⚠️ System IN and Manual IN differ by **{abs(manual_vs_system):,.1f}L** — "
                "please verify both records match."
            )
        else:
            st.success(f"✅ System IN vs Manual IN difference is {abs(manual_vs_system):,.1f}L — within acceptable range.")

        if official_balance < 0:
            st.error(
                f"🚨 Dispensed **{abs(official_balance):,.1f}L MORE** than received (System IN). "
                "Possible missing top-up record or dispensing error."
            )
        elif official_balance > 1000:
            st.info(f"ℹ️ {official_balance:,.1f}L balance — may be carried over from previous period.")
        else:
            st.success(f"✅ Bowser balance of {official_balance:,.1f}L looks reasonable.")

        st.divider()

        # ── Daily IN vs OUT Chart ──
        st.markdown("#### Daily Bowser Flow")

        # Daily pump-in
        pump_daily = (
            pump_in.groupby(pump_in["Date"].dt.date)["Diesel Litre"]
            .sum().reset_index()
            .rename(columns={"Date": "Date", "Diesel Litre": "Litres"})
        )
        pump_daily["Type"] = "Pump Station IN"

        # Daily office top-up
        office_daily = (
            b_in.groupby(b_in["Date"].dt.date)["Qty Litres"]
            .sum().reset_index()
            .rename(columns={"Date": "Date", "Qty Litres": "Litres"})
        )
        office_daily["Type"] = "Office Top-Up IN"

        # Daily dispensed
        out_daily = (
            b_out.groupby(b_out["Date"].dt.date)["Qty Litres"]
            .sum().reset_index()
            .rename(columns={"Date": "Date", "Qty Litres": "Litres"})
        )
        out_daily["Type"] = "Dispensed OUT"

        flow_df = pd.concat([pump_daily, office_daily, out_daily], ignore_index=True)
        flow_df["Date"] = flow_df["Date"].astype(str)

        fig_flow = px.bar(
            flow_df, x="Date", y="Litres", color="Type",
            barmode="group",
            title="Daily Bowser: Fuel IN vs Dispensed OUT",
            color_discrete_map={
                "Pump Station IN":  BRAND_YELLOW,    # official IN — primary brand colour
                "Office Top-Up IN": BRAND_YELLOW_D,  # manual IN — darker gold variant
                "Dispensed OUT":    "#d62728",        # dispensed — keep red (warning signal)
            },
        )
        fig_flow.update_layout(xaxis_tickangle=-45, height=420)
        st.plotly_chart(fig_flow, use_container_width=True)

        st.divider()
        # ── Site totals from bowser dispensing ──
        st.markdown("#### Bowser Dispensed by Site")

        # Site is stored in Remarks column (CR110, AIP2, TAC etc.)
        # Clean: exclude office top-up type remarks
        office_keywords = ["office top up", "office top", "kranji office"]
        b_out_site = b_out.copy()
        b_out_site["Site"] = b_out_site["Remarks"].astype(str).str.strip()
        b_out_site.loc[
            b_out_site["Site"].str.lower().isin(office_keywords), "Site"
        ] = "Unknown"

        site_total = (
            b_out_site.groupby("Site")["Qty Litres"]
            .sum().reset_index()
            .sort_values("Qty Litres", ascending=False)
            .reset_index(drop=True)
        )
        site_total["% of Total"] = (
            site_total["Qty Litres"] / site_total["Qty Litres"].sum() * 100
        ).round(1)

        sc1, sc2 = st.columns(2)
        with sc1:
            fig_site_bowser = px.bar(
                site_total.sort_values("Qty Litres"),
                x="Qty Litres", y="Site", orientation="h",
                title="Bowser Dispensed by Site (L)",
                color_discrete_sequence=[BRAND_GREY],
                text="Qty Litres",
            )
            fig_site_bowser.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
            fig_site_bowser.update_layout(
                yaxis={"categoryorder": "total ascending"},
                height=400, margin=dict(r=60)
            )
            st.plotly_chart(fig_site_bowser, use_container_width=True)

        with sc2:
            site_display = site_total.copy()
            site_display.index += 1
            site_display["Qty Litres"]   = site_display["Qty Litres"].map("{:,.1f}".format)
            site_display["% of Total"]   = site_display["% of Total"].map("{:.1f}%".format)
            site_display.columns = ["Site", "Total Dispensed (L)", "% of Total"]
            st.dataframe(site_display, use_container_width=True, height=400)

        st.divider()
        bcol1, bcol2 = st.columns(2)

        # ── Dispensed by Equipment with Site ──
        with bcol1:
            st.markdown("#### Diesel Dispensed by Equipment (with Site)")
            equip_df = (
                b_out_site.groupby(["Equipment ID", "Site"])["Qty Litres"]
                .sum().reset_index()
                .sort_values("Qty Litres", ascending=False)
                .reset_index(drop=True)
            )
            equip_df.index += 1
            equip_df["% of Total"] = (
                equip_df["Qty Litres"] / equip_df["Qty Litres"].sum() * 100
            ).round(1)
            equip_df.columns = ["Equipment ID", "Site", "Total Dispensed (L)", "% of Total"]
            equip_df["Total Dispensed (L)"] = equip_df["Total Dispensed (L)"].map("{:,.1f}".format)
            equip_df["% of Total"]          = equip_df["% of Total"].map("{:.1f}%".format)
            st.dataframe(equip_df, use_container_width=True, height=450)

        # ── Top 15 Equipment chart ──
        with bcol2:
            st.markdown("#### Top 15 Equipment by Consumption")
            top_equip = (
                b_out_site.groupby("Equipment ID")["Qty Litres"]
                .sum().nlargest(15).reset_index()
                .sort_values("Qty Litres")
            )
            # Add site label to each equipment
            equip_site_label = (
                b_out_site.groupby("Equipment ID")["Site"]
                .agg(lambda x: x.mode()[0])
                .reset_index()
                .rename(columns={"Site": "Main Site"})
            )
            top_equip = top_equip.merge(equip_site_label, on="Equipment ID", how="left")
            top_equip["Label"] = top_equip["Equipment ID"] + " (" + top_equip["Main Site"] + ")"

            fig_equip = px.bar(
                top_equip, x="Qty Litres", y="Label", orientation="h",
                color_discrete_sequence=[BRAND_YELLOW],
                text="Qty Litres",
                title="Top 15 Equipment (Site in brackets)",
            )
            fig_equip.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
            fig_equip.update_layout(
                yaxis={"categoryorder": "total ascending"},
                height=450, margin=dict(r=60)
            )
            st.plotly_chart(fig_equip, use_container_width=True)

        st.divider()

        # ── Full dispensing log ──
        st.markdown("#### Full Dispensing Log")
        log_cols = [c for c in ["Date", "Equipment ID", "Qty Litres", "Remarks",
                                  "Employee ID", "Record Type"] if c in bdf.columns]
        st.dataframe(
            bdf[log_cols].sort_values("Date", ascending=False).reset_index(drop=True),
            use_container_width=True, height=350
        )

        # Export
        def bowser_excel(b_in_df, b_out_df, pump_df, equip_data, site_df):
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                summary = pd.DataFrame({
                    "Item": [
                        "System IN — Transaction File (Official)",
                        "Manual IN — Office Top-Up Log (Reference)",
                        "System vs Manual Difference",
                        "Total Dispensed OUT",
                        "Balance (System IN − OUT)",
                    ],
                    "Litres": [
                        pump_in_total,
                        office_in_total,
                        pump_in_total - office_in_total,
                        total_out,
                        pump_in_total - total_out,
                    ]
                })
                summary.to_excel(writer,  index=False, sheet_name="Summary")
                site_df.to_excel(writer,   index=False, sheet_name="Dispensed by Site")
                equip_data.to_excel(writer, index=False, sheet_name="Dispensed by Equipment")
                b_in_df.to_excel(writer,  index=False, sheet_name="Office Top-Up IN")
                b_out_df.to_excel(writer, index=False, sheet_name="Dispensed OUT")
                pump_df.to_excel(writer,  index=False, sheet_name="Pump Station IN")
            return buffer.getvalue()

        st.download_button(
            label="📥 Download Bowser Report as Excel",
            data=bowser_excel(b_in, b_out, pump_in, equip_df, site_total),
            file_name="bowser_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )


# ══════════════════════════════════════════════
# TAB 5 — COMPARE MODE
# ══════════════════════════════════════════════
with tab5:
    st.subheader("📊 Compare Mode")

    if all_diesel_raw.empty:
        st.info(
            "Upload more than one diesel file in Report 1 to use Compare Mode. "
            "Each file should represent one month. You can select multiple files at once."
        )
    else:
        @st.cache_data
        def build_compare_df(raw, _job_raw, _veh_raw):
            dfc = clean_diesel(raw)
            jc  = clean_job(_job_raw) if _job_raw is not None else None
            dfc = merge_reports(dfc, jc)
            if _veh_raw is not None:
                dfc = dfc.merge(_veh_raw, on="Vehicle No", how="left")
                dfc["Model"] = dfc["Model"].fillna("Unknown")
                dfc["Type"]  = dfc["Type"].fillna("Unknown")
            else:
                dfc["Model"] = "N/A"
                dfc["Type"]  = "N/A"
            dfc["Month"]       = dfc["Date"].dt.strftime("%Y-%m")
            dfc["Month_Label"] = dfc["Date"].dt.strftime("%b %Y")
            return dfc

        cdf = build_compare_df(all_diesel_raw, job_raw, veh_raw)
        months_available = sorted(cdf["Month"].unique())
        month_labels_map = {m: cdf[cdf["Month"]==m]["Month_Label"].iloc[0] for m in months_available}

        st.success("Months loaded: " + ", ".join(month_labels_map.values()))

        # ── Filter controls in one row ──
        f1, f2, f3 = st.columns(3)

        with f1:
            compare_type = st.selectbox(
                "📊 Compare By",
                options=[
                    "All",
                    "Month vs Month",
                    "Site vs Site",
                    "Vehicle vs Vehicle",
                ],
            )

        with f2:
            sel_months = st.multiselect(
                "📅 Select Months",
                options=months_available,
                default=months_available,
                format_func=lambda m: month_labels_map[m],
            )

        with f3:
            # Site filter only relevant for Site and Vehicle views
            all_sites   = sorted(cdf["Project"].dropna().unique())
            sel_sites_c = st.multiselect("🏗️ Filter Sites", all_sites, default=all_sites)

        if not sel_months:
            st.warning("Please select at least one month.")
        else:
            cdf = cdf[cdf["Month"].isin(sel_months)]
            cdf = cdf[cdf["Project"].isin(sel_sites_c)]
            ordered_labels = [month_labels_map[m] for m in sorted(sel_months)]

            # ── Pre-compute shared aggregates ──
            month_sum = (
                cdf.groupby(["Month","Month_Label"])
                .agg(
                    Total_Litre  = ("Diesel Litre", "sum"),
                    Transactions = ("Diesel Litre", "count"),
                    Vehicles     = ("Vehicle No",   "nunique"),
                )
                .reset_index().sort_values("Month")
            )

            site_month = (
                cdf.groupby(["Project","Month_Label"])["Diesel Litre"]
                .sum().reset_index().sort_values(["Project","Month_Label"])
            )
            site_pivot = site_month.pivot(index="Project", columns="Month_Label", values="Diesel Litre").fillna(0)
            site_pivot = site_pivot[[c for c in ordered_labels if c in site_pivot.columns]]
            site_pivot["Total"] = site_pivot.sum(axis=1)
            site_pivot = site_pivot.sort_values("Total", ascending=False)

            show_month   = compare_type in ("All", "Month vs Month")
            show_site    = compare_type in ("All", "Site vs Site")
            show_vehicle = compare_type in ("All", "Vehicle vs Vehicle")

            st.divider()

            # ══════════════════════
            # MONTH VS MONTH
            # ══════════════════════
            if show_month:
                st.markdown("### 📅 Month vs Month")
                ma1, ma2 = st.columns(2)
                with ma1:
                    fig_mo = px.bar(month_sum, x="Month_Label", y="Total_Litre",
                        title="Total Diesel per Month (L)", text="Total_Litre",
                        color="Month_Label", labels={"Total_Litre":"Litres","Month_Label":"Month"})
                    fig_mo.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
                    fig_mo.update_layout(showlegend=False, height=380)
                    st.plotly_chart(fig_mo, use_container_width=True)
                with ma2:
                    fig_vm2 = px.bar(month_sum, x="Month_Label", y="Vehicles",
                        title="Unique Vehicles per Month", text="Vehicles",
                        color="Month_Label", labels={"Vehicles":"Vehicles","Month_Label":"Month"})
                    fig_vm2.update_traces(texttemplate="%{text}", textposition="outside")
                    fig_vm2.update_layout(showlegend=False, height=380)
                    st.plotly_chart(fig_vm2, use_container_width=True)

                disp_mo = month_sum.copy()
                disp_mo["Total_Litre"] = disp_mo["Total_Litre"].map("{:,.1f}".format)
                disp_mo.columns = ["Month","Month Label","Total Litre (L)","Top-Ups","Vehicles"]
                st.dataframe(disp_mo[["Month Label","Total Litre (L)","Top-Ups","Vehicles"]].reset_index(drop=True), use_container_width=True)
                if show_site or show_vehicle:
                    st.divider()

            # ══════════════════════
            # SITE VS SITE
            # ══════════════════════
            if show_site:
                st.markdown("### 🏗️ Site vs Site Across Months")
                fig_sm = px.bar(site_month, x="Month_Label", y="Diesel Litre",
                    color="Project", barmode="group",
                    title="Diesel by Site per Month",
                    labels={"Diesel Litre":"Litres","Month_Label":"Month"}, text="Diesel Litre")
                fig_sm.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
                fig_sm.update_layout(height=450, xaxis_tickangle=-30)
                st.plotly_chart(fig_sm, use_container_width=True)
                st.dataframe(site_pivot.map(lambda x: f"{x:,.1f}"), use_container_width=True)
                if show_vehicle:
                    st.divider()

            # ══════════════════════
            # VEHICLE VS VEHICLE
            # ══════════════════════
            if show_vehicle:
                st.markdown("### 🚛 Vehicle vs Vehicle Across Months")
                vc1, vc2 = st.columns([1, 3])
                with vc1:
                    top_n = st.number_input(
                        "Top N vehicles", min_value=5, max_value=50,
                        value=15, step=5, key="compare_topn"
                    )
                    chart_type = st.selectbox(
                        "Chart type",
                        ["Grouped Bar", "Stacked Bar", "Line"],
                        key="compare_chart_type"
                    )

                top_vehs = cdf.groupby("Vehicle No")["Diesel Litre"].sum().nlargest(int(top_n)).index.tolist()
                veh_month = (
                    cdf[cdf["Vehicle No"].isin(top_vehs)]
                    .groupby(["Vehicle No","Month_Label"])["Diesel Litre"]
                    .sum().reset_index()
                )

                if chart_type == "Line":
                    fig_vmc = px.line(veh_month, x="Month_Label", y="Diesel Litre",
                        color="Vehicle No", markers=True,
                        title=f"Top {int(top_n)} Vehicles — Diesel Trend by Month",
                        labels={"Diesel Litre":"Litres","Month_Label":"Month","Vehicle No":"Vehicle"})
                    fig_vmc.update_layout(height=480)
                else:
                    bmode = "group" if chart_type == "Grouped Bar" else "stack"
                    fig_vmc = px.bar(veh_month, x="Diesel Litre", y="Vehicle No",
                        color="Month_Label", barmode=bmode, orientation="h",
                        title=f"Top {int(top_n)} Vehicles — Diesel by Month",
                        labels={"Diesel Litre":"Litres","Vehicle No":"Vehicle","Month_Label":"Month"},
                        text="Diesel Litre")
                    fig_vmc.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
                    fig_vmc.update_layout(
                        yaxis={"categoryorder":"total ascending"},
                        height=max(400,int(top_n)*40), margin=dict(r=80)
                    )

                with vc2:
                    st.plotly_chart(fig_vmc, use_container_width=True)

                # Vehicle pivot table
                veh_pivot = (
                    cdf[cdf["Vehicle No"].isin(top_vehs)]
                    .groupby(["Vehicle No","Month_Label"])["Diesel Litre"]
                    .sum().reset_index()
                    .pivot(index="Vehicle No", columns="Month_Label", values="Diesel Litre")
                    .fillna(0)
                )
                veh_pivot = veh_pivot[[c for c in ordered_labels if c in veh_pivot.columns]]
                veh_pivot["Total"] = veh_pivot.sum(axis=1)
                veh_pivot = veh_pivot.sort_values("Total", ascending=False)
                if veh_raw is not None:
                    veh_info = cdf.drop_duplicates("Vehicle No")[["Vehicle No","Model","Type"]].set_index("Vehicle No")
                    veh_pivot = veh_pivot.join(veh_info, how="left")
                    cols_order = ["Model","Type"] + [c for c in ordered_labels if c in veh_pivot.columns] + ["Total"]
                    veh_pivot = veh_pivot[[c for c in cols_order if c in veh_pivot.columns]]
                st.dataframe(
                    veh_pivot.map(lambda x: f"{x:,.1f}" if isinstance(x, float) else x),
                    use_container_width=True, height=450
                )
            else:
                veh_pivot = pd.DataFrame()

            st.divider()

            # ── Export ──
            def compare_excel_export(ms, sp, vp, full):
                buf = BytesIO()
                with pd.ExcelWriter(buf, engine="openpyxl") as w:
                    ms.to_excel(w, index=False, sheet_name="Month Summary")
                    sp.to_excel(w, sheet_name="Site by Month")
                    if not vp.empty:
                        vp.to_excel(w, sheet_name="Vehicle by Month")
                    cols = [c for c in ["Date","Vehicle No","Model","Type","Project",
                                         "Diesel Litre","Month_Label"] if c in full.columns]
                    full[cols].to_excel(w, index=False, sheet_name="All Transactions")
                return buf.getvalue()

            st.download_button(
                label="📥 Download Compare Report as Excel",
                data=compare_excel_export(month_sum, site_pivot, veh_pivot, cdf),
                file_name="diesel_compare_report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )


# ══════════════════════════════════════════════
# TAB 6 — KM/L ANALYSIS
# ══════════════════════════════════════════════
with tab6:
    st.subheader("⚡ KM/L Analysis — Odometer Based")

    if odometer_raw is None or odometer_raw.empty:
        st.info(
            "Please upload the **Odometer Detail** file (Report 5) to enable KM/L analysis. "
            "The diesel top-up file alone cannot calculate KM/L accurately — "
            "the odometer report gives actual daily distance travelled per vehicle."
        )
    else:
        st.success(f"Odometer data loaded: {odometer_raw['Vehicle No'].nunique()} vehicles, "
                   f"{len(odometer_raw)} daily records.")

        # ── Correct KM/L calculation ──
        # Total KM = ALL daily distances from odometer (not just top-up days)
        # Total Diesel = all diesel topped up in the period
        # KM/L = Total Monthly KM / Total Monthly Diesel

        # Step 1: Total KM per vehicle per month from odometer
        odo_monthly = (
            odometer_raw.groupby(["Vehicle No", "Month"])
            .agg(
                Total_KM     = ("Distance KM", "sum"),
                Active_Days  = ("Date_Only",   "nunique"),
                Start_KM     = ("Start KM",    "min"),
                End_KM       = ("End KM",      "max"),
            )
            .reset_index()
        )

        # Step 2: Total diesel per vehicle per month from diesel report
        diesel_monthly = (
            df.groupby(["Vehicle No", "Month"])
            .agg(
                Total_Diesel = ("Diesel Litre", "sum"),
                Project      = ("Project",       lambda x: x.mode()[0]),
                Model        = ("Model",         "first"),
                Type         = ("Type",          "first"),
            )
            .reset_index()
        )

        # Step 3: Merge on vehicle + month
        kml_monthly = diesel_monthly.merge(odo_monthly, on=["Vehicle No", "Month"], how="left")
        kml_monthly["KM/L"] = kml_monthly["Total_KM"] / kml_monthly["Total_Diesel"]
        kml_monthly["KM/L"] = kml_monthly["KM/L"].replace([float("inf"), -float("inf")], None)
        kml_monthly.loc[kml_monthly["KM/L"] < 0, "KM/L"] = None

        # Step 4: Overall vehicle summary (across all months)
        veh_kml = (
            kml_monthly.groupby("Vehicle No")
            .agg(
                Model        = ("Model",        "first"),
                Type         = ("Type",         "first"),
                Total_Diesel = ("Total_Diesel", "sum"),
                Total_KM     = ("Total_KM",     "sum"),
                Days         = ("Active_Days",  "sum"),
            )
            .reset_index()
        )
        veh_kml["KM/L"] = veh_kml["Total_KM"] / veh_kml["Total_Diesel"]
        veh_kml["KM/L"] = veh_kml["KM/L"].replace([float("inf"), -float("inf")], None)
        veh_kml = veh_kml.dropna(subset=["KM/L"]).sort_values("KM/L", ascending=False)

        # Step 5: Daily detail — odometer joined with diesel for drill-down
        diesel_daily = (
            df.groupby(["Vehicle No", "Date_Only"])
            .agg(
                Diesel_Litre = ("Diesel Litre", "sum"),
                Project      = ("Project",      lambda x: x.mode()[0]),
            )
            .reset_index()
        )
        odo_daily = odometer_raw[["Vehicle No", "Date_Only", "Distance KM", "Start KM", "End KM"]].copy()
        # Full outer join so we see all days (with or without top-up)
        kml_df = odo_daily.merge(diesel_daily, on=["Vehicle No", "Date_Only"], how="left")
        kml_df = kml_df.merge(
            df.drop_duplicates("Vehicle No")[["Vehicle No","Model","Type"]],
            on="Vehicle No", how="left"
        )
        kml_df["Diesel_Litre"] = kml_df["Diesel_Litre"].fillna(0)

        # ── KPI Cards ──
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("📊 Vehicles with KM/L", veh_kml["Vehicle No"].nunique())
        k2.metric("🏆 Best KM/L",
                  f"{veh_kml['KM/L'].max():.2f} ({veh_kml.loc[veh_kml['KM/L'].idxmax(),'Vehicle No']})")
        k3.metric("⚠️ Worst KM/L",
                  f"{veh_kml['KM/L'].min():.2f} ({veh_kml.loc[veh_kml['KM/L'].idxmin(),'Vehicle No']})")
        k4.metric("📈 Fleet Avg KM/L", f"{veh_kml['KM/L'].mean():.2f}")

        st.divider()

        # ── Filter controls — persist thresholds across re-uploads ──
        if "kml_low" not in st.session_state:
            st.session_state["kml_low"] = 1.5
        if "kml_high" not in st.session_state:
            st.session_state["kml_high"] = 10.0

        kf1, kf2 = st.columns(2)
        with kf1:
            kml_low  = st.number_input("Flag KM/L below (abnormal low)",  value=st.session_state["kml_low"],
                                        step=0.1, format="%.1f", key="kml_low")
        with kf2:
            kml_high = st.number_input("Flag KM/L above (abnormal high)", value=st.session_state["kml_high"],
                                        step=0.5, format="%.1f", key="kml_high")

        veh_kml["Status"] = veh_kml["KM/L"].apply(
            lambda x: "🔴 Too Low"  if x < kml_low
            else ("🟡 Too High" if x > kml_high
            else "🟢 Normal")
        )

        st.divider()
        c1, c2 = st.columns(2)

        # ── Best vs Worst KM/L chart ──
        with c1:
            top15_kml = veh_kml.nlargest(15, "KM/L").sort_values("KM/L")
            fig_best = px.bar(
                top15_kml, x="KM/L", y="Vehicle No", orientation="h",
                title="Top 15 — Best KM/L (Most Efficient)",
                color="KM/L", color_continuous_scale="Greens",
                text="KM/L",
            )
            fig_best.update_traces(texttemplate="%{text:.2f}", textposition="outside")
            fig_best.update_layout(height=500, coloraxis_showscale=False)
            st.plotly_chart(fig_best, use_container_width=True)

        with c2:
            worst15_kml = veh_kml.nsmallest(15, "KM/L").sort_values("KM/L", ascending=False)
            fig_worst = px.bar(
                worst15_kml, x="KM/L", y="Vehicle No", orientation="h",
                title="Bottom 15 — Worst KM/L (Least Efficient)",
                color="KM/L", color_continuous_scale="Reds_r",
                text="KM/L",
            )
            fig_worst.update_traces(texttemplate="%{text:.2f}", textposition="outside")
            fig_worst.update_layout(height=500, coloraxis_showscale=False)
            st.plotly_chart(fig_worst, use_container_width=True)

        st.divider()

        # ── KM/L by Vehicle Type ──
        st.markdown("#### KM/L by Vehicle Type")
        type_kml = (
            veh_kml.groupby("Type")
            .agg(Avg_KML=("KM/L","mean"), Vehicles=("Vehicle No","count"))
            .reset_index().sort_values("Avg_KML", ascending=False)
        )
        fig_type = px.bar(
            type_kml, x="Type", y="Avg_KML",
            title="Average KM/L by Vehicle Type",
            text="Avg_KML", color="Avg_KML",
            color_continuous_scale=[[0, BRAND_YELLOW_L], [0.5, BRAND_YELLOW], [1, BRAND_YELLOW_D]],
            labels={"Avg_KML":"Avg KM/L","Type":"Vehicle Type"},
        )
        fig_type.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        fig_type.update_layout(coloraxis_showscale=False, height=380)
        st.plotly_chart(fig_type, use_container_width=True)

        st.divider()

        # ── Daily KM/L trend for selected vehicle ──
        st.markdown("#### Daily KM/L Trend — Single Vehicle Drill-Down")
        vehs_with_kml = sorted(veh_kml["Vehicle No"].unique())
        sel_veh_kml   = st.selectbox("Select Vehicle", vehs_with_kml, key="kml_veh_select")

        # Monthly trend for selected vehicle
        veh_monthly = kml_monthly[kml_monthly["Vehicle No"] == sel_veh_kml].sort_values("Month")

        # Daily odometer detail for selected vehicle
        veh_daily = kml_df[kml_df["Vehicle No"] == sel_veh_kml].sort_values("Date_Only").copy()
        veh_daily["Date_Str"] = veh_daily["Date_Only"].astype(str).str[:10]  # YYYY-MM-DD only

        # Compute daily KM/L only on days with BOTH distance and diesel top-up
        veh_daily["Daily_KML"] = veh_daily.apply(
            lambda r: r["Distance KM"] / r["Diesel_Litre"]
            if (pd.notna(r["Distance KM"]) and r["Diesel_Litre"] > 0)
            else None, axis=1
        )

        # ── Chart 1: Daily Distance bar ──
        st.markdown(f"#### Daily Distance (KM) — {sel_veh_kml}")
        fig_dist = px.bar(
            veh_daily, x="Date_Str", y="Distance KM",
            title=f"Daily Distance — {sel_veh_kml}",
            text="Distance KM",
            color_discrete_sequence=[BRAND_GREY],
            labels={"Distance KM": "KM", "Date_Str": "Date"},
        )
        fig_dist.update_traces(texttemplate="%{text:,.1f}", textposition="outside")
        fig_dist.update_layout(xaxis_tickangle=-45, height=380,
                                xaxis=dict(type="category"))
        st.plotly_chart(fig_dist, use_container_width=True)

        # ── Chart 2: Daily Diesel Top-Up bar ──
        st.markdown(f"#### Daily Diesel Top-Up (L) — {sel_veh_kml}")
        topup_only = veh_daily[veh_daily["Diesel_Litre"] > 0]
        fig_diesel = px.bar(
            topup_only, x="Date_Str", y="Diesel_Litre",
            title=f"Daily Diesel Top-Up — {sel_veh_kml}",
            text="Diesel_Litre",
            color_discrete_sequence=[BRAND_YELLOW],
            labels={"Diesel_Litre": "Litres", "Date_Str": "Date"},
        )
        fig_diesel.update_traces(texttemplate="%{text:,.1f}", textposition="outside")
        fig_diesel.update_layout(xaxis_tickangle=-45, height=320,
                                  xaxis=dict(type="category"))
        st.plotly_chart(fig_diesel, use_container_width=True)

        # ── Chart 3: Daily KM/L (only on top-up days) ──
        daily_kml_data = veh_daily[veh_daily["Daily_KML"].notna()]
        if not daily_kml_data.empty:
            st.markdown(f"#### Daily KM/L (Top-Up Days Only) — {sel_veh_kml}")
            fig_dkml = px.bar(
                daily_kml_data, x="Date_Str", y="Daily_KML",
                title=f"Daily KM/L on Top-Up Days — {sel_veh_kml}",
                text="Daily_KML",
                color_discrete_sequence=[BRAND_YELLOW],
                labels={"Daily_KML": "KM/L", "Date_Str": "Date"},
            )
            fig_dkml.update_traces(texttemplate="%{text:.2f}", textposition="outside")
            fig_dkml.add_hline(y=kml_low,  line_dash="dash", line_color="red",
                                annotation_text=f"Low: {kml_low}")
            fig_dkml.add_hline(y=kml_high, line_dash="dash", line_color="orange",
                                annotation_text=f"High: {kml_high}")
            fig_dkml.update_layout(xaxis_tickangle=-45, height=360,
                                    xaxis=dict(type="category"))
            st.plotly_chart(fig_dkml, use_container_width=True)

        veh_detail = veh_daily[["Date_Only","Start KM","End KM","Distance KM","Diesel_Litre","Project"]].copy()
        veh_detail.columns = ["Date","Start KM","End KM","Distance KM","Diesel Top-Up (L)","Project"]
        veh_detail["Distance KM"]      = veh_detail["Distance KM"].apply(lambda x: f"{x:,.2f}" if pd.notna(x) else "N/A")
        veh_detail["Start KM"]         = veh_detail["Start KM"].apply(lambda x: f"{x:,.2f}" if pd.notna(x) else "N/A")
        veh_detail["End KM"]           = veh_detail["End KM"].apply(lambda x: f"{x:,.2f}" if pd.notna(x) else "N/A")
        veh_detail["Diesel Top-Up (L)"] = veh_detail["Diesel Top-Up (L)"].apply(lambda x: f"{x:,.1f}" if x > 0 else "-")
        veh_detail["Project"]           = veh_detail["Project"].fillna("-")
        st.dataframe(veh_detail.reset_index(drop=True), use_container_width=True, height=320)

        st.divider()

        # ── Full KM/L Summary Table ──
        st.markdown("#### Full Vehicle KM/L Summary")
        display_kml = veh_kml.copy()
        display_kml["KM/L"]        = display_kml["KM/L"].map("{:.2f}".format)
        display_kml["Total_Diesel"] = display_kml["Total_Diesel"].map("{:,.1f}".format)
        display_kml["Total_KM"]     = display_kml["Total_KM"].map("{:,.1f}".format)
        display_kml = display_kml.rename(columns={
            "Vehicle No":   "Vehicle",
            "Total_Diesel": "Total Diesel (L)",
            "Total_KM":     "Total KM",
            "Days":         "Active Days",
        })
        st.dataframe(display_kml[["Vehicle","Model","Type","Total Diesel (L)",
                                   "Total KM","Active Days","KM/L","Status"]].reset_index(drop=True),
                     use_container_width=True, height=450)

        # ── Export ──
        def kml_excel(veh_sum, daily_detail):
            buf = BytesIO()
            with pd.ExcelWriter(buf, engine="openpyxl") as w:
                veh_sum.to_excel(w,    index=False, sheet_name="KML by Vehicle")
                daily_detail.to_excel(w, index=False, sheet_name="Daily KML Detail")
            return buf.getvalue()

        st.download_button(
            label="📥 Download KM/L Report as Excel",
            data=kml_excel(
                veh_kml,
                kml_monthly[["Vehicle No","Month","Total_KM","Total_Diesel","KM/L","Project"]]
            ),
            file_name="kml_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )


# ══════════════════════════════════════════════
# TAB 7 — VEHICLE PROOF SHEET
# ══════════════════════════════════════════════
with tab7:
    st.subheader("🖨️ Vehicle Proof Sheet — Printable Form")
    st.caption("Generate a printable daily diesel usage form per vehicle.")

    # ── Selectors ──
    ps1, ps2, ps3 = st.columns(3)
    with ps1:
        proof_vehs    = sorted(df["Vehicle No"].dropna().unique())
        sel_proof_veh = st.selectbox("Select Vehicle", proof_vehs, key="proof_veh")
    with ps2:
        proof_months       = sorted(df["Month"].unique())
        proof_month_labels = {m: df[df["Month"]==m]["Month_Label"].iloc[0] for m in proof_months}
        sel_proof_month    = st.selectbox(
            "Select Month", proof_months,
            format_func=lambda m: proof_month_labels[m], key="proof_month"
        )
    with ps3:
        company_name = st.text_input("Company Name", value="My Company Pte Ltd", key="proof_company")

    show_all_days = st.checkbox("Show all days (incl. no activity)", value=False)

    # ── Filter data ──
    veh_diesel = df[
        (df["Vehicle No"] == sel_proof_veh) &
        (df["Month"] == sel_proof_month)
    ].copy()

    if odometer_raw is not None and not odometer_raw.empty:
        veh_odo = odometer_raw[
            (odometer_raw["Vehicle No"] == sel_proof_veh) &
            (odometer_raw["Month"] == sel_proof_month)
        ][["Date_Only","Start KM","End KM","Distance KM"]].copy()
    else:
        veh_odo = pd.DataFrame(columns=["Date_Only","Start KM","End KM","Distance KM"])

    if veh_diesel.empty and veh_odo.empty:
        st.info("No data found for this vehicle and month.")
    else:
        # ── Build date range ──
        if not veh_diesel.empty:
            month_start = veh_diesel["Date"].dt.to_period("M").iloc[0].start_time.date()
            month_end   = veh_diesel["Date"].dt.to_period("M").iloc[0].end_time.date()
        else:
            month_start = veh_odo["Date_Only"].min().date()
            month_end   = veh_odo["Date_Only"].max().date()

        all_dates = pd.DataFrame({"Date": pd.date_range(month_start, month_end, freq="D")})
        all_dates["Date_Only"] = all_dates["Date"].dt.normalize()

        # ── Aggregate diesel per day ──
        diesel_daily_proof = (
            veh_diesel.groupby("Date_Only")
            .agg(
                Diesel_Litre = ("Diesel Litre", "sum"),
                Top_Ups      = ("Diesel Litre", "count"),
                Site         = ("Project",      lambda x: ", ".join(sorted(set(str(v) for v in x.dropna())))),
                Fuel_Station = ("Fuel Station", lambda x: ", ".join(sorted(set(str(v) for v in x.dropna())))),
                Driver       = ("Driver",       lambda x: x.mode()[0] if not x.dropna().empty else "-"),
            )
            .reset_index()
        )

        proof_df = all_dates.merge(diesel_daily_proof, on="Date_Only", how="left")
        if not veh_odo.empty:
            proof_df = proof_df.merge(veh_odo, on="Date_Only", how="left")
        else:
            proof_df["Start KM"]    = None
            proof_df["End KM"]      = None
            proof_df["Distance KM"] = None

        if not show_all_days:
            proof_df = proof_df[
                proof_df["Diesel_Litre"].notna() |
                proof_df["Distance KM"].notna()
            ].copy()

        # ── Summary stats ──
        veh_info_row        = df[df["Vehicle No"] == sel_proof_veh].iloc[0]
        veh_model           = veh_info_row.get("Model", "N/A")
        veh_type            = veh_info_row.get("Type",  "N/A")
        total_diesel_proof  = proof_df["Diesel_Litre"].fillna(0).sum()
        total_km_proof      = proof_df["Distance KM"].fillna(0).sum() if "Distance KM" in proof_df else 0
        kml_proof           = total_km_proof / total_diesel_proof if total_diesel_proof > 0 else 0
        total_cost_proof    = total_diesel_proof * price_per_litre
        topup_count         = int(proof_df["Top_Ups"].fillna(0).sum())

        # ── Build HTML rows ──
        rows_html = ""
        for _rn, (i, row) in enumerate(proof_df.iterrows(), start=1):
            date_str    = row["Date"].strftime("%d %b %Y")
            day_str     = row["Date"].strftime("%a")
            is_weekend  = row["Date"].dayofweek >= 5
            site        = row.get("Site","")        if pd.notna(row.get("Site",""))        else "-"
            driver      = row.get("Driver","")      if pd.notna(row.get("Driver",""))      else "-"
            diesel      = f"{row['Diesel_Litre']:,.1f}" if pd.notna(row.get("Diesel_Litre")) and row.get("Diesel_Litre",0) > 0 else "-"
            topups      = str(int(row["Top_Ups"]))  if pd.notna(row.get("Top_Ups")) and row.get("Top_Ups",0) > 0 else "-"
            station     = row.get("Fuel_Station","") if pd.notna(row.get("Fuel_Station","")) else "-"
            start_km    = f"{row['Start KM']:,.1f}"  if pd.notna(row.get("Start KM"))  else "-"
            end_km      = f"{row['End KM']:,.1f}"    if pd.notna(row.get("End KM"))    else "-"
            dist        = f"{row['Distance KM']:,.1f}" if pd.notna(row.get("Distance KM")) else "-"
            row_bg      = "#fff8e1" if is_weekend else ("" if _rn % 2 == 0 else "#f9f9f9")
            wkd_color   = "#e53935" if is_weekend else "#333"

            rows_html += f"""
            <tr style="background:{row_bg}">
                <td style="text-align:center;color:#888">{_rn}</td>
                <td style="text-align:center;font-weight:{'bold' if is_weekend else 'normal'};color:{wkd_color}">{date_str}</td>
                <td style="text-align:center;color:{wkd_color}">{day_str}</td>
                <td>{site}</td>
                <td>{driver}</td>
                <td style="text-align:center;font-weight:bold;color:{'#b8960a' if diesel!='-' else '#bbb'}">{diesel}</td>
                <td style="text-align:center">{topups}</td>
                <td style="text-align:center;font-size:9px">{station}</td>
                <td style="text-align:right">{start_km}</td>
                <td style="text-align:right">{end_km}</td>
                <td style="text-align:right;font-weight:bold">{dist}</td>
            </tr>"""

        # ── Logo HTML ──
        if LOGO_B64:
            logo_html = f'<img src="data:image/png;base64,{LOGO_B64}" style="height:100px;width:auto;object-fit:contain;">'
        else:
            logo_html = '<div style="font-size:22px;font-weight:bold;color:#1a1a1a;letter-spacing:2px;">SHINGDA</div>'

        # ── Full HTML form — Professional letterhead style ──
        html_form = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @page {{
    size: A4;
    margin: 8mm 10mm;
  }}
  @media print {{
    .no-print {{ display: none !important; }}
    tr {{ page-break-inside: avoid; }}
    html, body {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: Arial, sans-serif;
    font-size: 11px;
    color: #222;
    background: white;
    padding: 28px 36px;
    max-width: 980px;
    margin: 0 auto;
  }}

  /* ── LETTERHEAD HEADER ── */
  .lh-header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    padding-bottom: 14px;
    border-bottom: 2px solid #222;
    margin-bottom: 16px;
  }}
  .lh-title {{
    text-align: right;
    font-size: 20px;
    font-weight: bold;
    color: #222;
    letter-spacing: 0.5px;
    line-height: 1.35;
  }}

  /* ── INFO BLOCK ── */
  .info-block {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0 48px;
    margin-bottom: 18px;
    padding-bottom: 14px;
    border-bottom: 1px solid #ccc;
  }}
  .info-row {{
    display: flex;
    gap: 6px;
    margin-bottom: 5px;
    line-height: 1.5;
  }}
  .i-lbl {{ font-weight: bold; min-width: 110px; color: #444; }}
  .i-col {{ color: #444; }}
  .i-val {{ color: #222; }}

  /* ── TABLE ── */
  table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 10.5px;
    margin-bottom: 0;
  }}
  thead th {{
    background: #f3d03e;
    color: #1a1a1a;
    padding: 7px 8px;
    text-align: center;
    font-weight: bold;
    border: 1px solid #c9a800;
    white-space: nowrap;
    font-size: 9.5px;
    text-transform: uppercase;
    letter-spacing: 0.3px;
  }}
  tbody td {{
    padding: 5px 8px;
    border: 1px solid #ddd;
    vertical-align: middle;
  }}
  tbody tr:nth-child(even) {{ background: #fafafa; }}
  .wkd {{ background: #fff8e1 !important; }}
  .total-row {{
    background: #f5f5f5 !important;
    font-weight: bold;
    border-top: 2px solid #222 !important;
  }}
  .total-row td {{ border-color: #ccc !important; }}

  /* ── TOTALS BOX (bottom-right, like PO) ── */
  .totals-wrap {{
    display: flex;
    justify-content: flex-end;
    margin-top: 0;
    margin-bottom: 22px;
    border-top: 1px solid #ddd;
  }}
  .totals-box {{ width: 290px; border: 1px solid #ccc; border-top: none; }}
  .tot-row {{
    display: flex;
    border-bottom: 1px solid #eee;
  }}
  .tot-row:last-child {{ border-bottom: none; }}
  .tot-lbl {{ flex: 1; padding: 5px 12px; color: #555; border-right: 1px solid #eee; }}
  .tot-val {{ width: 110px; padding: 5px 12px; text-align: right; font-weight: bold; }}
  .tot-grand {{ background: #f3d03e; }}
  .tot-grand .tot-lbl {{ color: #1a1a1a; border-right-color: #c9a800; font-weight: bold; }}
  .tot-grand .tot-val {{ color: #1a1a1a; font-size: 12px; }}

  /* ── SIGNATURES ── */
  .sig-section {{
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 40px;
    margin-top: 20px;
    margin-bottom: 28px;
  }}
  .sig-box {{ border-top: 1px solid #555; padding-top: 8px; font-size: 10px; color: #555; }}
  .sig-title {{ font-weight: bold; color: #333; margin-bottom: 22px; font-size: 10.5px; }}
  .sig-line {{ margin-bottom: 6px; }}

  /* ── DOCUMENT FOOTER ── */
  .doc-footer {{
    border-top: 1px solid #ccc;
    padding-top: 10px;
    margin-top: 8px;
  }}
  .ft-member {{ font-size: 9.5px; color: #666; font-style: italic; margin-bottom: 5px; }}
  .ft-name   {{ font-size: 11px; font-weight: bold; color: #222; margin-bottom: 3px; }}
  .ft-chinese {{ font-size: 10px; font-weight: bold; color: #444; }}
  .ft-detail {{ font-size: 9px; color: #666; line-height: 1.8; margin-bottom: 2px; }}
  .ft-yellow-bar {{
    height: 10px;
    background: #f3d03e;
    margin: 10px -36px 0 -36px;
  }}

  /* ── PRINT BUTTON ── */
  .print-btn {{
    display: inline-block; margin-bottom: 20px;
    padding: 9px 26px; background: #f3d03e; color: #1a1a1a;
    border: none; border-radius: 4px; font-size: 13px;
    cursor: pointer; font-weight: bold;
  }}
  .print-btn:hover {{ background: #d4b900; }}
</style>
</head>
<body>

<button class="print-btn no-print" onclick="window.print()">🖨️ Print / Save as PDF</button>

<div class="lh-header">
  <div>{logo_html}</div>
  <div class="lh-title">VEHICLE DIESEL USAGE<br>PROOF SHEET</div>
</div>

<div class="info-block">
  <div>
    <div class="info-row"><span class="i-lbl">Vehicle No</span><span class="i-col">:</span><span class="i-val">{sel_proof_veh}</span></div>
    <div class="info-row"><span class="i-lbl">Model</span><span class="i-col">:</span><span class="i-val">{veh_model}</span></div>
    <div class="info-row"><span class="i-lbl">Vehicle Type</span><span class="i-col">:</span><span class="i-val">{veh_type}</span></div>
    <div class="info-row"><span class="i-lbl">Report Period</span><span class="i-col">:</span><span class="i-val">{proof_month_labels[sel_proof_month]}</span></div>
  </div>
  <div>
    <div class="info-row"><span class="i-lbl">Company</span><span class="i-col">:</span><span class="i-val">{company_name}</span></div>
    <div class="info-row"><span class="i-lbl">Prepared By</span><span class="i-col">:</span><span class="i-val">_______________________</span></div>
    <div class="info-row"><span class="i-lbl">Prepared Date</span><span class="i-col">:</span><span class="i-val">_______________________</span></div>
    <div class="info-row"><span class="i-lbl">Page No.</span><span class="i-col">:</span><span class="i-val">1 of 1</span></div>
  </div>
</div>

<table>
  <thead>
    <tr>
      <th>No.</th><th>Date</th><th>Day</th><th>Site / Project</th>
      <th>Driver</th><th>Diesel (L)</th><th>Top-Ups</th>
      <th>Fuel Station</th><th>Start KM</th><th>End KM</th><th>Distance (KM)</th>
    </tr>
  </thead>
  <tbody>
    {rows_html}
    <tr class="total-row">
      <td colspan="5" style="text-align:right;padding-right:12px;">TOTAL</td>
      <td style="text-align:center">{total_diesel_proof:,.1f}</td>
      <td style="text-align:center">{topup_count}</td>
      <td></td><td></td><td></td>
      <td style="text-align:right">{total_km_proof:,.1f}</td>
    </tr>
  </tbody>
</table>

<div class="totals-wrap">
  <div class="totals-box">
    <div class="tot-row"><span class="tot-lbl">Total Diesel (L)</span><span class="tot-val">{total_diesel_proof:,.1f}</span></div>
    <div class="tot-row"><span class="tot-lbl">Total Distance (KM)</span><span class="tot-val">{total_km_proof:,.1f}</span></div>
    <div class="tot-row"><span class="tot-lbl">KM / Litre</span><span class="tot-val">{f"{kml_proof:.2f}" if kml_proof > 0 else "N/A"}</span></div>
    <div class="tot-row"><span class="tot-lbl">No. of Top-Ups</span><span class="tot-val">{topup_count}</span></div>
    <div class="tot-row tot-grand"><span class="tot-lbl">Est. Cost (SGD)</span><span class="tot-val">SGD&nbsp;{total_cost_proof:,.2f}</span></div>
  </div>
</div>

<div class="sig-section">
  <div class="sig-box">
    <div class="sig-title">Driver / Operator</div>
    <div class="sig-line">Signature : _____________________</div>
    <div class="sig-line">Name &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: _____________________</div>
  </div>
  <div class="sig-box">
    <div class="sig-title">Verified By (Supervisor)</div>
    <div class="sig-line">Signature : _____________________</div>
    <div class="sig-line">Name &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: _____________________</div>
  </div>
  <div class="sig-box">
    <div class="sig-title">Approved By</div>
    <div class="sig-line">Signature : _____________________</div>
    <div class="sig-line">Name &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: _____________________</div>
  </div>
</div>

<div class="doc-footer">
  <div class="ft-member">A member of SHINGDA Group of Companies</div>
  <div class="ft-name">SHINGDA GROUP OF COMPANIES</div>
  <div class="ft-detail">
    SHINGDA Building, 10 Kranji Crescent, Singapore 728660 &nbsp;|&nbsp;
    T (65) 6368 8936 &nbsp;|&nbsp; F (65) 6366 1470 &nbsp;|&nbsp; W shingdagroup.com
  </div>
  <div class="ft-yellow-bar"></div>
</div>

</body>
</html>"""

        # ── Show preview in dashboard ──
        st.components.v1.html(html_form, height=900, scrolling=True)

        # ── Download as HTML (open in browser → print) ──
        st.download_button(
            label="📥 Download as HTML (Open in Browser → Print / Save PDF)",
            data=html_form.encode("utf-8"),
            file_name=f"proof_{sel_proof_veh}_{sel_proof_month}.html",
            mime="text/html",
        )
        st.caption("💡 Tip: Open the downloaded HTML file in your browser, then press Ctrl+P to print or save as PDF.")


# ══════════════════════════════════════════════
# TAB 8 — NO JOB ALERT
# ══════════════════════════════════════════════
with tab8:
    st.subheader("🚨 No Job Alert — Diesel Filled But No Job Scheduled")
    st.caption("Vehicles that topped up diesel on a date with no matching job in the Job List.")

    if job_raw is None:
        st.info("Please upload the Job List (Report 2) to use this feature.")
    else:
        # ── Build no-job records ──
        # These are diesel records where Project is unscheduled
        nojob_labels = ["Off-day / No Schedule", "Vehicle Not in Job List"]
        nojob_df = df[df["Project"].isin(nojob_labels)].copy()

        if nojob_df.empty:
            st.success("✅ All diesel top-up records have a matching job schedule!")
        else:
            total_nojob_litre = nojob_df["Diesel Litre"].sum()
            _price = df["Cost (SGD)"].sum() / df["Diesel Litre"].sum() if "Cost (SGD)" in df.columns and df["Diesel Litre"].sum() > 0 else 0
            total_nojob_cost = nojob_df["Diesel Litre"].sum() * _price
            pct_total         = total_nojob_litre / df["Diesel Litre"].sum() * 100

            # ── KPI Cards ──
            nj1, nj2, nj3, nj4 = st.columns(4)
            nj1.metric("🚨 Unscheduled Records",   len(nojob_df))
            nj2.metric("🚛 Vehicles Affected",      nojob_df["Vehicle No"].nunique())
            nj3.metric("⛽ Total Diesel (L)",        f"{total_nojob_litre:,.1f}")
            nj4.metric("💰 Est. Cost (SGD)",         f"SGD {total_nojob_cost:,.2f} ({pct_total:.1f}%)")

            st.divider()

            # ── Reason breakdown ──
            reason_counts = nojob_df["Project"].value_counts().reset_index()
            reason_counts.columns = ["Reason", "Records"]
            r1, r2 = st.columns(2)

            with r1:
                st.markdown("#### By Reason")
                fig_reason = px.pie(
                    reason_counts, names="Reason", values="Records",
                    color_discrete_sequence=[BRAND_GREY, BRAND_YELLOW],
                    title="Unscheduled Records by Reason",
                )
                st.plotly_chart(fig_reason, use_container_width=True)

            with r2:
                st.markdown("#### By Reason — Detail")
                for _, row in reason_counts.iterrows():
                    litres = nojob_df[nojob_df["Project"]==row["Reason"]]["Diesel Litre"].sum()
                    st.markdown(f"""
                    **{row['Reason']}**
                    - Records: {row['Records']}
                    - Diesel: {litres:,.1f} L
                    """)
                    if row["Reason"] == "Off-day / No Schedule":
                        st.caption("Vehicle exists in Job List but had no job on that specific date.")
                    else:
                        st.caption("Vehicle never appears in the Job List at all.")

            st.divider()

            # ── Vehicle summary ──
            st.markdown("#### By Vehicle — Which Vehicles & Which Dates")
            nojob_veh = (
                nojob_df.groupby(["Vehicle No","Project"])
                .agg(
                    Model        = ("Model",       "first"),
                    Type         = ("Type",        "first"),
                    Missing_Days = ("Date_Only",   "nunique"),
                    Total_Diesel = ("Diesel Litre","sum"),
                    Dates        = ("Day_Sort",    lambda x: ", ".join(sorted(set(str(d) for d in x)))),
                )
                .reset_index()
                .sort_values("Total_Diesel", ascending=False)
                .reset_index(drop=True)
            )
            nojob_veh.index += 1
            nojob_veh["Total_Diesel"] = nojob_veh["Total_Diesel"].map("{:,.1f}".format)
            nojob_veh.columns = ["Vehicle No","Reason","Model","Type",
                                  "Missing Days","Diesel (L)","Dates Not Scheduled"]
            st.dataframe(nojob_veh, use_container_width=True, height=400)

            st.divider()

            # ── Daily detail ──
            st.markdown("#### Full Record Detail")

            # Filter controls
            fc1, fc2 = st.columns(2)
            with fc1:
                nojob_reasons = sorted(nojob_df["Project"].unique())
                sel_nojob_reason = st.multiselect(
                    "Filter by Reason", nojob_reasons, default=nojob_reasons,
                    key="nojob_reason"
                )
            with fc2:
                nojob_vehs = sorted(nojob_df["Vehicle No"].unique())
                sel_nojob_veh = st.multiselect(
                    "Filter by Vehicle", nojob_vehs, default=nojob_vehs,
                    key="nojob_veh"
                )

            filtered_nojob = nojob_df[
                nojob_df["Project"].isin(sel_nojob_reason) &
                nojob_df["Vehicle No"].isin(sel_nojob_veh)
            ].copy()

            detail_cols = [c for c in ["Date","Vehicle No","Model","Type",
                                        "Diesel Litre","Project","Fuel Station","Driver"]
                           if c in filtered_nojob.columns]
            detail_out = (
                filtered_nojob[detail_cols]
                .sort_values(["Vehicle No","Date"])
                .reset_index(drop=True)
            )
            detail_out.index += 1
            st.dataframe(detail_out, use_container_width=True, height=420)

            # ── Export ──
            def nojob_excel(veh_sum, detail):
                buf = BytesIO()
                with pd.ExcelWriter(buf, engine="openpyxl") as w:
                    # Summary by vehicle
                    veh_sum.to_excel(w, index=True, sheet_name="By Vehicle")
                    # Full detail
                    detail.to_excel(w, index=True, sheet_name="All Records")
                    # Pivot — Vehicle vs Date
                    pivot = (
                        nojob_df.groupby(["Vehicle No","Day_Sort"])["Diesel Litre"]
                        .sum().reset_index()
                        .pivot(index="Vehicle No", columns="Day_Sort", values="Diesel Litre")
                        .fillna(0)
                    )
                    pivot.columns = [str(c) for c in pivot.columns]
                    pivot["Total"] = pivot.sum(axis=1)
                    pivot.to_excel(w, sheet_name="Date Pivot")
                return buf.getvalue()

            st.download_button(
                label="📥 Download No-Job Alert Report as Excel",
                data=nojob_excel(nojob_veh, detail_out),
                file_name="no_job_alert.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )

        st.divider()

        # ══════════════════════════════════════════
        # SECTION 2: Had Job BUT No Diesel Top-Up
        # ══════════════════════════════════════════
        st.markdown("### 🔵 Section 2 — Had Job But No Diesel Top-Up")
        st.caption("Vehicles that were scheduled to work but did not record any diesel top-up that day.")

        if job_raw is None:
            st.info("Please upload the Job List (Report 2) to use this feature.")
        else:
            # All vehicle+date combos in job list (within filtered date range)
            job_filtered = job_raw[
                (job_raw["Date_Only"] >= pd.Timestamp(date_from)) &
                (job_raw["Date_Only"] <= pd.Timestamp(date_to))
            ].copy()

            # All vehicle+date combos that have diesel top-up
            diesel_keys = set(zip(df["Vehicle No"], df["Date_Only"]))

            # Job records with no matching diesel top-up
            job_filtered["Has_Diesel"] = job_filtered.apply(
                lambda r: (r["Vehicle No"], r["Date_Only"]) in diesel_keys, axis=1
            )
            no_diesel_df = job_filtered[~job_filtered["Has_Diesel"]].copy()

            # Exclude vehicles not in the diesel report at all
            # (guard: Vehicle No column may be absent if job list columns weren't recognised)
            if "Vehicle No" not in no_diesel_df.columns:
                st.warning("⚠️ Job List file loaded but 'Vehicle No' column was not recognised. "
                           "Check the column is named: Vehicle No, Veh No, Plate No, or similar.")
                st.stop()
            all_diesel_vehs = set(df["Vehicle No"].unique())
            no_diesel_df = no_diesel_df[no_diesel_df["Vehicle No"].isin(all_diesel_vehs)]

            if no_diesel_df.empty:
                st.success("✅ All scheduled vehicles have diesel top-up records.")
            else:
                nd1, nd2, nd3 = st.columns(3)
                nd1.metric("📋 Records",          len(no_diesel_df))
                nd2.metric("🚛 Vehicles Affected", no_diesel_df["Vehicle No"].nunique())
                nd3.metric("📅 Days Affected",     no_diesel_df["Date_Only"].nunique())

                st.divider()

                # ── Vehicle summary ──
                st.markdown("#### By Vehicle — Days With Job But No Diesel")
                no_diesel_veh = (
                    no_diesel_df.groupby("Vehicle No")
                    .agg(
                        Days  = ("Date_Only", "nunique"),
                        Sites = ("Site",      lambda x: ", ".join(sorted(x.dropna().unique()))),
                        Dates = ("Date_Only", lambda x: ", ".join(sorted(set(str(d.date()) for d in x)))),
                    )
                    .reset_index()
                    .sort_values("Days", ascending=False)
                    .reset_index(drop=True)
                )
                # Add model & type
                no_diesel_veh = no_diesel_veh.merge(
                    df.drop_duplicates("Vehicle No")[["Vehicle No","Model","Type"]],
                    on="Vehicle No", how="left"
                )
                no_diesel_veh.index += 1
                no_diesel_veh = no_diesel_veh[["Vehicle No","Model","Type","Days","Sites","Dates"]]
                no_diesel_veh.columns = ["Vehicle","Model","Type",
                                          "Days With No Top-Up","Sites Worked","Dates"]
                st.dataframe(no_diesel_veh, use_container_width=True, height=380)

                st.divider()

                # ── Daily detail ──
                st.markdown("#### Full Detail — Job Scheduled But No Diesel")
                nd_fc1, nd_fc2 = st.columns(2)
                with nd_fc1:
                    nd_vehs = sorted(no_diesel_df["Vehicle No"].unique())
                    sel_nd_veh = st.multiselect(
                        "Filter by Vehicle", nd_vehs, default=nd_vehs, key="nd_veh"
                    )
                with nd_fc2:
                    nd_sites = sorted(no_diesel_df["Site"].dropna().unique())
                    sel_nd_site = st.multiselect(
                        "Filter by Site", nd_sites, default=nd_sites, key="nd_site"
                    )

                nd_detail = no_diesel_df[
                    no_diesel_df["Vehicle No"].isin(sel_nd_veh) &
                    no_diesel_df["Site"].isin(sel_nd_site)
                ].copy()

                nd_cols = [c for c in ["Date_Only","Vehicle No","Site",
                                        "Foreman / Driver","Status"]
                           if c in nd_detail.columns]
                nd_out = (
                    nd_detail[nd_cols]
                    .sort_values(["Vehicle No","Date_Only"])
                    .reset_index(drop=True)
                )
                nd_out.index += 1
                nd_out = nd_out.rename(columns={"Date_Only":"Date"})
                st.dataframe(nd_out, use_container_width=True, height=400)

                # ── Export both sections ──
                def nojob_full_excel(nj_veh, nj_detail, nd_veh, nd_det):
                    buf = BytesIO()
                    with pd.ExcelWriter(buf, engine="openpyxl") as w:
                        nj_veh.to_excel(w,    index=True,  sheet_name="NoJob-By Vehicle")
                        nj_detail.to_excel(w, index=True,  sheet_name="NoJob-All Records")
                        nd_veh.to_excel(w,    index=True,  sheet_name="NoTopUp-By Vehicle")
                        nd_det.to_excel(w,    index=False, sheet_name="NoTopUp-All Records")
                    return buf.getvalue()

                st.download_button(
                    label="📥 Download Full Alert Report (Both Sections) as Excel",
                    data=nojob_full_excel(nojob_veh, detail_out, no_diesel_veh, nd_out),
                    file_name="no_job_no_topup_alert.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )

# TAB 9 — FULL DATA & EXPORT
# ══════════════════════════════════════════════
with tab9:
    st.subheader("📋 Full Filtered Data")

    show_cols = [c for c in ["Date", "Vehicle No", "Model", "Type", "Project", "Diesel Litre",
                               "KM Reading", "Fuel Type", "Fuel Station"]
                 if c in df.columns]
    st.dataframe(df[show_cols].reset_index(drop=True), use_container_width=True)

    # Export — 3 sheets
    def to_excel_multi(diesel_df, proj_df, veh_df, daily_df):
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            diesel_df.to_excel(writer, index=False, sheet_name="All Transactions")
            proj_df.to_excel(writer,   index=True,  sheet_name="By Project")
            veh_df.to_excel(writer,    index=True,  sheet_name="By Vehicle")
            daily_df.to_excel(writer,  index=False, sheet_name="Daily Trend")
        return buffer.getvalue()

    excel_bytes = to_excel_multi(
        df[show_cols],
        proj_df,
        veh_df[["Vehicle No", "Total Diesel", "% of Total", "Avg / Day",
                 "# Projects", "Project Names"]],
        daily_df[["Day", "Daily Total"]],
    )

    st.download_button(
        label="📥 Download Full Report as Excel (4 sheets)",
        data=excel_bytes,
        file_name="diesel_dashboard_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

st.caption("Diesel Consumption Dashboard · Built with Streamlit")

st.divider()

# ═════════════════════════════════════════════
# HIGH VALUE FEATURES
# ═════════════════════════════════════════════
hv1, hv2, hv3 = st.tabs([
    "💰 1. Fuel Cost Estimation",
    "⚠️ 2. Refuel Frequency Alert",
    "🛢️ 3. Tank Capacity Check",
])

# ══════════════════════════════════════════════
# HV TAB 1 — FUEL COST ESTIMATION
# ══════════════════════════════════════════════
with hv1:
    st.subheader("💰 Fuel Cost Estimation")

    st.info(f"💡 Using price: **SGD {price_per_litre:.2f}/L** — adjust in the sidebar.")
    df["Cost (SGD)"] = df["Diesel Litre"] * price_per_litre
    total_cost = df["Cost (SGD)"].sum()

    # Cost KPI
    kc1, kc2, kc3 = st.columns(3)
    kc1.metric("💵 Total Fuel Cost (SGD)", f"SGD {total_cost:,.2f}")
    kc2.metric("📅 Avg Cost / Day (SGD)",  f"SGD {total_cost / num_days:,.2f}")
    kc3.metric("🚛 Avg Cost / Vehicle (SGD)",
               f"SGD {total_cost / df['Vehicle No'].nunique():,.2f}")

    st.divider()

    # ── Prepare aggregates ──
    cost_proj = (
        df.groupby("Project")["Cost (SGD)"]
        .sum().reset_index()
        .sort_values("Cost (SGD)", ascending=False)
        .reset_index(drop=True)
    )
    cost_proj.index += 1
    cost_proj["% of Total"] = (cost_proj["Cost (SGD)"] / cost_proj["Cost (SGD)"].sum() * 100).round(1)

    cost_veh = (
        df.groupby(["Vehicle No"])
        .agg(
            Model       = ("Model",       "first"),
            Type        = ("Type",        "first"),
            Total_Litre = ("Diesel Litre","sum"),
            Total_Cost  = ("Cost (SGD)",  "sum"),
            Project     = ("Project",     lambda x: x.mode()[0]),
        )
        .reset_index()
        .sort_values("Total_Cost", ascending=False)
        .reset_index(drop=True)
    )
    cost_veh.index += 1
    cost_veh["% of Total"] = (cost_veh["Total_Cost"] / cost_veh["Total_Cost"].sum() * 100).round(1)

    cost_period = (
        df.groupby(period_label)["Cost (SGD)"]
        .sum().reset_index().sort_values(period_label)
    )

    # ── Section A: Period Trend ──
    st.markdown(f"#### 📅 {view_mode} Cost Trend (SGD)")
    fig_cm = px.bar(
        cost_period, x=period_label, y="Cost (SGD)",
        color_discrete_sequence=["#8c564b"],
        labels={"Cost (SGD)": "SGD", period_label: view_mode},
        text="Cost (SGD)",
    )
    fig_cm.update_traces(texttemplate="SGD %{text:,.0f}", textposition="inside",
                          textfont_color="white")
    fig_cm.update_layout(height=360, xaxis=dict(type="category"),
                          xaxis_tickangle=-30)
    st.plotly_chart(fig_cm, use_container_width=True)

    st.divider()

    # ── Section B: Project vs Vehicle side by side ──
    st.markdown("#### 🏗️ Cost by Project & 🚛 Top 15 Vehicles")
    cb1, cb2 = st.columns(2)

    with cb1:
        fig_cp = px.bar(
            cost_proj.sort_values("Cost (SGD)"),
            x="Cost (SGD)", y="Project", orientation="h",
            color="Cost (SGD)", color_continuous_scale="Greens",
            labels={"Cost (SGD)": "SGD", "Project": "Project"},
            text="Cost (SGD)",
        )
        fig_cp.update_traces(texttemplate="%{text:,.0f}", textposition="inside",
                              textfont_color="white")
        fig_cp.update_layout(
            height=max(350, len(cost_proj) * 38),
            coloraxis_showscale=False,
            margin=dict(l=10, r=20),
            yaxis_title="",
        )
        st.plotly_chart(fig_cp, use_container_width=True)

        # Project table below chart
        proj_disp = cost_proj[["Project","Cost (SGD)","% of Total"]].copy()
        proj_disp["Cost (SGD)"] = proj_disp["Cost (SGD)"].map("SGD {:,.2f}".format)
        proj_disp["% of Total"] = proj_disp["% of Total"].map("{:.1f}%".format)
        st.dataframe(proj_disp, use_container_width=True, hide_index=False)

    with cb2:
        top15_cost = cost_veh.head(15).sort_values("Total_Cost")
        fig_cv = px.bar(
            top15_cost, x="Total_Cost", y="Vehicle No", orientation="h",
            color="Total_Cost", color_continuous_scale="Blues",
            labels={"Total_Cost": "SGD", "Vehicle No": "Vehicle"},
            text="Total_Cost",
            hover_data=["Model", "Type", "% of Total"],
        )
        fig_cv.update_traces(texttemplate="%{text:,.0f}", textposition="inside",
                              textfont_color="white")
        fig_cv.update_layout(
            height=500,
            coloraxis_showscale=False,
            margin=dict(l=10, r=20),
            yaxis_title="",
        )
        st.plotly_chart(fig_cv, use_container_width=True)

    st.divider()

    # ── Section C: Full Cost Table ──
    st.markdown("#### 📋 Full Cost Summary Table")
    cost_table = cost_veh.copy()
    cost_table["Total_Litre"] = cost_table["Total_Litre"].map("{:,.1f}".format)
    cost_table["Total_Cost"]  = cost_table["Total_Cost"].map("SGD {:,.2f}".format)
    cost_table["% of Total"]  = cost_table["% of Total"].map("{:.1f}%".format)
    cost_table = cost_table.rename(columns={
        "Vehicle No":   "Vehicle",
        "Total_Litre":  "Total Litre (L)",
        "Total_Cost":   "Total Cost (SGD)",
        "Project":      "Main Project",
    })
    st.dataframe(
        cost_table[["Vehicle","Model","Type","Main Project",
                    "Total Litre (L)","Total Cost (SGD)","% of Total"]],
        use_container_width=True, height=400, hide_index=False
    )

    # Export
    def cost_excel(dataframe, price):
        out = dataframe.copy()
        out["Cost (SGD)"] = out["Diesel Litre"] * price
        cols = [c for c in ["Date", "Vehicle No", "Model", "Type", "Project",
                             "Diesel Litre", "Cost (SGD)"] if c in out.columns]
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            out[cols].to_excel(writer, index=False, sheet_name="Cost Detail")
            cost_table.to_excel(writer, index=True, sheet_name="Cost by Vehicle")
            cost_proj.to_excel(writer, index=False, sheet_name="Cost by Project")
        return buffer.getvalue()

    st.download_button(
        label="📥 Download Cost Report as Excel",
        data=cost_excel(df, price_per_litre),
        file_name="fuel_cost_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

# ══════════════════════════════════════════════
# HV TAB 2 — REFUEL FREQUENCY ALERT
# ══════════════════════════════════════════════
with hv2:
    st.subheader("⚠️ Refuel Frequency Alert")

    rf_col1, rf_col2 = st.columns([1, 3])
    with rf_col1:
        max_topups = st.number_input(
            "Flag if top-ups per day exceeds", min_value=1, value=2, step=1
        )

    # Count top-ups per vehicle per day
    freq_df = (
        df.groupby(["Vehicle No", "Day_Sort", "Day"])
        .agg(
            TopUp_Count  = ("Diesel Litre", "count"),
            Total_Litre  = ("Diesel Litre", "sum"),
            Model        = ("Model",  "first"),
            Type         = ("Type",   "first"),
            Project      = ("Project","first"),
        )
        .reset_index()
    )
    alert_df = freq_df[freq_df["TopUp_Count"] > max_topups].sort_values(
        "TopUp_Count", ascending=False
    ).reset_index(drop=True)
    alert_df.index += 1

    # Summary KPIs
    ra1, ra2, ra3 = st.columns(3)
    ra1.metric("🚨 Alert Days",          len(alert_df))
    ra2.metric("🚛 Vehicles Flagged",    alert_df["Vehicle No"].nunique() if not alert_df.empty else 0)
    ra3.metric("⛽ Total Litre Flagged", f"{alert_df['Total_Litre'].sum():,.1f} L" if not alert_df.empty else "0 L")

    if alert_df.empty:
        st.success(f"No vehicles exceeded {max_topups} top-ups in a single day. ✅")
    else:
        st.warning(f"**{len(alert_df)} vehicle-days** exceeded {max_topups} top-ups in a single day.")

        # Chart — flagged vehicles
        flag_veh = (
            alert_df.groupby("Vehicle No")["TopUp_Count"]
            .sum().reset_index()
            .sort_values("TopUp_Count", ascending=False)
        )
        fig_freq = px.bar(
            flag_veh, x="TopUp_Count", y="Vehicle No", orientation="h",
            title="Total Excess Top-Up Days by Vehicle",
            labels={"TopUp_Count": "Total Flagged Top-Ups", "Vehicle No": "Vehicle"},
            color_discrete_sequence=["#d62728"],
            text="TopUp_Count",
        )
        fig_freq.update_traces(texttemplate="%{text}", textposition="outside")
        fig_freq.update_layout(yaxis={"categoryorder": "total ascending"}, height=400)
        st.plotly_chart(fig_freq, use_container_width=True)

        # Detail table
        st.markdown("#### Flagged Records Detail")
        alert_display = alert_df.rename(columns={
            "Vehicle No":  "Vehicle",
            "Day":         "Date",
            "TopUp_Count": "Top-Up Count",
            "Total_Litre": "Total Litre (L)",
        })
        alert_display["Total Litre (L)"] = alert_display["Total Litre (L)"].map("{:,.1f}".format)
        st.dataframe(
            alert_display[["Vehicle", "Model", "Type", "Date", "Top-Up Count",
                            "Total Litre (L)", "Project"]],
            use_container_width=True, height=400
        )

        # Drill-down: show all individual top-ups for flagged vehicle-days
        st.markdown("#### Individual Top-Up Records for Flagged Days")
        flagged_keys = set(zip(alert_df["Vehicle No"], alert_df["Day_Sort"]))
        drill_df = df[df.apply(
            lambda r: (r["Vehicle No"], r["Day_Sort"]) in flagged_keys, axis=1
        )].copy()
        drill_cols = [c for c in ["Date", "Vehicle No", "Model", "Type",
                                   "Diesel Litre", "Project", "Fuel Station"]
                      if c in drill_df.columns]
        st.dataframe(
            drill_df[drill_cols].sort_values(["Vehicle No", "Date"]).reset_index(drop=True),
            use_container_width=True, height=350
        )

        st.download_button(
            label="📥 Download Frequency Alert Report",
            data=alert_df.to_csv(index=False).encode(),
            file_name="refuel_frequency_alert.csv",
            mime="text/csv",
        )

# ══════════════════════════════════════════════
# HV TAB 3 — TANK CAPACITY CHECK
# ══════════════════════════════════════════════
with hv3:
    st.subheader("🛢️ Tank Capacity Check")

    # Exclude diesel tank lorry from capacity check
    excluded_types = ["DIESEL TANK Lorry", "DIESEL TANK LORRY"]
    check_df = df[~df["Type"].str.upper().isin([t.upper() for t in excluded_types])].copy()

    st.info(
        "💡 Diesel Tank Lorries are excluded from this check as they carry bulk fuel. "
        f"({len(df) - len(check_df)} records excluded)"
    )

    tc1, tc2 = st.columns([1, 3])
    with tc1:
        tank_capacity = st.number_input(
            "Standard Tank Capacity (Litres)", min_value=50, value=400, step=50
        )
        st.caption("Typical 10-wheel tipper: 300–400L. Adjust to match your fleet.")

    # Flag single top-ups exceeding tank capacity
    over_df = check_df[check_df["Diesel Litre"] > tank_capacity].copy()
    over_df = over_df.sort_values("Diesel Litre", ascending=False).reset_index(drop=True)
    over_df.index += 1

    # KPIs
    tc_a, tc_b, tc_c = st.columns(3)
    tc_a.metric("🚨 Over-Capacity Records", len(over_df))
    tc_b.metric("🚛 Vehicles Affected",     over_df["Vehicle No"].nunique() if not over_df.empty else 0)
    tc_c.metric("⛽ Excess Litres",
                f"{max(over_df['Diesel Litre'].sum() - tank_capacity * len(over_df), 0):,.1f} L"
                if not over_df.empty else "0 L")

    if over_df.empty:
        st.success(f"No single top-up exceeded {tank_capacity}L tank capacity. ✅")
    else:
        st.warning(
            f"**{len(over_df)} records** show a single top-up exceeding {tank_capacity}L. "
            "This may indicate a data entry error, siphoning, or wrong vehicle assignment."
        )

        # Scatter chart — all top-up amounts with capacity line
        fig_tank = px.scatter(
            check_df, x="Date", y="Diesel Litre", color="Vehicle No",
            title=f"All Top-Ups vs Tank Capacity ({tank_capacity}L limit)",
            labels={"Diesel Litre": "Litres per Top-Up"},
            opacity=0.6,
        )
        fig_tank.add_hline(
            y=tank_capacity, line_dash="dash", line_color="red",
            annotation_text=f"Capacity Limit: {tank_capacity}L",
            annotation_position="top left",
        )
        fig_tank.update_layout(height=420, showlegend=False)
        st.plotly_chart(fig_tank, use_container_width=True)

        # Over-capacity detail table
        st.markdown("#### Over-Capacity Records")
        over_cols = [c for c in ["Date", "Vehicle No", "Model", "Type",
                                  "Diesel Litre", "Project", "Fuel Station"]
                     if c in over_df.columns]
        over_display = over_df[over_cols].copy()
        over_display["Diesel Litre"] = over_display["Diesel Litre"].map("{:,.1f}".format)
        st.dataframe(over_display, use_container_width=True, height=400)

        st.download_button(
            label="📥 Download Over-Capacity Report",
            data=over_df[over_cols].to_csv(index=False).encode(),
            file_name="tank_capacity_alert.csv",
            mime="text/csv",
        )

st.divider()

# ─────────────────────────────────────────────
# UNSCHEDULED RECORDS
# ─────────────────────────────────────────────
st.subheader("🔍 Unscheduled Diesel Top-Ups (No Matching Job Schedule)")

unscheduled_labels = ["Off-day / No Schedule", "Vehicle Not in Job List", "No Job List Uploaded"]
unscheduled_df = df[df["Project"].isin(unscheduled_labels)].copy()

if unscheduled_df.empty:
    st.success("All diesel top-up records matched to a job schedule. ✅")
else:
    total_unscheduled = unscheduled_df["Diesel Litre"].sum()
    st.warning(
        f"**{len(unscheduled_df)} records** ({total_unscheduled:,.1f} L) have no matching job schedule."
    )

    ua, ub = st.columns(2)

    with ua:
        st.markdown("#### By Vehicle — Unscheduled Days")
        veh_unsched = (
            unscheduled_df.groupby("Vehicle No")
            .agg(
                Missing_Days   = ("Day_Sort", "nunique"),
                Total_Diesel   = ("Diesel Litre", "sum"),
                Reason         = ("Project", lambda x: x.mode()[0]),
                Dates          = ("Day_Sort", lambda x: ", ".join(
                                    sorted(set(str(d) for d in x))
                                  )),
            )
            .reset_index()
            .sort_values("Total_Diesel", ascending=False)
            .rename(columns={
                "Vehicle No":  "Vehicle No",
                "Missing_Days":"Missing Days",
                "Total_Diesel":"Diesel (L)",
                "Dates":       "Dates Not in Schedule",
            })
        )
        # Add model & type
        veh_unsched = veh_unsched.merge(
            df.drop_duplicates("Vehicle No")[["Vehicle No", "Model", "Type"]],
            on="Vehicle No", how="left"
        )
        veh_unsched = veh_unsched[["Vehicle No", "Model", "Type", "Missing Days",
                                    "Diesel (L)", "Reason", "Dates Not in Schedule"]]
        veh_unsched.rename(columns={"Vehicle No": "Vehicle"}, inplace=True)
        veh_unsched["Diesel (L)"] = veh_unsched["Diesel (L)"].map("{:,.1f}".format)
        st.dataframe(veh_unsched.reset_index(drop=True), use_container_width=True, height=420)

    with ub:
        st.markdown("#### Detail — Every Unscheduled Record")
        detail_cols = [c for c in ["Date", "Vehicle No", "Model", "Type", "Diesel Litre", "Project", "Fuel Station"]
                       if c in unscheduled_df.columns]
        detail = (
            unscheduled_df[detail_cols]
            .sort_values(["Vehicle No", "Date"])
            .reset_index(drop=True)
        )
        detail.index += 1
        st.dataframe(detail, use_container_width=True, height=420)

    def to_excel_unsched(summary_df, detail_df):
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            summary_df.to_excel(writer, index=False, sheet_name="By Vehicle")
            detail_df.to_excel(writer,  index=False, sheet_name="All Records")
        return buffer.getvalue()

    st.download_button(
        label="📥 Download Unscheduled Records as Excel",
        data=to_excel_unsched(veh_unsched, detail),
        file_name="unscheduled_diesel.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

# ─────────────────────────────────────────────────────────────────────────────
# BRANDED FOOTER — Bottom.png (horizontal company divisions, from brand manual)
# ─────────────────────────────────────────────────────────────────────────────
if BOTTOM_B64:
    st.markdown(f"""
<div style="
    margin: 48px -2rem 0 -2rem;
    border-top: 3px solid #f3d03e;
    background: white;
    box-shadow: 0 -4px 20px rgba(0,0,0,0.08);
">
    <img src="data:image/png;base64,{BOTTOM_B64}"
         style="width:100%;height:auto;display:block;padding:16px 32px;box-sizing:border-box;">
</div>
""", unsafe_allow_html=True)
else:
    st.caption("Shingda Group of Companies — Diesel Consumption Dashboard")
