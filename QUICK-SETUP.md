# 🦆 WIGEON Quick Setup Guide

**Set up automated email report collection in 10 minutes.**

---

## What is WIGEON?

WIGEON automatically collects report attachments from your email, parses them (Excel, XML, ZIP), and consolidates the data into a searchable database. Perfect for managing reports from vendors, logistics partners, or any third-party sender.

**WIGEON = Workflow Intelligence for Gathering Email-Originated Notifications**

---

## What You Need

- Goose with `gmail` and `googledrive` extensions
- Google account with Gmail access
- Reports sent to your email (e.g., from vendors)

---

## Start WIGEON

```bash
# Navigate to WIGEON
cd ~/Desktop/WIGEON

# Show dashboard
python3 wigeon.py dashboard

# Or ask Goose:
# "Use WIGEON to fetch reports from vendor@example.com"
```

---

## Setup (One-Time, 2 Minutes)

### Step 1: Deploy the Apps Script
1. Go to [script.google.com](https://script.google.com) → New Project
2. Paste the script from: `~/Desktop/WIGEON/automation/WIGEON_Collector_Universal.gs`

### Step 2: Enter Your Vendor Email
Find this line at the top of the script:
```javascript
const VENDOR_EMAIL = 'YOUR_VENDOR_EMAIL@example.com';
```
Change it to your vendor's email:
```javascript
const VENDOR_EMAIL = 'reports@yourvendor.com';
```

### Step 3: Save & Run Setup
1. Save (Cmd+S)
2. Select **`setup`** from the dropdown → Click ▶️ Run
3. Authorize when prompted (click Advanced → Go to WIGEON → Allow)

**Done!** Reports collected daily at 7 AM.

### Adding More Vendors Later
1. Find `addSender` function
2. Edit the email address
3. Run `addSender`

---

## Daily Usage

**Automatic**: Google Apps Script collects reports at 7 AM daily.

**Manual ingest** (when needed):
```bash
cd ~/Desktop/WIGEON
python3 wigeon.py ingest --file "new_report.xlsx" --third-party "Vendor" --email "vendor@example.com"
```

**View dashboard**:
```bash
python3 wigeon.py dashboard
```

**Export data**:
```bash
python3 wigeon.py export --third-party "Vendor" --output data.csv
```

---

## Customize the Apps Script

Edit `SEARCH_QUERY` to match your emails:

```javascript
// Example: Reports from specific sender
const SEARCH_QUERY = 'from:reports@vendor.com has:attachment newer_than:7d';

// Example: Reports with specific subject
const SEARCH_QUERY = 'subject:"Daily Report" has:attachment newer_than:7d';

// Example: Multiple senders
const SEARCH_QUERY = '(from:vendor1@example.com OR from:vendor2@example.com) has:attachment newer_than:7d';
```

---

## Deploy Web Dashboard (Optional)

```bash
# Update index.html with your data
# Then deploy to Blockcell:
blockcell__manage_site(
  action="upload",
  site_name="my-wigeon-dashboard",
  directory_path="/path/to/WIGEON/web-dashboard"
)
```

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Gmail extension error | Reset macOS Keychain, re-authorize |
| No files collected | Check SEARCH_QUERY matches your emails |
| Ingest fails | Verify file is .xlsx or .xml format |
| Dashboard empty | Run `python3 wigeon.py stats` to check data |

---

## Resources

- **Project**: `~/Desktop/WIGEON/`
- **Database**: `~/Desktop/WIGEON/database/wigeon.db`
- **Scripts**: `~/Desktop/WIGEON/automation/`
- **Docs**: `~/Desktop/WIGEON/docs/`

---

**Questions?** Say "Resume WIGEON work" to continue where you left off! 🦆
