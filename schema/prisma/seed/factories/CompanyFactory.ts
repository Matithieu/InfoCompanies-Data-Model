/**
 * Factory for creating company data
 */

import { Prisma } from '../../generated/prisma'
import { BaseFactory } from './BaseFactory'

// Import utility functions
import {
    generateBusinessEmail,
    generateNicNumber,
    generateRealisticCompanyName,
    generateRealisticPhoneNumber,
    generateSirenNumber,
} from '../utils/companyGenerator'
import {
    determineCompanyCategoryFromEmployees,
    determineLegalFormFromEmployeeNumber,
    generateRealisticEmployeeNumber,
} from '../utils/employee'
import { generateCompleteFinancialData, generateSocialMedia } from '../utils/financial'
import {
    pickAdequateAPECode,
    pickGeographicallyConsistentLocation,
    pickRandomIndustrySector,
} from '../utils/random'

export type CompanyCreateInput = Omit<Prisma.CompanyCreateInput, 'id'>

export class CompanyFactory extends BaseFactory<CompanyCreateInput> {
  create(overrides?: Partial<CompanyCreateInput>): CompanyCreateInput {
    // Generate base data
    const industrySector = pickRandomIndustrySector()
    const location = pickGeographicallyConsistentLocation()
    const numberOfEmployees = generateRealisticEmployeeNumber(industrySector)
    const legalForm = determineLegalFormFromEmployeeNumber(numberOfEmployees)
    const companyCategory = determineCompanyCategoryFromEmployees(numberOfEmployees)

    const companyName = generateRealisticCompanyName(industrySector)
    const registrationDate = this.faker.date.between({ from: '2010-01-01', to: '2023-12-31' })
    const isActive = this.faker.datatype.boolean(0.9) // 90% chance company is still active

    const allFinancialData = generateCompleteFinancialData(industrySector)
    const socialMedia = generateSocialMedia()

    // Generate realistic schedule data
    const schedule = this.generateSchedule()

    // Generate realistic reviews data
    const reviews = this.generateReviews()

    const defaults: CompanyCreateInput = {
      company_name: companyName,
      siren_number: generateSirenNumber(),
      nic_number: generateNicNumber(),
      legal_form: legalForm,
      ape_code: pickAdequateAPECode(industrySector),
      ape_label: `${industrySector} - ${this.faker.commerce.department()}`,
      address: this.faker.location.streetAddress(),
      postal_code: location.postalCode,
      department_number: location.departmentNumber,
      department: location.department,
      city: location.city,
      region: location.region,
      trade_name: this.faker.datatype.boolean(0.3) ? this.faker.company.name() : null,
      phone_number: generateRealisticPhoneNumber(),
      email: generateBusinessEmail(companyName),
      website: this.faker.datatype.boolean(0.7) ? this.faker.internet.url() : null,
      number_of_employee: numberOfEmployees,
      company_category: companyCategory,
      registration_date: registrationDate,
      deregistration_date: isActive
        ? null
        : this.faker.date.between({ from: registrationDate, to: new Date() }),
      industry_sector: industrySector,
      facebook: socialMedia.facebook,
      linkedin: socialMedia.linkedin,
      twitter: socialMedia.twitter,
      instagram: socialMedia.instagram,
      schedule: schedule as Prisma.InputJsonValue,
      reviews: reviews as Prisma.InputJsonValue,
    }

    return this.mergeOverrides(defaults, overrides)
  }

  /**
   * Create a company with specific characteristics
   */
  createWithProfile(profile: {
    size?: 'small' | 'medium' | 'large'
    sector?: string
    active?: boolean
    hasWebsite?: boolean
  }): CompanyCreateInput {
    let numberOfEmployees: number

    // Determine employee count based on size
    switch (profile.size) {
      case 'small':
        numberOfEmployees = this.faker.number.int({ min: 1, max: 50 })
        break
      case 'medium':
        numberOfEmployees = this.faker.number.int({ min: 51, max: 250 })
        break
      case 'large':
        numberOfEmployees = this.faker.number.int({ min: 251, max: 5000 })
        break
      default:
        numberOfEmployees = generateRealisticEmployeeNumber(profile.sector || 'Technology')
    }

    return this.create({
      number_of_employee: numberOfEmployees,
      deregistration_date: profile.active === false ? this.faker.date.recent() : null,
      website: profile.hasWebsite ? this.faker.internet.url() : null,
    })
  }

  private generateSchedule(): Record<string, any> {
    const days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    const schedule: Record<string, any> = {}

    days.forEach(day => {
      const isWeekend = day === 'saturday' || day === 'sunday'
      const isOpen = isWeekend ? this.faker.datatype.boolean(0.3) : this.faker.datatype.boolean(0.9)

      if (isOpen) {
        const openTime = isWeekend
          ? '10:00'
          : this.faker.helpers.arrayElement(['08:00', '09:00', '08:30'])
        const closeTime = isWeekend
          ? '17:00'
          : this.faker.helpers.arrayElement(['17:00', '18:00', '19:00'])

        schedule[day] = {
          open: openTime,
          close: closeTime,
          breaks: this.faker.datatype.boolean(0.5) ? [{ start: '12:00', end: '13:00' }] : [],
        }
      } else {
        schedule[day] = { closed: true }
      }
    })

    return schedule
  }

  private generateReviews(): Record<string, any> {
    const reviewCount = this.faker.number.int({ min: 0, max: 50 })
    if (reviewCount === 0) {
      return { count: 0, average: 0, reviews: [] }
    }

    const reviews = Array.from({ length: Math.min(reviewCount, 10) }, () => ({
      rating: this.faker.number.int({ min: 1, max: 5 }),
      comment: this.faker.lorem.sentences(2),
      author: this.faker.person.firstName(),
      date: this.faker.date.recent({ days: 365 }).toISOString(),
    }))

    const averageRating = reviews.reduce((sum, review) => sum + review.rating, 0) / reviews.length

    return {
      count: reviewCount,
      average: Math.round(averageRating * 10) / 10,
      reviews,
    }
  }
}
