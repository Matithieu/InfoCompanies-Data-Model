import { faker } from '@faker-js/faker'
import { LegalFormTypes } from '../reference/legalForms'
import { IndustrySectorTypes } from '../reference/industries'

export function determineLegalFormFromEmployeeNumber(numberOfEmployees: number): LegalFormTypes {
  if (numberOfEmployees <= 1) {
    return 'EI (Entreprise Individuelle)'
  } else if (numberOfEmployees <= 10) {
    return 'Micro-entreprise (Auto-entrepreneur)'
  } else if (numberOfEmployees <= 50) {
    return 'EURL (Entreprise Unipersonnelle à Responsabilité Limitée)'
  } else if (numberOfEmployees <= 250) {
    return 'SARL (Société à Responsabilité Limitée)'
  } else {
    return 'SA (Société Anonyme)'
  }
}

export function generateRealisticEmployeeNumber(industry: IndustrySectorTypes): number {
  // Define typical employee ranges for each industry
  const getEmployeeRange = (sector: IndustrySectorTypes) => {
    const ranges = {
      'Agriculture, Sylviculture, Pêche et Chasse': { min: 1, max: 50, typical: 8 },
      'Mines, Carrières et Extraction de Pétrole et de Gaz': { min: 10, max: 500, typical: 80 },
      'Services Publics': { min: 50, max: 1000, typical: 200 },
      Construction: { min: 2, max: 200, typical: 15 },
      Fabrication: { min: 5, max: 1000, typical: 50 },
      'Commerce de Gros': { min: 2, max: 100, typical: 12 },
      'Commerce de Détail': { min: 1, max: 50, typical: 8 },
      'Transport et Entreposage': { min: 3, max: 200, typical: 25 },
      Information: { min: 1, max: 100, typical: 15 },
      'Finance et Assurance': { min: 5, max: 500, typical: 35 },
      'Immobilier et Location': { min: 1, max: 30, typical: 6 },
      'Services Professionnels, Scientifiques et Techniques': { min: 1, max: 50, typical: 8 },
      "Gestion d'Entreprises": { min: 5, max: 200, typical: 25 },
      'Services Administratifs et de Soutien et Gestion des Déchets': {
        min: 2,
        max: 100,
        typical: 20,
      },
      'Services Éducatifs': { min: 2, max: 100, typical: 15 },
      'Soins de Santé et Assistance Sociale': { min: 1, max: 200, typical: 12 },
      'Arts, Spectacles et Loisirs': { min: 1, max: 50, typical: 5 },
      'Hébergement et Services de Restauration': { min: 2, max: 100, typical: 12 },
      'Autres Services (sauf Administration Publique)': { min: 1, max: 20, typical: 4 },
      'Administration Publique': { min: 10, max: 2000, typical: 150 },
    }
    return ranges[sector] || { min: 1, max: 50, typical: 8 }
  }

  const { min, max, typical } = getEmployeeRange(industry)

  // 70% chance to be close to typical, 30% chance to be at extremes
  if (faker.datatype.boolean(0.7)) {
    // Generate around typical value with some variation
    const variation = typical * 0.5
    return faker.number.int({
      min: Math.max(min, Math.round(typical - variation)),
      max: Math.min(max, Math.round(typical + variation)),
    })
  } else {
    // Generate from full range for outliers
    return faker.number.int({ min, max })
  }
}

export function determineCompanyCategoryFromEmployees(numberOfEmployees: number): string {
  if (numberOfEmployees <= 9) {
    return 'Micro-entreprise'
  } else if (numberOfEmployees <= 49) {
    return 'TPE' // Très Petite Entreprise
  } else if (numberOfEmployees <= 249) {
    return 'PME' // Petite et Moyenne Entreprise
  } else if (numberOfEmployees <= 4999) {
    return 'ETI' // Entreprise de Taille Intermédiaire
  } else {
    return 'Grande entreprise'
  }
}
