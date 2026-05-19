"""
onedrive_loader.py — Shingda Diesel Dashboard
Scans a OneDrive / SharePoint folder via Microsoft Graph API (app-only auth)
and returns file objects that slot directly into the existing load_* functions.

File-type detection rules (based on actual filenames):
  diesel    → filename contains "transaction"
  job       → filename contains "job list", or contains both "selpl" and "vehicle"
  vehicle   → filename contains "vehicle" but NOT "job" and NOT "odometer"
  bowser    → filename contains "fuel record" or the Chinese "燃油记录"
  odometer  → filename contains "odometer"
"""

from __future__ import annotations
import io
import requests


# ─────────────────────────────────────────────────────────────────────────────
# FILE-TYPE DETECTION
# ─────────────────────────────────────────────────────────────────────────────

DETECTION_RULES: list[tuple[str, callable]] = [
    ("diesel",   lambda n: "transaction" in n),
    ("job",      lambda n: "job list" in n or ("selpl" in n and "vehicle" in n)),
    ("vehicle",  lambda n: "vehicle" in n and "job" not in n and "odometer" not in n),
    ("bowser",   lambda n: "fuel record" in n or "燃油记录" in n),
    ("odometer", lambda n: "odometer" in n),
]


def detect_file_type(filename: str) -> str | None:
    """Return the report slot name for a given filename, or None if unrecognised."""
    lower = filename.lower()
    for slot, rule in DETECTION_RULES:
        # Pass original filename for Chinese character check, lower for everything else
        test_str = lower if slot != "bowser" else filename
        if rule(test_str if slot != "bowser" else filename.lower()) or (
            slot == "bowser" and "燃油记录" in filename
        ):
            return slot
    return None


# ─────────────────────────────────────────────────────────────────────────────
# AUTHENTICATION  (client-credentials / app-only)
# ─────────────────────────────────────────────────────────────────────────────

def get_access_token(tenant_id: str, client_id: str, client_secret: str) -> str:
    """
    Obtain an app-only OAuth2 token from Azure AD.
    Requires 'Files.Read.All' or 'Sites.Read.All' application permission.
    """
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    resp = requests.post(url, data={
        "grant_type":    "client_credentials",
        "client_id":     client_id,
        "client_secret": client_secret,
        "scope":         "https://graph.microsoft.com/.default",
    }, timeout=15)
    resp.raise_for_status()
    token = resp.json().get("access_token")
    if not token:
        raise ValueError(f"Token request failed: {resp.json()}")
    return token


# ─────────────────────────────────────────────────────────────────────────────
# GRAPH API HELPERS
# ─────────────────────────────────────────────────────────────────────────────

GRAPH = "https://graph.microsoft.com/v1.0"


def _get_json(token: str, url: str) -> dict:
    resp = requests.get(url, headers={"Authorization": f"Bearer {token}"}, timeout=30)
    resp.raise_for_status()
    return resp.json()


def list_folder_files(token: str, user_or_site: str, folder_path: str) -> list[dict]:
    """
    Return all file items inside a OneDrive folder (handles pagination).

    user_or_site examples
    ─────────────────────
    Personal OneDrive  →  "users/yuwei.phang@shingda.com"
    SharePoint site    →  "sites/{hostname},{site-id},{web-id}"
                          (get this from /sites?search=<site-name>)

    folder_path
    ───────────
    Path relative to the drive root, e.g.  "Fleet Reports/Diesel 2025"
    Use "/" for the root itself.
    """
    if folder_path.strip() in ("", "/"):
        url = f"{GRAPH}/{user_or_site}/drive/root/children"
    else:
        encoded = folder_path.replace(" ", "%20")
        url = f"{GRAPH}/{user_or_site}/drive/root:/{encoded}:/children"

    files = []
    while url:
        data = _get_json(token, url)
        files.extend(i for i in data.get("value", []) if "file" in i)
        url = data.get("@odata.nextLink")   # follow pagination
    return files


def download_file_bytes(token: str, item: dict) -> bytes:
    """
    Download a Graph API drive item and return the raw bytes.
    Callers should wrap in a fresh io.BytesIO when passing to pandas,
    to avoid the EOF seek bug when the same object is reused across re-runs.
    """
    dl_url = item.get("@microsoft.graph.downloadUrl")
    if not dl_url:
        raise ValueError(f"No download URL for item: {item.get('name')}")

    resp = requests.get(
        dl_url,
        headers={"Authorization": f"Bearer {token}"},
        timeout=60,
    )
    resp.raise_for_status()
    return resp.content


# ─────────────────────────────────────────────────────────────────────────────
# MAIN ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

ReportSlots = dict[str, list[dict]]   # {"diesel": [{"file": BytesIO, "name": str, "modified": str}]}


def load_reports_from_onedrive(
    tenant_id:     str,
    client_id:     str,
    client_secret: str,
    user_or_site:  str,
    folder_path:   str,
) -> ReportSlots:
    """
    Scan the OneDrive folder and return a dict keyed by report slot.

    Returns
    ───────
    {
        "diesel":   [{"file": BytesIO, "name": str, "modified": str}, ...],
        "job":      [...],
        "vehicle":  [...],
        "bowser":   [...],
        "odometer": [...],
    }
    Each slot is sorted newest-first by lastModifiedDateTime.
    Unrecognised files are silently skipped.
    """
    token  = get_access_token(tenant_id, client_id, client_secret)
    items  = list_folder_files(token, user_or_site, folder_path)

    slots: ReportSlots = {k: [] for k in ("diesel", "job", "vehicle", "bowser", "odometer")}

    for item in items:
        slot = detect_file_type(item["name"])
        if slot is None:
            continue
        try:
            raw_bytes = download_file_bytes(token, item)
        except Exception as exc:
            # Don't crash the whole scan if one file fails to download
            print(f"[onedrive_loader] Warning: could not download {item['name']}: {exc}")
            continue
        slots[slot].append({
            "bytes":    raw_bytes,          # raw bytes — _wire_files wraps in fresh BytesIO
            "name":     item["name"],
            "modified": item.get("lastModifiedDateTime", "")[:16].replace("T", "  "),
        })

    # Sort each slot newest-first
    for key in slots:
        slots[key].sort(key=lambda x: x["modified"], reverse=True)

    return slots


# ─────────────────────────────────────────────────────────────────────────────
# UTILITY — find a SharePoint site ID (run once to configure secrets)
# ─────────────────────────────────────────────────────────────────────────────

def find_site_id(token: str, hostname: str, site_name: str) -> str:
    """
    Helper to look up a SharePoint site ID by name.
    Example: find_site_id(token, "shingda.sharepoint.com", "FleetReports")
    Prints the value you should use for user_or_site in secrets.toml.
    """
    url = f"{GRAPH}/sites/{hostname}:/sites/{site_name}"
    data = _get_json(token, url)
    site_id = data.get("id", "")
    print(f"SharePoint site id: sites/{site_id}")
    return f"sites/{site_id}"
