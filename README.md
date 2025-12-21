# InfoCompanies Data Model

This repository manages the **InfoCompanies** project's data model and database operations. It provides a complete workflow for company data using a Dockerized PostgreSQL database and modern schema management with Prisma.

## 🚀 Main Features

- **Dockerized PostgreSQL**: Easy local setup with persistent volumes and PgAdmin UI.
- **Data Enrichment**: Python scripts for scraping and loading company data.
- **Modern Schema Management**: Prisma ORM with type-safe database access and robust migrations.
- **Automated Data Loading**: Bash scripts to orchestrate pulling, unzipping, and importing CSVs into the database.
- **Backup & Restore**: Tools for SQL/CSV backup and restore, including gzip support.
- **Autocomplete Support**: Extraction and indexing of unique values for fast autocomplete APIs.
- **Database GUI**: Built-in Prisma Studio for visual database exploration and management.
- **Type Safety**: Auto-generated, fully typed database client for multiple languages.
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

### 3. Install Dependencies

#### For Prisma (Database ORM)

See [schema/README.md](schema/README.md) for detailed Prisma setup.

#### For Python Scripts (Data Processing)
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

#### Set up Prisma and generate client
```bash
cd schema
prisma generate
prisma db push  # Push schema to database
```

#### Run the main orchestration script
```bash
./db.sh
```

This will:
- Start Docker containers
- Set up database schema with Prisma
- Load CSVs from the ETL
- Shut down containers

#### Optional: Open Prisma Studio (Database GUI)
```bash
cd schema
pnpm exec prisma studio
```

---

## 🧩 Key Components

### Database Schema

- **Prisma Schema**: Modern database schema defined in [schema/prisma/schema.prisma](schema/prisma/schema.prisma)
- **Model Documentation**: Individual model references in [schema/prisma/models/](schema/prisma/models/)
- **Type-Safe Client**: Auto-generated Prisma Client for database operations
- **Migration System**: Robust schema versioning and migration management

### Database Models

- **Company**: Comprehensive business data with financial information (2018-2023)
- **Leader**: Company leadership and management information  
- **Autocomplete Models**: City, Industry Sector, Legal Form, Region reference data
- **User Management**: User quotas and company interaction tracking
- **Configuration**: System settings and configuration data

### Parsing

- Web scraping and data enrichment in [parsing/parsing.py](parsing/parsing.py) and [parsing/parsing_request.py](parsing/parsing_request.py)
- Loads and updates company info from Google and other sources

### Data Operations

- **Database Management**: Prisma CLI commands for schema and data management
- **Backup/Restore**: [scripts/backup.sh](scripts/backup.sh)
- **CSV Transfer**: [scripts/util.sh](scripts/util.sh)
- **Data Loading**: [scripts/load-csv-to-database.sh](scripts/load-csv-to-database.sh)
- **Database GUI**: Prisma Studio for visual data exploration and editing

### Development Tools

- **Prisma Studio**: Visual database browser and editor (`prisma studio`)
- **Type Generation**: Auto-generated type-safe database client
- **Schema Validation**: Built-in schema validation and error checking
- **Migration Management**: Version-controlled database schema evolution

### CI/CD

- Linting, formatting, and build checks in [.github/workflows/action.yml](.github/workflows/action.yml)

---

## 📚 Documentation

- [README.md](README.md): Main usage and features
- [schema/README.md](schema/README.md): Prisma schema management and migration guide
- [schema/prisma/models/README.md](schema/prisma/models/README.md): Database models overview
- [docs/AUTOCOMPLETE.md](docs/AUTOCOMPLETE.md): How to add autocomplete support

## 🚀 Quick Start Commands

```bash
# Start database services
docker compose up -d

# Generate Prisma client (after schema changes)
cd schema && pnpm exec prisma generate

# Push schema to database (development)
cd schema && pnpm exec prisma db push

# Create and apply migrations (production)
cd schema && pnpm exec prisma migrate dev --name "your_migration_name"

# Open database GUI
cd schema && pnpm exec prisma studio

# Load data
./db.sh
```

## 📝 Notes

- All scripts assume a Unix-like environment and require Docker.
- Data files (`.csv`, `.dump`, etc.) are git-ignored by default.
- For troubleshooting, check logs in the output pane or use `docker logs`.
- **Prisma Client**: Generated client is located in `schema/generated/prisma/`
- **Environment**: Ensure `DATABASE_URL` is properly configured in your `.env` file
- **Development**: Use `pnpm exec prisma db push` for quick schema changes, `pnpm exec prisma migrate dev` for production-ready migrations
