# 🦆 WIGEON

**Workflow Intelligence for Gathering Email-Originated Notifications**

WIGEON is a universal agent that collects email report attachments from any third-party provider and stores the data in a queryable SQLite database for easy analysis.

Whether you receive daily inventory reports, sales summaries, shipment tracking, or any other recurring email attachments — WIGEON automates the collection, parsing, and storage so you can focus on analysis instead of file management.

---

## ✨ Features

- **Any Provider** — Works with any email sender. Add as many providers as you need.
- **Multi-Format** — Parses Excel (.xlsx, .xls), CSV, XML, and ZIP archives automatically.
- **Smart Ingestion** — Detects delimiters (comma, pipe, tab), handles multi-sheet workbooks, and normalizes data.
- **Local Database** — All data stored in a local SQLite database. No cloud dependencies.
- **Web Dashboard** — Clean, dynamic HTML dashboard to visualize your report data.
- **CLI Interface** — Full command-line tool for setup, ingestion, querying, and export.
- **Automated Collection** — Google Apps Script collects attachments from Gmail to Google Drive on a daily schedule.
- **Goose Integration** — Works as a Goose recipe/agent for conversational data management.

---

## 🚀 Quick Start

### 1. Clone and install

```bash
git clone https://github.com/dsteffy85/wigeon.git
cd wigeon
pip install -r requirements.txt
```

### 2. Run setup

```bash
python3 wigeon.py setup
```

This interactive wizard will:
- Ask for your first provider's name and email address
- Optionally configure a Google Drive folder for automated collection
- Create a `config.json` with your settings

### 3. Add report files

Place report files (Excel, CSV, XML, ZIP) in the `inbox/` directory, then:

```bash
python3 wigeon.py refresh
```

WIGEON will parse every file, match it to a provider, and store the data.

### 4. Explore your data

```bash
python3 wigeon.py stats          # Database overview
python3 wigeon.py list           # List all reports
python3 wigeon.py dashboard      # Full terminal dashboard
python3 wigeon.py export --output data.csv --format csv  # Export
```

---

## 📖 Commands

| Command | Description |
|---------|-------------|
| `setup` | First-time setup or manage providers |
| `setup --add-provider` | Add a new email provider |
| `setup --list-providers` | List configured providers |
| `setup --remove-provider` | Remove a provider |
| `setup --show` | Show full configuration |
| `refresh` | Ingest all files from `inbox/` |
| `ingest` | Ingest a single file with explicit provider info |
| `list` | List reports (with optional filters) |
| `query` | Query report data rows |
| `export` | Export data to CSV, JSON, or Excel |
| `stats` | Show database statistics |
| `dashboard` | Terminal dashboard view |
| `dashboard --export-json` | Export JSON for the web dashboard |
| `dashboard --interactive` | Interactive terminal dashboard |

---

## 🌐 Web Dashboard

WIGEON includes a dynamic web dashboard that reads from your database:

```bash
# Generate the dashboard data
python3 wigeon.py dashboard --export-json

# Open in browser
open web-dashboard/index.html
```

The dashboard shows:
- Provider cards with report counts and row totals
- Report type distribution chart
- Searchable report table
- Quick command reference

---

## 🤖 Automated Collection (Google Apps Script)

For fully automated daily collection, deploy the included Google Apps Script:

1. Go to [script.google.com](https://script.google.com) → New Project
2. Paste the contents of `automation/WigeonCollector.gs`
3. Run the `setup` function (grants permissions, creates folder + trigger)
4. Edit the email in `addFirstSender()` and run it

The script will:
- Search Gmail daily at 7 AM for emails with attachments from your providers
- Save Excel/CSV/XML/ZIP attachments to a `WIGEON_Reports` folder in Google Drive
- Keep only the 2 most recent copies of each report type (automatic cleanup)
- Mark processed emails with a `WIGEON_Processed` label

Then use Goose or the CLI to download from Drive and ingest:

```bash
# Download files from Google Drive to inbox/ (via Goose googledrive extension)
# Then ingest:
python3 wigeon.py refresh
```

See [SETUP.md](SETUP.md) for the complete setup guide.

---

## 🦢 Using with Goose

WIGEON works as a Goose recipe for conversational interaction:

```bash
goose run wigeon_recipe.yaml
```

Or use the auto-ingest recipe for scheduled automation:

```bash
goose run automation/wigeon-auto-ingest.yaml
```

Example conversation:
> **You:** Fetch the latest reports from Acme Logistics  
> **Goose:** Searching Google Drive... Found 3 new files. Downloading and ingesting...  
> ✅ Ingested 3 reports (12,450 rows). Run `stats` to see the updated totals.

---

## 📁 Project Structure

```
wigeon/
├── wigeon.py                    # Main CLI (setup, refresh, ingest, query, export, dashboard)
├── wigeon_recipe.yaml           # Goose recipe for conversational use
├── config.json                  # Your provider config (created by setup, gitignored)
├── config.example.json          # Example config for reference
├── pyproject.toml               # Project metadata
├── requirements.txt             # Python dependencies
│
├── scripts/
│   ├── wigeon_config.py         # Config management
│   ├── wigeon_processor.py      # Core processing engine
│   ├── database_schema.py       # SQLite schema and queries
│   ├── dashboard.py             # Terminal dashboard
│   ├── file_parser.py           # Multi-format file parser
│   └── exceptions.py            # Custom exceptions
│
├── automation/
│   ├── WigeonCollector.gs       # Google Apps Script (deploy to script.google.com)
│   └── wigeon-auto-ingest.yaml  # Goose recipe for automated ingestion
│
├── web-dashboard/
│   ├── index.html               # Dynamic web dashboard
│   └── dashboard-data.json      # Generated by: dashboard --export-json
│
├── database/                    # SQLite database (gitignored)
├── inbox/                       # Drop report files here (gitignored)
├── exports/                     # Exported data files (gitignored)
│
├── tests/
│   ├── conftest.py              # Shared test fixtures
│   ├── test_database_schema.py  # Database tests
│   ├── test_file_parser.py      # Parser tests
│   ├── test_wigeon_processor.py # Processor integration tests
│   └── test_wigeon_cli.py       # CLI tests
│
└── docs/
    └── USER_GUIDE.md            # Detailed user guide
```

---

## 🧪 Testing

```bash
pip install -r requirements-dev.txt
pytest
```

The test suite covers:
- Database schema creation and CRUD operations
- File parsing (CSV, Excel, XML, ZIP) with various formats
- End-to-end processing pipeline
- CLI argument parsing and command routing
- Edge cases (empty files, missing files, unsupported formats)

---

## 🔧 Configuration

WIGEON stores its configuration in `config.json` (created by `setup`):

```json
{
  "version": "2.0.0",
  "providers": [
    {
      "name": "Acme Logistics",
      "email": "reports@acme-logistics.com",
      "subject_filter": "",
      "description": "Daily warehouse reports"
    }
  ],
  "google_drive_folder_id": "",
  "google_drive_folder_name": "WIGEON_Reports",
  "inbox_dir": "inbox",
  "database_path": "database/wigeon.db",
  "retention": {
    "max_copies_per_report": 2,
    "days_to_search": 7
  }
}
```

- **providers** — Add as many as you need. Each has a name, email, optional subject filter, and description.
- **google_drive_folder_id** — Set this to the ID of your WIGEON_Reports Drive folder for automated workflows.
- **retention** — Controls how many copies of each report type the Apps Script keeps.

---

## 📊 Supported File Formats

| Format | Extensions | Notes |
|--------|-----------|-------|
| Excel | `.xlsx`, `.xlsm` | Multi-sheet support, date handling |
| Excel (legacy) | `.xls` | Requires `xlrd` |
| CSV | `.csv` | Auto-detects delimiter (comma, pipe, tab) |
| XML | `.xml` | Handles repeating elements and nested structures |
| ZIP | `.zip` | Recursively parses contained files |

---

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create a feature branch
3. Run tests: `pytest`
4. Submit a pull request

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🦆 Why "WIGEON"?

A [wigeon](https://en.wikipedia.org/wiki/Wigeon) is a duck known for its resourcefulness — it often feeds by taking food gathered by other birds. Similarly, WIGEON gathers data from reports that others send you, making it easy to access and analyze.

*Workflow Intelligence for Gathering Email-Originated Notifications*
