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
    print("Démarrage de l'API...")
    load_dataset()
    yield
    print("Arrêt de l'API.")


app = FastAPI(
    title="Banking Transactions API",
    description="API for portfolio asset retrieval management",
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
