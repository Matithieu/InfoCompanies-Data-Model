/**
 * Factory for creating reference data (cities, regions, industries, etc.)
 */

import { City, IndustrySector, LegalForm, Region } from '../../generated/prisma'
import { BaseFactory } from './BaseFactory'

// Import reference data
import { CITIES } from '../reference/cities'
import { INDUSTRY_SECTORS } from '../reference/industries'
import { LEGAL_FORMS } from '../reference/legalForms'
import { REGIONS } from '../reference/regions'

export class CityFactory extends BaseFactory<Omit<City, 'id'>> {
  private static readonly cities = CITIES

  create(overrides?: Partial<Omit<City, 'id'>>): Omit<City, 'id'> {
    const defaults: Omit<City, 'id'> = {
      name: this.randomPick(CityFactory.cities),
    }

    return this.mergeOverrides(defaults, overrides)
  }

  createAll(): Omit<City, 'id'>[] {
    return CityFactory.cities.map(name => ({ name }))
  }
}

export class RegionFactory extends BaseFactory<Omit<Region, 'id'>> {
  private static readonly regions = REGIONS

  create(overrides?: Partial<Omit<Region, 'id'>>): Omit<Region, 'id'> {
    const region = this.randomPick(RegionFactory.regions)
    const defaults: Omit<Region, 'id'> = {
      name: region.name,
      code: region.code,
    }

    return this.mergeOverrides(defaults, overrides)
  }

  createAll(): Omit<Region, 'id'>[] {
    return RegionFactory.regions.map(region => ({
      name: region.name,
      code: region.code,
    }))
  }
}

export class IndustrySectorFactory extends BaseFactory<Omit<IndustrySector, 'id'>> {
  private static readonly sectors = INDUSTRY_SECTORS

  create(overrides?: Partial<Omit<IndustrySector, 'id'>>): Omit<IndustrySector, 'id'> {
    const defaults: Omit<IndustrySector, 'id'> = {
      name: this.randomPick(IndustrySectorFactory.sectors),
    }

    return this.mergeOverrides(defaults, overrides)
  }

  createAll(): Omit<IndustrySector, 'id'>[] {
    return IndustrySectorFactory.sectors.map(name => ({ name }))
  }
}

export class LegalFormFactory extends BaseFactory<Omit<LegalForm, 'id'>> {
  private static readonly legalForms = LEGAL_FORMS

  create(overrides?: Partial<Omit<LegalForm, 'id'>>): Omit<LegalForm, 'id'> {
    const legalForm = this.randomPick(LegalFormFactory.legalForms)
    const defaults: Omit<LegalForm, 'id'> = {
      name: legalForm.name,
      abbreviation: legalForm.abbreviation,
    }

    return this.mergeOverrides(defaults, overrides)
  }

  createAll(): Omit<LegalForm, 'id'>[] {
    return LegalFormFactory.legalForms.map(form => ({
      name: form.name,
      abbreviation: form.abbreviation,
    }))
  }
}

// Combined reference data factory
export class ReferenceDataFactory {
  private cityFactory = new CityFactory()
  private regionFactory = new RegionFactory()
  private industrySectorFactory = new IndustrySectorFactory()
  private legalFormFactory = new LegalFormFactory()

  getAllReferenceData() {
    return {
      cities: this.cityFactory.createAll(),
      regions: this.regionFactory.createAll(),
      industrySectors: this.industrySectorFactory.createAll(),
      legalForms: this.legalFormFactory.createAll(),
    }
  }

  getCityFactory(): CityFactory {
    return this.cityFactory
  }

  getRegionFactory(): RegionFactory {
    return this.regionFactory
  }

  getIndustrySectorFactory(): IndustrySectorFactory {
    return this.industrySectorFactory
  }

  getLegalFormFactory(): LegalFormFactory {
    return this.legalFormFactory
  }
}
