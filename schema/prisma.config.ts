import 'dotenv/config'
import { defineConfig, env } from 'prisma/config'

export default defineConfig({
  migrations: {
    path: './prisma/schema/migrations/',
  },
  schema: './prisma/schema/',
  datasource: {
    url: env("DATABASE_URL")
  }
})