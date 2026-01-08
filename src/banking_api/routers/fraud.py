from fastapi import APIRouter
from typing import List
from pydantic import BaseModel

from src.banking_api.services import fraud_detection_service as fraud_service

router = APIRouter(prefix="/api/fraud", tags=["Fraude & Surveillance"])


# --- Modèles ---
class FraudSummary(BaseModel):
    total_frauds: int
    flagged_by_system: int
    fraud_rate: float


class FraudByType(BaseModel):
    type: str
    count: int


class PredictionInput(BaseModel):
    type: str
    amount: float
    oldbalanceOrg: float = (
        0  # Pas utilisé dans notre logique simplifiée mais demandé par le PDF
    )
    newbalanceOrig: float = 0


class PredictionResult(BaseModel):
    isFraud: bool
    probability: float
    risk_level: str


# --- Routes ---


@router.get("/summary", response_model=FraudSummary)
def get_fraud_summary():
    """Route 13: Résumé de la fraude"""
    return fraud_service.get_fraud_summary()


@router.get("/by-type", response_model=List[FraudByType])
def get_fraud_distribution():
    """Route 14: Fraude par type"""
    return fraud_service.get_fraud_by_type()


@router.post("/predict", response_model=PredictionResult)
def predict_transaction_risk(data: PredictionInput):
    """Route 15: Prédire si une transaction est risquée"""
    return fraud_service.predict_fraud(data.amount, data.type)
