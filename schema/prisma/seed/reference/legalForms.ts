export const LEGAL_FORMS = [
  'SARL (Société à Responsabilité Limitée)',
  'SAS (Société par Actions Simplifiée)',
  'SASU (Société par Actions Simplifiée Unipersonnelle)',
  'SA (Société Anonyme)',
  'SNC (Société en Nom Collectif)',
  'SCS (Société en Commandite Simple)',
  'SCA (Société en Commandite par Actions)',
  'EURL (Entreprise Unipersonnelle à Responsabilité Limitée)',
  'EI (Entreprise Individuelle)',
  'Micro-entreprise (Auto-entrepreneur)',
  'EIRL (Entreprise Individuelle à Responsabilité Limitée)',
  'Association',
  'Coopérative (SCOP/SCIC)',
  "GIE (Groupement d'Intérêt Économique)",
  'SCI (Société Civile Immobilière)',
] as const

export type LegalFormTypes = (typeof LEGAL_FORMS)[number]
