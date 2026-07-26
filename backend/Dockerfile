# =========================
# Builder Stage
# =========================
FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Configure uv
ENV UV_LINK_MODE=copy
ENV UV_PYTHON=/usr/local/bin/python3
ENV UV_PYTHON_DOWNLOADS=never

WORKDIR /app

# System dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        g++ \
        curl && \
    rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install --no-cache-dir uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install project dependencies
RUN uv sync --frozen --no-dev

# Copy source code
COPY . .

# Sync project again (installs local package)
RUN uv sync --frozen --no-dev

# ------------------------------------------------------------
# Install spaCy English model into the SAME virtual environment
# ------------------------------------------------------------
RUN uv pip install \
    --python /app/.venv/bin/python \
    https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl

# Verify installation
RUN /app/.venv/bin/python -c "import en_core_web_sm; print(en_core_web_sm.__file__)"
RUN /app/.venv/bin/python -m spacy validate

# =========================
# Runtime Stage
# =========================
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl && \
    rm -rf /var/lib/apt/lists/*

RUN groupadd --system synapseos && \
    useradd --system \
        --gid synapseos \
        --create-home \
        synapseos

COPY --from=builder --chown=synapseos:synapseos /app /app

RUN mkdir -p \
    /app/artifacts/forecast \
    /app/artifacts/models \
    /app/artifacts/evaluation && \
    chown -R synapseos:synapseos /app/artifacts

USER synapseos

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
CMD curl -f http://localhost:8000/health || exit 1

CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]