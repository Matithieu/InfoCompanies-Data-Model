/**
 * Base factory class for creating test data
 */

import { faker } from '@faker-js/faker'
import { IFactory } from '../types'

export abstract class BaseFactory<T> implements IFactory<T> {
  protected faker = faker

  /**
   * Create a single instance with optional overrides
   */
  abstract create(overrides?: Partial<T>): T

  /**
   * Create multiple instances
   */
  createMany(count: number, overrides?: Partial<T>): T[] {
    return Array.from({ length: count }, () => this.create(overrides))
  }

  /**
   * Create a batch of instances with different configurations
   */
  createBatch(configurations: Partial<T>[]): T[] {
    return configurations.map(config => this.create(config))
  }

  /**
   * Merge default values with overrides
   */
  protected mergeOverrides(defaults: T, overrides?: Partial<T>): T {
    if (!overrides) return defaults
    return { ...defaults, ...overrides }
  }

  /**
   * Generate a random subset from an array
   */
  protected randomSubset<U>(items: U[], minCount = 1, maxCount?: number): U[] {
    const max = maxCount ?? items.length
    const count = faker.number.int({ min: minCount, max: Math.min(max, items.length) })
    return faker.helpers.arrayElements(items, count)
  }

  /**
   * Pick a random item from an array
   */
  protected randomPick<U>(items: U[]): U {
    return faker.helpers.arrayElement(items)
  }

  /**
   * Generate a weighted random choice
   */
  protected weightedChoice<U>(choices: Array<{ item: U; weight: number }>): U {
    const totalWeight = choices.reduce((sum, choice) => sum + choice.weight, 0)
    let random = faker.number.float({ min: 0, max: totalWeight })

    for (const choice of choices) {
      random -= choice.weight
      if (random <= 0) {
        return choice.item
      }
    }

    // Fallback to first item
    return choices[0].item
  }
}
