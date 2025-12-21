# Migration Guide: Old Seed System → New Clean Architecture

This guide helps you migrate from the old seeding system to the new clean architecture.

## Overview of Changes

### What Changed

1. **File Structure**: Organized into logical folders (types, core, factories, seeders)
2. **Architecture**: Implemented clean architecture with dependency injection
3. **Configuration**: Environment-specific configurations
4. **Testing**: Comprehensive test suite with unit and integration tests
5. **Error Handling**: Better error handling and reporting
6. **Performance**: Batch processing and optimized database operations

### What Stayed the Same

- The generated data quality and realism
- The underlying Prisma schema
- The basic seeding functionality

## File Mapping

### Old Structure → New Structure

```
Old:
├── seed.ts                    → index.ts
├── business/
│   ├── companies.ts          → factories/CompanyFactory.ts + seeders/CompanySeeder.ts
│   ├── config.ts             → seeders/ConfigSeeder.ts
│   ├── leaders.ts            → (removed for now, can be added later)
│   ├── userCompanyStatus.ts  → (removed for now, can be added later)
│   └── userQuota.ts          → (removed for now, can be added later)
├── reference/
│   └── referenceData.ts      → factories/ReferenceDataFactory.ts + seeders/ReferenceDataSeeder.ts
└── utils/                    → utils/ (preserved)

New:
├── index.ts                  # Main entry point
├── types/                    # TypeScript interfaces
├── core/                     # Core services
├── factories/                # Data factories
├── seeders/                  # Database seeders
├── config/                   # Environment configurations
├── reference/                # Static reference data (preserved)
├── utils/                    # Utility functions (preserved)
└── __tests__/                # Test suite
```

## Code Migration

### Old Seed Script

```typescript
// OLD: Direct execution in seed.ts
const companies = []
for (let i = 0; i < numberOfCompanies; i++) {
  const company = generateCompany()
  companies.push(company)
}
await prisma.company.createMany({ data: companies })
```

### New Seed Script

```typescript
// NEW: Using SeedService and factories
const seedService = new SeedService(prisma)
seedService
  .register(new ReferenceDataSeeder(prisma))
  .register(new CompanySeeder(prisma))

await seedService.seed({
  numberOfCompanies: 100,
  verbose: true
})
```

### Factory Pattern Migration

```typescript
// OLD: Direct generation function
export function generateCompany(): Company {
  return {
    company_name: generateRealisticCompanyName(),
    siren_number: generateSirenNumber(),
    // ... other fields
  }
}

// NEW: Factory class
export class CompanyFactory extends BaseFactory<CompanyCreateInput> {
  create(overrides?: Partial<CompanyCreateInput>): CompanyCreateInput {
    const defaults = {
      company_name: generateRealisticCompanyName(),
      siren_number: generateSirenNumber(),
      // ... other fields
    }
    return this.mergeOverrides(defaults, overrides)
  }
}
```

## Command Changes

### Old Commands

```bash
# Old way
pnpm run run:seed
```

### New Commands

```bash
# New ways - environment specific
pnpm run seed:dev     # Development environment
pnpm run seed:test    # Test environment  
pnpm run seed:prod    # Production environment
pnpm run seed         # Uses NODE_ENV

# Testing
pnpm test             # Run all tests
pnpm test:seed        # Run only seed tests
pnpm test:coverage    # Run with coverage
```

## Configuration Migration

### Old Configuration

```typescript
// OLD: Hardcoded values in seed.ts
const numberOfCompanies = 100
const isActive = faker.datatype.boolean(0.9)
```

### New Configuration

```typescript
// NEW: Environment-specific configurations
import { getEnvironmentConfig } from './config/environments'

const config = getEnvironmentConfig('development')
// config.numberOfCompanies = 100
// config.verbose = true
// config.clearExistingData = true
```

## Testing Migration

### Before: No Tests

The old system had no automated tests.

### After: Comprehensive Testing

```bash
# Run all tests
pnpm test

# Test specific components
pnpm test CompanyFactory
pnpm test SeedService
pnpm test integration
```

## Breaking Changes

### 1. Import Changes

```typescript
// OLD
import { generateCompany } from './business/companies'
import { generateConfig } from './business/config'

// NEW
import { CompanyFactory } from './factories/CompanyFactory'
import { ConfigSeeder } from './seeders/ConfigSeeder'
```

### 2. Function Signatures

```typescript
// OLD
generateCompany(): Company

// NEW
const factory = new CompanyFactory()
factory.create(): CompanyCreateInput
factory.create({ company_name: 'Override' }): CompanyCreateInput
factory.createWithProfile({ size: 'large' }): CompanyCreateInput
```

### 3. Database Operations

```typescript
// OLD: Direct Prisma calls in main seed file
await prisma.company.createMany({ data: companies })

// NEW: Encapsulated in seeders
const seeder = new CompanySeeder(prisma)
const companies = await seeder.seed(config)
```

## Migration Steps

### Step 1: Backup

```bash
# Backup your current seed directory
cp -r prisma/seed prisma/seed.backup
```

### Step 2: Install New Dependencies

```bash
pnpm install @types/jest jest ts-jest
```

### Step 3: Update Scripts

Update your `package.json` scripts:

```json
{
  "scripts": {
    "seed": "pnpm exec tsx prisma/seed/index.ts",
    "seed:dev": "NODE_ENV=development pnpm exec tsx prisma/seed/index.ts",
    "seed:test": "NODE_ENV=test pnpm exec tsx prisma/seed/index.ts",
    "test": "jest",
    "test:seed": "NODE_ENV=test jest --testPathPattern=seed"
  }
}
```

### Step 4: Migrate Custom Logic

If you have custom seeding logic, migrate it to the new system:

1. **Custom Data Generation**: Move to factories
2. **Custom Database Logic**: Move to seeders
3. **Configuration**: Move to `config/environments.ts`

### Step 5: Test Migration

```bash
# Test the new system
pnpm run seed:test

# Run tests
pnpm test

# Verify data quality
pnpm run seed:dev
# Check database manually
```

## Custom Extensions

### Adding New Seeders

```typescript
// 1. Create factory
export class MyEntityFactory extends BaseFactory<MyEntity> {
  create(overrides?: Partial<MyEntity>): MyEntity {
    // Implementation
  }
}

// 2. Create seeder
export class MyEntitySeeder extends BaseSeeder<MyEntity> {
  constructor(prisma: PrismaClient) {
    super('MyEntity', prisma)
  }

  async seed(config: SeedConfig): Promise<MyEntity[]> {
    // Implementation
  }

  async clear(): Promise<void> {
    await this.prisma.myEntity.deleteMany()
  }

  async count(): Promise<number> {
    return this.prisma.myEntity.count()
  }
}

// 3. Register in main seed file
seedService.register(new MyEntitySeeder(prisma))
```

### Custom Configurations

```typescript
// Add to config/environments.ts
export const STAGING_CONFIG: SeedConfig = {
  numberOfCompanies: 500,
  numberOfUsers: 100,
  generateTestData: false,
  clearExistingData: true,
  verbose: false,
}
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Update import paths to new structure
2. **Type Errors**: Ensure Prisma types are correctly imported
3. **Test Failures**: Set up test database connection
4. **Performance**: Use batch processing for large datasets

### Getting Help

1. Check the comprehensive README.md
2. Look at test files for usage examples
3. Review the factory and seeder implementations
4. Check TypeScript types in the types/ directory

## Rollback Plan

If you need to rollback:

```bash
# Restore backup
rm -rf prisma/seed
mv prisma/seed.backup prisma/seed

# Restore old package.json scripts
git checkout package.json
```

## Benefits of Migration

1. **Better Testing**: Comprehensive test coverage
2. **Better Maintainability**: Clean architecture with separation of concerns
3. **Better Performance**: Optimized database operations
4. **Better Configuration**: Environment-specific settings
5. **Better Error Handling**: Detailed error reporting
6. **Better Documentation**: Comprehensive guides and API docs
7. **Better Extensibility**: Easy to add new seeders and factories

## Next Steps

After migration:

1. Run the test suite to ensure everything works
2. Customize configurations for your environments
3. Add any missing seeders for your specific needs
4. Set up CI/CD integration with the new test commands
5. Train your team on the new architecture
