from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional, Union
from pydantic import BaseModel

from src.banking_api.services import customer_service

router = APIRouter(prefix="/api/customers", tags=["Customers"])

# --- Modèles Pydantic Intégrés ---


class Customer(BaseModel):
    id: Union[str, int]
    name: str


class CustomerPagination(BaseModel):
    page: int
    total_items: int
    customers: List[Customer]
    total_pages: Optional[int] = None


class CustomerStats(BaseModel):
    transaction_count: int
    total_spent: float
    total_received: float
    current_balance: float


class CustomerProfile(BaseModel):
    id: Union[str, int]
    name: str
    stats: CustomerStats


class CustomerTop(BaseModel):
    id: Union[str, int]
    transaction_count: int
    total_spent: Optional[float] = None

# --- Routes ---


@router.get("", response_model=CustomerPagination)
def list_customers(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
):
    return customer_service.get_all_customers(page, limit)


@router.get("/top", response_model=List[CustomerTop])
def get_top_customers(n: int = 5):
    return customer_service.get_top_customers(n)


@router.get("/{customer_id}", response_model=CustomerProfile)
def get_customer_details(customer_id: int):

    profile = customer_service.get_customer_profile(customer_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Customer not found")
    return profile
