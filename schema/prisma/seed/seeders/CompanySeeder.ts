/**
 * Seeder for company data
 */

import { Company, PrismaClient } from '../../generated/prisma'
import { CompanyFactory } from '../factories/CompanyFactory'
import { BaseSeeder, SeedConfig } from '../types'

export class CompanySeeder extends BaseSeeder<Company> {
  private factory = new CompanyFactory()

  constructor(prisma: PrismaClient) {
    super('Companies', prisma)
  }

  async seed(config: SeedConfig): Promise<Company[]> {
    const { numberOfCompanies } = config
    this.log(`Generating ${numberOfCompanies} companies...`, config)

    // Create a mix of different company profiles
    const companies = []

    // 60% small companies
    const smallCount = Math.floor(numberOfCompanies * 0.6)
    for (let i = 0; i < smallCount; i++) {
      companies.push(this.factory.createWithProfile({ size: 'small' }))
    }

    // 30% medium companies
    const mediumCount = Math.floor(numberOfCompanies * 0.3)
    for (let i = 0; i < mediumCount; i++) {
      companies.push(this.factory.createWithProfile({ size: 'medium' }))
    }

    // 10% large companies
    const largeCount = numberOfCompanies - smallCount - mediumCount
    for (let i = 0; i < largeCount; i++) {
      companies.push(this.factory.createWithProfile({ size: 'large' }))
    }

    this.log(`Creating ${companies.length} companies in database...`, config)

    // Insert companies in batches to avoid memory issues
    const batchSize = 50
    const createdCompanies: Company[] = []

    for (let i = 0; i < companies.length; i += batchSize) {
      const batch = companies.slice(i, i + batchSize)
      const batchResult = await this.prisma.company.createManyAndReturn({
        data: batch,
      })
      createdCompanies.push(...batchResult)

      if (config.verbose && companies.length > batchSize) {
        this.log(
          `Created batch ${Math.floor(i / batchSize) + 1}/${Math.ceil(companies.length / batchSize)}`,
          config,
        )
      }
    }

    this.log(`Successfully created ${createdCompanies.length} companies`, config)
    return createdCompanies
  }

  async clear(): Promise<void> {
    await this.prisma.company.deleteMany()
  }

  async count(): Promise<number> {
    return this.prisma.company.count()
  }

  /**
   * Seed companies with specific characteristics for testing
   */
  async seedTestData(config: SeedConfig): Promise<Company[]> {
    this.log('Creating test companies with specific profiles...', config)

    const testCompanies = [
      // Active tech startup
      this.factory.createWithProfile({
        size: 'small',
        sector: 'Technology',
        active: true,
        hasWebsite: true,
      }),
      // Large inactive manufacturing company
      this.factory.createWithProfile({
        size: 'large',
        sector: 'Manufacturing',
        active: false,
        hasWebsite: false,
      }),
      // Medium retail company
      this.factory.createWithProfile({
        size: 'medium',
        sector: 'Retail',
        active: true,
        hasWebsite: true,
      }),
    ]

    const createdCompanies = await this.prisma.company.createManyAndReturn({
      data: testCompanies,
    })

    this.log(`Created ${createdCompanies.length} test companies`, config)
    return createdCompanies
  }
}
