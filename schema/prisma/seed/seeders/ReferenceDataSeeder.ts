/**
 * Seeder for reference data (cities, regions, industries, legal forms)
 */

import { City, IndustrySector, LegalForm, PrismaClient, Region } from '../../generated/prisma'
import { ReferenceDataFactory } from '../factories/ReferenceDataFactory'
import type { SeedConfig } from '../types'
import { BaseSeeder } from '../types'

export interface ReferenceData {
  cities: City[]
  regions: Region[]
  industrySectors: IndustrySector[]
  legalForms: LegalForm[]
}

export class ReferenceDataSeeder extends BaseSeeder<ReferenceData> {
  private factory = new ReferenceDataFactory()

  constructor(prisma: PrismaClient) {
    super('ReferenceData', prisma)
  }

  async seed(config: SeedConfig): Promise<ReferenceData[]> {
    this.log('Generating reference data...', config)

    // Generate all reference data
    const referenceData = this.factory.getAllReferenceData()

    // Seed cities
    this.log(`Creating ${referenceData.cities.length} cities...`, config)
    const cities = await this.prisma.city.createManyAndReturn({
      data: referenceData.cities,
    })

    // Seed regions
    this.log(`Creating ${referenceData.regions.length} regions...`, config)
    const regions = await this.prisma.region.createManyAndReturn({
      data: referenceData.regions,
    })

    // Seed industry sectors
    this.log(`Creating ${referenceData.industrySectors.length} industry sectors...`, config)
    const industrySectors = await this.prisma.industrySector.createManyAndReturn({
      data: referenceData.industrySectors,
    })

    // Seed legal forms
    this.log(`Creating ${referenceData.legalForms.length} legal forms...`, config)
    const legalForms = await this.prisma.legalForm.createManyAndReturn({
      data: referenceData.legalForms,
    })

    const result: ReferenceData = {
      cities,
      regions,
      industrySectors,
      legalForms,
    }

    this.log('Reference data seeding completed', config)
    return [result]
  }

  async clear(): Promise<void> {
    // Clear in order that respects foreign key constraints
    await this.prisma.city.deleteMany()
    await this.prisma.industrySector.deleteMany()
    await this.prisma.legalForm.deleteMany()
    await this.prisma.region.deleteMany()
  }

  async count(): Promise<number> {
    const [cities, regions, industrySectors, legalForms] = await Promise.all([
      this.prisma.city.count(),
      this.prisma.region.count(),
      this.prisma.industrySector.count(),
      this.prisma.legalForm.count(),
    ])

    return cities + regions + industrySectors + legalForms
  }
}
