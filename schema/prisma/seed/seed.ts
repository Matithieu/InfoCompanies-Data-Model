import { Prisma, PrismaClient } from '../generated/prisma'
import { generateCompany } from './business/companies'
import { generateConfig } from './business/config'
import { generateRealisticLeadersForCompany } from './business/leaders'
import { generateRealisticUserCompanyStatuses } from './business/userCompanyStatus'
import { generateBusinessScenarioQuotas } from './business/userQuota'
import { generateAllReferenceData } from './reference/referenceData'

const prisma = new PrismaClient()

async function main() {
  console.log('🌱 Starting database seeding...')

  // 1. Seed reference data first (these are lookup tables)
  console.log('📋 Seeding reference data...')
  const referenceData = generateAllReferenceData()

  // Clear existing reference data
  await prisma.city.deleteMany()
  await prisma.industrySector.deleteMany()
  await prisma.legalForm.deleteMany()
  await prisma.region.deleteMany()

  // Insert reference data
  await prisma.city.createMany({ data: referenceData.cities })
  await prisma.industrySector.createMany({ data: referenceData.industrySectors })
  await prisma.legalForm.createMany({ data: referenceData.legalForms })
  await prisma.region.createMany({ data: referenceData.regions })

  console.log(`✅ Created ${referenceData.cities.length} cities`)
  console.log(`✅ Created ${referenceData.industrySectors.length} industry sectors`)
  console.log(`✅ Created ${referenceData.legalForms.length} legal forms`)
  console.log(`✅ Created ${referenceData.regions.length} regions`)

  // 2. Seed companies
  console.log('🏢 Seeding companies...')
  await prisma.company.deleteMany()

  const companies = []
  const numberOfCompanies = 100 // Adjust as needed

  for (let i = 0; i < numberOfCompanies; i++) {
    const company = generateCompany()
    // Remove id field and ensure reviews is properly typed for Prisma
    const { reviews, ...companyData } = company
    companies.push({
      ...companyData,
      schedule: company.schedule as Prisma.InputJsonValue, // Cast to satisfy Prisma's InputJsonValue type
      reviews: reviews as Prisma.InputJsonValue, // Cast to satisfy Prisma's InputJsonValue type
    })
  }

  await prisma.company.createMany({ data: companies })
  console.log(`✅ Created ${companies.length} companies`)

  // 3. Seed leaders (linked to companies)
  console.log('👔 Seeding leaders...')
  await prisma.leader.deleteMany()

  const leaders = []
  const createdCompanies = await prisma.company.findMany()

  for (const company of createdCompanies) {
    // Determine company size based on employee count
    let companySize: 'small' | 'medium' | 'large' = 'small'
    if (company.number_of_employee) {
      if (company.number_of_employee > 250) {
        companySize = 'large'
      } else if (company.number_of_employee > 50) {
        companySize = 'medium'
      }
    }

    const companyLeaders = generateRealisticLeadersForCompany(
      company.siren_number || '',
      company.company_name || '',
      company.legal_form || '',
      companySize,
    )

    leaders.push(...companyLeaders)
  }

  await prisma.leader.createMany({ data: leaders })
  console.log(`✅ Created ${leaders.length} leaders`)

  // 4. Seed user quotas
  console.log('📊 Seeding user quotas...')
  await prisma.userQuota.deleteMany()

  const quotaScenarios = generateBusinessScenarioQuotas()
  const allQuotas = [
    ...quotaScenarios.freeUsers,
    ...quotaScenarios.paidUsers,
    ...quotaScenarios.enterpriseUsers,
  ]

  await prisma.userQuota.createMany({ data: allQuotas })
  console.log(`✅ Created ${allQuotas.length} user quotas`)

  // 5. Seed user company statuses
  console.log('📝 Seeding user company statuses...')
  await prisma.userCompanyStatus.deleteMany()

  const companyIds = createdCompanies.map(c => c.id)
  const userCompanyStatuses = generateRealisticUserCompanyStatuses(companyIds)

  await prisma.userCompanyStatus.createMany({ data: userCompanyStatuses })
  console.log(`✅ Created ${userCompanyStatuses.length} user company statuses`)

  // 6. Seed system configuration
  console.log('⚙️ Seeding system configuration...')
  await prisma.config.deleteMany()

  const config = generateConfig()
  await prisma.config.create({ data: config })
  console.log('✅ Created system configuration')

  console.log('🎉 Database seeding completed successfully!')

  // Print summary statistics
  const stats = await getDatabaseStats()
  console.log('\n📈 Database Statistics:')
  console.log(`   Companies: ${stats.companies}`)
  console.log(`   Leaders: ${stats.leaders}`)
  console.log(`   User Quotas: ${stats.userQuotas}`)
  console.log(`   User Company Statuses: ${stats.userCompanyStatuses}`)
  console.log(`   Cities: ${stats.cities}`)
  console.log(`   Industry Sectors: ${stats.industrySectors}`)
  console.log(`   Legal Forms: ${stats.legalForms}`)
  console.log(`   Regions: ${stats.regions}`)
}

async function getDatabaseStats() {
  const [
    companies,
    leaders,
    userQuotas,
    userCompanyStatuses,
    cities,
    industrySectors,
    legalForms,
    regions,
  ] = await Promise.all([
    prisma.company.count(),
    prisma.leader.count(),
    prisma.userQuota.count(),
    prisma.userCompanyStatus.count(),
    prisma.city.count(),
    prisma.industrySector.count(),
    prisma.legalForm.count(),
    prisma.region.count(),
  ])

  return {
    companies,
    leaders,
    userQuotas,
    userCompanyStatuses,
    cities,
    industrySectors,
    legalForms,
    regions,
  }
}

// Run the seed function
main()
  .catch(e => {
    console.error('❌ Error during seeding:', e)
    process.exit(1)
  })
  .finally(async () => {
    await prisma.$disconnect()
  })

// Export functions for testing
export { getDatabaseStats, main as seedDatabase }
