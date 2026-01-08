from fastapi import APIRouter
from src.banking_api.services import system_service

router = APIRouter(prefix="/api/system", tags=["Administration"])


@router.get("/health")
def check_health():
    return system_service.get_health_status()


@router.get("/metadata")
def get_metadata():
    return system_service.get_metadata()
