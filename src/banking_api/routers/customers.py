from fastapi import APIRouter, HTTPException, Query
from typing import List
from pydantic import BaseModel

from src.banking_api.services import customer_service

router = APIRouter(prefix="/api/customers", tags=["Clients"])


# --- Modèles ---
class CustomerSummary(BaseModel):
    id: str
    name: str


class CustomerListResponse(BaseModel):
    page: int
    total_pages: int
    total_items: int
    customers: List[CustomerSummary]


class CustomerProfile(BaseModel):
    id: str
    transactions_count: int
    avg_amount: float
    fraudulent: bool
    first_seen: str
    last_seen: str


class TopCustomer(BaseModel):
    id: str
    total_spent: float


# --- Routes ---


@router.get("", response_model=CustomerListResponse)
def list_customers(page: int = Query(1, ge=1), limit: int = Query(10, ge=1)):
    """Route 16: Liste paginée des clients"""
    return customer_service.get_all_customers(page, limit)


@router.get("/top", response_model=List[TopCustomer])
def get_top_customers(n: int = Query(10, ge=1, le=100)):
    """Route 18: Top N clients par volume (Whales)"""
    return customer_service.get_top_customers(n)


@router.get("/{customer_id}", response_model=CustomerProfile)
def get_customer_details(customer_id: str):
    """Route 17: Fiche client détaillée"""
    profile = customer_service.get_customer_profile(customer_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Client introuvable")
    return profile
