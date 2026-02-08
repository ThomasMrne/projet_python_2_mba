from typing import Optional, Dict
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from src.banking_api.services.customer_service import (
    get_all_customers,
    get_top_customers,
    get_customer_profile
)

router = APIRouter(prefix="/api/customers", tags=["Customers"])


# --- Modèles Pydantic ---

class Customer(BaseModel):
    id: int
    name: str


class CustomerPagination(BaseModel):
    page: int
    total_items: int
    customers: Dict[int, Customer]
    total_pages: Optional[int] = None


class CustomerStats(BaseModel):
    transaction_count: int
    total_spent: float
    total_received: float
    current_balance: float


class CustomerProfile(BaseModel):
    id: int
    name: str
    stats: CustomerStats


# --- Routes ---

@router.get("", response_model=CustomerPagination)
def list_customers(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
):
    """Récupère la liste paginée des clients."""
    return get_all_customers(page, limit)


@router.get("/top", response_model=Dict[int, int])
def get_top_customers_route(n: int = Query(5, ge=1, le=100)):
    """Récupère le top N des clients."""
    return get_top_customers(n)


@router.get("/{customer_id}", response_model=CustomerProfile)
def get_customer_details(customer_id: int):
    """Récupère le profil complet d'un client."""
    profile = get_customer_profile(customer_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Customer not found")
    return profile
