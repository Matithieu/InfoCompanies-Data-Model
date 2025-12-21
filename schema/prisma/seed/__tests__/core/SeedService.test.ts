/**
 * Tests for SeedService
 */

import { SeedService } from '../../core/SeedService'
import { DEFAULT_SEED_CONFIG, ISeeder, SeedConfig } from '../../types'

// Mock PrismaClient
const mockPrisma = {
  $disconnect: jest.fn(),
}

// Mock seeder for testing
class MockSeeder implements ISeeder<any> {
  public name: string
  public seedCalled = false
  public clearCalled = false
  public countCalled = false
  public shouldFail = false
  public recordCount = 5

  constructor(name: string) {
    this.name = name
  }

  async seed(config: SeedConfig): Promise<any[]> {
    this.seedCalled = true

    if (this.shouldFail) {
      throw new Error(`${this.name} seeding failed`)
    }

    return new Array(this.recordCount).fill({}).map((_, i) => ({ id: i + 1 }))
  }

  async clear(): Promise<void> {
    this.clearCalled = true
  }

  async count(): Promise<number> {
    this.countCalled = true
    return this.recordCount
  }

  reset() {
    this.seedCalled = false
    this.clearCalled = false
    this.countCalled = false
    this.shouldFail = false
  }
}

describe('SeedService', () => {
  let seedService: SeedService
  let mockSeeder1: MockSeeder
  let mockSeeder2: MockSeeder

  beforeEach(() => {
    seedService = new SeedService(mockPrisma as any)
    mockSeeder1 = new MockSeeder('TestSeeder1')
    mockSeeder2 = new MockSeeder('TestSeeder2')
  })

  describe('register', () => {
    it('should register a single seeder', () => {
      const result = seedService.register(mockSeeder1)

      expect(result).toBe(seedService) // Should return this for chaining
    })

    it('should allow method chaining', () => {
      const result = seedService.register(mockSeeder1).register(mockSeeder2)

      expect(result).toBe(seedService)
    })
  })

  describe('registerMany', () => {
    it('should register multiple seeders at once', () => {
      const result = seedService.registerMany([mockSeeder1, mockSeeder2])

      expect(result).toBe(seedService) // Should return this for chaining
    })
  })

  describe('seed', () => {
    beforeEach(() => {
      seedService.register(mockSeeder1).register(mockSeeder2)
    })

    it('should execute all registered seeders successfully', async () => {
      const summary = await seedService.seed()

      expect(summary.success).toBe(true)
      expect(summary.results).toHaveLength(2)
      expect(summary.totalRecords).toBe(10) // 5 + 5
      expect(summary.totalDuration).toBeGreaterThan(0)

      expect(mockSeeder1.seedCalled).toBe(true)
      expect(mockSeeder2.seedCalled).toBe(true)
    })

    it('should use default config when none provided', async () => {
      const summary = await seedService.seed()

      expect(summary.success).toBe(true)
      // Verify that seeders were called (implying config was passed)
      expect(mockSeeder1.seedCalled).toBe(true)
      expect(mockSeeder2.seedCalled).toBe(true)
    })

    it('should merge provided config with defaults', async () => {
      const customConfig = { numberOfCompanies: 200, verbose: false }
      const summary = await seedService.seed(customConfig)

      expect(summary.success).toBe(true)
    })

    it('should clear existing data when clearExistingData is true', async () => {
      await seedService.seed({ clearExistingData: true })

      expect(mockSeeder1.clearCalled).toBe(true)
      expect(mockSeeder2.clearCalled).toBe(true)
    })

    it('should not clear existing data when clearExistingData is false', async () => {
      await seedService.seed({ clearExistingData: false })

      expect(mockSeeder1.clearCalled).toBe(false)
      expect(mockSeeder2.clearCalled).toBe(false)
    })

    it('should handle seeder failure gracefully', async () => {
      mockSeeder1.shouldFail = true

      const summary = await seedService.seed()

      expect(summary.success).toBe(false)
      expect(summary.results).toHaveLength(1) // Should stop after first failure
      expect(summary.results[0].success).toBe(false)
      expect(summary.results[0].error).toBeDefined()
      expect(summary.results[0].seederName).toBe('TestSeeder1')
    })

    it('should track individual seeder performance', async () => {
      const summary = await seedService.seed()

      summary.results.forEach(result => {
        expect(result.duration).toBeGreaterThan(0)
        expect(result.seederName).toBeDefined()
        expect(result.recordsCreated).toBeGreaterThan(0)
        expect(result.success).toBe(true)
      })
    })
  })

  describe('clearAllData', () => {
    beforeEach(() => {
      seedService.register(mockSeeder1).register(mockSeeder2)
    })

    it('should clear all registered seeders', async () => {
      await seedService.clearAllData(DEFAULT_SEED_CONFIG)

      expect(mockSeeder1.clearCalled).toBe(true)
      expect(mockSeeder2.clearCalled).toBe(true)
    })

    it('should clear seeders in reverse order', async () => {
      const clearOrder: string[] = []

      // Override clear methods to track order
      mockSeeder1.clear = jest.fn().mockImplementation(async () => {
        clearOrder.push('TestSeeder1')
      })
      mockSeeder2.clear = jest.fn().mockImplementation(async () => {
        clearOrder.push('TestSeeder2')
      })

      await seedService.clearAllData(DEFAULT_SEED_CONFIG)

      // Should clear in reverse registration order
      expect(clearOrder).toEqual(['TestSeeder2', 'TestSeeder1'])
    })

    it('should throw error if clearing fails', async () => {
      mockSeeder1.clear = jest.fn().mockRejectedValue(new Error('Clear failed'))

      await expect(seedService.clearAllData(DEFAULT_SEED_CONFIG)).rejects.toThrow('Clear failed')
    })
  })

  describe('getStats', () => {
    beforeEach(() => {
      seedService.register(mockSeeder1).register(mockSeeder2)
    })

    it('should return stats for all seeders', async () => {
      const stats = await seedService.getStats()

      expect(stats).toHaveProperty('TestSeeder1', 5)
      expect(stats).toHaveProperty('TestSeeder2', 5)
      expect(mockSeeder1.countCalled).toBe(true)
      expect(mockSeeder2.countCalled).toBe(true)
    })

    it('should handle count errors gracefully', async () => {
      mockSeeder1.count = jest.fn().mockRejectedValue(new Error('Count failed'))

      const stats = await seedService.getStats()

      expect(stats).toHaveProperty('TestSeeder1', 0)
      expect(stats).toHaveProperty('TestSeeder2', 5)
    })
  })

  describe('error handling', () => {
    it('should handle seeder registration errors', () => {
      // This shouldn't throw, as registration is just adding to array
      expect(() => {
        seedService.register(null as any)
      }).not.toThrow()
    })

    it('should provide detailed error information', async () => {
      mockSeeder1.shouldFail = true
      seedService.register(mockSeeder1)

      const summary = await seedService.seed()

      expect(summary.success).toBe(false)
      expect(summary.results[0].error).toBeInstanceOf(Error)
      expect(summary.results[0].error?.message).toContain('TestSeeder1 seeding failed')
    })
  })
})
