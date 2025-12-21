import { faker } from '@faker-js/faker'
import { IndustrySectorTypes } from '../reference/industries'
import { Prisma } from '../../generated/prisma'

/**
 * Get realistic revenue ranges based on industry sector
 */
function getIndustryRevenueRange(industry: IndustrySectorTypes) {
  const ranges: Record<IndustrySectorTypes, { min: number; max: number }> = {
    'Agriculture, Sylviculture, Pêche et Chasse': { min: 50000, max: 5000000 },
    'Mines, Carrières et Extraction de Pétrole et de Gaz': { min: 1000000, max: 100000000 },
    'Services Publics': { min: 500000, max: 50000000 },
    Construction: { min: 100000, max: 20000000 },
    Fabrication: { min: 200000, max: 50000000 },
    'Commerce de Gros': { min: 500000, max: 100000000 },
    'Commerce de Détail': { min: 100000, max: 10000000 },
    'Transport et Entreposage': { min: 200000, max: 15000000 },
    Information: { min: 100000, max: 10000000 },
    'Finance et Assurance': { min: 500000, max: 50000000 },
    'Immobilier et Location': { min: 100000, max: 10000000 },
    'Services Professionnels, Scientifiques et Techniques': { min: 50000, max: 5000000 },
    "Gestion d'Entreprises": { min: 200000, max: 20000000 },
    'Services Administratifs et de Soutien et Gestion des Déchets': { min: 100000, max: 5000000 },
    'Services Éducatifs': { min: 50000, max: 2000000 },
    'Soins de Santé et Assistance Sociale': { min: 100000, max: 5000000 },
    'Arts, Spectacles et Loisirs': { min: 30000, max: 2000000 },
    'Hébergement et Services de Restauration': { min: 100000, max: 5000000 },
    'Autres Services (sauf Administration Publique)': { min: 50000, max: 2000000 },
    'Administration Publique': { min: 500000, max: 100000000 },
  }

  return ranges[industry] || { min: 100000, max: 5000000 }
}

/**
 * Generate realistic financial data for a given year with industry context
 */
export function generateFinancialDataForYear(year: number, industry?: IndustrySectorTypes) {
  const revenueRange = industry ? getIndustryRevenueRange(industry) : { min: 100000, max: 5000000 }
  const baseRevenue = faker.number.int(revenueRange)

  // Apply year-over-year growth/decline trends
  let growthFactor = 1

  // COVID impact for 2020-2021
  if (year === 2020) {
    const covidSensitiveIndustries = [
      'Hébergement et Services de Restauration',
      'Arts, Spectacles et Loisirs',
      'Transport et Entreposage',
      'Commerce de Détail',
    ]

    if (industry && covidSensitiveIndustries.includes(industry)) {
      growthFactor = 1 + faker.number.float({ min: -0.4, max: -0.1 }) // -40% to -10%
    } else {
      growthFactor = 1 + faker.number.float({ min: -0.2, max: 0.1 }) // -20% to +10%
    }
  } else if (year === 2021) {
    growthFactor = 1 + faker.number.float({ min: -0.1, max: 0.3 }) // Recovery year
  } else {
    growthFactor = 1 + faker.number.float({ min: -0.15, max: 0.25 }) // Normal growth
  }

  // Generate quarterly data with seasonal variations
  const q1Revenue = Math.round(
    baseRevenue * growthFactor * faker.number.float({ min: 0.8, max: 1.2 }),
  )
  const q2Revenue = Math.round(
    baseRevenue * growthFactor * faker.number.float({ min: 0.9, max: 1.3 }),
  )
  const q3Revenue = Math.round(
    baseRevenue * growthFactor * faker.number.float({ min: 0.85, max: 1.25 }),
  )

  // Turnover is typically 90-110% of revenue
  const turnoverMultiplier = faker.number.float({ min: 0.9, max: 1.1 })

  return {
    [`closing_date_${year}_1`]: new Date(year, 2, 31), // March 31
    [`revenue_${year}_1`]: q1Revenue,
    [`turnover_${year}_1`]: Math.round(q1Revenue * turnoverMultiplier),
    [`closing_date_${year}_2`]: new Date(year, 5, 30), // June 30
    [`revenue_${year}_2`]: q2Revenue,
    [`turnover_${year}_2`]: Math.round(q2Revenue * turnoverMultiplier),
    [`closing_date_${year}_3`]: new Date(year, 11, 31), // December 31
    [`revenue_${year}_3`]: q3Revenue,
    [`turnover_${year}_3`]: Math.round(q3Revenue * turnoverMultiplier),
  } as Record<string, Date | number>
}

/**
 * Generate complete financial history (2018-2023) with industry context
 */
export function generateCompleteFinancialData(industry?: IndustrySectorTypes) {
  const allFinancialData: Record<string, Date | number> = {}
  for (let year = 2018; year <= 2023; year++) {
    Object.assign(allFinancialData, generateFinancialDataForYear(year, industry))
  }
  return allFinancialData
}

/**
 * Generate realistic social media presence
 */
export function generateSocialMedia() {
  return {
    instagram: faker.datatype.boolean(0.4) ? `@${faker.internet.username()}` : null,
    facebook: faker.datatype.boolean(0.3) ? faker.internet.url() : null,
    twitter: faker.datatype.boolean(0.2) ? `@${faker.internet.username()}` : null,
    linkedin: faker.datatype.boolean(0.6) ? faker.internet.url() : null,
    youtube: faker.datatype.boolean(0.1) ? faker.internet.url() : null,
  }
}

/**
 * Generate realistic business schedule based on industry
 */
export function generateBusinessSchedule(industry?: IndustrySectorTypes) {
  const baseSchedule = {
    monday: '9:00-18:00',
    tuesday: '9:00-18:00',
    wednesday: '9:00-18:00',
    thursday: '9:00-18:00',
    friday: '9:00-18:00',
    saturday: 'closed',
    sunday: 'closed',
  }

  if (!industry) {
    return JSON.stringify(baseSchedule)
  }

  // Industry-specific schedules
  switch (industry) {
    case 'Commerce de Détail':
      baseSchedule.saturday = faker.datatype.boolean(0.8) ? '9:00-19:00' : 'closed'
      baseSchedule.sunday = faker.datatype.boolean(0.4) ? '14:00-18:00' : 'closed'
      break
    case 'Hébergement et Services de Restauration':
      baseSchedule.monday = '7:00-22:00'
      baseSchedule.tuesday = '7:00-22:00'
      baseSchedule.wednesday = '7:00-22:00'
      baseSchedule.thursday = '7:00-22:00'
      baseSchedule.friday = '7:00-23:00'
      baseSchedule.saturday = '7:00-23:00'
      baseSchedule.sunday = faker.datatype.boolean(0.6) ? '7:00-21:00' : 'closed'
      break
    case 'Soins de Santé et Assistance Sociale':
      baseSchedule.saturday = faker.datatype.boolean(0.5) ? '9:00-12:00' : 'closed'
      break
    case 'Services Publics':
    case 'Administration Publique':
      baseSchedule.friday = '9:00-17:00'
      break
    case 'Arts, Spectacles et Loisirs':
      baseSchedule.saturday = '14:00-22:00'
      baseSchedule.sunday = '14:00-20:00'
      break
    default:
      baseSchedule.saturday = faker.datatype.boolean(0.4) ? '9:00-12:00' : 'closed'
  }

  return JSON.stringify(baseSchedule)
}

/**
 * Generate realistic reviews data based on industry
 */
export function generateReviews(industry?: IndustrySectorTypes) {
  let baseRating = faker.number.float({ min: 3.0, max: 5.0, fractionDigits: 1 })
  let reviewCount = faker.number.int({ min: 0, max: 100 })

  // Industry-specific review patterns
  if (industry) {
    switch (industry) {
      case 'Hébergement et Services de Restauration':
        baseRating = faker.number.float({ min: 2.5, max: 4.8, fractionDigits: 1 })
        reviewCount = faker.number.int({ min: 5, max: 500 })
        break
      case 'Commerce de Détail':
        baseRating = faker.number.float({ min: 3.2, max: 4.7, fractionDigits: 1 })
        reviewCount = faker.number.int({ min: 0, max: 200 })
        break
      case 'Soins de Santé et Assistance Sociale':
        baseRating = faker.number.float({ min: 3.5, max: 4.9, fractionDigits: 1 })
        reviewCount = faker.number.int({ min: 0, max: 50 })
        break
      case 'Services Professionnels, Scientifiques et Techniques':
        baseRating = faker.number.float({ min: 3.8, max: 4.9, fractionDigits: 1 })
        reviewCount = faker.number.int({ min: 0, max: 30 })
        break
      case 'Arts, Spectacles et Loisirs':
        baseRating = faker.number.float({ min: 3.0, max: 4.5, fractionDigits: 1 })
        reviewCount = faker.number.int({ min: 5, max: 300 })
        break
      default:
        // Keep default values
        break
    }
  }

  return JSON.stringify({
    average_rating: baseRating,
    review_count: reviewCount,
  }) as Prisma.JsonValue
}
