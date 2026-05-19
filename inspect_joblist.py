"""
Run this script once to inspect your Job List file structure.
Usage:  python inspect_joblist.py
"""
import pandas as pd
import glob, os

# ── Find the job list file ───────────────────────────────────────────────────
folder   = r"I:\Fleet\Diesel Report\Diesel Consumption\Job List"
patterns = ["*.xlsx", "*.xls", "*.xlsm", "*.csv"]
files    = []
for p in patterns:
    files.extend(glob.glob(os.path.join(folder, p)))

if not files:
    print("No files found in", folder)
    input("Press Enter to exit.")
    exit()

fpath = files[0]
print(f"\nReading: {fpath}\n{'='*60}")

# ── Load raw (no header assumption) ─────────────────────────────────────────
raw = pd.read_excel(fpath, header=None)
print(f"Total rows x cols: {raw.shape}")
print("\n--- First 20 rows (raw) ---")
for i, row in raw.head(20).iterrows():
    vals = [str(v).strip() for v in row.values if str(v).strip() not in ("nan", "")]
    if vals:
        print(f"  Row {i:2d}: {vals}")

# ── Auto-detect header row ────────────────────────────────────────────────────
header_row = 0
for i, row in raw.iterrows():
    vals_lower = {str(v).strip().lower() for v in row.values}
    if "date" in vals_lower:
        header_row = i
        print(f"\n>>> Header row detected at row {i}")
        break

df = pd.read_excel(fpath, header=header_row)
df.columns = df.columns.str.strip()

print(f"\n--- Column names (after header={header_row}) ---")
for c in df.columns:
    sample = df[c].dropna().head(3).tolist()
    print(f"  '{c}' → {sample}")

print(f"\n--- Date range ---")
for c in df.columns:
    if "date" in str(c).lower():
        try:
            dates = pd.to_datetime(df[c], errors="coerce").dropna()
            print(f"  '{c}': {dates.min().date()} → {dates.max().date()} ({len(dates)} rows)")
        except:
            pass

print(f"\n--- Vehicle No samples ---")
for c in df.columns:
    if any(k in str(c).lower() for k in ("vehicle", "veh", "plate", "reg")):
        sample = df[c].dropna().astype(str).str.strip().unique()[:10].tolist()
        print(f"  '{c}': {sample}")

print(f"\n--- Site/Project samples ---")
for c in df.columns:
    if any(k in str(c).lower() for k in ("site", "project", "location", "description")):
        sample = df[c].dropna().astype(str).str.strip().unique()[:15].tolist()
        print(f"  '{c}': {sample}")

input("\nDone — press Enter to exit.")
