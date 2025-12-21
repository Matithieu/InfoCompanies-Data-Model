#!/bin/bash

# Backup script for old seed system
# Run this before adopting the new architecture

echo "🔄 Backing up old seed system..."

# Create backup directory
BACKUP_DIR="./old-seed-backup-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Backup old seed.ts if it exists
if [ -f "./seed.ts" ]; then
    echo "📦 Backing up seed.ts..."
    cp "./seed.ts" "$BACKUP_DIR/"
fi

# Backup business directory if it exists
if [ -d "./business" ]; then
    echo "📦 Backing up business directory..."
    cp -r "./business" "$BACKUP_DIR/"
fi

# Create a migration checklist
cat > "$BACKUP_DIR/MIGRATION_CHECKLIST.md" << 'EOF'
# Migration Checklist

## Before Migration
- [ ] Backup completed successfully
- [ ] Current seed system is working
- [ ] Database is accessible

## During Migration
- [ ] New dependencies installed (`@types/jest`, `jest`, `ts-jest`)
- [ ] New scripts added to package.json
- [ ] Jest configuration created
- [ ] TypeScript configuration updated

## After Migration
- [ ] New seed system runs successfully (`pnpm run seed:test`)
- [ ] Tests pass (`pnpm test`)
- [ ] Data quality verified
- [ ] Team trained on new commands

## Rollback (if needed)
- [ ] Restore files from this backup directory
- [ ] Revert package.json changes
- [ ] Remove new dependencies
EOF

echo "✅ Backup completed in: $BACKUP_DIR"
echo "📋 Check the migration checklist in: $BACKUP_DIR/MIGRATION_CHECKLIST.md"
echo ""
echo "Next steps:"
echo "1. Review the new architecture in the current directory"
echo "2. Test the new system: pnpm run seed:test"
echo "3. Run tests: pnpm test"
echo "4. Follow the MIGRATION_GUIDE.md for detailed steps"
