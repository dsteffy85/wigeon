# Contributing to WIGEON

Thanks for your interest in contributing! 🦆

## Getting Started

```bash
git clone https://github.com/dsteffy85/wigeon.git
cd wigeon
pip install -r requirements-dev.txt
```

## Running Tests

```bash
pytest
pytest --cov=scripts  # with coverage
```

## Code Style

We use [Ruff](https://docs.astral.sh/ruff/) for linting and formatting:

```bash
ruff check .
ruff format .
```

## Project Structure

- `wigeon.py` — Main CLI entry point
- `scripts/` — Core modules (processor, database, parser, config, dashboard)
- `tests/` — Test suite (pytest)
- `automation/` — Google Apps Script and Goose recipes
- `web-dashboard/` — Browser-based dashboard

## How to Contribute

1. **Fork** the repository
2. **Create a branch** for your feature or fix
3. **Write tests** for new functionality
4. **Run the test suite** to make sure everything passes
5. **Submit a pull request** with a clear description

## Ideas for Contributions

- Additional file format parsers (PDF tables, Parquet, etc.)
- Enhanced web dashboard features (charts, date range filters)
- Notification integrations (Slack, email alerts)
- Data deduplication and validation rules
- Scheduled ingestion improvements
- Documentation improvements

## Reporting Issues

Please open a GitHub issue with:
- What you expected to happen
- What actually happened
- Steps to reproduce
- Your Python version and OS
