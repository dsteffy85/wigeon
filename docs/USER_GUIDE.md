# 🦆 WIGEON User Guide

**Complete Guide to Using WIGEON for Data Integration**

---

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Core Workflows](#core-workflows)
4. [Advanced Usage](#advanced-usage)
5. [Best Practices](#best-practices)
6. [Troubleshooting](#troubleshooting)
7. [FAQ](#faq)

---

## Introduction

### What is WIGEON?

WIGEON is a data integration agent that helps you consolidate email-based reports from multiple third-party sources into a unified, queryable database.

### Key Benefits

- **Automated**: Fetch reports directly from Gmail
- **Flexible**: Supports Excel, XML, ZIP, and more
- **Organized**: All data tagged by source and date
- **Queryable**: SQLite backend for powerful queries
- **Exportable**: Output to CSV, JSON, or Excel

### When to Use WIGEON

✅ You receive regular reports via email from vendors/partners  
✅ Reports come in various formats (Excel, XML, etc.)  
✅ You need to consolidate data from multiple sources  
✅ You want to query historical data easily  
✅ You need to export combined datasets  

---

## Getting Started

### Prerequisites

- Goose platform installed
- Gmail account with report emails
- Python 3.x with required libraries

### Installation Check

```bash
cd ~/Desktop/WIGEON
python3 wigeon.py --help
```

You should see the WIGEON help menu.

### First Run

Let's test WIGEON with sample data:

```bash
# Ingest sample sales report
python3 wigeon.py ingest \
  --file samples/sales_report.xlsx \
  --third-party "Acme Corp" \
  --email vendor@acme.com \
  --report-type "Sales Report"

# Check statistics
python3 wigeon.py stats

# Query the data
python3 wigeon.py query --report-id 1 --limit 5
```

---

## Core Workflows

### Workflow 1: Fetch and Ingest Email Report

**Scenario**: You receive weekly sales reports from Acme Corp

#### Step 1: Ask Goose to Fetch Report

```
"Use WIGEON to fetch reports from vendor@acme.com for the last 7 days"
```

Goose will:
1. Search Gmail for emails from vendor@acme.com
2. Download attachments to ~/Desktop/WIGEON/inbox/
3. Parse files and extract data
4. Store in database with Acme Corp identification

#### Step 2: Verify Ingestion

```bash
python3 wigeon.py list --third-party "Acme Corp"
```

#### Step 3: Query Data

```bash
python3 wigeon.py query --third-party "Acme Corp" --limit 10
```

---

### Workflow 2: Manual File Ingestion

**Scenario**: You have a report file on your Desktop

#### Step 1: Ingest File

```bash
python3 wigeon.py ingest \
  --file ~/Desktop/monthly_report.xlsx \
  --third-party "TechStart Inc" \
  --email reports@techstart.com \
  --report-type "Monthly Summary" \
  --report-date "2026-03-01"
```

#### Step 2: Verify

```bash
python3 wigeon.py list
```

---

### Workflow 3: Export Consolidated Data

**Scenario**: You need all data from multiple vendors in one CSV

#### Step 1: Export All Data

```bash
python3 wigeon.py export \
  --output ~/Desktop/consolidated_reports.csv \
  --format csv
```

#### Step 2: Export Specific Third-Party

```bash
python3 wigeon.py export \
  --output ~/Desktop/acme_data.xlsx \
  --third-party "Acme Corp" \
  --format excel
```

---

### Workflow 4: Query and Analyze

**Scenario**: You want to analyze specific data

#### Query by Third-Party

```bash
python3 wigeon.py query \
  --third-party "Acme Corp" \
  --limit 100 \
  --format json > acme_data.json
```

#### Query Specific Report

```bash
python3 wigeon.py query \
  --report-id 5 \
  --limit 50
```

#### Query with Pagination

```bash
# First page (rows 1-50)
python3 wigeon.py query --limit 50 --offset 0

# Second page (rows 51-100)
python3 wigeon.py query --limit 50 --offset 50
```

---

## Advanced Usage

### Using WIGEON with Goose Recipes

Create a custom recipe for your specific use case:

```yaml
name: acme-weekly-reports
description: Fetch weekly sales reports from Acme Corp

instructions: |
  Use WIGEON to fetch and process weekly sales reports from Acme Corp.
  
  Steps:
  1. Search Gmail for emails from vendor@acme.com in last 7 days
  2. Download Excel attachments
  3. Ingest using WIGEON with third-party "Acme Corp"
  4. Export consolidated data to CSV
  5. Show summary statistics

parameters:
  days_back:
    type: integer
    default: 7
```

### Automated Workflows

You can schedule WIGEON operations using Goose platform scheduler:

```bash
# Create scheduled job (example)
platform__manage_schedule \
  action="create" \
  recipe_path="~/Desktop/WIGEON/wigeon_recipe.yaml" \
  cron_expression="0 9 * * 1"  # Every Monday at 9 AM
```

### Custom Data Queries

Access SQLite database directly for complex queries:

```bash
sqlite3 ~/Desktop/WIGEON/database/wigeon.db

# Example queries
SELECT third_party_name, COUNT(*) as report_count 
FROM reports 
GROUP BY third_party_name;

SELECT * FROM report_data 
WHERE json_extract(data, '$.Total') > 10000;
```

---

## Best Practices

### 1. Consistent Naming

Use consistent third-party names:
- ✅ Good: "Acme Corp", "Acme Corp", "Acme Corp"
- ❌ Bad: "Acme Corp", "Acme", "ACME CORP"

### 2. Include Metadata

Always provide optional metadata:

```bash
python3 wigeon.py ingest \
  --file report.xlsx \
  --third-party "Acme Corp" \
  --email vendor@acme.com \
  --report-type "Weekly Sales" \
  --report-date "2026-03-08" \
  --subject "Week 10 Sales Report" \
  --notes "Q1 data, includes new product line"
```

### 3. Regular Exports

Export data regularly for backup:

```bash
# Weekly backup
python3 wigeon.py export \
  --output ~/Desktop/WIGEON/backups/backup_$(date +%Y%m%d).csv \
  --format csv
```

### 4. Monitor Statistics

Check database health regularly:

```bash
python3 wigeon.py stats
```

### 5. Validate Data

After ingestion, spot-check data:

```bash
python3 wigeon.py query --report-id 1 --limit 5
```

---

## Troubleshooting

### Problem: File Parsing Fails

**Symptoms**: Error message "Failed to parse file"

**Solutions**:
1. Check file format is supported
2. Verify file is not corrupted
3. Try opening file manually in Excel/text editor
4. Check for password protection

```bash
# Debug parsing
python3 -c "
from scripts.file_parser import FileParser
parser = FileParser()
data = parser.parse_file('problem_file.xlsx')
print(data)
"
```

### Problem: No Data Returned from Query

**Symptoms**: Query returns 0 rows

**Solutions**:
1. Verify report was ingested successfully
2. Check third-party name spelling
3. Verify report ID exists

```bash
# List all reports
python3 wigeon.py list

# Check specific third-party
python3 wigeon.py list --third-party "Acme Corp"
```

### Problem: Database Locked

**Symptoms**: "Database is locked" error

**Solutions**:
1. Close other connections to database
2. Check for hung processes

```bash
# Find processes using database
lsof ~/Desktop/WIGEON/database/wigeon.db

# Kill if necessary
kill -9 <PID>
```

### Problem: Email Not Found

**Symptoms**: Goose can't find email

**Solutions**:
1. Verify email address is correct
2. Check date range is appropriate
3. Confirm email exists in Gmail
4. Check Gmail search syntax

```bash
# Test Gmail search manually
gmail__search_tool \
  subject="Sales Report" \
  from="vendor@acme.com" \
  after="2026-03-01"
```

### Problem: Export Fails

**Symptoms**: Export command fails

**Solutions**:
1. Check output directory exists
2. Verify write permissions
3. Check disk space

```bash
# Create export directory
mkdir -p ~/Desktop/WIGEON/exports

# Check permissions
ls -la ~/Desktop/WIGEON/exports
```

---

## FAQ

### Q: Can WIGEON handle multiple sheets in Excel files?

**A**: Yes! WIGEON processes all sheets and tags data with sheet name.

```bash
# Query will show _sheet field
python3 wigeon.py query --report-id 1 --format json
```

### Q: How do I delete old reports?

**A**: Use SQLite directly:

```bash
sqlite3 ~/Desktop/WIGEON/database/wigeon.db

DELETE FROM report_data WHERE report_id = 5;
DELETE FROM reports WHERE id = 5;
```

### Q: Can I use WIGEON with non-Gmail email?

**A**: Currently WIGEON uses Gmail extension. For other email providers, download attachments manually and use `ingest` command.

### Q: What's the maximum file size?

**A**: No hard limit, but performance may degrade with files >100MB. Consider splitting large files.

### Q: Can I rename a third-party?

**A**: Yes, update in database:

```bash
sqlite3 ~/Desktop/WIGEON/database/wigeon.db

UPDATE third_parties 
SET name = 'New Name' 
WHERE name = 'Old Name';

UPDATE reports 
SET third_party_name = 'New Name' 
WHERE third_party_name = 'Old Name';
```

### Q: How do I backup the database?

**A**: Copy the SQLite file:

```bash
cp ~/Desktop/WIGEON/database/wigeon.db \
   ~/Desktop/WIGEON/database/wigeon_backup_$(date +%Y%m%d).db
```

### Q: Can WIGEON handle PDF files?

**A**: Not currently. Convert PDFs to Excel/CSV first using external tools.

### Q: How do I share data with colleagues?

**A**: Export to shared format:

```bash
# Export to CSV for sharing
python3 wigeon.py export \
  --output ~/Desktop/shared_data.csv \
  --format csv
```

### Q: Can I filter exports by date?

**A**: Use SQLite query for advanced filtering:

```bash
sqlite3 ~/Desktop/WIGEON/database/wigeon.db

.headers on
.mode csv
.output filtered_data.csv

SELECT * FROM report_data rd
JOIN reports r ON rd.report_id = r.id
WHERE r.report_date >= '2026-03-01' 
  AND r.report_date <= '2026-03-08';

.quit
```

### Q: How do I update existing data?

**A**: WIGEON doesn't update existing data. Re-ingest the file with updated data, or use SQLite to update directly.

### Q: Can I use WIGEON programmatically?

**A**: Yes! Import the modules:

```python
from scripts.wigeon_processor import WigeonProcessor

processor = WigeonProcessor()
processor.process_file(
    file_path="report.xlsx",
    third_party_name="Acme Corp",
    third_party_email="vendor@acme.com"
)
```

---

## Examples Gallery

### Example 1: Weekly Vendor Report Consolidation

```bash
# Monday morning routine
python3 wigeon.py ingest \
  --file ~/Downloads/acme_weekly.xlsx \
  --third-party "Acme Corp" \
  --email vendor@acme.com \
  --report-type "Weekly Sales" \
  --report-date "2026-03-08"

python3 wigeon.py export \
  --output ~/Desktop/weekly_summary.csv \
  --format csv
```

### Example 2: Multi-Vendor Analysis

```bash
# Fetch from multiple vendors
# Vendor 1
python3 wigeon.py ingest \
  --file vendor1_report.xlsx \
  --third-party "Vendor One" \
  --email v1@vendor.com

# Vendor 2
python3 wigeon.py ingest \
  --file vendor2_report.xml \
  --third-party "Vendor Two" \
  --email v2@vendor.com

# Export consolidated
python3 wigeon.py export \
  --output multi_vendor_analysis.xlsx \
  --format excel
```

### Example 3: Historical Data Query

```bash
# Query last 30 days
python3 wigeon.py list \
  --start-date 2026-02-08 \
  --end-date 2026-03-08

# Export specific period
python3 wigeon.py export \
  --output february_data.csv \
  --format csv
```

---

## Getting Help

### In Goose

```
"Help me use WIGEON"
"Show WIGEON examples"
"Explain WIGEON query command"
```

### CLI Help

```bash
python3 wigeon.py --help
python3 wigeon.py ingest --help
python3 wigeon.py query --help
python3 wigeon.py export --help
```

### Check Documentation

- README.md - Quick start guide
- USER_GUIDE.md - This comprehensive guide
- wigeon_recipe.yaml - Goose integration details

---

## Support & Feedback

WIGEON is built for the Goose platform. For issues or suggestions:

1. Check this guide and README.md
2. Review troubleshooting section
3. Ask Goose for help
4. Check database directly with SQLite

---

**Happy data integrating! 🦆**

*WIGEON - Making email-based data integration effortless*
