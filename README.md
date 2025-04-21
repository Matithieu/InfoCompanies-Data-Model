# InfoCompanies Database Management Script

This Bash script is used to manage database operations for the **InfoCompanies** project using a **Dockerized PostgreSQL** instance. It supports backups, data insertion, exports, CSV transfers, and more.

---

## 🧰 Features

- Database backup (to `SQL` or `CSV`)
- Data insertion from Python ETL scripts
- Export unique values using custom SQL queries
- Create simple, composite, or trigram indexes
- Transfer CSV data into the database
- Export and import data for end-to-end (E2E) testing
- Load existing SQL or CSV backups

---

## 🚀 Requirements

- Docker (with a running PostgreSQL container)
- Python 3 with required ETL dependencies
- `sudo` access (needed for some file operations)

---

## 🧪 Usage

### Syntax:

```bash
./infocompanies_db.sh <command> [options]
```

### Available Commands:

- **backup**: Backup the database to an SQL or CSV file.
- **insert**: Run Python ETL scripts and insert data into the database.
- **export**: Export specific data from the database using a custom SQL query.
- **index**: Create database indexes (simple, composite, or trigram).
- **transfer**: Import a CSV file into the specified database table.
- **export-e2e**: Export minimal data for end-to-end testing.
- **import-e2e**: Import a previously exported E2E dataset.
- **load**: Load a backup file into the database.

---

### 📂 Examples

```bash
# Backup the database to SQL
./infocompanies_db.sh backup

# Insert data using ETL scripts
./infocompanies_db.sh insert

# Export unique values from a column
./infocompanies_db.sh export "SELECT DISTINCT sector FROM companies"

# Create a trigram index
./infocompanies_db.sh index trigram name

# Transfer CSV data into a table
./infocompanies_db.sh transfer companies.csv companies

# Export a lightweight E2E dataset
./infocompanies_db.sh export-e2e

# Import the E2E dataset
./infocompanies_db.sh import-e2e

# Load a previous SQL or CSV backup
./infocompanies_db.sh load path/to/backup.sql
```

---

### 📝 Notes

- Make sure the Docker container is running and the database is accessible.
- Customize the script to fit your database name, user, or container settings if necessary.
- For E2E testing, only minimal required data is handled to keep tests lightweight.

---

## 🌱 Environment Configuration

To configure the environment, ensure the following:

1. **Docker**: Install Docker and ensure the PostgreSQL container is running.
2. **Python Dependencies**: Install required Python dependencies for ETL scripts:
  ```bash
  pip install -r requirements.txt
  ```
3. **Script Permissions**: Make the script executable:
  ```bash
  chmod +x infocompanies_db.sh
  ```

