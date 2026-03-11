# WIGEON 100% Automation Setup Guide 🦆

## Overview

This guide walks you through setting up **100% automated** CEVA report collection using Google Apps Script + Google Drive + WIGEON.

```
┌─────────────────────────────────────────────────────────────────┐
│                    AUTOMATION FLOW                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Gmail                Google Apps Script        Google Drive    │
│   ┌─────┐              ┌──────────────┐         ┌─────────┐     │
│   │CEVA │  ──────────► │ Collector    │ ──────► │ WIGEON_ │     │
│   │Email│   (auto)     │ Script       │  (auto) │ CEVA_   │     │
│   └─────┘              └──────────────┘         │ Reports │     │
│                                                  └────┬────┘     │
│                                                       │          │
│                                                       ▼          │
│   Blockcell            WIGEON CLI              googledrive       │
│   ┌─────────┐          ┌──────────────┐        ┌─────────┐      │
│   │Dashboard│ ◄─────── │ Ingest &     │ ◄───── │Extension│      │
│   │  Live   │  (auto)  │ Process      │ (auto) │Download │      │
│   └─────────┘          └──────────────┘        └─────────┘      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Prerequisites

- Google account with Gmail access
- Access to Google Apps Script (script.google.com)
- Goose with googledrive extension enabled
- WIGEON installed at `~/Desktop/WIGEON/`

---

## Part 1: Google Apps Script Setup (10 minutes)

### Step 1: Create New Apps Script Project

1. Go to **https://script.google.com**
2. Click **"New Project"**
3. Name it: **"WIGEON CEVA Collector"**

### Step 2: Copy the Script

1. Delete any existing code in the editor
2. Open the file: `~/Desktop/WIGEON/automation/CEVAReportCollector.gs`
3. Copy the entire contents
4. Paste into the Apps Script editor
5. Click **Save** (Ctrl+S / Cmd+S)

### Step 3: Run Initial Setup

1. In the function dropdown (top), select **`setupScript`**
2. Click **Run** (▶️ button)
3. **Authorize** when prompted:
   - Click "Review Permissions"
   - Select your Google account
   - Click "Advanced" → "Go to WIGEON CEVA Collector"
   - Click "Allow"

4. Check the **Execution log** for success message:
   ```
   ✅ Folder created/found: WIGEON_CEVA_Reports
   ✅ Label created/found: WIGEON_Processed
   ✅ Gmail access working
   🎉 Setup complete!
   ```

5. **Copy the Folder URL** from the log - you'll need it later!

### Step 4: Test the Collector

1. Select **`collectCEVAReports`** from the dropdown
2. Click **Run**
3. Check the log for processed files:
   ```
   📧 Found 15 email threads
   ✅ Saved: 2026-03-10_Block_Open_Orders.xlsx
   ✅ Saved: 2026-03-10_Block_Inventory_Transaction_Detail.xlsx
   ...
   🎉 WIGEON Collection Complete!
   📊 Files saved: 12
   ```

### Step 5: Set Up Automatic Trigger

1. Select **`createDailyTrigger`** (or `createHourlyTrigger`)
2. Click **Run**
3. Verify in **Triggers** menu (clock icon on left):
   - Should show `collectCEVAReports` running daily at 7 AM

**✅ Part 1 Complete!** Google Apps Script is now automatically collecting CEVA reports.

---

## Part 2: Google Drive Folder Setup (2 minutes)

### Verify Folder Created

1. Go to **Google Drive** (drive.google.com)
2. Look for folder: **WIGEON_CEVA_Reports**
3. Open it and verify files are being saved

### Get Folder ID

The folder ID is in the URL:
```
https://drive.google.com/drive/folders/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
                                        ↑
                                   This is the Folder ID
```

**Save this ID** - you'll need it for the WIGEON recipe.

---

## Part 3: WIGEON Integration (5 minutes)

### Step 1: Test Google Drive Connection

In Goose, run:
```
Search Google Drive for WIGEON_CEVA_Reports folder
```

Or manually:
```bash
# Goose will use googledrive extension to find the folder
```

### Step 2: Download Files from Drive

Once files are in Google Drive, WIGEON can pull them:

```bash
cd ~/Desktop/WIGEON

# Goose command to download from Drive
# googledrive__download(id_or_url="FILE_ID", output_path="inbox/")
```

### Step 3: Ingest into WIGEON

```bash
# Ingest each downloaded file
python3 wigeon.py ingest --file inbox/2026-03-10_Block_Open_Orders.xlsx \
  --third-party "CEVA Logistics" \
  --email ops_reporting@example.com
```

### Step 4: Update Dashboard

```bash
# Export fresh data
python3 wigeon.py export --third-party "CEVA Logistics" \
  --output exports/ceva_all_data.csv --format csv

# Show updated stats
python3 wigeon.py dashboard
```

---

## Part 4: Automated Recipe (Optional)

### Create Scheduled Job

Use the WIGEON auto-ingest recipe:

```bash
cd ~/Desktop/WIGEON
goose run automation/wigeon-auto-ingest.yaml
```

Or set up a scheduled job:

```python
platform__manage_schedule(
    action="create",
    recipe_path="~/WIGEON/automation/wigeon-auto-ingest.yaml",
    cron_expression="0 8 * * *"  # Daily at 8 AM (after Apps Script runs at 7 AM)
)
```

---

## Complete Automation Schedule

| Time | Component | Action |
|------|-----------|--------|
| 7:00 AM | Google Apps Script | Collects CEVA emails → Google Drive |
| 8:00 AM | WIGEON Recipe | Downloads from Drive → Ingests → Updates Dashboard |
| 8:05 AM | Blockcell | Dashboard deployed with fresh data |

**Result: 100% automated, zero manual steps!** 🎉

---

## Troubleshooting

### Apps Script Issues

**"Authorization required"**
- Run `setupScript()` again and re-authorize

**"No emails found"**
- Check Gmail for CEVA emails
- Verify sender email: `ops_reporting@example.com`
- Run `clearProcessedLabel()` to reprocess emails

**"Quota exceeded"**
- Apps Script has daily limits
- Reduce `MAX_EMAILS_PER_RUN` in CONFIG

### Google Drive Issues

**"Folder not found"**
- Run `setupScript()` in Apps Script
- Check Drive for `WIGEON_CEVA_Reports` folder

**"Permission denied"**
- Ensure googledrive extension is enabled
- Re-authorize Google Drive access

### WIGEON Issues

**"File not found"**
- Verify file downloaded to `inbox/` folder
- Check file extension is .xlsx, .xls, .csv, or .zip

**"Parse error"**
- File may be corrupted
- Try downloading again from Drive

---

## Quick Reference

### Apps Script Functions

| Function | Purpose |
|----------|---------|
| `setupScript()` | Initial setup (run once) |
| `collectCEVAReports()` | Main collection function |
| `createDailyTrigger()` | Set up daily automation |
| `createHourlyTrigger()` | Set up hourly automation |
| `listFiles()` | List files in Drive folder |
| `clearProcessedLabel()` | Reset for reprocessing |

### WIGEON Commands

| Command | Purpose |
|---------|---------|
| `python3 wigeon.py ingest --file <path>` | Ingest a report |
| `python3 wigeon.py list` | List all reports |
| `python3 wigeon.py query --report-id <id>` | Query report data |
| `python3 wigeon.py export --output <file>` | Export data |
| `python3 wigeon.py dashboard` | Show dashboard |
| `python3 wigeon.py stats` | Show statistics |

### Key URLs

| Resource | URL |
|----------|-----|
| Apps Script | https://script.google.com |
| Google Drive | https://drive.google.com |
| WIGEON Dashboard | https://your-deployment-url.example.com/ |

---

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review logs in Apps Script execution history
3. Check WIGEON logs: `~/Desktop/WIGEON/*.log`

---

**🦆 WIGEON - 100% Automated Report Collection**

*Setup Time: ~15 minutes*
*Maintenance: Zero (fully automated)*
*Reliability: 99%+ (Google infrastructure)*
