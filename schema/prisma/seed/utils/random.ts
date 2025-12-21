import { faker } from '@faker-js/faker'
import { APE_CODES, INDUSTRY_SECTORS, IndustrySectorTypes } from '../reference/industries'
import { DEPARTMENTS_BY_REGION, REGIONS, RegionType } from '../reference/regions'
import { CITIES } from '../reference/cities'
import { LEGAL_FORMS } from '../reference/legalForms'
import { getRandomCityLocation, generatePostalCode } from '../reference/cityDepartmentMapping'

function getRandomIntemFromArray<T>(array: readonly T[]): T {
  return faker.helpers.arrayElement(array)
}

export function pickRandomIndustrySector() {
  return getRandomIntemFromArray(INDUSTRY_SECTORS)
}

export function pickRandomRegion() {
  return getRandomIntemFromArray(REGIONS)
}

export function pickRandomCity() {
  return getRandomIntemFromArray(CITIES)
}

export function pickRandomDepartmentFromRegion(region: RegionType) {
  const department = DEPARTMENTS_BY_REGION[region]
  return getRandomIntemFromArray(department)
}

export function pickRandomLegalForm() {
  return getRandomIntemFromArray(LEGAL_FORMS)
}

export function pickAdequateAPECode(industry: IndustrySectorTypes) {
  const apeCodes = APE_CODES[industry]
  return getRandomIntemFromArray(apeCodes)
}

export function pickGeographicallyConsistentLocation() {
  const location = getRandomCityLocation()

  return {
    city: location.city,
    department: location.department,
    departmentNumber: location.departmentNumber,
    region: location.region,
    postalCode: generatePostalCode(location.postalCodePattern),
  }
}
