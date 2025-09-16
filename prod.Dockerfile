FROM node:22-slim AS migrations

WORKDIR /app

# Copy only package files first
COPY schema ./schema

# Install dependencies
RUN npm install -g --no-fund pnpm@10.10.0

WORKDIR /app/schema
RUN pnpm install --frozen-lockfile \
 && pnpm exec prisma generate

ENTRYPOINT ["pnpm", "exec", "prisma", "db", "push"]
