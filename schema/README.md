

# 📦 Database Migrations with Alembic

This project uses **Alembic** for managing SQLAlchemy schema migrations.

---

## 📁 Directory structure

```
InfoCompanies-Data-Model/
├── app/
│   ├── models/
│   │   └── company.py          # Your model(s)
├── schema/
│   └── alembic/                # Alembic config and migrations
│       └── env.py              # Configure metadata here
│       └── database.py         # Init the database
```

---

## 🛠️ Setup

1. **Install dependencies**:

```bash
pip install alembic psycopg2-binary
```

2. **Initialize Alembic** (only needed once):

```bash
cd schema
alembic upgrade head
PYTHONPATH=. python3 app/database/database.py
```

3. **Edit `alembic/env.py`** to link Alembic to your models:

```python
# At the top of env.py
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from app.db.database import Base
from app.models import company  # force model import

# Then set:
target_metadata = Base.metadata
```

---

## 🚀 Common Commands

### Create a new migration (auto-generate)

```bash
cd schema
alembic revision --autogenerate -m "add company model"
```

### Apply migrations (upgrade database)

```bash
alembic upgrade head
```

### Downgrade (undo last migration)

```bash
alembic downgrade -1
```

---

## 🧠 Tips

- Always **import all models** before running `alembic revision --autogenerate`, or Alembic won’t detect them.
- Make sure the correct `DATABASE_URL` is set in your `database.py`.