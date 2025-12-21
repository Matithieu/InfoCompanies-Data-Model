/**
 * Tests for CompanyFactory
 */

import { CompanyFactory } from '../../factories/CompanyFactory'

describe('CompanyFactory', () => {
  let factory: CompanyFactory

  beforeEach(() => {
    factory = new CompanyFactory()
  })

  describe('create', () => {
    it('should create a valid company object', () => {
      const company = factory.create()

      expect(company).toBeDefined()
      expect(company.company_name).toBeDefined()
      expect(typeof company.company_name).toBe('string')
      expect(company.siren_number).toBeDefined()
      expect(company.nic_number).toBeDefined()
      expect(company.legal_form).toBeDefined()
      expect(company.ape_code).toBeDefined()
      expect(company.address).toBeDefined()
      expect(company.postal_code).toBeDefined()
      expect(company.city).toBeDefined()
      expect(company.region).toBeDefined()
    })

    it('should create company with valid email format', () => {
      const company = factory.create()

      if (company.email) {
        expect(company.email).toBeValidEmail()
      }
    })

    it('should create company with valid dates', () => {
      const company = factory.create()

      expect(company.registration_date).toBeValidDate()

      if (company.deregistration_date) {
        expect(company.deregistration_date).toBeValidDate()
        expect(company.deregistration_date.getTime()).toBeGreaterThan(
          company.registration_date.getTime(),
        )
      }
    })

    it('should respect overrides', () => {
      const overrides = {
        company_name: 'Test Company Ltd',
        deregistration_date: new Date('2023-01-01'),
        number_of_employee: 500,
      }

      const company = factory.create(overrides)

      expect(company.company_name).toBe('Test Company Ltd')
      expect(company.deregistration_date).toEqual(new Date('2023-01-01'))
      expect(company.number_of_employee).toBe(500)
    })

    it('should create valid schedule object', () => {
      const company = factory.create()

      expect(company.schedule).toBeDefined()
      expect(typeof company.schedule).toBe('object')

      const schedule = company.schedule as Record<string, any>
      const days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

      days.forEach(day => {
        expect(schedule[day]).toBeDefined()

        if (!schedule[day].closed) {
          expect(schedule[day].open).toBeDefined()
          expect(schedule[day].close).toBeDefined()
          expect(typeof schedule[day].open).toBe('string')
          expect(typeof schedule[day].close).toBe('string')
        }
      })
    })

    it('should create valid reviews object', () => {
      const company = factory.create()

      expect(company.reviews).toBeDefined()
      expect(typeof company.reviews).toBe('object')

      const reviews = company.reviews as Record<string, any>
      expect(reviews.count).toBeDefined()
      expect(reviews.average).toBeDefined()
      expect(reviews.reviews).toBeDefined()
      expect(Array.isArray(reviews.reviews)).toBe(true)

      if (reviews.count > 0) {
        expect(reviews.average).toBeGreaterThan(0)
        expect(reviews.average).toBeLessThanOrEqual(5)
      }
    })
  })

  describe('createMany', () => {
    it('should create multiple companies', () => {
      const companies = factory.createMany(5)

      expect(companies).toHaveLength(5)
      companies.forEach(company => {
        expect(company.company_name).toBeDefined()
        expect(company.siren_number).toBeDefined()
      })
    })

    it('should create companies with same overrides', () => {
      const overrides = { deregistration_date: new Date('2023-01-01') }
      const companies = factory.createMany(3, overrides)

      expect(companies).toHaveLength(3)
      companies.forEach(company => {
        expect(company.deregistration_date).toEqual(new Date('2023-01-01'))
      })
    })
  })

  describe('createWithProfile', () => {
    it('should create small company', () => {
      const company = factory.createWithProfile({ size: 'small' })

      expect(company.number_of_employee).toBeDefined()
      expect(company.number_of_employee!).toBeGreaterThan(0)
      expect(company.number_of_employee!).toBeLessThanOrEqual(50)
    })

    it('should create medium company', () => {
      const company = factory.createWithProfile({ size: 'medium' })

      expect(company.number_of_employee).toBeDefined()
      expect(company.number_of_employee!).toBeGreaterThan(50)
      expect(company.number_of_employee!).toBeLessThanOrEqual(250)
    })

    it('should create large company', () => {
      const company = factory.createWithProfile({ size: 'large' })

      expect(company.number_of_employee).toBeDefined()
      expect(company.number_of_employee!).toBeGreaterThan(250)
    })

    it('should respect active flag', () => {
      const activeCompany = factory.createWithProfile({ active: true })
      const inactiveCompany = factory.createWithProfile({ active: false })

      expect(activeCompany.deregistration_date).toBeNull()
      expect(inactiveCompany.deregistration_date).not.toBeNull()
    })

    it('should respect website flag', () => {
      const companyWithWebsite = factory.createWithProfile({ hasWebsite: true })
      const companyWithoutWebsite = factory.createWithProfile({ hasWebsite: false })

      expect(companyWithWebsite.website).toBeDefined()
      expect(companyWithWebsite.website).not.toBeNull()
      expect(companyWithoutWebsite.website).toBeNull()
    })
  })

  describe('data validation', () => {
    it('should create companies with valid SIREN numbers', () => {
      const company = factory.create()

      expect(company.siren_number).toBeDefined()
      expect(company.siren_number).toMatch(/^\d{9}$/)
    })

    it('should create companies with valid NIC numbers', () => {
      const company = factory.create()

      expect(company.nic_number).toBeDefined()
      expect(company.nic_number).toMatch(/^\d{5}$/)
    })

    it('should create companies with valid postal codes', () => {
      const company = factory.create()

      expect(company.postal_code).toBeDefined()
      expect(company.postal_code).toMatch(/^\d{5}$/)
    })

    it('should create consistent location data', () => {
      const company = factory.create()

      expect(company.city).toBeDefined()
      expect(company.region).toBeDefined()
      expect(company.department).toBeDefined()
      expect(company.department_number).toBeDefined()
      expect(company.postal_code).toBeDefined()
    })
  })
})
