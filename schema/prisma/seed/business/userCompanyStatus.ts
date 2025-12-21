import { faker } from '@faker-js/faker'
import { Status, UserCompanyStatus } from '../../generated/prisma'

// User ID patterns (could be UUIDs, email-based, or custom IDs)
const USER_ID_PATTERNS = [
  'user_{uuid}',
  'usr_{random}',
  'client_{number}',
  'admin_{uuid}',
  'guest_{random}',
] as const

// Status distribution weights (realistic usage patterns)
const STATUS_DISTRIBUTION = {
  NOT_DONE: 0.15, // 15% - New companies not yet processed
  TO_DO: 0.25, // 25% - Companies queued for processing
  DONE: 0.6, // 60% - Companies already processed
} as const

function generateUserId(): string {
  const pattern = faker.helpers.arrayElement(USER_ID_PATTERNS)

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

function pickWeightedStatus(): Status {
  const totalWeight = Object.values(STATUS_DISTRIBUTION).reduce((sum, weight) => sum + weight, 0)
  let random = Math.random() * totalWeight

  for (const [status, weight] of Object.entries(STATUS_DISTRIBUTION)) {
    random -= weight
    if (random <= 0) {
      return status as Status
    }
  }

  // Fallback to DONE (most common)
  return 'DONE'
}

export function generateUserCompanyStatus(companyId?: number): UserCompanyStatus {
  return {
    id: undefined as never, // Force undefined for Prisma auto-generated ID
    user_id: generateUserId(),
    status: pickWeightedStatus(),
    company_id: companyId || faker.number.int({ min: 1, max: 10000 }),
  } satisfies UserCompanyStatus
}

// Generate multiple statuses for a single company (multiple users can interact with same company)
export function generateUserCompanyStatusesForCompany(
  companyId: number,
  numberOfUsers: number = 1,
): UserCompanyStatus[] {
  const statuses: UserCompanyStatus[] = []

  for (let i = 0; i < numberOfUsers; i++) {
    const status = generateUserCompanyStatus(companyId)
    statuses.push(status)
  }

  return statuses
}

// Generate statuses with realistic user behavior patterns
export function generateRealisticUserCompanyStatuses(companyIds: number[]): UserCompanyStatus[] {
  const allStatuses: UserCompanyStatus[] = []

  for (const companyId of companyIds) {
    // Some companies have no user interactions (20% chance)
    if (Math.random() < 0.2) {
      continue
    }

    // Determine number of users for this company
    // Most companies have 1-2 users, some have more
    let numberOfUsers: number
    const rand = Math.random()

    if (rand < 0.6) {
      numberOfUsers = 1
    } else if (rand < 0.85) {
      numberOfUsers = 2
    } else if (rand < 0.95) {
      numberOfUsers = 3
    } else {
      numberOfUsers = 4 + Math.floor(Math.random() * 3) // 4-6 users
    }

    const companyStatuses = generateUserCompanyStatusesForCompany(companyId, numberOfUsers)
    allStatuses.push(...companyStatuses)
  }

  return allStatuses
}

// Generate statuses for a specific user across multiple companies
export function generateUserCompanyStatusesForUser(
  userId: string,
  companyIds: number[],
  statusDistribution?: Partial<typeof STATUS_DISTRIBUTION>,
): UserCompanyStatus[] {
  const statuses: UserCompanyStatus[] = []

  // Use custom distribution if provided, otherwise use default
  const distribution = statusDistribution
    ? { ...STATUS_DISTRIBUTION, ...statusDistribution }
    : STATUS_DISTRIBUTION

  for (const companyId of companyIds) {
    const status = generateUserCompanyStatus(companyId)
    status.user_id = userId

    // Apply custom status distribution
    const totalWeight = Object.values(distribution).reduce((sum, weight) => sum + weight, 0)
    let random = Math.random() * totalWeight

    for (const [statusName, weight] of Object.entries(distribution)) {
      random -= weight
      if (random <= 0) {
        status.status = statusName as Status
        break
      }
    }

    statuses.push(status)
  }

  return statuses
}

// Generate statuses with temporal patterns (recent activity)
export function generateRecentUserCompanyStatuses(companyIds: number[]): UserCompanyStatus[] {
  const statuses = generateRealisticUserCompanyStatuses(companyIds)

  // Add temporal information by modifying status based on recency
  // This is a simplified approach - in a real system you might have created_at timestamps
  return statuses.map(status => {
    // Recent activity is more likely to be TO_DO or DONE
    if (Math.random() < 0.8) {
      status.status = faker.helpers.arrayElement(['TO_DO', 'DONE'])
    }
    return status
  })
}
