FROM python:3.11-slim AS migrations

# Install Postgres client (optional: for raw SQL commands or debugging)
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Create virtualenv
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies
COPY requirements/build.in /tmp/requirements.in
RUN pip install --no-cache-dir -r /tmp/requirements.in

# Copy app/migrations code
WORKDIR /app
COPY schema ./schema
COPY scripts ./scripts

# Default command runs alembic inside schema folder
WORKDIR /app/schema
ENTRYPOINT ["alembic", "upgrade", "head"]
