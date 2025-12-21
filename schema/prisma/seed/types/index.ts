/**
 * Core types and interfaces for the seeding system
 */

import { PrismaClient } from '../../generated/prisma'

// Seed configuration interface
export interface SeedConfig {
  numberOfCompanies: number
  numberOfUsers: number
  generateTestData: boolean
  clearExistingData: boolean
  verbose: boolean
}

// Default seed configuration
export const DEFAULT_SEED_CONFIG: SeedConfig = {
  numberOfCompanies: 100,
  numberOfUsers: 50,
  generateTestData: true,
  clearExistingData: true,
  verbose: true,
}

// Seeder interface for all data seeders
export interface ISeeder<T> {
  name: string
  seed(config: SeedConfig): Promise<T[]>
  clear(): Promise<void>
  count(): Promise<number>
}

// Base seeder class
export abstract class BaseSeeder<T> implements ISeeder<T> {
  protected prisma: PrismaClient

  constructor(
    public readonly name: string,
    prisma: PrismaClient,
  ) {
    this.prisma = prisma
  }

  abstract seed(config: SeedConfig): Promise<T[]>
  abstract clear(): Promise<void>
  abstract count(): Promise<number>

  protected log(message: string, config: SeedConfig): void {
    if (config.verbose) {
      console.log(`[${this.name}] ${message}`)
    }
  }
}

// Seed execution result
export interface SeedResult {
  seederName: string
  recordsCreated: number
  duration: number
  success: boolean
  error?: Error
}

// Complete seed execution summary
export interface SeedSummary {
  totalDuration: number
  totalRecords: number
  results: SeedResult[]
  success: boolean
}

// Factory interface for creating entities
export interface IFactory<T> {
  create(overrides?: Partial<T>): T
  createMany(count: number, overrides?: Partial<T>): T[]
}

// Builder interface for complex entity creation
export interface IBuilder<T> {
  build(): T
  reset(): this
}
