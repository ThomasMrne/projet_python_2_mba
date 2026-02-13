# Banking Transactions API

API REST performante développée avec **FastAPI** pour l'analyse et l'exposition de données bancaires massives (13M+ de transactions).
Projet réalisé dans le cadre du cours **Python MBA 2**.

> **Note : Version Finale (V2)** > Cette version intègre les corrections de robustesse (gestion des types Pandas), une couverture de tests complète et une documentation technique exhaustive.

## 📋 Fonctionnalités

L'API expose **20 endpoints** organisés pour une exploitation métier complète :
* **Transactions** : Consultation paginée, recherche multicritères, filtrage par commerçant et simulation de gestion.
* **Statistiques** : Analyse de tendances, agrégations globales et statistiques sur les types de transactions.
* **Clients** : Analyse de profils individuels, détection des "Whales" (gros portefeuilles) et statistiques de possession de cartes.
* **Fraude** : Moteur de scoring de risque basé sur des règles métier (analyse des montants et des ruptures de solde).
* **Système** : Endpoints de santé (Healthcheck) et de métriques.

## 🛠️ Installation & Lancement

Ce projet utilise un packaging moderne pour une installation isolée et propre.

1.  **Prérequis** : Python 3.12+
2.  **Environnement virtuel** :
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Sur Windows: .venv\Scripts\activate
    ```
3.  **Installation** (mode éditable avec dépendances de développement) :
    ```bash
    pip install -e ".[dev]"
    ```
4.  **Lancement de l'API** :
    ```bash
    uvicorn src.banking_api.main:app --reload
    ```
    Accédez à la documentation interactive : `http://127.0.0.1:8000/docs`

## 🧪 Tests et Qualité

La qualité du code est assurée par une suite d'outils automatisés :

* **Tests Unitaires** : Exécutés avec `pytest`. Couverture globale > 80%.
    ```bash
    pytest --cov=src.banking_api
    ```
* **Typage Statique** : Vérification stricte avec `mypy`.
    ```bash
    mypy src --ignore-missing-imports
    ```
* **Conformité PEP8** : Linters `flake8` pour garantir la lisibilité du code.
    ```bash
    flake8 src
    ```

## 🚀 Améliorations de Robustesse

Suite aux audits de code, les points suivants ont été renforcés :
* **Cohérence des données** : Conversion robuste des identifiants clients (gestion des types flottants générés par Pandas).
* **Sécurité des schémas** : Utilisation systématique de `Pydantic` pour la validation des données d'entrée/sortie.
* **Algorithme de Fraude** : Implémentation d'une logique basée sur l'évolution du solde (`oldbalance` vs `newbalance`).
* **Résilience** : Gestion sécurisée des colonnes manquantes dans le dataset original.

---
*Réalisé par Thomas M-A*