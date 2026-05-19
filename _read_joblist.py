"""
Diagnostic — inspects Job List AND Transaction file to find why projects aren't matching.
Output saved to I:\Fleet\Diesel Report\Diesel Consumption\_joblist_info.txt
"""
import pandas as pd, os, glob, sys, io

ROOT   = r"I:\Fleet\Diesel Report\Diesel Consumption"
out    = os.path.join(ROOT, "_joblist_info.txt")
lines  = []

def pr(msg=""):
    print(msg)
    lines.append(str(msg))

def read_excel_smart(path):
    """Read Excel, auto-detecting the real header row."""
    raw = pd.read_excel(path, header=None)
    hrow = 0
    veh_kw = {"vehicle no","veh no","plate no","reg no","vehicle","registration"}
    for i, row in raw.iterrows():
        lv = {str(v).strip().lower() for v in row.values}
        if "date" in lv and bool(lv & veh_kw):
            hrow = i; break
    df = pd.read_excel(path, header=hrow)
    df.columns = df.columns.str.strip()
    return df, hrow

def find_files(folder, exts=("*.xlsx","*.xls","*.xlsm","*.csv")):
    files = []
    for e in exts:
        files.extend(glob.glob(os.path.join(folder, e)))
    return files

# ─── 1. JOB LIST ────────────────────────────────────────────────────────────
pr("=" * 60)
pr("JOB LIST")
pr("=" * 60)
jfiles = find_files(os.path.join(ROOT, "Job List"))
if not jfiles:
    pr("  No files found in Job List subfolder!")
else:
    jpath = jfiles[0]
    pr(f"  File: {os.path.basename(jpath)}")
    jdf, hrow = read_excel_smart(jpath)
    pr(f"  Header at row: {hrow}")
    pr(f"  Columns: {list(jdf.columns)}")
    pr(f"  Shape: {jdf.shape}")
    if "Date" in jdf.columns:
        d = pd.to_datetime(jdf["Date"], errors="coerce").dropna()
        pr(f"  Date range: {d.min().date()} → {d.max().date()} ({len(d)} valid / {len(jdf)} total rows)")
        pr(f"  Date dtype (raw): {jdf['Date'].dtype}")
        pr(f"  Date samples (first 3): {jdf['Date'].dropna().head(3).tolist()}")
    if "Vehicle No" in jdf.columns:
        vehs = sorted(jdf["Vehicle No"].dropna().astype(str).str.strip().str.upper().str.replace(r'\s+','',regex=True).unique())
        pr(f"  Vehicle No ({len(vehs)} unique, first 10): {vehs[:10]}")
    if "Site" in jdf.columns:
        sites = sorted(jdf["Site"].dropna().astype(str).str.strip().unique())
        pr(f"  Sites ({len(sites)} unique): {sites[:20]}")

# ─── 2. TRANSACTION FILE ────────────────────────────────────────────────────
pr()
pr("=" * 60)
pr("TRANSACTIONS (Diesel)")
pr("=" * 60)
tfiles = find_files(os.path.join(ROOT, "Transactions"))
if not tfiles:
    pr("  No files found in Transactions subfolder!")
else:
    for tpath in tfiles:
        pr(f"  File: {os.path.basename(tpath)}")
        tdf = pd.read_excel(tpath) if not tpath.endswith(".csv") else pd.read_csv(tpath)
        tdf.columns = tdf.columns.str.strip()
        pr(f"  Columns: {list(tdf.columns)}")
        pr(f"  Shape: {tdf.shape}")
        # find date col
        for dc in tdf.columns:
            if "date" in dc.lower() or "time" in dc.lower():
                d = pd.to_datetime(tdf[dc], errors="coerce").dropna()
                pr(f"  '{dc}' range: {d.min().date()} → {d.max().date()} ({len(d)} rows)")
                pr(f"  '{dc}' dtype: {tdf[dc].dtype}")
                pr(f"  '{dc}' samples: {tdf[dc].dropna().head(3).tolist()}")
                break
        # show ALL vehicle/plate related columns
        for vc in tdf.columns:
            if any(k in vc.lower() for k in ("vehicle","plate","reg","licen")):
                vs = sorted(tdf[vc].dropna().astype(str).str.strip().str.upper().str.replace(r'\s+','',regex=True).unique())
                pr(f"  '{vc}' ({len(vs)} unique, first 10): {vs[:10]}")
        pr()

# ─── 3. VEHICLE LIST ────────────────────────────────────────────────────────
pr("=" * 60)
pr("VEHICLE LIST")
pr("=" * 60)
vfiles = find_files(os.path.join(ROOT, "Vehicle List"))
if not vfiles:
    pr("  No files found in Vehicle List subfolder!")
else:
    vpath = vfiles[0]
    pr(f"  File: {os.path.basename(vpath)}")
    vdf = pd.read_excel(vpath, engine="openpyxl")
    vdf.columns = vdf.columns.str.strip()
    pr(f"  Columns: {list(vdf.columns)}")
    pr(f"  Shape: {vdf.shape}")
    pr(f"  First 3 rows:\n{vdf.head(3).to_string()}")

# ─── Save ────────────────────────────────────────────────────────────────────
pr()
pr("Done.")
with open(out, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print(f"\nSaved to: {out}")
input("Press Enter to exit.")
