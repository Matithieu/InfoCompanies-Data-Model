import { faker } from '@faker-js/faker'
import { Company } from '../../generated/prisma'
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

export function generateCompany(): Company {
  const industrySector = pickRandomIndustrySector()
  const location = pickGeographicallyConsistentLocation()
  const numberOfEmployees = generateRealisticEmployeeNumber(industrySector)
  const legalForm = determineLegalFormFromEmployeeNumber(numberOfEmployees)
  const companyCategory = determineCompanyCategoryFromEmployees(numberOfEmployees)

  const companyName = generateRealisticCompanyName(industrySector)
  const registrationDate = faker.date.between({ from: '2010-01-01', to: '2023-12-31' })
  const isActive = faker.datatype.boolean(0.9) // 90% chance company is still active

  const allFinancialData = generateCompleteFinancialData(industrySector)
  const socialMedia = generateSocialMedia()

  return {
    id: undefined as never, // Force undefined for Prisma auto-generated ID
    company_name: companyName,
    siren_number: generateSirenNumber(),
    nic_number: generateNicNumber(),
    legal_form: legalForm,
    ape_code: pickAdequateAPECode(industrySector),
    ape_label: `${industrySector} - ${faker.commerce.department()}`,
    address: faker.location.streetAddress(),
    postal_code: location.postalCode,
    department_number: location.departmentNumber,
    department: location.department,
    city: location.city,
    region: location.region,
    trade_name: faker.datatype.boolean(0.3) ? faker.company.name() : null,
    registration_date: registrationDate,
    deregistration_date: isActive
      ? null
      : faker.date.between({ from: registrationDate, to: new Date() }),

    // Financial data (2018-2023)
    closing_date_2018_1: allFinancialData['closing_date_2018_1'] as Date,
    revenue_2018_1: allFinancialData['revenue_2018_1'] as number,
    turnover_2018_1: allFinancialData['turnover_2018_1'] as number,
    closing_date_2018_2: allFinancialData['closing_date_2018_2'] as Date,
    revenue_2018_2: allFinancialData['revenue_2018_2'] as number,
    turnover_2018_2: allFinancialData['turnover_2018_2'] as number,
    closing_date_2018_3: allFinancialData['closing_date_2018_3'] as Date,
    revenue_2018_3: allFinancialData['revenue_2018_3'] as number,
    turnover_2018_3: allFinancialData['turnover_2018_3'] as number,

    closing_date_2019_1: allFinancialData['closing_date_2019_1'] as Date,
    revenue_2019_1: allFinancialData['revenue_2019_1'] as number,
    turnover_2019_1: allFinancialData['turnover_2019_1'] as number,
    closing_date_2019_2: allFinancialData['closing_date_2019_2'] as Date,
    revenue_2019_2: allFinancialData['revenue_2019_2'] as number,
    turnover_2019_2: allFinancialData['turnover_2019_2'] as number,
    closing_date_2019_3: allFinancialData['closing_date_2019_3'] as Date,
    revenue_2019_3: allFinancialData['revenue_2019_3'] as number,
    turnover_2019_3: allFinancialData['turnover_2019_3'] as number,

    closing_date_2020_1: allFinancialData['closing_date_2020_1'] as Date,
    revenue_2020_1: allFinancialData['revenue_2020_1'] as number,
    turnover_2020_1: allFinancialData['turnover_2020_1'] as number,
    closing_date_2020_2: allFinancialData['closing_date_2020_2'] as Date,
    revenue_2020_2: allFinancialData['revenue_2020_2'] as number,
    turnover_2020_2: allFinancialData['turnover_2020_2'] as number,
    closing_date_2020_3: allFinancialData['closing_date_2020_3'] as Date,
    revenue_2020_3: allFinancialData['revenue_2020_3'] as number,
    turnover_2020_3: allFinancialData['turnover_2020_3'] as number,

    closing_date_2021_1: allFinancialData['closing_date_2021_1'] as Date,
    revenue_2021_1: allFinancialData['revenue_2021_1'] as number,
    turnover_2021_1: allFinancialData['turnover_2021_1'] as number,
    closing_date_2021_2: allFinancialData['closing_date_2021_2'] as Date,
    revenue_2021_2: allFinancialData['revenue_2021_2'] as number,
    turnover_2021_2: allFinancialData['turnover_2021_2'] as number,
    closing_date_2021_3: allFinancialData['closing_date_2021_3'] as Date,
    revenue_2021_3: allFinancialData['revenue_2021_3'] as number,
    turnover_2021_3: allFinancialData['turnover_2021_3'] as number,

    closing_date_2022_1: allFinancialData['closing_date_2022_1'] as Date,
    revenue_2022_1: allFinancialData['revenue_2022_1'] as number,
    turnover_2022_1: allFinancialData['turnover_2022_1'] as number,
    closing_date_2022_2: allFinancialData['closing_date_2022_2'] as Date,
    revenue_2022_2: allFinancialData['revenue_2022_2'] as number,
    turnover_2022_2: allFinancialData['turnover_2022_2'] as number,
    closing_date_2022_3: allFinancialData['closing_date_2022_3'] as Date,
    revenue_2022_3: allFinancialData['revenue_2022_3'] as number,
    turnover_2022_3: allFinancialData['turnover_2022_3'] as number,

    closing_date_2023_1: allFinancialData['closing_date_2023_1'] as Date,
    revenue_2023_1: allFinancialData['revenue_2023_1'] as number,
    turnover_2023_1: allFinancialData['turnover_2023_1'] as number,
    closing_date_2023_2: allFinancialData['closing_date_2023_2'] as Date,
    revenue_2023_2: allFinancialData['revenue_2023_2'] as number,
    turnover_2023_2: allFinancialData['turnover_2023_2'] as number,
    closing_date_2023_3: allFinancialData['closing_date_2023_3'] as Date,
    revenue_2023_3: allFinancialData['revenue_2023_3'] as number,
    turnover_2023_3: allFinancialData['turnover_2023_3'] as number,
    // Business info
    industry_sector: industrySector,
    phone_number: generateRealisticPhoneNumber(),
    website: faker.internet.url(),
    // reviews: generateReviews(industrySector),
    // schedule: generateBusinessSchedule(industrySector),
    reviews: null,
    schedule: null,
    // Social media
    instagram: socialMedia.instagram,
    facebook: socialMedia.facebook,
    twitter: socialMedia.twitter,
    linkedin: socialMedia.linkedin,
    youtube: socialMedia.youtube,
    // Contact & meta
    email: generateBusinessEmail(companyName),
    scraping_date: faker.datatype.boolean(0.7) ? faker.date.recent({ days: 30 }) : null,
    date_creation: new Date(),
    last_processing_date: faker.date.recent({ days: 7 }),
    number_of_employee: numberOfEmployees,
    company_category: companyCategory,
  } satisfies Company
}
