# Base image
FROM python:3.11-slim AS builder

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    UV_HOME=/opt/uv

# Install curl  and clean up
RUN apt-get update && apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="${UV_HOME}/bin:${PATH}"

# Copy dependency files
WORKDIR /app
COPY pyproject.toml .

# Install dependencies with uv
RUN uv pip install .

# Runtime stage
FROM python:3.11-slim

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
WORKDIR /app
COPY src ./src

# Expose server port
EXPOSE 9100

CMD ["uv", "run", "apiserver.py"]
