import { faker } from '@faker-js/faker'
import { Config } from '../../generated/prisma'

// Typical reset dates for different patterns
function generateResetDate(pattern: string): Date {
  const now = new Date()

  switch (pattern) {
    case 'monthly':
      // Reset on 1st of current month
      return new Date(now.getFullYear(), now.getMonth(), 1)
    case 'weekly':
      // Reset on Monday of current week
      now.setDate(now.getDate() - now.getDay() + 1)
      return now
    case 'daily':
      // Reset at midnight today
      return new Date(now.getFullYear(), now.getMonth(), now.getDate())
    case 'yearly':
      // Reset on January 1st of current year
      return new Date(now.getFullYear(), 0, 1)
    default:
      // Default to monthly
      return new Date(now.getFullYear(), now.getMonth(), 1)
  }
}

export function generateConfig(): Config {
  // Most systems have a single config record
  // The last_reset_quota_date represents when quotas were last reset

  // 80% chance the reset was recent (within last 30 days)
  // 20% chance it was longer ago (system might be new or had issues)
  const isRecentReset = Math.random() < 0.8

  let lastResetDate: Date

  if (isRecentReset) {
    // Recent reset (within last 30 days)
    lastResetDate = faker.date.recent({ days: 30 })
  } else {
    // Older reset (up to 1 year ago)
    lastResetDate = faker.date.between({
      from: new Date(Date.now() - 365 * 24 * 60 * 60 * 1000),
      to: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000),
    })
  }

  return {
    id: undefined as never, // Force undefined for Prisma auto-generated ID
    last_reset_quota_date: lastResetDate,
  } satisfies Config
}

// Generate config with specific reset pattern
export function generateConfigWithResetPattern(
  pattern: 'monthly' | 'weekly' | 'daily' | 'yearly',
): Config {
  const lastResetDate = generateResetDate(pattern)

  return {
    id: undefined as never, // Force undefined for Prisma auto-generated ID
    last_reset_quota_date: lastResetDate,
  } satisfies Config
}

// Generate config for a new system (no previous resets)
export function generateNewSystemConfig(): Config {
  return {
    id: 0,
    last_reset_quota_date: null, // New system, no resets yet
  } satisfies Config
}

// Generate config for a system that needs quota reset soon
export function generateConfigNeedingReset(): Config {
  // Generate a date that's close to needing a reset
  // For monthly resets, this would be close to end of month
  const now = new Date()

  // Set reset date to be 25-29 days ago (close to needing reset)
  const daysAgo = faker.number.int({ min: 25, max: 29 })
  const lastResetDate = new Date(now.getTime() - daysAgo * 24 * 60 * 60 * 1000)

  return {
    id: undefined as never, // Force undefined for Prisma auto-generated ID
    last_reset_quota_date: lastResetDate,
  } satisfies Config
}

// Generate config for a system with recent reset
export function generateConfigWithRecentReset(): Config {
  // Reset within last 7 days
  const lastResetDate = faker.date.recent({ days: 7 })

  return {
    id: undefined as never, // Force undefined for Prisma auto-generated ID
    last_reset_quota_date: lastResetDate,
  } satisfies Config
}

// Generate multiple config scenarios for testing
export function generateConfigScenarios(): {
  newSystem: Config
  recentReset: Config
  needsReset: Config
  monthlyPattern: Config
  weeklyPattern: Config
} {
  return {
    newSystem: generateNewSystemConfig(),
    recentReset: generateConfigWithRecentReset(),
    needsReset: generateConfigNeedingReset(),
    monthlyPattern: generateConfigWithResetPattern('monthly'),
    weeklyPattern: generateConfigWithResetPattern('weekly'),
  }
}

// Generate config based on system state
export function generateConfigForSystemState(
  state: 'new' | 'active' | 'maintenance' | 'recovery',
): Config {
  switch (state) {
    case 'new':
      return generateNewSystemConfig()
    case 'active':
      return generateConfigWithRecentReset()
    case 'maintenance':
      return generateConfigNeedingReset()
    case 'recovery': {
      // System recovering from issues, reset was a while ago
      const recoveryDate = faker.date.between({
        from: new Date(Date.now() - 60 * 24 * 60 * 60 * 1000), // 60 days ago
        to: new Date(Date.now() - 15 * 24 * 60 * 60 * 1000), // 15 days ago
      })
      return {
        id: undefined as never, // Force undefined for Prisma auto-generated ID
        last_reset_quota_date: recoveryDate,
      } satisfies Config
    }
    default:
      return generateConfig()
  }
}
