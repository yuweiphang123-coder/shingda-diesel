# Shingda Diesel Dashboard — Deployment Setup Guide

This guide walks through the three steps needed to make the dashboard
auto-load files from your office network folder via OneDrive and run on
Streamlit Cloud.

---

## Overview

```
Network Folder  →  OneDrive Sync  →  OneDrive Cloud  →  Dashboard reads files  →  Streamlit Cloud URL
(office server)     (one-time IT)     (Microsoft 365)    (Microsoft Graph API)     (shareable link)
```

---

## STEP A — Sync the Network Folder to OneDrive

> **Who does this:** IT admin or any user who has access to the network folder
> and has OneDrive for Business installed.

1. On a PC that can see the network folder (e.g. `\\SERVER\Fleet Reports\Diesel`),
   open **File Explorer**.

2. Navigate to the network folder:
   ```
   I:\Fleet\Diesel Report\Diesel Consumption
   ```

3. Right-click the folder → **"Add shortcut to OneDrive"**
   (or drag it into your OneDrive folder if the shortcut option isn't available).

   - Alternatively: open the **OneDrive sync client** (system tray icon),
     go to **Settings → Account → Add a folder**, and point it to the network path.

4. Wait for the initial sync to complete (the folder icon turns to a green tick ✓).

5. From now on, any file saved to the network folder will automatically appear
   in OneDrive within a few minutes.

> **Tip:** The PC doing the sync must stay powered on and connected to the network.
> A dedicated always-on machine (e.g. a server or office workstation) is ideal.

---

## STEP B — Create an Azure App Registration

> **Who does this:** Azure AD admin (or ask IT to do it and send you the three values at the end).

This creates a "service account" that lets the dashboard read OneDrive files
without anyone needing to log in each time.

### B1. Open the Azure Portal

Go to **https://portal.azure.com** and sign in with your Microsoft 365 admin account.

### B2. Register a new App

1. Search for **"App registrations"** in the top search bar → click it.
2. Click **"+ New registration"**.
3. Fill in:
   - **Name:** `Shingda Diesel Dashboard`
   - **Supported account types:** *Accounts in this organizational directory only*
   - **Redirect URI:** leave blank (not needed for app-only auth)
4. Click **Register**.

### B3. Note your IDs (you'll need these later)

On the app's **Overview** page, copy:
- **Application (client) ID** → this is your `client_id`
- **Directory (tenant) ID** → this is your `tenant_id`

### B4. Create a Client Secret

1. In the left menu, go to **Certificates & secrets**.
2. Click **"+ New client secret"**.
3. Description: `Dashboard secret`  |  Expires: **24 months** (or your preference)
4. Click **Add**.
5. **Copy the Value immediately** — you cannot see it again after leaving this page.
   This is your `client_secret`.

### B5. Grant API Permissions

1. In the left menu, go to **API permissions**.
2. Click **"+ Add a permission"** → **Microsoft Graph** → **Application permissions**.
3. Search for and tick:
   - `Files.Read.All`   ← allows reading any user's OneDrive files
4. Click **Add permissions**.
5. Click **"Grant admin consent for [your organisation]"** → **Yes**.
   The status column should now show a green tick.

### B6. Find the OneDrive folder path

You need two things: who owns the OneDrive and the folder path inside it.

**If files are in a user's personal OneDrive** (e.g. synced under your account):
- `user_or_site` = `users/yuwei.phang@shingda.com`
- `folder_path`  = the path inside OneDrive, e.g. `Fleet Reports/Diesel`

**If files are in a SharePoint document library** (shared team site):
- You need the site ID.  After completing Step B, run this once in Python to find it:

```python
import onedrive_loader
token = onedrive_loader.get_access_token("YOUR_TENANT_ID", "YOUR_CLIENT_ID", "YOUR_CLIENT_SECRET")
site_id = onedrive_loader.find_site_id(token, "shingda.sharepoint.com", "YOUR_SITE_NAME")
print(site_id)   # → "sites/shingda.sharepoint.com,abc-123,def-456"
```

- `user_or_site` = the printed value
- `folder_path`  = the folder path inside the document library, e.g. `Shared Documents/Fleet Reports/Diesel`

---

## STEP C — Deploy to Streamlit Cloud

### C1. Push code to GitHub

Streamlit Cloud deploys from a GitHub repository.

1. Create a free account at **https://github.com** if you don't have one.
2. Create a new **private** repository called `shingda-diesel-dashboard`.
3. Upload these files to the repo:
   - `app.py`
   - `onedrive_loader.py`
   - `requirements.txt`
   - `Top.png`
   - `Bottom.png`
   - `.streamlit/config.toml`

   You can do this via the GitHub web UI (drag-and-drop upload) or using Git.

### C2. Deploy on Streamlit Cloud

1. Go to **https://share.streamlit.io** and sign in with your GitHub account.
2. Click **"New app"**.
3. Select:
   - **Repository:** `shingda-diesel-dashboard`
   - **Branch:** `main`
   - **Main file path:** `app.py`
4. Click **"Advanced settings…"** → open the **Secrets** section.
5. Paste the following (replace all placeholder values):

```toml
[onedrive]
tenant_id     = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
client_id     = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
client_secret = "your-client-secret-value-here"
user_or_site  = "users/yuwei.phang@shingda.com"
folder_path   = "Fleet Reports/Diesel"
```

6. Click **Save** → **Deploy**.
7. Wait ~2 minutes for the first build. You'll get a public URL like:
   `https://shingda-diesel-dashboard.streamlit.app`

### C3. Share the URL

Send the URL to anyone who needs access.  The dashboard will always show
the latest files from OneDrive automatically each time it's opened.
Click the **🔄 Refresh** button to force an immediate re-scan if you know
new files have just been added.

---

## File Detection Rules

The dashboard identifies each report by keywords in the filename:

| Report | Keyword(s) detected | Example filename |
|--------|---------------------|------------------|
| Diesel Transactions | `transaction` | `Transactions.xls -Apr 26` |
| Job List | `job list` OR (`selpl` + `vehicle`) | `SELPL Vehicle Job List Apr 26.xlsx` |
| Vehicle List | `vehicle` (without "job" or "odometer") | `Vehicle List.xlsx` |
| Bowser / Fuel Records | `fuel record` or `燃油记录` | `Fuel Records 燃油记录(25001-25690) May until 5th.xlsx` |
| Odometer | `odometer` | `Odometer Detail Apr 26.xlsx` |

> If a file isn't being picked up, check that its name contains the right keyword.
> Keyword matching is **case-insensitive**.

---

## Local Testing (before deploying)

To test OneDrive loading on your own machine before deploying:

1. Create the file `.streamlit/secrets.toml` in the project folder with the same
   contents as the secrets block in Step C2.
2. Run `streamlit run app.py` as usual.
3. The dashboard will auto-load from OneDrive instead of showing upload boxes.

> **Security note:** Never commit `secrets.toml` to GitHub.
> Add it to `.gitignore`:  `echo ".streamlit/secrets.toml" >> .gitignore`

---

## Troubleshooting

| Problem | Likely cause | Fix |
|---------|-------------|-----|
| "Could not connect to OneDrive" | Wrong tenant/client ID or secret | Double-check the three values in secrets |
| Files not found in folder | File keyword not matched | Check filename contains the expected keyword |
| "Admin consent required" | API permission not granted | Repeat Step B5 and grant admin consent |
| Dashboard shows old data | Files not yet synced | Wait a few minutes, then click 🔄 Refresh |
| Transactions file not loading | `.xls` format (old Excel) | `xlrd` in requirements.txt handles this — check it's installed |
