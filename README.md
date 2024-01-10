# Simplon-Fastapi

## Brief projet dans le cadre de developement d'app immo

Création d'une API REST pour exposer les données de la BDD immobillier France (dataset kaggle)  

## Prérequis

Besoin des packages et dépendences suivantes:  

- uvicorn
    serveur web asynchrone  
    pour lancer le serveur :
```
uvicorn main:app --reload
```
- FastAPI
    librairie avec toutes les fonctions necessaires aux API
- sqlite3 
    pour se connecter à la BDD
    
## Structure :
main.py : le code principal de l'API  
loadnpz.py : le code qui nous a permit de doxwload le fichier transactions.npz et de le transférer en csv  