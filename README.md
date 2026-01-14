> **Note:**
> Ceci est une version intermédiaire (V1) soumise pour feedback.
> L'architecture technique, les tests et le packaging sont complets.

# Banking Transactions API

API REST développée avec FastAPI pour l'exposition et l'analyse de données bancaires.
Projet réalisé dans le cadre du cours Python MBA 2.

## 📋 Fonctionnalités

L'API expose 20 endpoints répartis en 5 catégories :
* **Transactions** : Consultation paginée, filtrage avancé, recherche multicritères.
* **Statistiques** : Agrégations globales, tendances annuelles et distribution des montants.
* **Clients** : Analyse de portefeuille et identification des gros clients ("Whales").
* **Fraude** : Détection des anomalies et scoring de risque.
* **Système** : Monitoring de l'état de santé de l'API.

## 🛠️ Installation

Ce projet est packagé pour être installé comme une librairie Python standard.

1. **Prérequis** : Python 3.12 ou supérieur.
2. **Installation** :
   Placez-vous à la racine du projet et exécutez :

   ```bash
   pip install -e .
