import { faker } from '@faker-js/faker'
import { UserQuota } from '../../generated/prisma'

// Quota allocation tiers (realistic business model)
const QUOTA_TIERS = {
  FREE: { min: 10, max: 50, weight: 0.4 }, // 40% - Free tier users
  BASIC: { min: 100, max: 500, weight: 0.3 }, // 30% - Basic paid users
  PREMIUM: { min: 1000, max: 5000, weight: 0.2 }, // 20% - Premium users
  ENTERPRISE: { min: 10000, max: 50000, weight: 0.1 }, // 10% - Enterprise users
} as const

// Usage patterns (how much of allocated quota is typically used)
const USAGE_PATTERNS = {
  LIGHT: { min: 0.1, max: 0.3, weight: 0.25 }, // 25% - Light users (10-30% usage)
  MODERATE: { min: 0.3, max: 0.7, weight: 0.45 }, // 45% - Moderate users (30-70% usage)
  HEAVY: { min: 0.7, max: 0.95, weight: 0.25 }, // 25% - Heavy users (70-95% usage)
  EXHAUSTED: { min: 0.95, max: 1.0, weight: 0.05 }, // 5% - Users at quota limit
} as const

function generateUserId(): string {
  // Reuse the same pattern as UserCompanyStatus for consistency
  const patterns = [
    'user_{uuid}',
    'usr_{random}',
    'client_{number}',
    'admin_{uuid}',
    'guest_{random}',
  ] as const

  const pattern = faker.helpers.arrayElement(patterns)

  switch (pattern) {
    case 'user_{uuid}':
      return `user_${faker.string.uuid()}`
    case 'usr_{random}':
      return `usr_${faker.string.alphanumeric(8)}`
    case 'client_{number}':
      return `client_${faker.string.numeric(6)}`
    case 'admin_{uuid}':
      return `admin_${faker.string.uuid()}`
    case 'guest_{random}':
      return `guest_${faker.string.alphanumeric(6)}`
    default:
      return `user_${faker.string.uuid()}`
  }
}

function pickWeightedQuotaTier(): { min: number; max: number } {
  const totalWeight = Object.values(QUOTA_TIERS).reduce((sum, tier) => sum + tier.weight, 0)
  let random = Math.random() * totalWeight

  for (const tier of Object.values(QUOTA_TIERS)) {
    random -= tier.weight
    if (random <= 0) {
      return { min: tier.min, max: tier.max }
    }
  }

  // Fallback to FREE tier
  return { min: QUOTA_TIERS.FREE.min, max: QUOTA_TIERS.FREE.max }
}

function pickWeightedUsagePattern(): { min: number; max: number } {
  const totalWeight = Object.values(USAGE_PATTERNS).reduce(
    (sum, pattern) => sum + pattern.weight,
    0,
  )
  let random = Math.random() * totalWeight

  for (const pattern of Object.values(USAGE_PATTERNS)) {
    random -= pattern.weight
    if (random <= 0) {
      return { min: pattern.min, max: pattern.max }
    }
  }

  // Fallback to MODERATE usage
  return { min: USAGE_PATTERNS.MODERATE.min, max: USAGE_PATTERNS.MODERATE.max }
}

function generateQuotaAllocated(): number {
  const tier = pickWeightedQuotaTier()
  return faker.number.int({ min: tier.min, max: tier.max })
}

function generateQuotaUsed(quotaAllocated: number): number {
  const usagePattern = pickWeightedUsagePattern()
  const usageRatio = faker.number.float({
    min: usagePattern.min,
    max: usagePattern.max,
    fractionDigits: 2,
  })

  return Math.floor(quotaAllocated * usageRatio)
}

export function generateUserQuota(): UserQuota {
  const quotaAllocated = generateQuotaAllocated()
  const quotaUsed = generateQuotaUsed(quotaAllocated)

  return {
    user_id: generateUserId(),
    quota_allocated: quotaAllocated,
    quota_used: quotaUsed,
  } satisfies UserQuota
}

// Generate quota for a specific user
export function generateUserQuotaForUser(
  userId: string,
  tier?: keyof typeof QUOTA_TIERS,
): UserQuota {
  let quotaAllocated: number

  if (tier) {
    const tierData = QUOTA_TIERS[tier]
    quotaAllocated = faker.number.int({ min: tierData.min, max: tierData.max })
  } else {
    quotaAllocated = generateQuotaAllocated()
  }

  const quotaUsed = generateQuotaUsed(quotaAllocated)

  return {
    user_id: userId,
    quota_allocated: quotaAllocated,
    quota_used: quotaUsed,
  } satisfies UserQuota
}

// Generate multiple quotas with realistic distribution
export function generateUserQuotas(count: number): UserQuota[] {
  const quotas: UserQuota[] = []

  for (let i = 0; i < count; i++) {
    quotas.push(generateUserQuota())
  }

  return quotas
}

// Generate quotas for existing users (from UserCompanyStatus)
export function generateUserQuotasForUsers(userIds: string[]): UserQuota[] {
  return userIds.map(userId => generateUserQuotaForUser(userId))
}

// Generate quotas with specific business scenarios
export function generateBusinessScenarioQuotas(): {
  freeUsers: UserQuota[]
  paidUsers: UserQuota[]
  enterpriseUsers: UserQuota[]
} {
  const freeUsers = Array.from({ length: 40 }, () =>
    generateUserQuotaForUser(generateUserId(), 'FREE'),
  )
  const paidUsers = Array.from({ length: 30 }, () =>
    generateUserQuotaForUser(generateUserId(), 'BASIC'),
  )
  const enterpriseUsers = Array.from({ length: 10 }, () =>
    generateUserQuotaForUser(generateUserId(), 'ENTERPRISE'),
  )

  return {
    freeUsers,
    paidUsers,
    enterpriseUsers,
  }
}

// Generate quota with specific usage patterns
export function generateQuotaWithUsagePattern(
  userId: string,
  quotaAllocated: number,
  usagePattern: 'light' | 'moderate' | 'heavy' | 'exhausted',
): UserQuota {
  let usageRatio: number

  switch (usagePattern) {
    case 'light':
      usageRatio = faker.number.float({ min: 0.1, max: 0.3, fractionDigits: 2 })
      break
    case 'moderate':
      usageRatio = faker.number.float({ min: 0.3, max: 0.7, fractionDigits: 2 })
      break
    case 'heavy':
      usageRatio = faker.number.float({ min: 0.7, max: 0.95, fractionDigits: 2 })
      break
    case 'exhausted':
      usageRatio = faker.number.float({ min: 0.95, max: 1.0, fractionDigits: 2 })
      break
  }

  const quotaUsed = Math.floor(quotaAllocated * usageRatio)

  return {
    user_id: userId,
    quota_allocated: quotaAllocated,
    quota_used: quotaUsed,
  } satisfies UserQuota
}

// Generate quota with realistic monthly reset patterns
export function generateQuotaWithResetPattern(
  userId: string,
  baseQuota: number,
  daysSinceReset: number = 0,
): UserQuota {
  // Simulate usage accumulation over time
  const maxDaysInMonth = 30
  const usageProgress = Math.min(daysSinceReset / maxDaysInMonth, 1)

  // Usage tends to be higher later in the month
  const usageMultiplier = 0.3 + usageProgress * 0.7 // 30% to 100% based on time
  const usageRatio = faker.number.float({
    min: 0.1,
    max: usageMultiplier,
    fractionDigits: 2,
  })

  const quotaUsed = Math.floor(baseQuota * usageRatio)

  return {
    user_id: userId,
    quota_allocated: baseQuota,
    quota_used: quotaUsed,
  } satisfies UserQuota
}
