from src.banking_api.services.data_loader import get_data


def get_health_status():
    """Route 19: Vérifie si le service est opérationnel et prêt."""
    df = get_data()
    # Renvoie l'état du serveur et confirme si le CSV est bien en mémoire
    return {
        "status": "ok",
        "dataset_loaded": not df.empty,
        "total_rows": len(df) if not df.empty else 0,
    }


def get_metadata():
    """Route 20: Fournit les informations de version du projet."""
    return {"version": "1.0.0", "last_update": "2025-12-20T22:00:00Z"}
