# 🦆 WIGEON - CEVA Report Automation Guide

Complete guide for fetching CEVA logistics reports automatically.

---

## 🎯 Three Ways to Fetch CEVA Reports

### **Method 1: Natural Language (Easiest!)**

Just ask Goose:

```
"Fetch all CEVA reports from the past 7 days"
```

Or use the recipe:

```bash
cd ~/Desktop/WIGEON
goose run ceva_fetch_recipe.yaml
```

Goose will handle everything automatically!

---

### **Method 2: Semi-Automated (Most Reliable)**

Best when Gmail extension has issues:

```bash
cd ~/Desktop/WIGEON
./fetch_ceva_simple.sh
```

**What happens:**
1. ✅ Script opens Gmail with CEVA search
2. 👆 You download attachments (30 seconds)
3. ✅ WIGEON auto-detects and ingests files
4. ✅ Shows consolidated data

**Time:** ~1 minute total

---

### **Method 3: Fully Manual**

If you already have files downloaded:

```bash
cd ~/Desktop/WIGEON

# Ingest each file
python3 wigeon.py ingest \
  --file ~/Downloads/Block_Open_Orders.xlsx \
  --third-party "CEVA Logistics" \
  --email "ops_reporting@example.com" \
  --report-type "Block Open Orders"

# View results
python3 wigeon.py stats
python3 wigeon.py list
```

---

## 📊 CEVA Report Types

WIGEON auto-detects these report types from filenames:

| Report Type | Filename Pattern |
|-------------|------------------|
| Block Open Orders | Contains "Open Order" (not Cancel) |
| Block Open Orders - BKO WMS Cancel | "Open Order" + "Cancel" |
| Block Service Level Detail | "Service Level" |
| Block Inventory Transaction Detail | "Inventory Transaction" |
| Block SRL Returns Disposition | "Return" + "Disposition" |
| Block SRL Return Receipts | "Return" + "Receipt" |

---

## 🔍 Email Search Patterns

WIGEON looks for emails matching:

- **From:** `ops_reporting@example.com`
- **Subject:** Contains "CEVA CLS NORTAM"
- **Time:** Last 7 days (configurable)
- **Has:** Attachments

**Gmail Search:**
```
from:ops_reporting@example.com newer_than:7d has:attachment CEVA
```

---

## 📥 After Ingestion

### View Statistics
```bash
python3 wigeon.py stats
```

### List CEVA Reports
```bash
python3 wigeon.py list --third-party "CEVA Logistics"
```

### Query Data
```bash
# All CEVA data
python3 wigeon.py query --third-party "CEVA Logistics"

# Specific report
python3 wigeon.py query --report-id 2 --limit 100

# Filter by date
python3 wigeon.py query --third-party "CEVA Logistics" --limit 50
```

### Export Consolidated Data
```bash
# Export to CSV
python3 wigeon.py export \
  --third-party "CEVA Logistics" \
  --output ceva_consolidated.csv \
  --format csv

# Export to Excel
python3 wigeon.py export \
  --third-party "CEVA Logistics" \
  --output ceva_consolidated.xlsx \
  --format excel

# Export to JSON
python3 wigeon.py export \
  --third-party "CEVA Logistics" \
  --output ceva_consolidated.json \
  --format json
```

---

## 🛠️ Troubleshooting

### Gmail Extension Not Working

**Issue:** Keychain password errors

**Solution:** Use Method 2 (semi-automated):
```bash
./fetch_ceva_simple.sh
```

This opens Gmail in your browser, you download files manually (30 sec), then WIGEON auto-ingests them.

---

### No Files Found in Downloads

**Check:**
```bash
ls -lt ~/Downloads/*.xlsx | head -5
```

**Solution:**
- Make sure files downloaded successfully
- Check Downloads folder in Finder
- Try re-downloading attachments

---

### Files Not Auto-Detected

**Manual ingest:**
```bash
python3 wigeon.py ingest \
  --file ~/Downloads/[filename] \
  --third-party "CEVA Logistics" \
  --email "ops_reporting@example.com"
```

---

### Browser Automation Fails

**Fallback:**
1. Open Gmail manually
2. Search: `from:ops_reporting@example.com newer_than:7d CEVA`
3. Download attachments
4. Run: `./fetch_ceva_simple.sh` and press Enter twice

---

## 📅 Scheduling (Future)

To run automatically every day:

```bash
# Create scheduled job
platform__manage_schedule \
  action="create" \
  recipe_path="~/Desktop/WIGEON/ceva_fetch_recipe.yaml" \
  cron_expression="0 9 * * *"  # 9 AM daily
```

---

## 💡 Pro Tips

1. **Run weekly** to keep data fresh
2. **Export regularly** for backup
3. **Query by date** to track trends
4. **Combine with other reports** for full visibility

---

## 🎯 Quick Reference

| Task | Command |
|------|---------|
| Fetch reports (auto) | `goose run ceva_fetch_recipe.yaml` |
| Fetch reports (semi) | `./fetch_ceva_simple.sh` |
| View stats | `python3 wigeon.py stats` |
| List reports | `python3 wigeon.py list` |
| Query data | `python3 wigeon.py query --third-party "CEVA Logistics"` |
| Export CSV | `python3 wigeon.py export --output ceva.csv` |

---

## 📞 Need Help?

See full documentation:
- `README.md` - Overview
- `QUICK_START.md` - 5-minute tutorial
- `docs/USER_GUIDE.md` - Complete reference

---

**Last Updated:** March 8, 2026  
**Status:** Production Ready  
**WIGEON Version:** 1.0
