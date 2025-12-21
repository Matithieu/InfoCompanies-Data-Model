/**
 * Jest environment setup
 */

// Set test environment variables
process.env.NODE_ENV = 'test'
process.env.DATABASE_URL =
  process.env.TEST_DATABASE_URL || 'postgresql://test:test@localhost:5432/test_db'
