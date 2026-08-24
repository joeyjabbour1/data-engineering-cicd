# ============================
# Stage 1 — Builder
# ============================
FROM python:3.12-slim AS builder

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml .
COPY src/ ./src

# Install the package into a temporary directory
RUN pip install --upgrade pip \
    && pip install . --prefix /install


# ============================
# Stage 2 — Runtime
# ============================
FROM python:3.12-slim

# Create non-root user
RUN useradd -m appuser

WORKDIR /app

# Copy installed package from builder stage
COPY --from=builder /install /usr/local

# Copy source code (optional for debugging)
COPY src/ ./src

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Switch to non-root user
USER appuser

# Default entrypoint (can be changed later)
ENTRYPOINT ["python", "-m", "order_pipeline"]