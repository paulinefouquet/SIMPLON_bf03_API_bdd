from fastapi import FastAPI, HTTPException
import sqlite3

app = FastAPI()
con = sqlite3.connect(r"C:\Users\Utilisateur\AppData\Roaming\DBeaverData\workspace6\.metadata\sample-database-sqlite-1\Chinook.db")

def validate_year(year: str):
    if not year.isdigit() or not (len(year) == 4) :
        raise HTTPException(status_code=400, detail="L'année doit être une valeur numérique de 4 chiffres")

    return int(year)

def apply_request (request) : 
    cur = con.cursor()
    cur.execute(request)    
    result = cur.fetchall()  # Récupère les résultats de la requête
    if result is None or len(result)==0:
        return  HTTPException(status_code=400, detail="Aucune valeur trouvée, merci de vérifier les paramètres entrés, attention à la casse")
    elif len(result)==1 : 
        return result[0][0]
    else: return result
        #return {r[2]: r[0] for r in result}


#us1 En tant qu'Agent je veux pouvoir consulter le revenu fiscal moyen des foyers de ma ville (Montpellier)

@app.get("/revenu_fiscal_moyen/")
async def revenu_fiscal_moyen(year: str, city: str ):
    year = validate_year(year)
    req = f"SELECT revenu_fiscal_moyen, date, ville FROM foyers_fiscaux WHERE date LIKE '%{year}%' AND ville = '{city}'"
    return apply_request(req)



#us2: En tant qu'Agent je veux consulter les 10 dernières transactions dans ma ville (Lyon)

@app.get("/transactions/last")
async def last_transactions(city: str, limit: int):
    req= f"SELECT * FROM transactions t WHERE ville LIKE '%{city}%' ORDER BY date_transaction DESC LIMIT {limit};"
    return apply_request(req)

#us3: En tant qu'Agent je souhaite connaitre le nombre d'acquisitions dans ma ville (Paris) durant l'année 2022

@app.get("/transactions/count")
async def count_transactions(city: str, year: str):
    year = validate_year(year)
    req= f"SELECT COUNT(id_transaction) FROM transactions t WHERE ville LIKE '%{city}%' AND date_transaction LIKE '%{year}%';"
    return apply_request(req)
     

#us4: En tant qu'Agent je souhaite connaitre le prix au m2 moyen pour les maisons vendues l'année 2022

@app.get("/transactions/prix-moyen")
async def avg_price(year, type_batiment: str):
    year = validate_year(year)
    req=  f"SELECT AVG(prix / surface_habitable) FROM transactions WHERE date_transaction LIKE '%{year}%'\
    AND type_batiment LIKE '{type_batiment}';"
    answer=apply_request(req)

    return answer

#us5: En tant qu'Agent je souhaite connaitre le nombre d'acquisitions de studios dans ma ville (Rennes) durant l'année 2022

@app.get("/transactions/count-studio")
async def count_studio(city: str, year, nb_piece: int):
    year = validate_year(year)
    req= f"SELECT COUNT(*) FROM transactions t WHERE ville LIKE '%{city}%' AND date_transaction LIKE '%{year}%'\
    AND n_pieces = {nb_piece};"
    answer=apply_request(req)

    return answer
    

#us6: En tant qu'Agent je souhaite connaitre la répartition des appartements vendus (à Marseille) durant l'année 2022 en fonction du nombre de pièces

@app.get("/transactions/repartition")
async def repartition(city: str, year: str):
    year = validate_year(year)
    req=  f"SELECT n_pieces, count(*) FROM transactions WHERE ville LIKE '%{city}%' AND \
    date_transaction LIKE '%{year}%' GROUP BY n_pieces;"

    answer=apply_request(req)

    return answer

#us7: En tant qu'Agent je souhaite connaitre le prix au m2 moyen pour les maisons vendues à Avignon l'année 2022*/  

@app.get("/transactions/prix-moyen-maison")
async def prix_moy(city: str, year: str, type_batiment):
    year = validate_year(year)
    req=f"SELECT AVG(prix /surface_habitable) FROM transactions\
    WHERE ville LIKE '%{city}%' AND date_transaction LIKE '%{year}%' AND type_batiment = '{type_batiment}';"

    answer=apply_request(req)

    return answer

#us8: En tant que CEO, je veux consulter le nombre de transactions (tout type confondu) par département, ordonnées par ordre décroissant*/

@app.get("/transactions/departement")
async def topdepartment():
    #year = validate_year(year)
    req=f"SELECT departement, COUNT(*) AS nb FROM transactions GROUP BY departement ORDER BY nb DESC;"

    answer=apply_request(req)

    return answer


#us9:En tant que CEO je souhaite connaitre le nombre total de vente d'appartements en 2022 dans toutes les villes où le revenu fiscal moyen en 2018 est supérieur à 70k

@app.get("/transactions/prix-moyen")
async def repartition(city: str, year: str):
    year = validate_year(year)
    req=f"SELECT t.ville, COUNT(t.id_transaction) AS n_total FROM transactions t\
        JOIN foyers_fiscaux ff ON t.ville = UPPER(ff.ville) \
        WHERE t.date_transaction like '2022%' AND ff.revenu_fiscal_moyen > 70000 AND ff.date = 2018\
        GROUP BY t.ville;"

    answer=apply_request(req)

    return answer


@app.get("/transactions/prix-moyen")
async def repartition(city: str, year: str):
    year = validate_year(year)
    req=f"SELECT ville, COUNT(id_transaction) AS n_transac  FROM transactions GROUP BY ville\
        ORDER BY n_transac DESC LIMIT 10 ; "

    answer=apply_request(req)

    return answer


@app.get("/transactions/prix-moyen/appartement")
async def repartition(city: str, year: str):
    year = validate_year(year)
    req=f"SELECT ville, type_batiment, AVG(ROUND(prix/surface_habitable)) as prix_m2_moy FROM transactions\
        WHERE type_batiment = 'Appartement' GROUP BY ville  ORDER BY prix_m2_moy ASC LIMIT 10"

    answer=apply_request(req)

    return answer


@app.get("/transactions/prix-moyen/maison")
async def repartition(city: str, year: str):
    year = validate_year(year)
    req=f"SELECT ville, type_batiment, AVG(ROUND(prix/surface_habitable)) as prix_m2_moy FROM transactions\
            WHERE type_batiment = 'Maison' GROUP BY ville ORDER BY prix_m2_moy DESC LIMIT 10"

    answer=apply_request(req)

    return answer



