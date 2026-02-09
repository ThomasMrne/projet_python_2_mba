from fastapi import APIRouter
from src.banking_api.services import system_service

# Configuration du router pour les fonctions d'administration technique
router = APIRouter(prefix="/api/system", tags=["Administration"])


@router.get("/health")
def check_health():
    """Vérifie l'état de santé de l'API et du chargement des données."""
    return system_service.get_health_status()


@router.get("/metadata")
def get_metadata():
    """Récupère les informations techniques sur le dataset chargé."""
    return system_service.get_metadata()
