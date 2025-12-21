export const CITIES = [
  // Île-de-France
  'Paris',

  // Provence-Alpes-Côte d'Azur
  'Marseille',
  'Nice',
  'Toulon',
  'Aix-en-Provence',

  // Auvergne-Rhône-Alpes
  'Lyon',
  'Grenoble',
  'Clermont-Ferrand',
  'Saint-Étienne',
  'Villeurbanne',

  // Occitanie
  'Toulouse',
  'Montpellier',
  'Nîmes',
  'Perpignan',

  // Pays de la Loire
  'Nantes',
  'Angers',

  // Grand Est
  'Strasbourg',
  'Reims',
  'Metz',

  // Nouvelle-Aquitaine
  'Bordeaux',
  'Limoges',

  // Hauts-de-France
  'Lille',
  'Amiens',

  // Bretagne
  'Rennes',
  'Brest',

  // Normandie
  'Le Havre',
  'Caen',

  // Bourgogne-Franche-Comté
  'Dijon',

  // Centre-Val de Loire
  'Tours',
  'Orléans',

  // Outre-mer
  'Saint-Denis', // La Réunion
  'Cayenne', // Guyane
  'Fort-de-France', // Martinique
  'Pointe-à-Pitre', // Guadeloupe
  'Mamoudzou', // Mayotte
] as const

export type CityTypes = (typeof CITIES)[number]

export const POSTAL_CODES_BY_CITY: Record<CityTypes, string> = {
  // Île-de-France
  Paris: '75000',

  // Provence-Alpes-Côte d'Azur
  Marseille: '13000',
  Nice: '06000',
  Toulon: '83000',
  'Aix-en-Provence': '13100',

  // Auvergne-Rhône-Alpes
  Lyon: '69000',
  Grenoble: '38000',
  'Clermont-Ferrand': '63000',
  'Saint-Étienne': '42000',
  Villeurbanne: '69100',

  // Occitanie
  Toulouse: '31000',
  Montpellier: '34000',
  Nîmes: '30000',
  Perpignan: '66000',

  // Pays de la Loire
  Nantes: '44000',
  Angers: '49000',

  // Grand Est
  Strasbourg: '67000',
  Reims: '51100',
  Metz: '57000',

  // Nouvelle-Aquitaine
  Bordeaux: '33000',
  Limoges: '87000',

  // Hauts-de-France
  Lille: '59000',
  Amiens: '80000',

  // Bretagne
  Rennes: '35000',
  Brest: '29200',

  // Normandie
  'Le Havre': '76600',
  Caen: '14000',

  // Bourgogne-Franche-Comté
  Dijon: '21000',

  // Centre-Val de Loire
  Tours: '37000',
  Orléans: '45000',

  // Outre-mer
  'Saint-Denis': '97400', // La Réunion
  Cayenne: '97300', // Guyane
  'Fort-de-France': '97200', // Martinique
  'Pointe-à-Pitre': '97110', // Guadeloupe
  Mamoudzou: '97600', // Mayotte
} as const
