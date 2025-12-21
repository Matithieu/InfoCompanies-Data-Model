/**
 * Jest type extensions
 */

declare namespace jest {
  interface Matchers<R> {
    toBeValidDate(): R
    toBeValidEmail(): R
  }
}
