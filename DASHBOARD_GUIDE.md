# 🦆 WIGEON Dashboard Guide

## Overview

The WIGEON Dashboard provides an interactive, visual way to explore your consolidated report data. It offers multiple views, search capabilities, and detailed breakdowns of all ingested reports.

---

## Quick Start

### View Full Dashboard
```bash
cd ~/Desktop/WIGEON
python3 wigeon.py dashboard
```

This shows:
- 📊 Summary statistics (third parties, reports, data rows)
- 📋 Third party breakdown
- 📊 Report types
- ✅ Status breakdown
- 📆 Reports by date (last 7 days)
- 📅 Recent reports (last 10)

---

## Dashboard Commands

### 1. Full Dashboard (Default)
```bash
python3 wigeon.py dashboard
```

Shows complete overview with all sections.

### 2. Recent Reports
```bash
# Show last 20 reports
python3 wigeon.py dashboard --recent 20

# Show last 5 reports
python3 wigeon.py dashboard --recent 5
```

### 3. Search Reports
```bash
# Search by filename or report type
python3 wigeon.py dashboard --search "Open Orders"

# Search for CEVA reports
python3 wigeon.py dashboard --search "CEVA"

# Search by date
python3 wigeon.py dashboard --search "2026-03"
```

### 4. Reports by Date Range
```bash
# Last 7 days (default)
python3 wigeon.py dashboard --days 7

# Last 30 days
python3 wigeon.py dashboard --days 30

# Last 90 days
python3 wigeon.py dashboard --days 90
```

### 5. Interactive Mode
```bash
python3 wigeon.py dashboard --interactive
```

Provides a menu-driven interface with options:
1. Show full dashboard
2. Show summary statistics
3. Show recent reports
4. Show reports by third party
5. Show reports by type
6. Show reports by date
7. Search reports
8. View report details
9. Exit

---

## Dashboard Sections Explained

### 📊 Summary Statistics
- **Third Parties**: Number of unique vendors/sources
- **Total Reports**: Number of reports ingested
- **Total Data Rows**: Total rows across all reports

### 📋 Third Party Breakdown
For each third party:
- Company name and email
- Number of reports
- Total data rows
- Date of first report
- Date of most recent report

### 📊 Report Types
Shows breakdown by report type:
- Report type name
- Number of reports
- Total rows

### ✅ Status Breakdown
Reports grouped by status:
- **processed**: Successfully ingested
- **pending**: Awaiting processing
- **failed**: Processing errors

### 📆 Reports by Date
Daily breakdown showing:
- Date
- Number of reports received
- Total rows ingested

### 📅 Recent Reports
Table showing most recent reports:
- Report ID
- Third party name
- Report type
- Report date
- Row count
- Status

---

## Use Cases

### Daily Monitoring
```bash
# Check what came in today
python3 wigeon.py dashboard --days 1

# View recent activity
python3 wigeon.py dashboard --recent 10
```

### Weekly Review
```bash
# Full dashboard for weekly overview
python3 wigeon.py dashboard

# Check last 7 days
python3 wigeon.py dashboard --days 7
```

### Finding Specific Reports
```bash
# Search by vendor
python3 wigeon.py dashboard --search "CEVA"

# Search by report type
python3 wigeon.py dashboard --search "Inventory"

# Search by date
python3 wigeon.py dashboard --search "2026-03-08"
```

### Data Quality Checks
```bash
# View full dashboard to check:
# - Are all expected vendors reporting?
# - Are reports coming in daily?
# - Are there any failed reports?
# - Are row counts consistent?

python3 wigeon.py dashboard
```

---

## Interactive Mode Walkthrough

Start interactive mode:
```bash
python3 wigeon.py dashboard --interactive
```

### Menu Options:

**1. Show full dashboard**
- Displays complete overview
- Best for initial check

**2. Show summary statistics**
- Quick high-level numbers
- Fastest view

**3. Show recent reports**
- Prompts for number of reports
- Shows latest activity

**4. Show reports by third party**
- Breakdown by vendor
- Shows reporting frequency

**5. Show reports by type**
- Groups by report category
- Identifies most common reports

**6. Show reports by date**
- Prompts for number of days
- Shows daily trends

**7. Search reports**
- Prompts for search term
- Searches filenames and types

**8. View report details**
- Prompts for report ID
- Shows complete metadata
- Displays sample data rows

**9. Exit**
- Closes interactive mode

---

## Advanced Usage

### Combining with Other Commands

**Dashboard → Query → Export**
```bash
# 1. Find report ID
python3 wigeon.py dashboard --search "Open Orders"

# 2. Query specific report
python3 wigeon.py query --report-id 5 --limit 10

# 3. Export to CSV
python3 wigeon.py export --report-id 5 --output orders.csv
```

**Dashboard → List → Export**
```bash
# 1. Check what CEVA reports exist
python3 wigeon.py dashboard --search "CEVA"

# 2. List all CEVA reports
python3 wigeon.py list --third-party "CEVA Logistics"

# 3. Export all CEVA data
python3 wigeon.py export --third-party "CEVA Logistics" --output ceva_all.csv
```

---

## Dashboard Output Examples

### Full Dashboard Output
```
================================================================================
🦆 WIGEON DASHBOARD - Report Overview
================================================================================

📊 SUMMARY STATISTICS
--------------------------------------------------------------------------------
  Third Parties:     3
  Total Reports:     45
  Total Data Rows:   12,450

📋 THIRD PARTY BREAKDOWN
--------------------------------------------------------------------------------

  CEVA Logistics
    Email:        ops_reporting@example.com
    Reports:      35
    Total Rows:   10,200
    First Report: 2026-03-01
    Last Report:  2026-03-08

  Acme Corp
    Email:        vendor@acme.com
    Reports:      8
    Total Rows:   1,850
    First Report: 2026-03-05
    Last Report:  2026-03-08

  Global Shipping
    Email:        reports@globalship.com
    Reports:      2
    Total Rows:   400
    First Report: 2026-03-07
    Last Report:  2026-03-08

📊 REPORT TYPES
--------------------------------------------------------------------------------
  Block Open Orders - Daily                 7 reports     2,100 rows
  Block Inventory Transaction Detail - MTD  5 reports     3,500 rows
  Block Service Level Detail - Daily        7 reports     1,750 rows
  Sales Report                              8 reports     1,850 rows
  Shipment Tracking                         2 reports       400 rows

✅ STATUS BREAKDOWN
--------------------------------------------------------------------------------
  processed          43 reports
  pending             2 reports

📆 REPORTS BY DATE (Last 7 days)
--------------------------------------------------------------------------------
Date         Reports    Total Rows  
--------------------------------------------------------------------------------
2026-03-08           12        3,200
2026-03-07            8        2,100
2026-03-06            6        1,500
2026-03-05            9        2,400
2026-03-04            5        1,800
2026-03-03            3        1,050
2026-03-02            2          400

📅 RECENT REPORTS (Last 10)
--------------------------------------------------------------------------------
ID   Third Party          Report Type                    Date         Rows     Status    
--------------------------------------------------------------------------------
  45 CEVA Logistics       Block Open Orders - Daily      2026-03-08        300 processed 
  44 CEVA Logistics       Block Service Level Detail     2026-03-08        250 processed 
  43 Acme Corp            Sales Report                   2026-03-08         50 processed 
  42 CEVA Logistics       Block Inventory Transaction    2026-03-07        700 processed 
  41 Global Shipping      Shipment Tracking              2026-03-07        200 processed 
  40 CEVA Logistics       Block Open Orders - Daily      2026-03-07        300 processed 
  39 CEVA Logistics       Block Service Level Detail     2026-03-07        250 processed 
  38 Acme Corp            Sales Report                   2026-03-07         50 processed 
  37 CEVA Logistics       Block Open Orders - Daily      2026-03-06        300 processed 
  36 CEVA Logistics       Block Service Level Detail     2026-03-06        250 processed 
```

### Search Results Output
```
🔍 SEARCH RESULTS for 'Open Orders'
--------------------------------------------------------------------------------
ID   Third Party          Report Type                    Date         Rows    
--------------------------------------------------------------------------------
  45 CEVA Logistics       Block Open Orders - Daily      2026-03-08        300
  40 CEVA Logistics       Block Open Orders - Daily      2026-03-07        300
  37 CEVA Logistics       Block Open Orders - Daily      2026-03-06        300
  34 CEVA Logistics       Block Open Orders - Daily      2026-03-05        300
  31 CEVA Logistics       Block Open Orders - Daily      2026-03-04        300

Found 5 matching reports
```

---

## Tips & Best Practices

### Daily Workflow
1. Start with full dashboard to get overview
2. Check recent reports for today's activity
3. Search for specific vendors if needed
4. Export any reports that need analysis

### Weekly Review
1. Run `--days 7` to see weekly trends
2. Check third party breakdown for consistency
3. Verify all expected vendors are reporting
4. Look for any failed reports

### Monthly Analysis
1. Run `--days 30` for monthly view
2. Export consolidated data for analysis
3. Review report types and frequencies
4. Identify any gaps or anomalies

### Troubleshooting
- **No reports showing**: Check if data has been ingested
- **Wrong dates**: Reports show by ingestion date, not report date
- **Missing vendor**: Search by email or partial name
- **Status = failed**: View report details to see error

---

## Integration with Goose

You can also invoke the dashboard through natural language:

```
"Show me the WIGEON dashboard"
"Search WIGEON for CEVA reports"
"Show me recent reports in WIGEON"
```

Goose will automatically run the appropriate dashboard command.

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `dashboard` | Full overview |
| `dashboard --recent 20` | Last 20 reports |
| `dashboard --search "term"` | Search reports |
| `dashboard --days 30` | Last 30 days |
| `dashboard --interactive` | Menu mode |

---

## Next Steps

After viewing the dashboard:

1. **Query specific data**: Use `wigeon.py query`
2. **Export reports**: Use `wigeon.py export`
3. **Ingest more data**: Use `wigeon.py ingest`
4. **List reports**: Use `wigeon.py list`

---

**Dashboard Version**: 1.0  
**Last Updated**: March 9, 2026  
**Status**: Production Ready ✅
