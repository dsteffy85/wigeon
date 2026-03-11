# 🦆 WIGEON Quick Start Guide

**Get started with WIGEON in 5 minutes!**

---

## What is WIGEON?

WIGEON is a data integration agent that fetches email reports, parses multiple file formats, and consolidates data into a queryable database.

**WIGEON** = **W**orkflow **I**ntelligence for **G**athering **E**mail-**O**riginated **N**otifications

---

## 🚀 Three Ways to Use WIGEON

### 1. Through Goose (Easiest!)

Just ask Goose naturally:

```
"Use WIGEON to fetch reports from vendor@acme.com for the last 7 days"
```

Goose will handle everything automatically!

### 2. CLI Commands (Direct Control)

```bash
cd ~/Desktop/WIGEON

# Ingest a file
python3 wigeon.py ingest \
  --file report.xlsx \
  --third-party "Acme Corp" \
  --email vendor@acme.com

# List reports
python3 wigeon.py list

# Query data
python3 wigeon.py query --report-id 1 --limit 10

# Export to CSV
python3 wigeon.py export --output data.csv --format csv

# Show stats
python3 wigeon.py stats
```

### 3. As a Goose Recipe

```bash
goose run ~/Desktop/WIGEON/wigeon_recipe.yaml
```

---

## 📝 5-Minute Tutorial

### Step 1: Test with Sample Data (30 seconds)

```bash
cd ~/Desktop/WIGEON

# Ingest sample sales report
python3 wigeon.py ingest \
  --file samples/sales_report.xlsx \
  --third-party "Acme Corp" \
  --email vendor@acme.com \
  --report-type "Sales Report"
```

**Expected output:**
```
✅ Successfully processed 50 rows
```

### Step 2: View the Data (15 seconds)

```bash
# Show statistics
python3 wigeon.py stats

# List reports
python3 wigeon.py list

# Query first 5 rows
python3 wigeon.py query --report-id 1 --limit 5
```

### Step 3: Export Data (15 seconds)

```bash
# Export to CSV
python3 wigeon.py export \
  --output my_first_export.csv \
  --format csv
```

**Check the file:**
```bash
open my_first_export.csv
```

### Step 4: Try More Samples (2 minutes)

```bash
# Ingest inventory report
python3 wigeon.py ingest \
  --file samples/inventory_report.xlsx \
  --third-party "TechStart Inc" \
  --email reports@techstart.com \
  --report-type "Inventory"

# Ingest XML shipments
python3 wigeon.py ingest \
  --file samples/shipments.xml \
  --third-party "Global Logistics" \
  --email shipping@global.com \
  --report-type "Shipments"

# Check stats again
python3 wigeon.py stats
```

### Step 5: Query Consolidated Data (1 minute)

```bash
# Query all data
python3 wigeon.py query --limit 20

# Query specific third-party
python3 wigeon.py query --third-party "Acme Corp"

# Export everything
python3 wigeon.py export \
  --output consolidated_data.xlsx \
  --format excel
```

---

## 🎯 Common Use Cases

### Use Case 1: Weekly Vendor Reports

**Scenario:** You receive weekly sales reports from Acme Corp every Monday.

**Solution:**
```
Ask Goose: "Use WIGEON to fetch reports from vendor@acme.com for the last 7 days"
```

Goose will:
1. Search Gmail for emails from vendor@acme.com
2. Download Excel attachments
3. Parse and store data
4. Show you a summary

### Use Case 2: Multi-Vendor Consolidation

**Scenario:** You need to combine data from 5 different vendors.

**Solution:**
```bash
# Ingest from each vendor
python3 wigeon.py ingest --file vendor1.xlsx --third-party "Vendor 1" --email v1@vendor.com
python3 wigeon.py ingest --file vendor2.xlsx --third-party "Vendor 2" --email v2@vendor.com
python3 wigeon.py ingest --file vendor3.xlsx --third-party "Vendor 3" --email v3@vendor.com
python3 wigeon.py ingest --file vendor4.xml --third-party "Vendor 4" --email v4@vendor.com
python3 wigeon.py ingest --file vendor5.xlsx --third-party "Vendor 5" --email v5@vendor.com

# Export consolidated
python3 wigeon.py export --output all_vendors.csv --format csv
```

### Use Case 3: Historical Data Analysis

**Scenario:** You need to analyze 3 months of historical data.

**Solution:**
```bash
# List reports from specific period
python3 wigeon.py list --start-date 2026-01-01 --end-date 2026-03-31

# Export specific period
python3 wigeon.py export --output q1_data.xlsx --format excel
```

---

## 📊 Command Cheat Sheet

### Ingest Command
```bash
python3 wigeon.py ingest \
  --file <path>                    # Required
  --third-party "Company Name"     # Required
  --email vendor@company.com       # Required
  --report-type "Report Type"      # Optional
  --report-date "2026-03-08"       # Optional
```

### List Command
```bash
python3 wigeon.py list                              # All reports
python3 wigeon.py list --third-party "Acme Corp"    # Specific vendor
python3 wigeon.py list --start-date 2026-03-01      # Date range
```

### Query Command
```bash
python3 wigeon.py query --report-id 1               # Specific report
python3 wigeon.py query --third-party "Acme Corp"   # Specific vendor
python3 wigeon.py query --limit 50 --offset 0       # Pagination
python3 wigeon.py query --format json               # JSON output
```

### Export Command
```bash
python3 wigeon.py export --output data.csv --format csv      # CSV
python3 wigeon.py export --output data.xlsx --format excel   # Excel
python3 wigeon.py export --output data.json --format json    # JSON
python3 wigeon.py export --third-party "Acme Corp" --output acme.csv  # Filtered
```

### Stats Command
```bash
python3 wigeon.py stats    # Show database statistics
```

---

## 🔍 Supported File Formats

| Format | Extension | Status |
|--------|-----------|--------|
| Excel (Modern) | .xlsx, .xlsm | ✅ Fully supported |
| Excel (Legacy) | .xls | ⚠️ Requires xlrd library |
| XML | .xml | ✅ Fully supported |
| ZIP Archives | .zip | ✅ Fully supported |

---

## 💡 Pro Tips

### Tip 1: Use Consistent Naming
Always use the same third-party name for the same vendor:
- ✅ Good: "Acme Corp", "Acme Corp", "Acme Corp"
- ❌ Bad: "Acme Corp", "Acme", "ACME CORP"

### Tip 2: Include Metadata
Add optional metadata for better organization:
```bash
python3 wigeon.py ingest \
  --file report.xlsx \
  --third-party "Acme Corp" \
  --email vendor@acme.com \
  --report-type "Weekly Sales" \
  --report-date "2026-03-08" \
  --notes "Q1 data, includes new product line"
```

### Tip 3: Regular Backups
Export data regularly:
```bash
python3 wigeon.py export \
  --output backup_$(date +%Y%m%d).csv \
  --format csv
```

### Tip 4: Use Goose for Automation
Let Goose handle the workflow:
```
"Use WIGEON to fetch all reports from vendor@acme.com this month and export to CSV"
```

### Tip 5: Check Stats Regularly
Monitor your database:
```bash
python3 wigeon.py stats
```

---

## 🐛 Quick Troubleshooting

### Problem: "xlrd not available"
**Solution:** This is just a warning. .xlsx files work fine. Only affects .xls files.

### Problem: File parsing fails
**Solution:** Check file format and try opening manually in Excel.

### Problem: No data in query
**Solution:** Verify report was ingested:
```bash
python3 wigeon.py list
```

### Problem: Email not found
**Solution:** Check sender email and date range:
```
Ask Goose: "Search Gmail for emails from vendor@acme.com in last 7 days"
```

---

## 📚 Learn More

- **Full Documentation:** `README.md`
- **Detailed Guide:** `docs/USER_GUIDE.md`
- **Recipe File:** `wigeon_recipe.yaml`
- **Sample Data:** `samples/` directory

---

## 🎉 You're Ready!

You now know how to:
- ✅ Ingest reports from files
- ✅ Query consolidated data
- ✅ Export to multiple formats
- ✅ Use WIGEON through Goose
- ✅ Handle common scenarios

**Next Steps:**
1. Try ingesting your own report files
2. Ask Goose to fetch reports from your email
3. Explore advanced queries in USER_GUIDE.md

---

## 🆘 Need Help?

### Ask Goose:
```
"Help me use WIGEON"
"Show WIGEON examples"
"Explain WIGEON commands"
```

### CLI Help:
```bash
python3 wigeon.py --help
python3 wigeon.py ingest --help
```

---

**Happy data integrating! 🦆**

*WIGEON - Making email-based data integration effortless*

**Project Location:** `~/Desktop/WIGEON/`  
**Database:** `~/Desktop/WIGEON/database/wigeon.db`  
**Version:** 1.0
