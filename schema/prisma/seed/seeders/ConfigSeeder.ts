/**
 * Seeder for system configuration
 */

import { faker } from '@faker-js/faker'
import { Config, PrismaClient } from '../../generated/prisma'
import { BaseSeeder, SeedConfig } from '../types'

export class ConfigSeeder extends BaseSeeder<Config> {
  constructor(prisma: PrismaClient) {
    super('Config', prisma)
  }

  async seed(config: SeedConfig): Promise<Config[]> {
    this.log('Creating system configuration...', config)

    // Generate a realistic last reset date
    const lastResetDate = this.generateResetDate()

    const configData = {
      last_reset_quota_date: lastResetDate,
    }

    const createdConfig = await this.prisma.config.create({
      data: configData,
    })

    this.log('System configuration created', config)
    return [createdConfig]
  }

  async clear(): Promise<void> {
    await this.prisma.config.deleteMany()
  }

  async count(): Promise<number> {
    return this.prisma.config.count()
  }

  private generateResetDate(): Date {
    // 80% chance the reset was recent (within last 30 days)
    // 20% chance it was longer ago
    const isRecentReset = Math.random() < 0.8

    if (isRecentReset) {
      return faker.date.recent({ days: 30 })
    } else {
      return faker.date.between({
        from: new Date(Date.now() - 365 * 24 * 60 * 60 * 1000), // 1 year ago
        to: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000), // 30 days ago
      })
    }
  }

  /**
   * Create config for testing with specific reset pattern
   */
  async seedWithResetPattern(
    pattern: 'monthly' | 'weekly' | 'daily' | 'yearly',
    config: SeedConfig,
  ): Promise<Config> {
    const resetDate = this.generateResetDateForPattern(pattern)

    const configData = {
      last_reset_quota_date: resetDate,
    }

    const createdConfig = await this.prisma.config.create({
      data: configData,
    })

    this.log(`Created config with ${pattern} reset pattern`, config)
    return createdConfig
  }

  private generateResetDateForPattern(pattern: string): Date {
    const now = new Date()

    switch (pattern) {
      case 'monthly':
        return new Date(now.getFullYear(), now.getMonth(), 1)
      case 'weekly':
        now.setDate(now.getDate() - now.getDay() + 1)
        return now
      case 'daily':
        return new Date(now.getFullYear(), now.getMonth(), now.getDate())
      case 'yearly':
        return new Date(now.getFullYear(), 0, 1)
      default:
        return new Date(now.getFullYear(), now.getMonth(), 1)
    }
  }
}
