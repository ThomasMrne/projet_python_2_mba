from fastapi import APIRouter
from typing import List, Optional, Union
from pydantic import BaseModel

from src.banking_api.services import stats_service

router = APIRouter(prefix="/api/stats", tags=["Stats"])

# --- Modèles Pydantic ---


class TopTransaction(BaseModel):
    id: Union[str, int, None] = None
    amount: float
    date: str


class GlobalStats(BaseModel):
    total_transactions: int
    average_amount: float
    top_transaction: Optional[TopTransaction] = None
    fraud_rate: Optional[float] = None
    most_common_type: Optional[str] = None


class StatDistribution(BaseModel):
    bins: List[str]
    counts: List[int]


class TypeStat(BaseModel):
    type: str
    count: int


class StepStat(BaseModel):
    date: str
    count: int

# --- Routes ---


@router.get("/overview", response_model=GlobalStats)
def get_overview():
    return stats_service.get_global_stats()


@router.get("/amount-distribution", response_model=StatDistribution)
def get_amount_distribution():
    return stats_service.get_amount_distribution()


@router.get("/by-type", response_model=List[TypeStat])
def get_transactions_by_type():
    return stats_service.get_transactions_by_type()


@router.get("/daily", response_model=List[StepStat])
def get_daily_volume():
    return stats_service.get_daily_transaction_volume()
