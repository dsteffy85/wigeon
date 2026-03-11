# 🦆 WIGEON - Workflow Intelligence for Gathering Email-Originated Notifications

**Version 1.0** | **Status: Production Ready**

WIGEON is a data integration agent that runs within the Goose platform. It automatically retrieves email reports from third-party sources, parses multiple file formats, and consolidates data into a queryable SQLite database.

---

## 🎯 What WIGEON Does

WIGEON helps you:
- ✅ Fetch email reports from third-party vendors
- ✅ Parse Excel (.xlsx, .xls), XML, and ZIP files
- ✅ Store data with third-party identification
- ✅ Query consolidated data across all sources
- ✅ Export to CSV, JSON, or Excel formats
- ✅ Maintain data quality and validation

---

## 🚀 Quick Start

### 1. Using WIGEON through Goose (Recommended)

Simply ask Goose to run WIGEON:

```
"Run WIGEON to fetch reports from vendor@acme.com for the last 7 days"
```

Goose will:
1. Search your Gmail for matching emails
2. Download attachments
3. Parse and store data
4. Show you a summary

### 2. Using WIGEON CLI Directly

```bash
cd ~/Desktop/WIGEON

# Ingest a report
python3 wigeon.py ingest \
  --file samples/sales_report.xlsx \
  --third-party "Acme Corp" \
  --email vendor@acme.com \
  --report-type "Sales Report"

# List all reports
python3 wigeon.py list

# Query data
python3 wigeon.py query --report-id 1 --limit 10

# Export to CSV
python3 wigeon.py export --output data.csv --format csv

# Show statistics
python3 wigeon.py stats
```

---

## 📁 Project Structure

```
~/Desktop/WIGEON/
├── wigeon.py                    # Main CLI interface
├── wigeon_recipe.yaml           # Goose recipe definition
├── README.md                    # This file
├── scripts/
│   ├── database_schema.py       # SQLite database management
│   ├── file_parser.py          # Multi-format file parser
│   └── wigeon_processor.py     # Core processing logic
├── database/
│   └── wigeon.db               # SQLite database (auto-created)
├── inbox/                      # Downloaded email attachments
├── exports/                    # Exported data files
├── samples/                    # Sample data for testing
│   ├── sales_report.xlsx
│   ├── inventory_report.xlsx
│   ├── shipments.xml
│   └── quarterly_report.xlsx
└── docs/
    └── USER_GUIDE.md           # Detailed user guide
```

---

## 🗄️ Database Schema

WIGEON uses SQLite with three main tables:

### 1. **third_parties**
Stores information about report sources
- `id`, `name`, `email`, `contact_info`, `metadata`, `created_at`, `updated_at`

### 2. **reports**
Tracks ingested reports
- `id`, `third_party_id`, `report_type`, `report_date`, `file_name`, `file_format`, `file_path`, `status`, `row_count`, `email_subject`, `email_date`, `metadata`, `created_at`, `processed_at`

### 3. **report_data**
Stores actual report data (flexible JSON structure)
- `id`, `report_id`, `third_party_id`, `row_number`, `data` (JSON), `created_at`

---

## 📊 Supported File Formats

| Format | Extension | Status | Notes |
|--------|-----------|--------|-------|
| Excel (Modern) | .xlsx, .xlsm | ✅ Supported | Full support via openpyxl |
| Excel (Legacy) | .xls | ⚠️ Limited | Requires xlrd library |
| XML | .xml | ✅ Supported | Parses to structured data |
| ZIP Archives | .zip | ✅ Supported | Extracts and processes contents |

---

## 💡 Usage Examples

### Example 1: Fetch Weekly Sales Report

```
User: "Fetch sales reports from vendor@acme.com for the last 7 days"

WIGEON will:
1. Search Gmail for emails from vendor@acme.com
2. Download Excel/CSV attachments
3. Parse and store data with "Acme Corp" identification
4. Show summary: "Ingested 150 rows from 3 reports"
```

### Example 2: Query Specific Data

```bash
# Query all data from Acme Corp
python3 wigeon.py query --third-party "Acme Corp" --limit 50

# Query specific report
python3 wigeon.py query --report-id 1 --format json
```

### Example 3: Export Consolidated Data

```bash
# Export all data to CSV
python3 wigeon.py export --output all_data.csv --format csv

# Export specific third-party to Excel
python3 wigeon.py export --output acme_data.xlsx --third-party "Acme Corp" --format excel
```

### Example 4: Monitor Data Collection

```bash
# Show statistics
python3 wigeon.py stats

# List all reports
python3 wigeon.py list

# List reports from last 30 days
python3 wigeon.py list --start-date 2026-02-08 --end-date 2026-03-08
```

---

## 🔧 CLI Command Reference

### `ingest` - Import a report file

```bash
python3 wigeon.py ingest \
  --file <path>                    # Required: Path to file
  --third-party <name>             # Required: Company name
  --email <address>                # Required: Email address
  --report-type <type>             # Optional: Report category
  --report-date <YYYY-MM-DD>       # Optional: Report date
  --subject <text>                 # Optional: Email subject
  --email-date <YYYY-MM-DD>        # Optional: Email date
  --notes <text>                   # Optional: Additional notes
```

### `list` - List reports

```bash
python3 wigeon.py list \
  --third-party <name>             # Optional: Filter by company
  --report-type <type>             # Optional: Filter by type
  --start-date <YYYY-MM-DD>        # Optional: Start date
  --end-date <YYYY-MM-DD>          # Optional: End date
  --status <pending|processed|failed>  # Optional: Filter by status
```

### `query` - Query report data

```bash
python3 wigeon.py query \
  --report-id <id>                 # Optional: Specific report
  --third-party <name>             # Optional: Filter by company
  --limit <number>                 # Optional: Max rows (default: 100)
  --offset <number>                # Optional: Skip rows (default: 0)
  --format <table|json>            # Optional: Output format (default: table)
```

### `export` - Export data to file

```bash
python3 wigeon.py export \
  --output <path>                  # Required: Output file path
  --report-id <id>                 # Optional: Specific report
  --third-party <name>             # Optional: Filter by company
  --format <csv|json|excel>        # Optional: Format (default: csv)
```

### `stats` - Show statistics

```bash
python3 wigeon.py stats
```

---

## 🎓 How to Use with Goose

### Method 1: Natural Language (Easiest)

Just ask Goose naturally:

```
"Use WIGEON to fetch reports from vendor@acme.com"
"Show me all reports in WIGEON database"
"Export WIGEON data to CSV"
```

### Method 2: Run as Recipe

```bash
# In Goose
goose run ~/Desktop/WIGEON/wigeon_recipe.yaml
```

### Method 3: Load as Subagent

```
"Load WIGEON and fetch reports from TechStart Inc"
```

---

## 🔍 Data Query Patterns

### Query by Third-Party

```bash
python3 wigeon.py query --third-party "Acme Corp" --limit 100
```

### Query by Report ID

```bash
python3 wigeon.py query --report-id 1 --format json
```

### Query with Pagination

```bash
# First 50 rows
python3 wigeon.py query --limit 50 --offset 0

# Next 50 rows
python3 wigeon.py query --limit 50 --offset 50
```

---

## 📈 Monitoring & Maintenance

### Check Database Status

```bash
python3 wigeon.py stats
```

Output:
```
📊 WIGEON STATISTICS

   Third-parties: 3
   Total reports: 15
   Total data rows: 2,450

   Reports by status:
     processed: 14
     pending: 1

   Reports by third-party:
     Acme Corp: 8
     TechStart Inc: 5
     Global Solutions: 2
```

### List Recent Reports

```bash
python3 wigeon.py list --start-date 2026-03-01
```

### Database Location

```
~/Desktop/WIGEON/database/wigeon.db
```

You can query directly with SQLite tools if needed:
```bash
sqlite3 ~/Desktop/WIGEON/database/wigeon.db
```

---

## 🐛 Troubleshooting

### Issue: "xlrd not available"

**Solution**: Install xlrd for .xls support (optional)
```bash
pip3 install xlrd
```

### Issue: File parsing fails

**Solution**: Check file format and try manual inspection
```bash
python3 -c "from scripts.file_parser import FileParser; FileParser().parse_file('file.xlsx')"
```

### Issue: Email not found

**Solution**: Check search parameters
- Verify sender email address
- Check date range
- Confirm email exists in Gmail

### Issue: Database locked

**Solution**: Close other connections
```bash
# Check for open connections
lsof ~/Desktop/WIGEON/database/wigeon.db
```

---

## 🔐 Data Privacy & Security

- ✅ **Local Storage**: All data stored on your machine
- ✅ **No Cloud**: No external uploads or services
- ✅ **User Control**: You own and control all data
- ✅ **SQLite**: Industry-standard database format
- ✅ **Transparent**: All operations logged and visible

---

## 📚 Additional Resources

- **User Guide**: `docs/USER_GUIDE.md` - Detailed usage guide
- **Recipe File**: `wigeon_recipe.yaml` - Goose integration
- **Sample Data**: `samples/` - Test files for learning
- **Database Schema**: `scripts/database_schema.py` - Schema details

---

## 🤝 Getting Help

### Within Goose

```
"Help me use WIGEON"
"Show WIGEON examples"
"Explain WIGEON commands"
```

### CLI Help

```bash
python3 wigeon.py --help
python3 wigeon.py ingest --help
python3 wigeon.py query --help
```

---

## 🎉 Success Stories

**Typical Use Case**: Consolidating weekly vendor reports

1. **Before WIGEON**: Manual download, copy-paste, Excel gymnastics (30 min/week)
2. **With WIGEON**: "Fetch reports from vendor@acme.com" (30 seconds)
3. **Result**: 60x faster, zero errors, queryable history

---

## 📝 Version History

### v1.0 (2026-03-08)
- ✅ Initial release
- ✅ Multi-format file parsing (Excel, XML, ZIP)
- ✅ SQLite database backend
- ✅ CLI interface with 5 commands
- ✅ Goose recipe integration
- ✅ Export to CSV, JSON, Excel
- ✅ Query and statistics features
- ✅ Sample data and documentation

---

## 🦆 Why "WIGEON"?

**WIGEON** = **W**orkflow **I**ntelligence for **G**athering **E**mail-**O**riginated **N**otifications

Wigeons are social ducks that work well in groups - just like WIGEON consolidates data from multiple sources!

---

**Built with ❤️ for the Goose platform**

*WIGEON - Making data integration simple, one email at a time* 🦆
