import { RegionType } from './regions'

export interface CityLocation {
  city: string
  department: string
  departmentNumber: string
  region: RegionType
  postalCodePattern: string
}

export const CITY_DEPARTMENT_MAPPING: CityLocation[] = [
  // Île-de-France
  {
    city: 'Paris',
    department: 'Paris',
    departmentNumber: '75',
    region: 'Île-de-France',
    postalCodePattern: '75###',
  },
  {
    city: 'Boulogne-Billancourt',
    department: 'Hauts-de-Seine',
    departmentNumber: '92',
    region: 'Île-de-France',
    postalCodePattern: '92###',
  },
  {
    city: 'Saint-Denis',
    department: 'Seine-Saint-Denis',
    departmentNumber: '93',
    region: 'Île-de-France',
    postalCodePattern: '93###',
  },
  {
    city: 'Créteil',
    department: 'Val-de-Marne',
    departmentNumber: '94',
    region: 'Île-de-France',
    postalCodePattern: '94###',
  },
  {
    city: 'Nanterre',
    department: 'Hauts-de-Seine',
    departmentNumber: '92',
    region: 'Île-de-France',
    postalCodePattern: '92###',
  },

  // Provence-Alpes-Côte d'Azur
  {
    city: 'Marseille',
    department: 'Bouches-du-Rhône',
    departmentNumber: '13',
    region: "Provence-Alpes-Côte d'Azur",
    postalCodePattern: '13###',
  },
  {
    city: 'Nice',
    department: 'Alpes-Maritimes',
    departmentNumber: '06',
    region: "Provence-Alpes-Côte d'Azur",
    postalCodePattern: '06###',
  },
  {
    city: 'Toulon',
    department: 'Var',
    departmentNumber: '83',
    region: "Provence-Alpes-Côte d'Azur",
    postalCodePattern: '83###',
  },
  {
    city: 'Aix-en-Provence',
    department: 'Bouches-du-Rhône',
    departmentNumber: '13',
    region: "Provence-Alpes-Côte d'Azur",
    postalCodePattern: '13###',
  },

  // Auvergne-Rhône-Alpes
  {
    city: 'Lyon',
    department: 'Rhône',
    departmentNumber: '69',
    region: 'Auvergne-Rhône-Alpes',
    postalCodePattern: '69###',
  },
  {
    city: 'Grenoble',
    department: 'Isère',
    departmentNumber: '38',
    region: 'Auvergne-Rhône-Alpes',
    postalCodePattern: '38###',
  },
  {
    city: 'Saint-Étienne',
    department: 'Loire',
    departmentNumber: '42',
    region: 'Auvergne-Rhône-Alpes',
    postalCodePattern: '42###',
  },
  {
    city: 'Clermont-Ferrand',
    department: 'Puy-de-Dôme',
    departmentNumber: '63',
    region: 'Auvergne-Rhône-Alpes',
    postalCodePattern: '63###',
  },
  {
    city: 'Villeurbanne',
    department: 'Rhône',
    departmentNumber: '69',
    region: 'Auvergne-Rhône-Alpes',
    postalCodePattern: '69###',
  },

  // Occitanie
  {
    city: 'Toulouse',
    department: 'Haute-Garonne',
    departmentNumber: '31',
    region: 'Occitanie',
    postalCodePattern: '31###',
  },
  {
    city: 'Montpellier',
    department: 'Hérault',
    departmentNumber: '34',
    region: 'Occitanie',
    postalCodePattern: '34###',
  },
  {
    city: 'Nîmes',
    department: 'Gard',
    departmentNumber: '30',
    region: 'Occitanie',
    postalCodePattern: '30###',
  },
  {
    city: 'Perpignan',
    department: 'Pyrénées-Orientales',
    departmentNumber: '66',
    region: 'Occitanie',
    postalCodePattern: '66###',
  },

  // Pays de la Loire
  {
    city: 'Nantes',
    department: 'Loire-Atlantique',
    departmentNumber: '44',
    region: 'Pays de la Loire',
    postalCodePattern: '44###',
  },
  {
    city: 'Angers',
    department: 'Maine-et-Loire',
    departmentNumber: '49',
    region: 'Pays de la Loire',
    postalCodePattern: '49###',
  },
  {
    city: 'Le Mans',
    department: 'Sarthe',
    departmentNumber: '72',
    region: 'Pays de la Loire',
    postalCodePattern: '72###',
  },

  // Grand Est
  {
    city: 'Strasbourg',
    department: 'Bas-Rhin',
    departmentNumber: '67',
    region: 'Grand Est',
    postalCodePattern: '67###',
  },
  {
    city: 'Reims',
    department: 'Marne',
    departmentNumber: '51',
    region: 'Grand Est',
    postalCodePattern: '51###',
  },
  {
    city: 'Metz',
    department: 'Moselle',
    departmentNumber: '57',
    region: 'Grand Est',
    postalCodePattern: '57###',
  },
  {
    city: 'Nancy',
    department: 'Meurthe-et-Moselle',
    departmentNumber: '54',
    region: 'Grand Est',
    postalCodePattern: '54###',
  },

  // Nouvelle-Aquitaine
  {
    city: 'Bordeaux',
    department: 'Gironde',
    departmentNumber: '33',
    region: 'Nouvelle-Aquitaine',
    postalCodePattern: '33###',
  },
  {
    city: 'Limoges',
    department: 'Haute-Vienne',
    departmentNumber: '87',
    region: 'Nouvelle-Aquitaine',
    postalCodePattern: '87###',
  },
  {
    city: 'Poitiers',
    department: 'Vienne',
    departmentNumber: '86',
    region: 'Nouvelle-Aquitaine',
    postalCodePattern: '86###',
  },

  // Hauts-de-France
  {
    city: 'Lille',
    department: 'Nord',
    departmentNumber: '59',
    region: 'Hauts-de-France',
    postalCodePattern: '59###',
  },
  {
    city: 'Amiens',
    department: 'Somme',
    departmentNumber: '80',
    region: 'Hauts-de-France',
    postalCodePattern: '80###',
  },

  // Bretagne
  {
    city: 'Rennes',
    department: 'Ille-et-Vilaine',
    departmentNumber: '35',
    region: 'Bretagne',
    postalCodePattern: '35###',
  },
  {
    city: 'Brest',
    department: 'Finistère',
    departmentNumber: '29',
    region: 'Bretagne',
    postalCodePattern: '29###',
  },

  // Normandie
  {
    city: 'Le Havre',
    department: 'Seine-Maritime',
    departmentNumber: '76',
    region: 'Normandie',
    postalCodePattern: '76###',
  },
  {
    city: 'Rouen',
    department: 'Seine-Maritime',
    departmentNumber: '76',
    region: 'Normandie',
    postalCodePattern: '76###',
  },
  {
    city: 'Caen',
    department: 'Calvados',
    departmentNumber: '14',
    region: 'Normandie',
    postalCodePattern: '14###',
  },

  // Bourgogne-Franche-Comté
  {
    city: 'Dijon',
    department: "Côte-d'Or",
    departmentNumber: '21',
    region: 'Bourgogne-Franche-Comté',
    postalCodePattern: '21###',
  },
  {
    city: 'Besançon',
    department: 'Doubs',
    departmentNumber: '25',
    region: 'Bourgogne-Franche-Comté',
    postalCodePattern: '25###',
  },

  // Centre-Val de Loire
  {
    city: 'Orléans',
    department: 'Loiret',
    departmentNumber: '45',
    region: 'Centre-Val de Loire',
    postalCodePattern: '45###',
  },
  {
    city: 'Tours',
    department: 'Indre-et-Loire',
    departmentNumber: '37',
    region: 'Centre-Val de Loire',
    postalCodePattern: '37###',
  },
  {
    city: 'Bourges',
    department: 'Cher',
    departmentNumber: '18',
    region: 'Centre-Val de Loire',
    postalCodePattern: '18###',
  },

  // Corse
  {
    city: 'Ajaccio',
    department: 'Corse-du-Sud',
    departmentNumber: '2A',
    region: 'Corse',
    postalCodePattern: '20###',
  },
  {
    city: 'Bastia',
    department: 'Haute-Corse',
    departmentNumber: '2B',
    region: 'Corse',
    postalCodePattern: '20###',
  },
]

export function getRandomCityLocation() {
  return CITY_DEPARTMENT_MAPPING[Math.floor(Math.random() * CITY_DEPARTMENT_MAPPING.length)]
}

export function generatePostalCode(pattern: string): string {
  return pattern.replace(/#/g, () => Math.floor(Math.random() * 10).toString())
}
