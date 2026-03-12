# Contributing to WIGEON 🦆

Thank you for your interest in contributing to WIGEON! This guide will help you get started.

## Getting Started

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git

### Development Setup

```bash
# Clone the repository
git clone https://github.com/dsteffy85/wigeon.git
cd wigeon

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Install production dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=scripts --cov-report=term-missing

# Run a specific test file
pytest tests/test_file_parser.py -v

# Run a specific test
pytest tests/test_file_parser.py::TestCSVParser::test_parse_simple_csv -v
```

### Linting

We use [ruff](https://github.com/astral-sh/ruff) for linting and formatting:

```bash
# Check for lint issues
ruff check scripts/ wigeon.py tests/

# Auto-fix lint issues
ruff check --fix scripts/ wigeon.py tests/

# Check formatting
ruff format --check scripts/ wigeon.py tests/

# Auto-format
ruff format scripts/ wigeon.py tests/
```

## Project Structure

```
wigeon/
├── wigeon.py                 # CLI entry point
├── scripts/
│   ├── database_schema.py    # SQLite database management
│   ├── file_parser.py        # Multi-format file parser
│   ├── wigeon_processor.py   # Core processing engine
│   ├── dashboard.py          # Interactive dashboard
│   └── exceptions.py         # Custom exception classes
├── tests/
│   ├── conftest.py           # Shared test fixtures
│   ├── test_file_parser.py   # Parser unit tests
│   ├── test_database_schema.py # Database unit tests
│   ├── test_wigeon_processor.py # Processor integration tests
│   └── test_wigeon_cli.py    # CLI tests
├── database/                 # SQLite database (auto-created)
├── samples/                  # Sample data for testing
├── docs/                     # Documentation
├── requirements.txt          # Production dependencies
├── requirements-dev.txt      # Development dependencies
└── pyproject.toml            # Project configuration
```

## How to Contribute

### Reporting Bugs

1. Check if the issue already exists in [GitHub Issues](https://github.com/dsteffy85/wigeon/issues)
2. Create a new issue with:
   - Clear title describing the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - Python version and OS
   - Sample file (if applicable, with sensitive data removed)

### Suggesting Features

1. Open a [GitHub Issue](https://github.com/dsteffy85/wigeon/issues) with the "enhancement" label
2. Describe the use case and expected behavior
3. Explain why this would be useful to other users

### Submitting Code

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass: `pytest tests/ -v`
6. Ensure linting passes: `ruff check scripts/ wigeon.py tests/`
7. Commit with a descriptive message: `git commit -m "Add CSV delimiter auto-detection"`
8. Push to your fork: `git push origin feature/my-feature`
9. Open a Pull Request

### Code Style

- Follow PEP 8 conventions (enforced by ruff)
- Add type hints to all function signatures
- Write docstrings for all public functions and classes
- Keep functions focused and under 50 lines where possible
- Use descriptive variable names

### Adding a New File Parser

To add support for a new file format:

1. Add the parsing method to `scripts/file_parser.py`:
   ```python
   def parse_newformat(self) -> dict:
       """Parse .newformat file"""
       # Return standardized dict with 'format', 'sheets'/'rows', counts
   ```

2. Register the format in `FileParser.parse()`:
   ```python
   elif self.file_format == '.newformat':
       return self.parse_newformat()
   ```

3. Add normalization support in `normalize_data()` if needed

4. Add tests in `tests/test_file_parser.py`

5. Update the README with the new supported format

### Adding a New CLI Command

1. Add the command handler in `wigeon.py`:
   ```python
   def cmd_newcommand(args):
       """Description of new command"""
       # Implementation
   ```

2. Add the subparser in `main()`:
   ```python
   new_parser = subparsers.add_parser('newcommand', help='Description')
   new_parser.add_argument('--flag', help='Flag description')
   ```

3. Add routing in the command dispatcher

4. Add tests in `tests/test_wigeon_cli.py`

## Testing Guidelines

- Every new feature should include tests
- Every bug fix should include a regression test
- Use fixtures from `conftest.py` for common setup
- Test both success and error paths
- Use temporary directories/databases for isolation

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

## Questions?

Open an issue or reach out — we're happy to help you get started! 🦆
