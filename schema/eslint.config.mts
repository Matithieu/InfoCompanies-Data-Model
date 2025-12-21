import js from '@eslint/js'
import globals from 'globals'
import tseslint from 'typescript-eslint'
import tsParser from '@typescript-eslint/parser'

import eslintPluginPrettierRecommended from 'eslint-plugin-prettier/recommended'

import { defineConfig } from 'eslint/config'

/** @type { import("eslint").Linter.Config[] } */
export default defineConfig([
  {
    name: 'global:settings',
    languageOptions: {
      parser: tsParser,
      ecmaVersion: 'latest',
      sourceType: 'module',

      parserOptions: {
        projectService: false,
      },
    },
  },
  js.configs.recommended,
  ...tseslint.configs.recommended,
  {
    files: ['**/*.{ts,js}'],
    languageOptions: {
      globals: globals.browser,
    },
  },
  eslintPluginPrettierRecommended,
])
