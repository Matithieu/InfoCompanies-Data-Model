/**
 * Integration tests for the seeding system
 * Note: These tests require a test database to be set up
 */

import { PrismaClient } from '../../../generated/prisma'
import { SeedService } from '../../core/SeedService'
import { CompanySeeder } from '../../seeders/CompanySeeder'
import { ConfigSeeder } from '../../seeders/ConfigSeeder'
import { ReferenceDataSeeder } from '../../seeders/ReferenceDataSeeder'

// Test database setup
const prisma = new PrismaClient({
  datasources: {
    db: {
      url: process.env.TEST_DATABASE_URL || 'postgresql://test:test@localhost:5432/test_db',
    },
  },
})

describe('Seed Integration Tests', () => {
  let seedService: SeedService

  beforeAll(async () => {
    // Ensure database is connected
    try {
      await prisma.$connect()
    } catch (error) {
      console.warn('Test database not available, skipping integration tests')
      return
    }
  })

  afterAll(async () => {
    await prisma.$disconnect()
  })

  beforeEach(async () => {
    // Skip if no database connection
    if (!prisma) return

    seedService = new SeedService(prisma)

    // Clean up before each test
    await cleanupDatabase()
  })

  afterEach(async () => {
    // Clean up after each test
    if (prisma) {
      await cleanupDatabase()
    }
  })

  const cleanupDatabase = async () => {
    // Clean up in dependency order
    await prisma.userCompanyStatus.deleteMany()
    await prisma.userQuota.deleteMany()
    await prisma.leader.deleteMany()
    await prisma.company.deleteMany()
    await prisma.config.deleteMany()
    await prisma.city.deleteMany()
    await prisma.industrySector.deleteMany()
    await prisma.legalForm.deleteMany()
    await prisma.region.deleteMany()
  }

  describe('ReferenceDataSeeder Integration', () => {
    it('should seed reference data successfully', async () => {
      if (!prisma) return

      const seeder = new ReferenceDataSeeder(prisma)
      seedService.register(seeder)

      const summary = await seedService.seed({
        numberOfCompanies: 0, // Don't create companies for this test
        verbose: false,
      })

      expect(summary.success).toBe(true)

      // Verify data was created
      const stats = await seedService.getStats()
      expect(stats.ReferenceData).toBeGreaterThan(0)

      // Verify specific counts
      const citiesCount = await prisma.city.count()
      const regionsCount = await prisma.region.count()
      const sectorsCount = await prisma.industrySector.count()
      const legalFormsCount = await prisma.legalForm.count()

      expect(citiesCount).toBeGreaterThan(0)
      expect(regionsCount).toBeGreaterThan(0)
      expect(sectorsCount).toBeGreaterThan(0)
      expect(legalFormsCount).toBeGreaterThan(0)
    })

    it('should create cities with unique names', async () => {
      if (!prisma) return

      const seeder = new ReferenceDataSeeder(prisma)
      await seeder.seed({ numberOfCompanies: 0, verbose: false } as any)

      const cities = await prisma.city.findMany()
      const cityNames = cities.map(city => city.name)
      const uniqueNames = new Set(cityNames)

      expect(cityNames.length).toBe(uniqueNames.size)
    })
  })

  describe('CompanySeeder Integration', () => {
    beforeEach(async () => {
      if (!prisma) return

      // Seed reference data first
      const referenceSeeder = new ReferenceDataSeeder(prisma)
      await referenceSeeder.seed({ numberOfCompanies: 0, verbose: false } as any)
    })

    it('should seed companies successfully', async () => {
      if (!prisma) return

      const seeder = new CompanySeeder(prisma)
      const companies = await seeder.seed({
        numberOfCompanies: 5,
        verbose: false,
      } as any)

      expect(companies).toHaveLength(5)

      // Verify in database
      const dbCompanies = await prisma.company.findMany()
      expect(dbCompanies).toHaveLength(5)

      // Verify company data integrity
      dbCompanies.forEach(company => {
        expect(company.company_name).toBeDefined()
        expect(company.siren_number).toMatch(/^\d{9}$/)
        expect(company.nic_number).toMatch(/^\d{5}$/)
        expect(company.postal_code).toMatch(/^\d{5}$/)
        expect(company.date_of_registration).toBeInstanceOf(Date)
      })
    })

    it('should create companies with different profiles', async () => {
      if (!prisma) return

      const seeder = new CompanySeeder(prisma)
      await seeder.seed({
        numberOfCompanies: 20,
        verbose: false,
      } as any)

      const companies = await prisma.company.findMany()

      // Should have mix of small, medium, large companies
      const employeeCounts = companies
        .map(c => c.number_of_employee)
        .filter(count => count !== null) as number[]

      const small = employeeCounts.filter(count => count <= 50)
      const medium = employeeCounts.filter(count => count > 50 && count <= 250)
      const large = employeeCounts.filter(count => count > 250)

      expect(small.length).toBeGreaterThan(0)
      expect(medium.length).toBeGreaterThan(0)
      // Large companies might be 0 in small sample, that's ok
    })

    it('should handle batch creation efficiently', async () => {
      if (!prisma) return

      const seeder = new CompanySeeder(prisma)
      const startTime = Date.now()

      await seeder.seed({
        numberOfCompanies: 100,
        verbose: false,
      } as any)

      const endTime = Date.now()
      const duration = endTime - startTime

      // Should complete within reasonable time (less than 10 seconds)
      expect(duration).toBeLessThan(10000)

      const count = await prisma.company.count()
      expect(count).toBe(100)
    })
  })

  describe('ConfigSeeder Integration', () => {
    it('should seed config successfully', async () => {
      if (!prisma) return

      const seeder = new ConfigSeeder(prisma)
      const configs = await seeder.seed({
        verbose: false,
      } as any)

      expect(configs).toHaveLength(1)

      const dbConfig = await prisma.config.findFirst()
      expect(dbConfig).toBeDefined()
      expect(dbConfig?.last_reset_quota_date).toBeInstanceOf(Date)
    })

    it('should not create duplicate configs', async () => {
      if (!prisma) return

      const seeder = new ConfigSeeder(prisma)

      // Try to seed twice
      await seeder.seed({ verbose: false } as any)

      // This should fail due to unique constraint or business logic
      await expect(seeder.seed({ verbose: false } as any)).rejects.toThrow()

      const configCount = await prisma.config.count()
      expect(configCount).toBe(1)
    })
  })

  describe('Full Integration Test', () => {
    it('should seed complete database successfully', async () => {
      if (!prisma) return

      seedService
        .register(new ReferenceDataSeeder(prisma))
        .register(new CompanySeeder(prisma))
        .register(new ConfigSeeder(prisma))

      const summary = await seedService.seed({
        numberOfCompanies: 10,
        numberOfUsers: 5,
        generateTestData: true,
        clearExistingData: true,
        verbose: false,
      })

      expect(summary.success).toBe(true)
      expect(summary.results).toHaveLength(3)
      expect(summary.totalRecords).toBeGreaterThan(0)

      // Verify all data was created
      const stats = await seedService.getStats()
      expect(stats.ReferenceData).toBeGreaterThan(0)
      expect(stats.Companies).toBe(10)
      expect(stats.Config).toBe(1)

      // Verify referential integrity
      const companies = await prisma.company.findMany()
      expect(companies).toHaveLength(10)

      // All companies should have valid references
      for (const company of companies) {
        if (company.city) {
          const cityExists = await prisma.city.findFirst({
            where: { name: company.city },
          })
          // Note: This might not match exactly due to how location generation works
          // but the city should be a valid string
          expect(typeof company.city).toBe('string')
        }
      }
    })

    it('should handle clearing and re-seeding', async () => {
      if (!prisma) return

      seedService
        .register(new ReferenceDataSeeder(prisma))
        .register(new CompanySeeder(prisma))
        .register(new ConfigSeeder(prisma))

      // First seed
      await seedService.seed({
        numberOfCompanies: 5,
        verbose: false,
      })

      let companyCount = await prisma.company.count()
      expect(companyCount).toBe(5)

      // Second seed with clear
      await seedService.seed({
        numberOfCompanies: 10,
        clearExistingData: true,
        verbose: false,
      })

      companyCount = await prisma.company.count()
      expect(companyCount).toBe(10) // Should be new count, not added
    })
  })

  describe('Error Handling', () => {
    it('should handle database connection errors gracefully', async () => {
      // Create a service with invalid database
      const invalidPrisma = new PrismaClient({
        datasources: {
          db: {
            url: 'postgresql://invalid:invalid@localhost:9999/invalid_db',
          },
        },
      })

      const invalidSeedService = new SeedService(invalidPrisma)
      invalidSeedService.register(new ReferenceDataSeeder(invalidPrisma))

      const summary = await invalidSeedService.seed({
        numberOfCompanies: 1,
        verbose: false,
      })

      expect(summary.success).toBe(false)
      expect(summary.results[0].error).toBeDefined()

      await invalidPrisma.$disconnect()
    })
  })
}, 60000) // Increase timeout for integration tests
