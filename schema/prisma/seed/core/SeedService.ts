/**
 * Main seed service that orchestrates all seeding operations
 */

import { PrismaClient } from '../../generated/prisma'
import { DEFAULT_SEED_CONFIG, ISeeder, SeedConfig, SeedResult, SeedSummary } from '../types'

export class SeedService {
  private seeders: ISeeder<any>[] = []
  private prisma: PrismaClient

  constructor(prisma: PrismaClient) {
    this.prisma = prisma
  }

  /**
   * Register a seeder to be executed
   */
  register<T>(seeder: ISeeder<T>): this {
    this.seeders.push(seeder)
    return this
  }

  /**
   * Register multiple seeders
   */
  registerMany<T>(seeders: ISeeder<T>[]): this {
    this.seeders.push(...seeders)
    return this
  }

  /**
   * Execute all registered seeders
   */
  async seed(config: Partial<SeedConfig> = {}): Promise<SeedSummary> {
    const finalConfig = { ...DEFAULT_SEED_CONFIG, ...config }
    const startTime = Date.now()
    const results: SeedResult[] = []
    let totalRecords = 0

    console.log('🌱 Starting database seeding...')
    if (finalConfig.verbose) {
      console.log(`Configuration:`, finalConfig)
    }

    // Clear existing data if requested
    if (finalConfig.clearExistingData) {
      await this.clearAllData(finalConfig)
    }

    // Execute each seeder
    for (const seeder of this.seeders) {
      const result = await this.executeSingleSeeder(seeder, finalConfig)
      results.push(result)
      totalRecords += result.recordsCreated

      if (!result.success) {
        console.error(`❌ Seeding failed at ${seeder.name}`)
        break
      }
    }

    const totalDuration = Date.now() - startTime
    const success = results.every(r => r.success)

    const summary: SeedSummary = {
      totalDuration,
      totalRecords,
      results,
      success,
    }

    this.printSummary(summary, finalConfig)
    return summary
  }

  /**
   * Clear all data from registered seeders
   */
  async clearAllData(config: SeedConfig): Promise<void> {
    console.log('🧹 Clearing existing data...')

    // Clear in reverse order to handle dependencies
    const reversedSeeders = [...this.seeders].reverse()

    for (const seeder of reversedSeeders) {
      try {
        await seeder.clear()
        if (config.verbose) {
          console.log(`✅ Cleared ${seeder.name}`)
        }
      } catch (error) {
        console.error(`❌ Failed to clear ${seeder.name}:`, error)
        throw error
      }
    }
  }

  /**
   * Get statistics for all seeded data
   */
  async getStats(): Promise<Record<string, number>> {
    const stats: Record<string, number> = {}

    for (const seeder of this.seeders) {
      try {
        stats[seeder.name] = await seeder.count()
      } catch (error) {
        console.error(`Failed to get count for ${seeder.name}:`, error)
        stats[seeder.name] = 0
      }
    }

    return stats
  }

  private async executeSingleSeeder(seeder: ISeeder<any>, config: SeedConfig): Promise<SeedResult> {
    const startTime = Date.now()

    try {
      console.log(`📦 Seeding ${seeder.name}...`)
      const records = await seeder.seed(config)
      const duration = Date.now() - startTime
      const recordsCreated = records.length

      if (config.verbose) {
        console.log(`✅ Created ${recordsCreated} ${seeder.name} records in ${duration}ms`)
      }

      return {
        seederName: seeder.name,
        recordsCreated,
        duration,
        success: true,
      }
    } catch (error) {
      const duration = Date.now() - startTime
      console.error(`❌ Failed to seed ${seeder.name}:`, error)

      return {
        seederName: seeder.name,
        recordsCreated: 0,
        duration,
        success: false,
        error: error as Error,
      }
    }
  }

  private printSummary(summary: SeedSummary, config: SeedConfig): void {
    console.log('\n🎉 Seeding completed!')
    console.log(`Total time: ${summary.totalDuration}ms`)
    console.log(`Total records: ${summary.totalRecords}`)

    if (config.verbose) {
      console.log('\n📈 Detailed Results:')
      summary.results.forEach(result => {
        const status = result.success ? '✅' : '❌'
        console.log(
          `   ${status} ${result.seederName}: ${result.recordsCreated} records (${result.duration}ms)`,
        )
        if (result.error) {
          console.log(`      Error: ${result.error.message}`)
        }
      })
    }

    if (!summary.success) {
      console.log('\n⚠️  Some seeders failed. Check the logs above.')
    }
  }
}
