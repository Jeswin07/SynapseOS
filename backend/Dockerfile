# -----------------------------------------------------------------------------
# Builder Stage
# -----------------------------------------------------------------------------

FROM python:3.11-slim AS builder

LABEL org.opencontainers.image.title="SynapseOS" \
      org.opencontainers.image.description="Enterprise Decision Intelligence Platform" \
      org.opencontainers.image.authors="Jeswin K Reji"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_PYTHON=/usr/local/bin/python3 \
    UV_PYTHON_DOWNLOADS=never

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

COPY . .

RUN uv sync --frozen --no-dev

RUN uv run python -m spacy download en_core_web_sm

# -----------------------------------------------------------------------------
# Runtime Stage
# -----------------------------------------------------------------------------

FROM python:3.11-slim

LABEL org.opencontainers.image.title="SynapseOS" \
      org.opencontainers.image.description="Enterprise Decision Intelligence Platform"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Install runtime tools (used by Docker healthcheck)
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd --system synapseos && \
    useradd --system --gid synapseos --create-home synapseos

# Copy application and virtual environment
COPY --from=builder /app /app

# Set ownership
RUN chown -R synapseos:synapseos /app

USER synapseos

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--forwarded-allow-ips=*"]