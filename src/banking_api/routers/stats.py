from fastapi import APIRouter
from typing import List
from pydantic import BaseModel

# Import de notre service de calcul
from src.banking_api.services import stats_service

router = APIRouter(prefix="/api/stats", tags=["Statistiques"])

# --- Modèles de réponse (Schemas) ---
# Ces modèles doivent correspondre EXACTEMENT à ce que renvoie stats_service.py


class OverviewStats(BaseModel):
    total_transactions: int
    fraud_rate: float
    avg_amount: float
    most_common_type: str


class DistributionStats(BaseModel):
    bins: List[str]  # ex: ["0-50", "50-100"...]
    counts: List[int]


class TypeStat(BaseModel):
    type: str  # ex: "Swipe Transaction"
    count: int
    avg_amount: float


class StepStat(BaseModel):
    step: int  # Correspondra à l'année (ex: 2010)
    count: int
    avg_amount: float


# --- Routes ---


@router.get("/overview", response_model=OverviewStats)
def get_overview():
    """Route 9: Statistiques globales du dataset"""
    return stats_service.get_global_stats()


@router.get("/amount-distribution", response_model=DistributionStats)
def get_distribution():
    """Route 10: Histogramme des montants"""
    return stats_service.get_amount_distribution()


@router.get("/by-type", response_model=List[TypeStat])
def get_stats_by_type():
    """Route 11: Stats par type d'utilisation (Chip, Swipe, Online)"""
    return stats_service.get_stats_by_type()


@router.get("/daily", response_model=List[StepStat])
def get_daily_trend():
    """Route 12: Tendance annuelle (Volume et Montant moyen)"""
    return stats_service.get_daily_stats()
