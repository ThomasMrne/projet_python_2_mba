# On part d'une image Python officielle légère
FROM python:3.13-slim

# On définit le dossier de travail dans le conteneur
WORKDIR /app

# On copie les fichiers de configuration indispensables
COPY pyproject.toml README.md requirements.txt ./

# On copie tout le code source
COPY src ./src

# On installe le projet et les dépendances
# L'option --no-cache-dir permet de garder l'image légère
RUN pip install --no-cache-dir -e .

# On expose le port 8000 (celui de l'API)
EXPOSE 8000

# La commande de démarrage automatique
# --host 0.0.0.0 est OBLIGATOIRE pour que Docker soit accessible de l'extérieur
CMD ["uvicorn", "src.banking_api.main:app", "--host", "0.0.0.0", "--port", "8000"]