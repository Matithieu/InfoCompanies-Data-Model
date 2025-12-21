/**
 * Tests for ReferenceDataFactory
 */

import {
    CityFactory,
    IndustrySectorFactory,
    LegalFormFactory,
    ReferenceDataFactory,
    RegionFactory,
} from '../../factories/ReferenceDataFactory'

describe('ReferenceDataFactory', () => {
  let factory: ReferenceDataFactory

  beforeEach(() => {
    factory = new ReferenceDataFactory()
  })

  describe('getAllReferenceData', () => {
    it('should return all reference data types', () => {
      const data = factory.getAllReferenceData()

      expect(data).toHaveProperty('cities')
      expect(data).toHaveProperty('regions')
      expect(data).toHaveProperty('industrySectors')
      expect(data).toHaveProperty('legalForms')

      expect(Array.isArray(data.cities)).toBe(true)
      expect(Array.isArray(data.regions)).toBe(true)
      expect(Array.isArray(data.industrySectors)).toBe(true)
      expect(Array.isArray(data.legalForms)).toBe(true)

      expect(data.cities.length).toBeGreaterThan(0)
      expect(data.regions.length).toBeGreaterThan(0)
      expect(data.industrySectors.length).toBeGreaterThan(0)
      expect(data.legalForms.length).toBeGreaterThan(0)
    })
  })

  describe('factory getters', () => {
    it('should return factory instances', () => {
      expect(factory.getCityFactory()).toBeInstanceOf(CityFactory)
      expect(factory.getRegionFactory()).toBeInstanceOf(RegionFactory)
      expect(factory.getIndustrySectorFactory()).toBeInstanceOf(IndustrySectorFactory)
      expect(factory.getLegalFormFactory()).toBeInstanceOf(LegalFormFactory)
    })
  })
})

describe('CityFactory', () => {
  let factory: CityFactory

  beforeEach(() => {
    factory = new CityFactory()
  })

  describe('create', () => {
    it('should create a valid city', () => {
      const city = factory.create()

      expect(city).toHaveProperty('name')
      expect(typeof city.name).toBe('string')
      expect(city.name.length).toBeGreaterThan(0)
    })

    it('should respect overrides', () => {
      const city = factory.create({ name: 'Test City' })

      expect(city.name).toBe('Test City')
    })
  })

  describe('createAll', () => {
    it('should create all cities from reference data', () => {
      const cities = factory.createAll()

      expect(Array.isArray(cities)).toBe(true)
      expect(cities.length).toBeGreaterThan(0)

      cities.forEach(city => {
        expect(city).toHaveProperty('name')
        expect(typeof city.name).toBe('string')
      })
    })
  })
})

describe('RegionFactory', () => {
  let factory: RegionFactory

  beforeEach(() => {
    factory = new RegionFactory()
  })

  describe('create', () => {
    it('should create a valid region', () => {
      const region = factory.create()

      expect(region).toHaveProperty('name')
      expect(region).toHaveProperty('code')
      expect(typeof region.name).toBe('string')
      expect(typeof region.code).toBe('string')
      expect(region.name.length).toBeGreaterThan(0)
      expect(region.code.length).toBeGreaterThan(0)
    })

    it('should respect overrides', () => {
      const region = factory.create({ name: 'Test Region', code: 'TR' })

      expect(region.name).toBe('Test Region')
      expect(region.code).toBe('TR')
    })
  })

  describe('createAll', () => {
    it('should create all regions from reference data', () => {
      const regions = factory.createAll()

      expect(Array.isArray(regions)).toBe(true)
      expect(regions.length).toBeGreaterThan(0)

      regions.forEach(region => {
        expect(region).toHaveProperty('name')
        expect(region).toHaveProperty('code')
        expect(typeof region.name).toBe('string')
        expect(typeof region.code).toBe('string')
      })
    })
  })
})

describe('IndustrySectorFactory', () => {
  let factory: IndustrySectorFactory

  beforeEach(() => {
    factory = new IndustrySectorFactory()
  })

  describe('create', () => {
    it('should create a valid industry sector', () => {
      const sector = factory.create()

      expect(sector).toHaveProperty('name')
      expect(typeof sector.name).toBe('string')
      expect(sector.name.length).toBeGreaterThan(0)
    })

    it('should respect overrides', () => {
      const sector = factory.create({ name: 'Test Sector' })

      expect(sector.name).toBe('Test Sector')
    })
  })

  describe('createAll', () => {
    it('should create all industry sectors from reference data', () => {
      const sectors = factory.createAll()

      expect(Array.isArray(sectors)).toBe(true)
      expect(sectors.length).toBeGreaterThan(0)

      sectors.forEach(sector => {
        expect(sector).toHaveProperty('name')
        expect(typeof sector.name).toBe('string')
      })
    })
  })
})

describe('LegalFormFactory', () => {
  let factory: LegalFormFactory

  beforeEach(() => {
    factory = new LegalFormFactory()
  })

  describe('create', () => {
    it('should create a valid legal form', () => {
      const legalForm = factory.create()

      expect(legalForm).toHaveProperty('name')
      expect(legalForm).toHaveProperty('abbreviation')
      expect(typeof legalForm.name).toBe('string')
      expect(typeof legalForm.abbreviation).toBe('string')
      expect(legalForm.name.length).toBeGreaterThan(0)
      expect(legalForm.abbreviation.length).toBeGreaterThan(0)
    })

    it('should respect overrides', () => {
      const legalForm = factory.create({
        name: 'Test Legal Form',
        abbreviation: 'TLF',
      })

      expect(legalForm.name).toBe('Test Legal Form')
      expect(legalForm.abbreviation).toBe('TLF')
    })
  })

  describe('createAll', () => {
    it('should create all legal forms from reference data', () => {
      const legalForms = factory.createAll()

      expect(Array.isArray(legalForms)).toBe(true)
      expect(legalForms.length).toBeGreaterThan(0)

      legalForms.forEach(legalForm => {
        expect(legalForm).toHaveProperty('name')
        expect(legalForm).toHaveProperty('abbreviation')
        expect(typeof legalForm.name).toBe('string')
        expect(typeof legalForm.abbreviation).toBe('string')
      })
    })
  })
})
