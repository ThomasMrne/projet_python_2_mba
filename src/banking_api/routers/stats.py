from fastapi import APIRouter
from typing import List, Optional, Union
from pydantic import BaseModel

# Import du service traitant les agrégations de données
from src.banking_api.services import stats_service

# Configuration du router pour les statistiques descriptives
router = APIRouter(prefix="/api/stats", tags=["Stats"])

# --- Modèles de données ---


class TopTransaction(BaseModel):
    """Représentation de la transaction ayant le montant le plus élevé."""
    id: Union[str, int, None] = None
    amount: float
    date: str


class GlobalStats(BaseModel):
    """Indicateurs clés de performance (KPI) pour l'ensemble du système."""
    total_transactions: int
    average_amount: float
    top_transaction: Optional[TopTransaction] = None
    fraud_rate: Optional[float] = None
    most_common_type: Optional[str] = None


class StatDistribution(BaseModel):
    """Données pour l'affichage d'un histogramme des montants."""
    bins: List[str]
    counts: List[int]


class TypeStat(BaseModel):
    """Volume de transactions groupé par catégorie (CASH_OUT, DEBIT...)."""
    type: str
    count: int


class StepStat(BaseModel):
    """Volume d'activité par unité de temps (Step)."""
    date: str
    count: int


@router.get("/overview", response_model=GlobalStats)
def get_overview():
    """Route 10: Récupère les chiffres clés et records du dataset."""
    return stats_service.get_global_stats()


@router.get("/amount-distribution", response_model=StatDistribution)
def get_amount_distribution():
    """Route 11: Analyse la répartition des montants par tranches."""
    return stats_service.get_amount_distribution()


@router.get("/by-type", response_model=List[TypeStat])
def get_transactions_by_type():
    """Route 12: Renvoie le décompte total pour chaque type de mouvement."""
    return stats_service.get_transactions_by_type()


@router.get("/daily", response_model=List[StepStat])
def get_daily_volume():
    """Route 13: Analyse l'évolution du volume au fil du temps (Steps)."""
    return stats_service.get_daily_transaction_volume()
