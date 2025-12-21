# 📦 Database Schema Management with Prisma

This project uses **Prisma** for database schema management, type-safe database access, and migrations.

---

## 🛠️ Setup

1. **Install Prisma CLI**:

```bash
npm install -g prisma
# or using your preferred package manager
```

2. **Install dependencies**:

```bash
cd schema
pnpm install
```

3. **Set up environment variables**:
   Make sure your `DATABASE_URL` is properly configured in your environment:

```bash
export DATABASE_URL="postgresql://username:password@localhost:5432/your_database"
```

4. **Generate Prisma Client**:

```bash
cd schema
pnpm exec prisma generate
```

---

## 🚀 Common Commands

### Generate Prisma Client (after schema changes)

```bash
cd schema
pnpm exec prisma generate
```

### Create and apply migrations

```bash
cd schema
# Create a new migration
pnpm exec prisma migrate dev --name "description_of_changes"

# Apply migrations to production
pnpm exec prisma migrate deploy
```

### Database introspection (sync schema with existing DB)

```bash
cd schema
pnpm exec prisma db pull
```

### Push schema changes without migrations (for development)

```bash
cd schema
pnpm exec prisma db push
```

### Reset database (careful in production!)

```bash
cd schema
pnpm exec prisma migrate reset
```

### Open Prisma Studio (database GUI)

```bash
cd schema
pnpm exec prisma studio
```

---

## 📊 Database Models

This schema includes the following models:

### Core Business Models
- **Company** - Comprehensive company data with financial information (2018-2023)
- **Leader** - Company leadership and management information

### Reference Data Models
- **City** - City reference data for autocomplete
- **IndustrySector** - Industry sector classifications
- **LegalForm** - Legal form types
- **Region** - Geographic regions

### User Management Models
- **UserCompanyStatus** - User interaction tracking with companies
- **UserQuota** - User quota management system

### Configuration Models
- **AppSettings** - System configuration settings

---

## 🧠 Migration from Alembic

This project has been migrated from SQLAlchemy + Alembic to Prisma. Key benefits:

- **Type Safety**: Auto-generated, fully typed database client
- **Better DX**: Intuitive query API and excellent IntelliSense
- **Database GUI**: Built-in Prisma Studio for data exploration
- **Migration Management**: Robust migration system with rollback support
- **Multi-language Support**: Works with JavaScript, TypeScript, Python, and more
- **I don't like Python**: I understand Python but I don't like it and I prefer TypeScript

### Key Changes:
- All SQLAlchemy models converted to Prisma schema
- Preserved all existing indexes and constraints
- Maintained database compatibility (same table names and structure)
- Enhanced with proper relations between models

---

## 🧭 Tips

- **Always run `prisma generate`** after modifying the schema file
- **Use `prisma migrate dev`** during development for schema changes
- **Use `prisma migrate deploy`** for production deployments
- **Backup your database** before running `prisma migrate reset`
- **Check the generated client** in `./generated/prisma` for available methods
- **Use Prisma Studio** (`prisma studio`) for easy data visualization and editing
- **Make sure the correct `DATABASE_URL` is set** in your environment variables

---

## 📚 Useful Resources

- [Prisma Documentation](https://www.prisma.io/docs)
- [Prisma Schema Reference](https://www.prisma.io/docs/reference/api-reference/prisma-schema-reference)
- [Prisma Client API Reference](https://www.prisma.io/docs/reference/api-reference/prisma-client-reference)
- [Migration Guide](https://www.prisma.io/docs/guides/migrate-to-prisma)
