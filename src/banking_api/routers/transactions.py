from typing import Optional, List, Union
from fastapi import APIRouter, HTTPException, Query, Path
from pydantic import BaseModel

# Import du service gérant la logique métier des transactions
from src.banking_api.services import transactions_service

# Définition du router pour les opérations sur les transactions
router = APIRouter(prefix="/api/transactions", tags=["Transactions"])


# --- Modèles Pydantic ---
class Transaction(BaseModel):
    """Représente une transaction complète avec tous ses attributs."""
    id: Union[str, int]
    date: str
    amount: float
    client_id: Union[str, int, None] = None
    merchant_id: Union[str, int, None] = None
    card_id: Union[str, int, None] = None
    use_chip: Optional[str] = None
    merchant_city: Optional[str] = None
    merchant_state: Optional[str] = None
    zip: Union[float, str, None] = None
    mcc: Optional[int] = None
    errors: Optional[str] = None
    type: Optional[str] = None
    nameOrig: Optional[str] = None
    nameDest: Optional[str] = None
    formatted_amount: Optional[str] = None


class PaginatedTransactionResponse(BaseModel):
    """Structure de réponse incluant les métadonnées de pagination."""
    page: int
    total_pages: int
    total_items: int
    transactions: List[Transaction]


class SearchCriteria(BaseModel):
    """Critères de filtrage pour les recherches complexes en POST."""
    type: Optional[str] = None
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None


# --- Routes ---

@router.get("", response_model=PaginatedTransactionResponse)
def get_transactions(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    type: Optional[str] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
):
    """Liste les transactions avec filtres optionnels et pagination."""
    return transactions_service.get_transactions(
        page, limit, type, min_amount, max_amount
    )


@router.get("/types", response_model=List[str])
def get_transaction_types():
    """Renvoie la liste unique des types de transactions (CASH_IN, etc.)."""
    return transactions_service.get_transaction_types()


@router.get("/recent", response_model=List[Transaction])
def get_recent_transactions(
    n: int = Query(10, ge=1, le=50)
):
    """Récupère les N dernières transactions enregistrées."""
    return transactions_service.get_recent_transactions(n)


@router.get("/search", response_model=PaginatedTransactionResponse)
def search_transactions_get(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    type: Optional[str] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
):
    """Recherche via paramètres d'URL (GET)."""
    return transactions_service.get_transactions(
        page, limit, type, min_amount, max_amount
    )


@router.post("/search", response_model=PaginatedTransactionResponse)
def search_transactions_post(
    criteria: SearchCriteria,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
):
    """Recherche via un corps de message JSON (POST)."""
    return transactions_service.get_transactions(
        page,
        limit,
        criteria.type,
        criteria.min_amount,
        criteria.max_amount
    )


@router.get("/by-customer/{customer_id}", response_model=List[Transaction])
def get_transactions_by_customer(
    customer_id: int = Path(..., ge=0)
):
    """Filtre l'historique pour un client spécifique."""
    return transactions_service.get_transactions_by_customer(customer_id)


@router.get("/to-merchant/{merchant_id}", response_model=List[Transaction])
def read_transactions_to_merchant(
    merchant_id: int = Path(..., ge=0)
):
    """Filtre les transactions envoyées vers un marchand spécifique."""
    return transactions_service.get_transactions_to_merchant(merchant_id)


@router.delete("/{id}")
def delete_transaction(
    id: int = Path(..., title="Transaction ID", ge=0)
):
    """Supprime une transaction après vérification d'existence."""
    result = transactions_service.get_transaction_by_id(id)
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Transaction with id {id} not found"
        )

    return {"message": f"Transaction {id} supprimée avec succès"}


@router.get("/{id}", response_model=Transaction)
def get_transaction_by_id(
    id: int = Path(..., title="Transaction ID", ge=0)
):
    """Récupère une transaction. Le type int gère la validation auto."""
    result = transactions_service.get_transaction_by_id(id)

    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Transaction with id {id} not found"
        )
    return result
