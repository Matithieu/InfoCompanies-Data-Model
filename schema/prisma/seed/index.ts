/**
 * Main seed entry point with clean architecture
 */

import { PrismaClient } from '../generated/prisma'
import {
    DEVELOPMENT_CONFIG,
    getEnvironmentConfig,
    PRODUCTION_CONFIG,
    TEST_CONFIG,
} from './config/environments'
import { SeedService } from './core/SeedService'
import { CompanySeeder } from './seeders/CompanySeeder'
import { ConfigSeeder } from './seeders/ConfigSeeder'
import { ReferenceDataSeeder } from './seeders/ReferenceDataSeeder'
import { SeedConfig } from './types'

// Initialize Prisma client
const prisma = new PrismaClient()

/**
 * Main seed function
 */
export async function seed(config: Partial<SeedConfig> = {}): Promise<void> {
  const seedService = new SeedService(prisma)

  // Register seeders in dependency order
  seedService
    .register(new ReferenceDataSeeder(prisma))
    .register(new CompanySeeder(prisma))
    .register(new ConfigSeeder(prisma))

  try {
    const summary = await seedService.seed(config)

    if (!summary.success) {
      console.error('❌ Seeding failed')
      process.exit(1)
    }

    console.log('✅ Seeding completed successfully!')

    // Print final statistics
    const stats = await seedService.getStats()
    console.log('\n📊 Final Database Statistics:')
    Object.entries(stats).forEach(([name, count]) => {
      console.log(`   ${name}: ${count}`)
    })
  } catch (error) {
    console.error('❌ Seeding error:', error)
    process.exit(1)
  } finally {
    await prisma.$disconnect()
  }
}

/**
 * Seed with development data
 */
export async function seedDevelopment(): Promise<void> {
  await seed(DEVELOPMENT_CONFIG)
}

/**
 * Seed with production-like data
 */
export async function seedProduction(): Promise<void> {
  await seed(PRODUCTION_CONFIG)
}

/**
 * Seed minimal data for testing
 */
export async function seedTest(): Promise<void> {
  await seed(TEST_CONFIG)
}

/**
 * Seed with environment-specific configuration
 */
export async function seedEnvironment(environment?: string): Promise<void> {
  const config = getEnvironmentConfig(environment)
  await seed(config)
}

// Run seed if called directly
if (require.main === module) {
  const environment = process.env.NODE_ENV || 'development'

  console.log(`🌱 Starting seed for ${environment} environment...`)

  seedEnvironment(environment).catch(error => {
    console.error('❌ Seeding failed:', error)
    process.exit(1)
  })
}

// Export for external use
export * from './factories/BaseFactory'
export * from './factories/CompanyFactory'
export * from './factories/ReferenceDataFactory'
export * from './types'
export { CompanySeeder, ConfigSeeder, ReferenceDataSeeder, SeedService }

