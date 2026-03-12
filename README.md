# 🦆 WIGEON

**Workflow Intelligence for Gathering Email-Originated Notifications**

[![CI](https://github.com/dsteffy85/wigeon/actions/workflows/ci.yml/badge.svg)](https://github.com/dsteffy85/wigeon/actions/workflows/ci.yml)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

WIGEON is a lightweight data integration agent that retrieves email reports from third-party vendors, parses multiple file formats, and consolidates everything into a queryable SQLite database.

---

## ✨ Features

- **Multi-format parsing** — Excel (`.xlsx`, `.xls`), CSV (comma/pipe/tab), XML, and ZIP archives
- **Auto-delimiter detection** — CSV files with commas, pipes, or tabs are handled automatically
- **Third-party tracking** — Tag every report with its source vendor for provenance
- **Flexible JSON storage** — Report data stored as JSON rows, so any schema works
- **CLI interface** — Six commands: `ingest`, `list`, `query`, `export`, `stats`, `dashboard`
- **Multiple export formats** — CSV, JSON, and Excel
- **Interactive dashboard** — Terminal-based report browser with search, filtering, and drill-down
- **Goose integration** — Use natural language to fetch and process reports via the Goose platform

---

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/dsteffy85/wigeon.git
cd wigeon

# Install dependencies
pip install -r requirements.txt
```

### Ingest a report

```bash
python3 wigeon.py ingest \
  --file samples/sales_report.xlsx \
  --third-party "Acme Corp" \
  --email vendor@acme.com
```

### Query the data

```bash
# List all reports
python3 wigeon.py list

# Query rows from a specific report
python3 wigeon.py query --report-id 1 --limit 20

# Export everything to CSV
python3 wigeon.py export --output data.csv --format csv

# Show database statistics
python3 wigeon.py stats

# Interactive dashboard
python3 wigeon.py dashboard --interactive
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     wigeon.py (CLI)                     │
│  ingest │ list │ query │ export │ stats │ dashboard     │
└────────────────────────┬────────────────────────────────┘
                         │
              ┌──────────▼──────────┐
              │  wigeon_processor   │  ← orchestrates parsing + storage
              └──────────┬──────────┘
                         │
          ┌──────────────┼──────────────┐
          ▼                             ▼
  ┌───────────────┐           ┌─────────────────┐
  │  file_parser  │           │ database_schema  │
  │               │           │                  │
  │  CSV  (.csv)  │           │  third_parties   │
  │  XLSX (.xlsx) │           │  reports         │
  │  XLS  (.xls)  │           │  report_data     │
  │  XML  (.xml)  │           │  (SQLite)        │
  │  ZIP  (.zip)  │           │                  │
  └───────────────┘           └─────────────────┘
```

**Data flow:** File → `FileParser.parse()` → `normalize_data()` → `WigeonDatabase.add_report_data()` → SQLite

---

## 📁 Project Structure

```
wigeon/
├── wigeon.py                   # CLI entry point (6 commands)
├── scripts/
│   ├── database_schema.py      # SQLite database management
│   ├── file_parser.py          # Multi-format file parser
│   ├── wigeon_processor.py     # Core processing engine
│   ├── dashboard.py            # Interactive terminal dashboard
│   └── exceptions.py           # Custom exception classes
├── tests/
│   ├── conftest.py             # Shared fixtures (temp DBs, sample files)
│   ├── test_file_parser.py     # 28 tests — CSV, XLSX, XML, ZIP, normalize
│   ├── test_database_schema.py # 29 tests — schema, CRUD, queries, stats
│   ├── test_wigeon_processor.py# 18 tests — end-to-end processing
│   └── test_wigeon_cli.py      # 23 tests — CLI args, subcommands
├── database/                   # SQLite database (auto-created, gitignored)
├── samples/                    # Sample data generators
├── docs/                       # Extended documentation
├── requirements.txt            # Production dependencies
├── requirements-dev.txt        # Dev dependencies (pytest, ruff)
├── pyproject.toml              # Project config, ruff + pytest settings
├── CONTRIBUTING.md             # Contributor guide
└── .github/workflows/ci.yml   # GitHub Actions CI (Python 3.9–3.12)
```

---

## 🧪 Testing

WIGEON has **98 automated tests** covering the parser, database, processor, and CLI:

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=scripts --cov-report=term-missing

# Run a specific test file
pytest tests/test_file_parser.py -v
```

| Module             | Tests | Coverage |
|--------------------|-------|----------|
| `database_schema`  | 29    | 93%      |
| `file_parser`      | 28    | 76%      |
| `wigeon_processor` | 18    | 71%      |
| CLI (`wigeon.py`)  | 23    | —        |

---

## 📖 CLI Reference

### `ingest` — Import a report file

```bash
python3 wigeon.py ingest \
  --file report.xlsx \
  --third-party "CEVA Logistics" \
  --email ops@example.com \
  --report-type "Inventory Snapshot" \
  --report-date 2026-03-01
```

### `list` — List ingested reports

```bash
python3 wigeon.py list
python3 wigeon.py list --third-party "CEVA Logistics" --status processed
```

### `query` — Query report data

```bash
python3 wigeon.py query --report-id 1 --limit 50
python3 wigeon.py query --third-party "Acme Corp" --format json
```

### `export` — Export data to file

```bash
python3 wigeon.py export --output data.csv --format csv
python3 wigeon.py export --output data.json --format json --third-party "CEVA"
python3 wigeon.py export --output data.xlsx --format excel
```

### `stats` — Database statistics

```bash
python3 wigeon.py stats
```

### `dashboard` — Interactive report browser

```bash
python3 wigeon.py dashboard                    # Full overview
python3 wigeon.py dashboard --interactive      # Menu-driven mode
python3 wigeon.py dashboard --recent 20        # Last 20 reports
python3 wigeon.py dashboard --search "CEVA"    # Search reports
python3 wigeon.py dashboard --days 30          # Last 30 days
```

---

## 🔌 Supported File Formats

| Format | Extensions        | Notes                                    |
|--------|-------------------|------------------------------------------|
| CSV    | `.csv`            | Auto-detects comma, pipe, tab delimiters |
| Excel  | `.xlsx`, `.xlsm`  | Multi-sheet support via openpyxl         |
| Excel  | `.xls`            | Legacy format via xlrd (optional)        |
| XML    | `.xml`            | Repeating elements → rows, attributes preserved |
| ZIP    | `.zip`            | Recursively parses contained files       |

---

## 🗄️ Database Schema

WIGEON uses SQLite with three tables:

- **`third_parties`** — Vendor registry (name, email, metadata)
- **`reports`** — Report tracking (file, type, date, status, row count)
- **`report_data`** — Actual data rows stored as flexible JSON

```sql
-- Direct SQL access
sqlite3 database/wigeon.db

-- Example queries
SELECT * FROM reports ORDER BY created_at DESC LIMIT 10;
SELECT COUNT(*) FROM report_data WHERE report_id = 1;
```

---

## 🤖 Goose Integration

WIGEON works as a [Goose](https://github.com/block/goose) agent. Just ask naturally:

```
"Use WIGEON to ingest the sales report from Acme Corp"
"Show me all CEVA reports from the last 7 days"
"Export WIGEON data to CSV"
```

See `wigeon_recipe.yaml` for the Goose recipe definition.

---

## 🛠️ Development

```bash
# Lint
ruff check scripts/ wigeon.py tests/

# Format
ruff format scripts/ wigeon.py tests/

# Run tests with coverage
pytest --cov=scripts --cov-report=term-missing
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full contributor guide.

---

## 📜 License

MIT

---

## 🦆 Why "WIGEON"?

**W**orkflow **I**ntelligence for **G**athering **E**mail-**O**riginated **N**otifications.

Wigeons are social ducks that forage in groups — just like WIGEON consolidates data from multiple sources into one place.
