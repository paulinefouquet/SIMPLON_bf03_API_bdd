# Simplon-Fastapi

## Brief projet dans le cadre de developement d'app immo

Création d'une API REST pour exposer les données de la BDD immo

## Documentation

Besoin des packages et dépendences suivantes

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
main.py est le code principal de l'API
dans loadnpz.py on trouve le code qui nous a permit de doxwload le fichier transactions.npz et de le transférer en csv