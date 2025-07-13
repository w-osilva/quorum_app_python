# Quorum App (Python/Flask)

A Flask + SQLAlchemy web app for managing and displaying legislative data from CSV files. 

## Context

This project is a python implementation of a previous [Ruby on Rails challenge](https://github.com/w-osilva/quorum-app) that I completed last year. 

The full challenge description and requirements can be found in the [docs/challenge.md](docs/challenge.md) file.

I have also included the [docs/questions.md](docs/questions.md) file with details about my implementation strategy, decisions, and answers to the challenge questions.

---

## Prerequisites

- Python 3.8+ (tested with Python 3.13)
- pip (Python package installer)

---

## Quick Start

### 1. Clone & Enter Project

```bash
git clone <repo-url>
cd quorum_app_python
```

### 2. Create Virtual Environment

```bash
# On Linux
python -m venv .venv && source .venv/bin/activate

# On Windows
# python -m venv .venv && source .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
make install
```

### 4. Set Up Database & Import Data

```bash
make db-create && make db-import
```

### 5. Run the App

```bash
make server
```

- Web: [http://localhost:8000/](http://localhost:8000/)

---

## Development

### Available Make Commands

```bash
make help            # Show all available commands
make install         # Install production and development dependencies
make install-dev     # Install development dependencies
make lint            # Run Ruff linter on Python code
make lint-templates  # Run djlint on HTML templates
make lint-fix        # Auto-fix code formatting and linting issues
make lint-check      # Run all checks (lint + format check)
make test            # Run tests
make test-cov        # Run tests with coverage
make clean           # Clean up build artifacts
make ci              # Run full CI pipeline
make db-create       # Create database tables
make db-drop         # Drop database tables
make db-reset        # Drop and recreate all tables
make db-import       # Import data from CSV files
make server          # Run Flask webserver   
```

---

## Troubleshooting

### Database Issues
If you need to reset the database:
```bash
make db-reset && make db-import
```

Or use the database management script directly:
```bash
python scripts/database.py reset --with-data    # Reset and import data in one command
python scripts/database.py drop legislators    # Drop specific table
python scripts/database.py create bills votes  # Create specific tables
```

### Virtual Environment Issues
Make sure you're using the correct virtual environment:
```bash
which python  # Should point to your .venv/bin/python
pip list      # Should show the installed packages
```

---

## Project Structure

```
quorum-app-python/
├── app/                     # Main application
│   ├── __init__.py          # Flask app factory
│   ├── constants/           # Application constants
│   ├── helpers/             # Helper utilities
│   ├── lib/                 # Shared libraries
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── routes/              # Flask blueprints
│   ├── services/            # Business logic
│   │   └── importers/       # CSV import services
│   ├── templates/           # Jinja2 HTML templates
│   └── static/              # CSS files
├── data/                    # CSV data files + SQLite DB
├── docs/                    # Documentation
├── scripts/                 # Utility scripts
│   ├── database.py          # Database management CLI
│   └── import_data.py       # CSV data importer
├── settings/                # Environment configurations
├── tests/                   # Test suite (mirrors app structure)
│   ├── conftest.py          # Pytest configuration
│   └── app/                 # Application tests
│       ├── models/          # Model tests
│       ├── routes/          # Route/API tests
│       ├── schemas/         # Schema validation tests
│       └── services/        # Service tests
├── .gitignore               # Git ignore rules
├── Makefile                 # Development commands
├── pyproject.toml           # Project configuration & dependencies
├── pytest.ini               # Pytest configuration
├── server.py                # Application entry point
└── README.md
```

---

## Technology Stack

- **Framework:** Flask 2.3+
- **Database:** SQLAlchemy 2.0+ with SQLite
- **Validation:** Pydantic 2.0+
- **Testing:** pytest with coverage
- **Code Quality:** Ruff (linting + formatting)
- **Template Linting:** djlint
- **Content Negotiation:** Custom multi-format responses (HTML/JSON/CSV)

---

## Features

### Multi-Format API
All endpoints support multiple output formats:
- **HTML:** Default web interface
- **JSON:** Add `?format=json` or `Accept: application/json`
- **CSV:** Add `?format=csv` or `Accept: text/csv`

### Data Management
- Import legislative data from CSV files
- Automatic database schema creation  
- Relationship mapping between entities
- Database management CLI with table-specific operations
- Support for creating, dropping, and resetting individual tables

### Web Interface
- Browse legislators, bills, votes, and vote results
- Clean, responsive design with PureCSS
- Easy navigation between related entities

---

## License

Part of the Quorum code challenge. 