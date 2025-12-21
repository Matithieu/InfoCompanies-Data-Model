/**
 * Environment-specific configurations for seeding
 */

import { SeedConfig } from '../types'

export const DEVELOPMENT_CONFIG: SeedConfig = {
  numberOfCompanies: 100,
  numberOfUsers: 50,
  generateTestData: true,
  clearExistingData: true,
  verbose: true,
}

export const TEST_CONFIG: SeedConfig = {
  numberOfCompanies: 10,
  numberOfUsers: 5,
  generateTestData: true,
  clearExistingData: true,
  verbose: false,
}

export const PRODUCTION_CONFIG: SeedConfig = {
  numberOfCompanies: 1000,
  numberOfUsers: 200,
  generateTestData: false,
  clearExistingData: false,
  verbose: false,
}

export const DEMO_CONFIG: SeedConfig = {
  numberOfCompanies: 50,
  numberOfUsers: 20,
  generateTestData: true,
  clearExistingData: true,
  verbose: true,
}

/**
 * Get configuration for the current environment
 */
export function getEnvironmentConfig(environment?: string): SeedConfig {
  const env = environment || process.env.NODE_ENV || 'development'

  switch (env.toLowerCase()) {
    case 'production':
      return PRODUCTION_CONFIG
    case 'test':
      return TEST_CONFIG
    case 'demo':
      return DEMO_CONFIG
    case 'development':
    default:
      return DEVELOPMENT_CONFIG
  }
}

/**
 * Create a custom configuration by merging with environment defaults
 */
export function createCustomConfig(
  environment: string,
  overrides: Partial<SeedConfig>,
): SeedConfig {
  const baseConfig = getEnvironmentConfig(environment)
  return { ...baseConfig, ...overrides }
}
