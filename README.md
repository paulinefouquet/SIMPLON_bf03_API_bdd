# Simplon-Fastapi

## Brief projet dans le cadre de developement d'app immo

Création d'une API REST pour exposer les données de la BDD immobillier France (dataset kaggle)

## Python Version
Version python 3.11.5

## Datas :
Il faut télécharger les données sources depuis https://www.kaggle.com/datasets/benoitfavier/immobilier-france
Important, le fichier transactions.npz necessite d'être transformer en csv pour être intégrer à une DB, cf Prérequis
Attention le chemin d'accès vers la DB doit être spécifié con = sqlite3.connect(r"Chemin d'accès à la DB")

## Structure :
main.py : le code principal de l'API  
loadnpz.py : ce code permet de download le fichier transactions.npz et de le transférer en csv.
Il faut ensuite l'intégrer manuellement à sa DB DBeaver en important la table

## Prérequis

Besoin des packages et de leurs dépendences suivantes à installer avec pip install

- uvicorn
    serveur web asynchrone  
    pour démarrer le serveur depuis le vscode :
```
uvicorn main:app --reload
```

- FastAPI
    librairie avec toutes les fonctions necessaires aux API
- sqlite3 
    pour se connecter à la BDD
- numpy et panda pour charger la bdd

