import { City, IndustrySector, LegalForm, Region } from '../../generated/prisma'
import { CITIES, CityTypes } from './cities'
import { INDUSTRY_SECTORS, IndustrySectorTypes } from './industries'
import { LEGAL_FORMS, LegalFormTypes } from './legalForms'
import { REGIONS, RegionType } from './regions'

// Generate City records from the reference data
export function generateCities(): City[] {
  return CITIES.map(
    (cityName, index) =>
      ({
        id: index + 1, // Start from 1
        name: cityName,
      }) satisfies City,
  )
}

// Generate IndustrySector records from the reference data
export function generateIndustrySectors(): IndustrySector[] {
  return INDUSTRY_SECTORS.map(
    (sectorName, index) =>
      ({
        id: index + 1, // Start from 1
        name: sectorName,
      }) satisfies IndustrySector,
  )
}

// Generate LegalForm records from the reference data
export function generateLegalForms(): LegalForm[] {
  return LEGAL_FORMS.map(
    (legalFormName, index) =>
      ({
        id: index + 1, // Start from 1
        name: legalFormName,
      }) satisfies LegalForm,
  )
}

// Generate Region records from the reference data
export function generateRegions(): Region[] {
  return REGIONS.map(
    (regionName, index) =>
      ({
        id: index + 1, // Start from 1
        name: regionName,
      }) satisfies Region,
  )
}

// Generate all reference data at once
export function generateAllReferenceData(): {
  cities: City[]
  industrySectors: IndustrySector[]
  legalForms: LegalForm[]
  regions: Region[]
} {
  return {
    cities: generateCities(),
    industrySectors: generateIndustrySectors(),
    legalForms: generateLegalForms(),
    regions: generateRegions(),
  }
}

// Helper functions to get reference data by name (useful for other generators)
export function getCityIdByName(cityName: CityTypes): number | null {
  const index = CITIES.indexOf(cityName)
  return index >= 0 ? index + 1 : null
}

export function getIndustrySectorIdByName(sectorName: IndustrySectorTypes): number | null {
  const index = INDUSTRY_SECTORS.indexOf(sectorName)
  return index >= 0 ? index + 1 : null
}

export function getLegalFormIdByName(legalFormName: LegalFormTypes): number | null {
  const index = LEGAL_FORMS.indexOf(legalFormName)
  return index >= 0 ? index + 1 : null
}

export function getRegionIdByName(regionName: RegionType): number | null {
  const index = REGIONS.indexOf(regionName)
  return index >= 0 ? index + 1 : null
}

// Helper functions to get random reference data
export function getRandomCity(): { id: number; name: string } {
  const randomIndex = Math.floor(Math.random() * CITIES.length)
  return {
    id: randomIndex + 1,
    name: CITIES[randomIndex],
  }
}

export function getRandomIndustrySector(): { id: number; name: string } {
  const randomIndex = Math.floor(Math.random() * INDUSTRY_SECTORS.length)
  return {
    id: randomIndex + 1,
    name: INDUSTRY_SECTORS[randomIndex],
  }
}

export function getRandomLegalForm(): { id: number; name: string } {
  const randomIndex = Math.floor(Math.random() * LEGAL_FORMS.length)
  return {
    id: randomIndex + 1,
    name: LEGAL_FORMS[randomIndex],
  }
}

export function getRandomRegion(): { id: number; name: string } {
  const randomIndex = Math.floor(Math.random() * REGIONS.length)
  return {
    id: randomIndex + 1,
    name: REGIONS[randomIndex],
  }
}
