import { faker } from '@faker-js/faker'
import { Leader } from '../../generated/prisma'

// French executive roles with their typical characteristics
const EXECUTIVE_ROLES = [
  { role: 'Président', type: 'Dirigeant', weight: 0.15 },
  { role: 'Directeur Général', type: 'Dirigeant', weight: 0.12 },
  { role: 'Directeur', type: 'Dirigeant', weight: 0.1 },
  { role: 'Gérant', type: 'Dirigeant', weight: 0.2 },
  { role: 'Associé Gérant', type: 'Dirigeant', weight: 0.08 },
  { role: 'Directeur Commercial', type: 'Dirigeant', weight: 0.08 },
  { role: 'Directeur Financier', type: 'Dirigeant', weight: 0.06 },
  { role: 'Directeur des Ressources Humaines', type: 'Dirigeant', weight: 0.05 },
  { role: 'Directeur Technique', type: 'Dirigeant', weight: 0.05 },
  { role: 'Directeur Marketing', type: 'Dirigeant', weight: 0.04 },
  { role: 'Secrétaire Général', type: 'Dirigeant', weight: 0.03 },
  { role: 'Directeur de Production', type: 'Dirigeant', weight: 0.04 },
] as const

// French first names (common business names)
const FRENCH_FIRST_NAMES = [
  'Jean',
  'Pierre',
  'Michel',
  'Alain',
  'Philippe',
  'Bernard',
  'André',
  'Daniel',
  'Claude',
  'Robert',
  'Marie',
  'Nathalie',
  'Isabelle',
  'Sylvie',
  'Catherine',
  'Françoise',
  'Monique',
  'Christine',
  'Nicole',
  'Martine',
  'David',
  'Laurent',
  'Stéphane',
  'Fabrice',
  'Sébastien',
  'Julien',
  'Nicolas',
  'Antoine',
  'Thomas',
  'Alexandre',
  'Sophie',
  'Céline',
  'Sandrine',
  'Valérie',
  'Patricia',
  'Véronique',
  'Caroline',
  'Aurélie',
  'Julie',
  'Emilie',
] as const

// French last names (common business surnames)
const FRENCH_LAST_NAMES = [
  'Martin',
  'Bernard',
  'Thomas',
  'Petit',
  'Robert',
  'Richard',
  'Durand',
  'Dubois',
  'Moreau',
  'Laurent',
  'Simon',
  'Michel',
  'Lefebvre',
  'Leroy',
  'Roux',
  'David',
  'Bertrand',
  'Morel',
  'Fournier',
  'Girard',
  'Bonnet',
  'Dupont',
  'Lambert',
  'Fontaine',
  'Rousseau',
  'Vincent',
  'Muller',
  'Lefevre',
  'Faure',
  'Andre',
  'Mercier',
  'Blanc',
  'Guerin',
  'Boyer',
  'Garnier',
  'Chevalier',
  'Francois',
  'Legrand',
  'Gauthier',
  'Garcia',
] as const

// Event types for leadership changes
const LEADERSHIP_EVENTS = [
  'Nomination',
  'Prise de fonction',
  'Démission',
  'Cessation',
  'Modification',
  'Renouvellement',
] as const

// Usage name types
const USAGE_NAME_TYPES = [
  'Nom de naissance',
  "Nom d'usage",
  'Nom marital',
  'Nom commercial',
] as const

function generateFrenchName(): { firstName: string; lastName: string } {
  return {
    firstName: faker.helpers.arrayElement(FRENCH_FIRST_NAMES),
    lastName: faker.helpers.arrayElement(FRENCH_LAST_NAMES),
  }
}

function generateGestionNumber(): string {
  // French gestion numbers are typically 9 digits
  return faker.string.numeric(9)
}

function generateIdData(): string {
  // ID data format varies, using a realistic pattern
  return faker.string.alphanumeric(12).toUpperCase()
}

function pickWeightedRole(): { role: string; type: string } {
  const totalWeight = EXECUTIVE_ROLES.reduce((sum, role) => sum + role.weight, 0)
  let random = Math.random() * totalWeight

  for (const roleData of EXECUTIVE_ROLES) {
    random -= roleData.weight
    if (random <= 0) {
      return { role: roleData.role, type: roleData.type }
    }
  }

  // Fallback to first role
  return { role: EXECUTIVE_ROLES[0].role, type: EXECUTIVE_ROLES[0].type }
}

function generateCompanyName(): string {
  // Generate a realistic French company name
  const businessTypes = [
    'Solutions',
    'Services',
    'Technologies',
    'Innovation',
    'Développement',
    'Consulting',
    'Expertise',
    'Partners',
    'Group',
    'International',
  ]
  const sectors = [
    'Informatique',
    'Conseil',
    'Formation',
    'Marketing',
    'Communication',
    'Finance',
    'Immobilier',
    'Construction',
    'Commerce',
    'Industrie',
  ]

  const businessType = faker.helpers.arrayElement(businessTypes)
  const sector = faker.helpers.arrayElement(sectors)

  // 60% chance to use a person's name, 40% generic business name
  if (Math.random() < 0.6) {
    const { lastName } = generateFrenchName()
    return `${lastName} ${businessType}`
  } else {
    return `${sector} ${businessType}`
  }
}

function generateLegalForm(): string {
  const legalForms = ['SARL', 'SA', 'EURL', 'SAS', 'SNC', 'SASU', 'EI', 'Micro-entreprise']
  return faker.helpers.arrayElement(legalForms)
}

export function generateLeader(companySiren: string, companyName: string): Leader {
  const { firstName, lastName } = generateFrenchName()
  const { role, type } = pickWeightedRole()

  // 15% chance to have a usage name (nom d'usage)
  const hasUsageName = Math.random() < 0.15
  const usageName = hasUsageName ? faker.helpers.arrayElement(USAGE_NAME_TYPES) : null

  // 10% chance to have a pseudo/nickname
  const hasPseudo = Math.random() < 0.1
  const pseudo = hasPseudo ? faker.person.firstName() : null

  // Generate event name (leadership change event)
  const eventName = faker.helpers.arrayElement(LEADERSHIP_EVENTS)

  return {
    id: undefined as never, // Force undefined for Prisma auto-generated ID
    siren: companySiren, // Use the company's SIREN to maintain relationship
    role: role,
    last_name: lastName,
    first_name: firstName,
    gestion_number: generateGestionNumber(),
    type: type,
    event_name: eventName,
    usage_name: usageName,
    pseudo: pseudo,
    company_name: companyName || generateCompanyName(),
    legal_form: generateLegalForm(),
    id_data: generateIdData(),
  } satisfies Leader
}

// Generate a standalone leader with a random SIREN (for testing purposes)
export function generateStandaloneLeader(): Leader {
  const { firstName, lastName } = generateFrenchName()
  const { role, type } = pickWeightedRole()

  // 15% chance to have a usage name (nom d'usage)
  const hasUsageName = Math.random() < 0.15
  const usageName = hasUsageName ? faker.helpers.arrayElement(USAGE_NAME_TYPES) : null

  // 10% chance to have a pseudo/nickname
  const hasPseudo = Math.random() < 0.1
  const pseudo = hasPseudo ? faker.person.firstName() : null

  // Generate event name (leadership change event)
  const eventName = faker.helpers.arrayElement(LEADERSHIP_EVENTS)

  return {
    id: undefined as never, // Force undefined for Prisma auto-generated ID
    siren: faker.string.numeric(9), // Generate random SIREN for standalone leader
    role: role,
    last_name: lastName,
    first_name: firstName,
    gestion_number: generateGestionNumber(),
    type: type,
    event_name: eventName,
    usage_name: usageName,
    pseudo: pseudo,
    company_name: generateCompanyName(),
    legal_form: generateLegalForm(),
    id_data: generateIdData(),
  } satisfies Leader
}

// Generate multiple leaders for a company (some companies have multiple executives)
export function generateLeadersForCompany(
  companySiren: string,
  companyName: string,
  companyLegalForm: string,
  numberOfLeaders: number = 1,
): Leader[] {
  const leaders: Leader[] = []

  for (let i = 0; i < numberOfLeaders; i++) {
    const leader = generateLeader(companySiren, companyName)
    // Override legal form to match company
    leader.legal_form = companyLegalForm
    leaders.push(leader)
  }

  return leaders
}

// Generate leaders with realistic distribution
// Most companies have 1-3 leaders, larger companies may have more
export function generateRealisticLeadersForCompany(
  companySiren: string,
  companyName: string,
  companyLegalForm: string,
  companySize: 'small' | 'medium' | 'large' = 'small',
): Leader[] {
  let numberOfLeaders: number

  switch (companySize) {
    case 'small': {
      // 70% have 1 leader, 25% have 2, 5% have 3
      const rand = Math.random()
      if (rand < 0.7) numberOfLeaders = 1
      else if (rand < 0.95) numberOfLeaders = 2
      else numberOfLeaders = 3
      break
    }
    case 'medium': {
      // 40% have 2 leaders, 35% have 3, 20% have 4, 5% have 5
      const rand = Math.random()
      if (rand < 0.4) numberOfLeaders = 2
      else if (rand < 0.75) numberOfLeaders = 3
      else if (rand < 0.95) numberOfLeaders = 4
      else numberOfLeaders = 5
      break
    }
    case 'large': {
      // 20% have 3 leaders, 30% have 4, 25% have 5, 15% have 6, 10% have 7+
      const randLarge = Math.random()
      if (randLarge < 0.2) numberOfLeaders = 3
      else if (randLarge < 0.5) numberOfLeaders = 4
      else if (randLarge < 0.75) numberOfLeaders = 5
      else if (randLarge < 0.9) numberOfLeaders = 6
      else numberOfLeaders = 7 + Math.floor(Math.random() * 3) // 7-9 leaders
      break
    }
  }

  return generateLeadersForCompany(companySiren, companyName, companyLegalForm, numberOfLeaders)
}
