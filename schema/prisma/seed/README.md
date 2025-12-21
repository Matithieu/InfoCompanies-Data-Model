# Database Seeding System

A clean, modular, and well-tested database seeding system for the InfoCompanies project.

## Overview

This seeding system provides a robust architecture for generating realistic test data for development, testing, and production environments. It follows clean architecture principles with clear separation of concerns, dependency injection, and comprehensive testing.

## Architecture

### Core Components

```
seed/
├── types/              # TypeScript interfaces and types
├── core/               # Core services and orchestration
├── factories/          # Data factories for creating entities
├── seeders/           # Individual data seeders
├── reference/         # Static reference data
├── utils/             # Utility functions
└── __tests__/         # Comprehensive test suite
```

### Key Design Principles

- **Single Responsibility**: Each seeder handles one type of data
- **Dependency Injection**: Services receive dependencies through constructors
- **Factory Pattern**: Consistent data creation through factories
- **Configuration-Driven**: Flexible configuration for different environments
- **Comprehensive Testing**: Unit and integration tests for all components
- **Error Handling**: Graceful error handling with detailed reporting

## Quick Start

### Installation

```bash
# Install dependencies
pnpm install

# Run database migrations
npx prisma migrate dev
```

### Basic Usage

```bash
# Seed with development data
pnpm run seed:dev

# Seed with test data
pnpm run seed:test

# Seed with production data
pnpm run seed:prod
```

### Programmatic Usage

```typescript
import { seed, seedTest } from './prisma/seed'

// Seed with custom configuration
await seed({
  numberOfCompanies: 50,
  numberOfUsers: 25,
  clearExistingData: true,
  verbose: true
})

// Seed minimal test data
await seedTest()
```

## Configuration

### SeedConfig Interface

```typescript
interface SeedConfig {
  numberOfCompanies: number    // Number of companies to generate
  numberOfUsers: number        // Number of users to generate
  generateTestData: boolean    // Include test-specific data
  clearExistingData: boolean   // Clear existing data before seeding
  verbose: boolean            // Enable verbose logging
}
```

### Environment-Specific Configurations

- **Development**: 100 companies, 50 users, verbose logging
- **Test**: 10 companies, 5 users, minimal logging
- **Production**: 1000 companies, 200 users, no test data

## Factories

Factories provide a consistent way to create entities with realistic data.

### BaseFactory

All factories extend `BaseFactory<T>` which provides:

- `create(overrides?)`: Create single entity
- `createMany(count, overrides?)`: Create multiple entities
- `createBatch(configurations[])`: Create entities with different configs

### Available Factories

#### CompanyFactory

```typescript
import { CompanyFactory } from './factories/CompanyFactory'

const factory = new CompanyFactory()

// Create basic company
const company = factory.create()

// Create with overrides
const company = factory.create({
  company_name: 'Acme Corp',
  is_active: true
})

// Create with profile
const company = factory.createWithProfile({
  size: 'large',
  sector: 'Technology',
  hasWebsite: true
})
```

#### ReferenceDataFactory

```typescript
import { ReferenceDataFactory } from './factories/ReferenceDataFactory'

const factory = new ReferenceDataFactory()

// Get all reference data
const data = factory.getAllReferenceData()

// Get specific factories
const cityFactory = factory.getCityFactory()
const regionFactory = factory.getRegionFactory()
```

## Seeders

Seeders implement the `ISeeder<T>` interface and handle database operations.

### Available Seeders

- **ReferenceDataSeeder**: Cities, regions, industry sectors, legal forms
- **CompanySeeder**: Company entities with realistic data
- **ConfigSeeder**: System configuration

### Creating Custom Seeders

```typescript
import { BaseSeeder, SeedConfig } from '../types'
import { MyEntity, PrismaClient } from '../../generated/prisma'

export class MyEntitySeeder extends BaseSeeder<MyEntity> {
  constructor(prisma: PrismaClient) {
    super('MyEntity', prisma)
  }

  async seed(config: SeedConfig): Promise<MyEntity[]> {
    this.log('Seeding my entities...', config)
    
    // Create entities
    const entities = this.factory.createMany(config.numberOfEntities)
    
    // Save to database
    const created = await this.prisma.myEntity.createManyAndReturn({
      data: entities
    })
    
    return created
  }

  async clear(): Promise<void> {
    await this.prisma.myEntity.deleteMany()
  }

  async count(): Promise<number> {
    return this.prisma.myEntity.count()
  }
}
```

## SeedService

The `SeedService` orchestrates all seeding operations.

### Usage

```typescript
import { SeedService } from './core/SeedService'
import { PrismaClient } from '../generated/prisma'

const prisma = new PrismaClient()
const seedService = new SeedService(prisma)

// Register seeders
seedService
  .register(new ReferenceDataSeeder(prisma))
  .register(new CompanySeeder(prisma))
  .register(new ConfigSeeder(prisma))

// Execute seeding
const summary = await seedService.seed({
  numberOfCompanies: 100,
  verbose: true
})

// Get statistics
const stats = await seedService.getStats()
```

### Features

- **Dependency Order**: Executes seeders in registration order
- **Error Handling**: Stops on first failure with detailed error reporting
- **Performance Tracking**: Tracks execution time for each seeder
- **Data Clearing**: Clears existing data in reverse dependency order
- **Statistics**: Provides counts for all seeded data

## Testing

### Running Tests

```bash
# Run all tests
pnpm test

# Run with coverage
pnpm test:coverage

# Run in watch mode
pnpm test:watch

# Run only seed tests
pnpm test:seed
```

### Test Structure

```
__tests__/
├── factories/           # Factory unit tests
├── core/               # Core service tests
├── seeders/            # Seeder unit tests
└── integration/        # Integration tests
```

### Integration Tests

Integration tests require a test database. Set up your test database and configure the connection:

```bash
export TEST_DATABASE_URL="postgresql://test:test@localhost:5432/test_db"
```

### Custom Matchers

The test suite includes custom Jest matchers:

- `toBeValidDate()`: Validates Date objects
- `toBeValidEmail()`: Validates email format

## Data Quality

### Realistic Data Generation

The system generates realistic data including:

- **Companies**: Proper SIREN/NIC numbers, realistic employee counts, industry-appropriate names
- **Locations**: Geographically consistent addresses, postal codes, departments
- **Financial Data**: Industry-appropriate turnover and capital figures
- **Contact Information**: Valid phone numbers, email addresses, websites
- **Schedules**: Realistic business hours with breaks
- **Reviews**: Customer reviews with ratings and comments

### Data Validation

All generated data is validated for:

- Format compliance (SIREN: 9 digits, NIC: 5 digits, postal codes: 5 digits)
- Business logic consistency (closure date after registration date)
- Referential integrity (valid cities, regions, industry sectors)
- Realistic ranges (employee counts, financial figures)

## Performance

### Optimization Features

- **Batch Processing**: Creates entities in batches to avoid memory issues
- **Efficient Queries**: Uses `createManyAndReturn` for bulk operations
- **Lazy Loading**: Reference data is loaded once and reused
- **Connection Pooling**: Proper Prisma client usage

### Performance Monitoring

The system tracks:

- Total execution time
- Individual seeder performance
- Memory usage during batch operations
- Database operation efficiency

## Environment Variables

```bash
# Database connections
DATABASE_URL="postgresql://user:pass@localhost:5432/db"
TEST_DATABASE_URL="postgresql://test:test@localhost:5432/test_db"

# Environment
NODE_ENV="development|test|production"
```

## Troubleshooting

### Common Issues

#### Database Connection Errors
```bash
# Check database is running
pg_isready -h localhost -p 5432

# Verify connection string
echo $DATABASE_URL
```

#### Migration Issues
```bash
# Reset database
npx prisma migrate reset

# Apply migrations
npx prisma migrate dev
```

#### Test Database Setup
```bash
# Create test database
createdb test_db

# Run migrations on test database
DATABASE_URL=$TEST_DATABASE_URL npx prisma migrate deploy
```

### Performance Issues

If seeding is slow:

1. Check database connection latency
2. Reduce batch sizes in configuration
3. Ensure database has sufficient resources
4. Consider using database-specific optimizations

### Memory Issues

For large datasets:

1. Reduce `numberOfCompanies` in configuration
2. Implement streaming for very large datasets
3. Monitor memory usage during execution

## Contributing

### Adding New Seeders

1. Create factory in `factories/`
2. Create seeder in `seeders/`
3. Add tests in `__tests__/`
4. Register in main seed file
5. Update documentation

### Code Standards

- Use TypeScript strict mode
- Follow existing naming conventions
- Add comprehensive tests
- Document public APIs
- Handle errors gracefully

### Testing Requirements

All new code must include:

- Unit tests for factories
- Unit tests for seeders
- Integration tests for database operations
- Error case testing
- Performance considerations

## API Reference

### Types

- `SeedConfig`: Configuration interface
- `ISeeder<T>`: Seeder interface
- `IFactory<T>`: Factory interface
- `SeedResult`: Individual seeder result
- `SeedSummary`: Complete execution summary

### Classes

- `SeedService`: Main orchestration service
- `BaseSeeder<T>`: Base class for seeders
- `BaseFactory<T>`: Base class for factories

### Functions

- `seed(config?)`: Main seeding function
- `seedDevelopment()`: Development environment seeding
- `seedTest()`: Test environment seeding
- `seedProduction()`: Production environment seeding

## License

This seeding system is part of the InfoCompanies project and follows the same license terms.
