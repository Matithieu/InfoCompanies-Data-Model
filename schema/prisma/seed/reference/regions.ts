import { DepartmentTypes } from './departments'

export const REGIONS = [
  'Auvergne-Rhône-Alpes',
  'Bourgogne-Franche-Comté',
  'Bretagne',
  'Centre-Val de Loire',
  'Corse',
  'Grand Est',
  'Hauts-de-France',
  'Île-de-France',
  'Normandie',
  'Nouvelle-Aquitaine',
  'Occitanie',
  'Pays de la Loire',
  "Provence-Alpes-Côte d'Azur",
  'Guadeloupe',
  'Martinique',
  'Guyane',
  'La Réunion',
  'Mayotte',
] as const

export type RegionType = (typeof REGIONS)[number]

export const DEPARTMENTS_BY_REGION: Record<RegionType, DepartmentTypes[]> = {
  'Auvergne-Rhône-Alpes': ['Ain', 'Haute-Savoie', 'Puy-de-Dôme'],
  'Bourgogne-Franche-Comté': ["Côte-d'Or", 'Doubs', 'Yonne'],
  Bretagne: ['Finistère', 'Ille-et-Vilaine', 'Morbihan'],
  'Centre-Val de Loire': ['Indre-et-Loire', 'Loiret', 'Cher'],
  Corse: ['Corse-du-Sud', 'Haute-Corse'],
  'Grand Est': ['Bas-Rhin', 'Moselle', 'Marne'],
  'Hauts-de-France': ['Nord', 'Pas-de-Calais', 'Somme'],
  'Île-de-France': ['Paris', 'Hauts-de-Seine', 'Val-de-Marne'],
  Normandie: ['Calvados', 'Manche', 'Seine-Maritime'],
  'Nouvelle-Aquitaine': ['Gironde', 'Dordogne', 'Pyrénées-Atlantiques'],
  Occitanie: ['Haute-Garonne', 'Hérault', 'Gard'],
  'Pays de la Loire': ['Loire-Atlantique', 'Maine-et-Loire', 'Vendée'],
  "Provence-Alpes-Côte d'Azur": ['Alpes-Maritimes', 'Bouches-du-Rhône', 'Var'],
  Guadeloupe: ['Guadeloupe (971)'],
  Martinique: ['Martinique (972)'],
  Guyane: ['Guyane (973)'],
  'La Réunion': ['La Réunion (974)'],
  Mayotte: ['Mayotte (976)'],
} as const
