import { CityTypes } from './cities'

export const DEPARTMENTS = [
  'Ain',
  'Haute-Savoie',
  'Puy-de-Dôme',
  "Côte-d'Or",
  'Doubs',
  'Yonne',
  'Finistère',
  'Ille-et-Vilaine',
  'Morbihan',
  'Indre-et-Loire',
  'Loiret',
  'Cher',
  'Corse-du-Sud',
  'Haute-Corse',
  'Bas-Rhin',
  'Moselle',
  'Marne',
  'Nord',
  'Pas-de-Calais',
  'Somme',
  'Paris',
  'Hauts-de-Seine',
  'Val-de-Marne',
  'Calvados',
  'Manche',
  'Seine-Maritime',
  'Gironde',
  'Dordogne',
  'Pyrénées-Atlantiques',
  'Haute-Garonne',
  'Hérault',
  'Gard',
  'Loire-Atlantique',
  'Maine-et-Loire',
  'Vendée',
  'Alpes-Maritimes',
  'Bouches-du-Rhône',
  'Var',
  'Guadeloupe (971)',
  'Martinique (972)',
  'Guyane (973)',
  'La Réunion (974)',
  'Mayotte (976)',
] as const

export type DepartmentTypes = (typeof DEPARTMENTS)[number]

export const CITIES_BY_DEPARTMENT: Record<DepartmentTypes, CityTypes[]> = {
  // Auvergne-Rhône-Alpes
  Ain: ['Lyon', 'Villeurbanne'],
  'Haute-Savoie': ['Grenoble'],
  'Puy-de-Dôme': ['Clermont-Ferrand'],

  // Bourgogne-Franche-Comté
  "Côte-d'Or": ['Dijon'],
  Doubs: [],
  Yonne: [],

  // Bretagne
  Finistère: ['Brest'],
  'Ille-et-Vilaine': ['Rennes'],
  Morbihan: [],

  // Centre-Val de Loire
  'Indre-et-Loire': ['Tours'],
  Loiret: ['Orléans'],
  Cher: [],

  // Corse
  'Corse-du-Sud': [],
  'Haute-Corse': [],

  // Grand Est
  'Bas-Rhin': ['Strasbourg'],
  Moselle: ['Metz'],
  Marne: ['Reims'],

  // Hauts-de-France
  Nord: ['Lille'],
  'Pas-de-Calais': [],
  Somme: ['Amiens'],

  // Île-de-France
  Paris: ['Paris'],
  'Hauts-de-Seine': [],
  'Val-de-Marne': [],

  // Normandie
  Calvados: ['Caen'],
  Manche: [],
  'Seine-Maritime': ['Le Havre'],

  // Nouvelle-Aquitaine
  Gironde: ['Bordeaux'],
  Dordogne: [],
  'Pyrénées-Atlantiques': [],

  // Occitanie
  'Haute-Garonne': ['Toulouse'],
  Hérault: ['Montpellier'],
  Gard: ['Nîmes'],

  // Pays de la Loire
  'Loire-Atlantique': ['Nantes'],
  'Maine-et-Loire': ['Angers'],
  Vendée: [],

  // Provence-Alpes-Côte d'Azur
  'Alpes-Maritimes': ['Nice'],
  'Bouches-du-Rhône': ['Marseille', 'Aix-en-Provence'],
  Var: ['Toulon'],

  // Outre-mer
  'Guadeloupe (971)': ['Pointe-à-Pitre'],
  'Martinique (972)': ['Fort-de-France'],
  'Guyane (973)': ['Cayenne'],
  'La Réunion (974)': ['Saint-Denis'],
  'Mayotte (976)': ['Mamoudzou'],
} as const
