/** @type {import('jest').Config} */
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>'],
  testMatch: ['**/__tests__/**/*.ts', '**/?(*.)+(spec|test).ts'],
  transform: {
    '^.+\\.ts$': 'ts-jest',
  },
  collectCoverageFrom: [
    'prisma/seed/**/*.ts',
    '!prisma/seed/**/*.d.ts',
    '!prisma/seed/reference/**/*.ts', // Exclude reference data files
    '!prisma/seed/utils/**/*.ts', // Exclude utility files for now
  ],
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'lcov', 'html'],
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  testTimeout: 30000, // 30 seconds for database operations
  verbose: true,
  // Environment variables for testing
  setupFiles: ['<rootDir>/jest.env.js'],
}
