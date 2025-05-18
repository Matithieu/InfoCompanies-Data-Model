# InfoCompanies Data Model

This repository manages the **InfoCompanies** project's data model, and database operations. It provides a complete workflow for company data using a Dockerized PostgreSQL database and robust migration/versioning with Alembic.

---

## 🗂️ Repository Structure

```
.
├── db.sh                      # Main orchestration script for DB setup and data loading
├── docker-compose.yml         # Docker services for PostgreSQL and PgAdmin
├── requirements-dev.in        # Python dependencies for DB scripts
├── README.md                  # Main usage and feature documentation
├── template.env               # Example environment variables
├── parsing/                   # Python scripts for web scraping and data enrichment
├── scripts/                   # Shell and Python scripts for data loading, backup, export, etc.
├── schema/                    # Database schema, Alembic migrations, and SQLAlchemy models
│   ├── alembic/               # Alembic migration scripts and config
│   └── app/                   # SQLAlchemy models and DB initialization
├── data/                      # Data exports, backups, and E2E test datasets
├── config/                    # PgAdmin configuration
├── docs/                      # Additional documentation (e.g., autocomplete guide)
└── .github/                   # CI/CD workflows
```

---

## 🚀 Main Features

- **Dockerized PostgreSQL**: Easy local setup with persistent volumes and PgAdmin UI.
- **Data Enrichment**: Python scripts for scraping and loading company data.
- **Database Schema Management**: SQLAlchemy models and Alembic migrations for versioned schema evolution.
- **Automated Data Loading**: Bash scripts to orchestrate pulling, unzipping, and importing CSVs into the database.
- **Backup & Restore**: Tools for SQL/CSV backup and restore, including gzip support.
- **Export for E2E Testing**: Export minimal datasets for integration/E2E tests.
- **Autocomplete Support**: Extraction and indexing of unique values for fast autocomplete APIs.
- **CI/CD**: GitHub Actions for linting, formatting, and build validation.

---

## 🛠️ Getting Started

### 1. Clone the Repository

```bash
git clone <repo-url>
cd InfoCompanies-Data-Model
```

### 2. Configure Environment

Copy and edit `.env` from `template.env`:

```bash
cp template.env .env
```

### 3. Install Python Dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.in
```

### 4. Start Database Services

```bash
docker compose up -d
```

### 5. Initialize Database & Load Data

Run the main orchestration script:

```bash
./db.sh
```

This will:
- Start Docker containers
- Run Alembic migrations
- Load CSVs from the ETL
- Export E2E datasets
- Shut down containers

---

## 🧩 Key Components

### Database Schema

- Defined in [schema/app/models/](schema/app/models/)
- Managed and versioned with Alembic ([schema/alembic/](schema/alembic/))

### Parsing

- Web scraping and data enrichment in [parsing/parsing.py](parsing/parsing.py) and [parsing/parsing_request.py](parsing/parsing_request.py)
- Loads and updates company info from Google and other sources

### Data Operations

- **Backup/Restore**: [scripts/backup.sh](scripts/backup.sh)
- **CSV Transfer**: [scripts/util.sh](scripts/util.sh)
- **Data Loading**: [scripts/load-csv-to-database.sh](scripts/load-csv-to-database.sh)
- **E2E Export**: [scripts/export-e2e-data.sh](scripts/export-e2e-data.sh)

### CI/CD

- Linting, formatting, and build checks in [.github/workflows/action.yml](.github/workflows/action.yml)

---

## 📚 Documentation

- [README.md](README.md): Main usage and features
- [schema/README.md](schema/README.md): Alembic and schema management
- [docs/AUTOCOMPLETE.md](docs/AUTOCOMPLETE.md): How to add autocomplete support

---

## 📝 Notes

- All scripts assume a Unix-like environment and require Docker.
- Data files (`.csv`, `.dump`, etc.) are git-ignored by default.
- For troubleshooting, check logs in the output pane or use `docker logs`.
