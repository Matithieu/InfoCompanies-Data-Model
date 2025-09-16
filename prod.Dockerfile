FROM node:22-slim AS migrations

WORKDIR /app

# Enable pnpm via corepack

# Copy only package files first
COPY schema/package.json schema/pnpm-lock.yaml ./

# Install dependencies
RUN npm install -g --no-fund pnpm@10.10.0 \
    pnpm install --frozen-lockfile

# Now copy the rest of the schema code
COPY schema .

# Prisma checks
RUN pnpm exec prisma generate

ENTRYPOINT ["pnpm", "exec", "prisma", "db", "push"]
