from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.banking_api.services.data_loader import load_dataset

# Import de tous les routeurs
from src.banking_api.routers import transactions
from src.banking_api.routers import stats
from src.banking_api.routers import customers
from src.banking_api.routers import fraud
from src.banking_api.routers import system


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gère le cycle de vie de l'application avec vérification des données."""
    print("Démarrage de l'API...")

    if not load_dataset():
        print("AVERTISSEMENT: Échec du chargement des données.")
    else:
        print("Données chargées avec succès.")

    yield
    print("Arrêt de l'API.")


app = FastAPI(
    title="Banking Transactions API",
    description="API for banking transaction management and analysis",
    version="1.0.0",
    lifespan=lifespan,
)

# Branchement
app.include_router(transactions.router)
app.include_router(stats.router)
app.include_router(customers.router)
app.include_router(fraud.router)
app.include_router(system.router)


@app.get("/")
def read_root():
    return {"message": "API is running correctly"}
