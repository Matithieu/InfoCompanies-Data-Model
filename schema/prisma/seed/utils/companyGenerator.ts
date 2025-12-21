import { faker } from '@faker-js/faker'
import { IndustrySectorTypes } from '../reference/industries'

interface CompanyNameTemplate {
  prefixes: string[]
  suffixes: string[]
  businessTerms: string[]
}

const COMPANY_NAME_TEMPLATES: Record<IndustrySectorTypes, CompanyNameTemplate> = {
  'Agriculture, Sylviculture, Pêche et Chasse': {
    prefixes: ['Ferme', 'Domaine', 'Exploitation', 'Élevage', 'Vignoble'],
    suffixes: ['Bio', 'Agricole', 'Rural', 'Fermier', 'Naturel'],
    businessTerms: ['SARL', 'EARL', 'Coopérative', 'SCA'],
  },
  Construction: {
    prefixes: ['Bâtiment', 'Construction', 'Travaux', 'Rénovation', 'Maçonnerie'],
    suffixes: ['Plus', 'Pro', 'Expert', 'Service', 'Technique'],
    businessTerms: ['SARL', 'SAS', 'SA', 'EURL'],
  },
  'Commerce de Détail': {
    prefixes: ['Boutique', 'Magasin', 'Shop', 'Store', 'Espace'],
    suffixes: ['Plus', 'Central', 'Express', 'Direct', 'Premium'],
    businessTerms: ['SARL', 'SAS', 'EURL', 'SA'],
  },
  'Commerce de Gros': {
    prefixes: ['Distribution', 'Négoce', 'Import', 'Export', 'Grossiste'],
    suffixes: ['France', 'Europe', 'International', 'Plus', 'Pro'],
    businessTerms: ['SA', 'SAS', 'SARL'],
  },
  'Transport et Entreposage': {
    prefixes: ['Transport', 'Logistique', 'Express', 'Livraison', 'Fret'],
    suffixes: ['Rapide', 'Service', 'Plus', 'Pro', 'Europe'],
    businessTerms: ['SARL', 'SAS', 'SA'],
  },
  'Hébergement et Services de Restauration': {
    prefixes: ['Restaurant', 'Brasserie', 'Café', 'Hôtel', 'Auberge'],
    suffixes: ['Gourmet', 'Central', 'Plaza', 'Royal', 'du Centre'],
    businessTerms: ['SARL', 'SAS', 'EURL'],
  },
  Information: {
    prefixes: ['Digital', 'Tech', 'Web', 'Informatique', 'Solutions'],
    suffixes: ['Tech', 'Systems', 'Solutions', 'Services', 'Innovation'],
    businessTerms: ['SAS', 'SARL', 'SASU'],
  },
  'Services Professionnels, Scientifiques et Techniques': {
    prefixes: ['Conseil', 'Expertise', 'Bureau', 'Cabinet', 'Consulting'],
    suffixes: ['Conseil', 'Expertise', 'Solutions', 'Services', 'Partners'],
    businessTerms: ['SAS', 'SARL', 'SASU', 'SA'],
  },
  'Finance et Assurance': {
    prefixes: ['Assurance', 'Finance', 'Capital', 'Crédit', 'Banque'],
    suffixes: ['Assurance', 'Finance', 'Capital', 'Services', 'Conseil'],
    businessTerms: ['SA', 'SAS', 'SARL'],
  },
  'Immobilier et Location': {
    prefixes: ['Immobilier', 'Patrimoine', 'Résidence', 'Foncier', 'Habitat'],
    suffixes: ['Immobilier', 'Patrimoine', 'Services', 'Conseil', 'Plus'],
    businessTerms: ['SARL', 'SAS', 'SA', 'SCI'],
  },
  'Soins de Santé et Assistance Sociale': {
    prefixes: ['Centre', 'Clinique', 'Cabinet', 'Pharmacie', 'Laboratoire'],
    suffixes: ['Médical', 'Santé', 'Care', 'Plus', 'Service'],
    businessTerms: ['SARL', 'SAS', 'Association'],
  },
  'Services Éducatifs': {
    prefixes: ['École', 'Institut', 'Centre', 'Formation', 'Académie'],
    suffixes: ['Formation', 'Éducation', 'Enseignement', 'Pédagogie', 'Plus'],
    businessTerms: ['Association', 'SARL', 'SAS'],
  },
  'Arts, Spectacles et Loisirs': {
    prefixes: ['Studio', 'Création', 'Art', 'Spectacle', 'Loisirs'],
    suffixes: ['Production', 'Création', 'Entertainment', 'Plus', 'Studio'],
    businessTerms: ['SAS', 'SARL', 'Association', 'SASU'],
  },
  Fabrication: {
    prefixes: ['Industrie', 'Manufacturing', 'Production', 'Usine', 'Fabrication'],
    suffixes: ['Industries', 'Manufacturing', 'Production', 'France', 'Plus'],
    businessTerms: ['SA', 'SAS', 'SARL'],
  },
  'Services Publics': {
    prefixes: ['Service', 'Régie', 'Syndicat', 'Collectivité', 'Public'],
    suffixes: ['Services', 'Public', 'Municipal', 'Communal', 'Territorial'],
    businessTerms: ['Régie', 'EPIC', 'Association'],
  },
  'Administration Publique': {
    prefixes: ['Administration', 'Service', 'Direction', 'Département', 'Ministère'],
    suffixes: ['Public', 'État', 'Territorial', 'Municipal', 'Régional'],
    businessTerms: ['Service Public', 'Administration'],
  },
  'Mines, Carrières et Extraction de Pétrole et de Gaz': {
    prefixes: ['Mines', 'Carrière', 'Extraction', 'Ressources', 'Énergie'],
    suffixes: ['Extraction', 'Ressources', 'Énergie', 'Industries', 'France'],
    businessTerms: ['SA', 'SAS', 'SARL'],
  },
  "Gestion d'Entreprises": {
    prefixes: ['Groupe', 'Holding', 'Management', 'Gestion', 'Direction'],
    suffixes: ['Groupe', 'Holding', 'Management', 'Partners', 'Capital'],
    businessTerms: ['SA', 'SAS', 'Holding'],
  },
  'Services Administratifs et de Soutien et Gestion des Déchets': {
    prefixes: ['Service', 'Nettoyage', 'Propreté', 'Environnement', 'Recyclage'],
    suffixes: ['Services', 'Propreté', 'Environnement', 'Plus', 'Pro'],
    businessTerms: ['SARL', 'SAS', 'SA'],
  },
  'Autres Services (sauf Administration Publique)': {
    prefixes: ['Service', 'Prestation', 'Conseil', 'Assistance', 'Support'],
    suffixes: ['Services', 'Plus', 'Pro', 'Expert', 'Solutions'],
    businessTerms: ['SARL', 'SAS', 'EURL', 'Association'],
  },
}

export function generateRealisticCompanyName(industrySector: IndustrySectorTypes): string {
  const template = COMPANY_NAME_TEMPLATES[industrySector]

  if (!template) {
    return faker.company.name()
  }

  const usePersonName = faker.datatype.boolean(0.3) // 30% chance to use a person's name

  if (usePersonName) {
    const surname = faker.person.lastName()
    const prefix = faker.helpers.arrayElement(template.prefixes)
    return `${prefix} ${surname}`
  }

  const prefix = faker.helpers.arrayElement(template.prefixes)
  const suffix = faker.helpers.arrayElement(template.suffixes)

  // Sometimes use just prefix, sometimes prefix + suffix
  if (faker.datatype.boolean(0.4)) {
    return prefix
  }

  return `${prefix} ${suffix}`
}

export function generateSirenNumber(): string {
  return faker.string.numeric(9)
}

export function generateNicNumber(): string {
  return faker.string.numeric(5)
}

export function generateRealisticPhoneNumber(): string {
  // French phone number formats
  const formats = [
    '01 ## ## ## ##', // Île-de-France
    '02 ## ## ## ##', // Northwest
    '03 ## ## ## ##', // Northeast
    '04 ## ## ## ##', // Southeast
    '05 ## ## ## ##', // Southwest
    '06 ## ## ## ##', // Mobile
    '07 ## ## ## ##', // Mobile
  ]

  const format = faker.helpers.arrayElement(formats)
  return format.replace(/#/g, () => faker.string.numeric(1))
}

export function generateBusinessEmail(companyName: string): string {
  const cleanName = companyName
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, '')
    .replace(/\s+/g, '-')
    .substring(0, 20)

  const domains = [
    'gmail.com',
    'orange.fr',
    'free.fr',
    'wanadoo.fr',
    'sfr.fr',
    'outlook.fr',
    'yahoo.fr',
    cleanName + '.fr',
    cleanName + '.com',
  ]

  const localParts = ['contact', 'info', 'admin', 'direction', 'commercial', 'service']

  const localPart = faker.helpers.arrayElement(localParts)
  const domain = faker.helpers.arrayElement(domains)

  return `${localPart}@${domain}`
}
