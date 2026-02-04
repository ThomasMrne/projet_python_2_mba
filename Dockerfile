# --- ÉTAPE 1 : Build ---
# On utilise l'image alpine qui est ultra légère et contient un shell
FROM ghcr.io/astral-sh/uv:python3.13-alpine AS builder

# Optimisations uv
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

WORKDIR /app

# Copie des fichiers de dépendances
COPY pyproject.toml uv.lock ./

# Installation des dépendances dans un venv local à /app/.venv
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# --- ÉTAPE 2 : Runtime ---
FROM python:3.13-slim

WORKDIR /app

# Récupération du venv du builder
COPY --from=builder /app/.venv /app/.venv

# Activation du venv
ENV PATH="/app/.venv/bin:$PATH"

# Copie du code et des données
COPY src/ ./src/
COPY data/ ./data/

EXPOSE 8000

# Lancement
CMD ["uvicorn", "src.banking_api.main:app", "--host", "0.0.0.0", "--port", "8000"]