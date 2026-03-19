# 🦆 WIGEON — Setup Guide

Complete step-by-step guide to get WIGEON running from scratch.

---

## Prerequisites

- **Python 3.9+** with pip
- **Google account** (for Gmail + Google Drive automation)
- **Goose** (optional — for conversational AI workflows)

---

## Step 1: Install WIGEON

```bash
git clone https://github.com/dsteffy85/wigeon.git
cd wigeon
pip install -r requirements.txt
```

Verify it works:

```bash
python3 wigeon.py --version
```

---

## Step 2: Run Setup

```bash
python3 wigeon.py setup
```

The setup wizard will ask:

1. **Provider name** — The company sending you reports (e.g., "Acme Logistics")
2. **Provider email** — The email address reports come from (e.g., `reports@acme.com`)
3. **Subject filter** — Optional keyword to match email subjects (e.g., "Daily Report")
4. **Google Drive folder ID** — Optional, for automated collection (set up in Step 3)

This creates a `config.json` file with your settings.

### Adding more providers later

```bash
python3 wigeon.py setup --add-provider
python3 wigeon.py setup --list-providers
python3 wigeon.py setup --remove-provider
```

---

## Step 3: Set Up Automated Collection (Optional)

This step deploys a Google Apps Script that automatically saves email attachments to Google Drive every day.

### 3a. Create the Apps Script

1. Go to [script.google.com](https://script.google.com)
2. Click **New Project**
3. Delete the default code
4. Copy the entire contents of `automation/WigeonCollector.gs` and paste it in
5. Save the project (name it "WIGEON Collector" or similar)

### 3b. Run Setup

1. In the Apps Script editor, select **`setup`** from the function dropdown (top toolbar)
2. Click **Run** ▶️
3. Grant the requested permissions (Gmail read, Drive write)
4. Check the **Execution log** — you should see:
   ```
   ✅ Folder ready: https://drive.google.com/...
   ✅ Label ready: WIGEON_Processed
   ✅ Daily trigger set for 7 AM
   🦆 WIGEON Setup Complete!
   ```

### 3c. Add Your First Sender

1. In the script, find the `addFirstSender()` function
2. Replace `'ENTER_VENDOR_EMAIL@example.com'` with your provider's actual email address
3. Select **`addFirstSender`** from the dropdown and click **Run** ▶️
4. You should see:
   ```
   ✅ Added: reports@acme.com
   📧 Tracking 1 sender(s):
      • reports@acme.com
   ```

### 3d. Test It

1. Select **`collectNow`** from the dropdown and click **Run** ▶️
2. Check your Google Drive for a new **WIGEON_Reports** folder
3. Any matching email attachments should appear as files

### 3e. Save the Folder ID

1. Open the **WIGEON_Reports** folder in Google Drive
2. Copy the folder ID from the URL: `https://drive.google.com/drive/folders/XXXXXXX`
3. Update your config:
   ```bash
   # Edit config.json and set google_drive_folder_id to the ID
   ```

### Adding more senders

To track emails from additional providers:

1. In the Apps Script, find `addSender()`
2. Replace `'ENTER_ANOTHER_EMAIL@example.com'` with the new email
3. Run `addSender`

---

## Step 4: Ingest Your First Reports

### Option A: Manual (place files in inbox/)

```bash
# Copy or download report files into the inbox directory
cp ~/Downloads/report.xlsx ~/path/to/wigeon/inbox/

# Ingest all files
python3 wigeon.py refresh
```

### Option B: From Google Drive (using Goose)

If you use Goose with the `googledrive` extension:

```
# In a Goose session:
"Download the latest files from WIGEON_Reports and ingest them"
```

Or run the auto-ingest recipe:

```bash
goose run automation/wigeon-auto-ingest.yaml
```

### Option C: Single file with explicit provider

```bash
python3 wigeon.py ingest \
  --file inbox/report.xlsx \
  --third-party "Acme Logistics" \
  --email reports@acme.com \
  --report-type "Daily Inventory"
```

---

## Step 5: Explore Your Data

```bash
# Overview
python3 wigeon.py stats

# List all reports
python3 wigeon.py list

# Full terminal dashboard
python3 wigeon.py dashboard

# Interactive dashboard
python3 wigeon.py dashboard --interactive

# Search reports
python3 wigeon.py dashboard --search "inventory"

# Query data from a specific provider
python3 wigeon.py query --third-party "Acme Logistics" --limit 10

# Export to CSV
python3 wigeon.py export --output exports/acme_data.csv --third-party "Acme Logistics"

# Export to JSON
python3 wigeon.py export --output exports/all_data.json --format json
```

---

## Step 6: Web Dashboard

```bash
# Generate dashboard data
python3 wigeon.py dashboard --export-json

# Open in browser
open web-dashboard/index.html
```

The web dashboard dynamically reads from `web-dashboard/dashboard-data.json` and displays:
- Provider cards with report counts
- Report type distribution chart
- Searchable report table
- Quick command reference

Re-run `dashboard --export-json` anytime to refresh the data.

---

## Daily Workflow

Once set up, your daily workflow is:

1. **Automatic** — Apps Script collects new email attachments at 7 AM
2. **Download** — Pull files from Google Drive to `inbox/`
3. **Ingest** — Run `python3 wigeon.py refresh`
4. **Analyze** — Query, export, or view the dashboard

Or with Goose, just say: *"Refresh WIGEON with the latest reports"*

---

## Troubleshooting

### No emails found by Apps Script
- Verify the sender email is correct: run `listSenders` in Apps Script
- Check that emails have attachments (xlsx, csv, xml, zip)
- Ensure the `WIGEON_Processed` label hasn't already been applied

### File parsing errors
- Check the file format is supported (xlsx, xls, csv, xml, zip)
- For CSV files, WIGEON auto-detects comma, pipe, and tab delimiters
- For ZIP files, the archive must contain supported file types

### Database issues
- Database location: `database/wigeon.db`
- Direct SQL access: `sqlite3 database/wigeon.db`
- Reset database: delete `database/wigeon.db` and re-ingest

### Config issues
- View config: `python3 wigeon.py setup --show`
- Example config: see `config.example.json`
- Reset config: delete `config.json` and run `python3 wigeon.py setup`

---

## Uninstall

WIGEON is fully self-contained. To remove:

```bash
rm -rf ~/path/to/wigeon
```

To remove the Apps Script:
1. Go to [script.google.com](https://script.google.com)
2. Delete the WIGEON Collector project
3. Delete the `WIGEON_Reports` folder from Google Drive
4. Delete the `WIGEON_Processed` label from Gmail (Settings → Labels)
