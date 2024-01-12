from fastapi import FastAPI, HTTPException
import sqlite3
from enum import Enum

app = FastAPI()

con = sqlite3.connect(r"C:\Users\Utilisateur\AppData\Roaming\DBeaverData\workspace6\.metadata\sample-database-sqlite-1\Chinook.db")

class TypeBatiment(Enum) :
    MAISON = "Maison"
    APPARTEMENT = "Appartement"

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

@app.get("/revenu_fiscal_moyen/", description = 'Retourne le revenu fiscal moyen des foyers d\'une ville donnée')
async def revenu_fiscal_moyen(city: str, year: str=""):
    req = f"SELECT revenu_fiscal_moyen, date, ville FROM foyers_fiscaux WHERE ville LIKE '{city}%'"
    if year != "":
        year = validate_year(year)
        req += f"AND date LIKE '%{year}%'"
    return apply_request(req)
       

#us2: En tant qu'Agent je veux consulter les 10 dernières transactions dans ma ville (Lyon)

@app.get("/transactions/last", description = 'Retourne les n dernières transactions d\'une ville donnée')
async def last_transactions(city: str, limit: int):
    req= f"SELECT * FROM transactions t WHERE ville LIKE '%{city}%' ORDER BY date_transaction DESC LIMIT {limit};"
    return apply_request(req)


#us3: En tant qu'Agent je souhaite connaitre le nombre d'acquisitions dans ma ville (Paris) durant l'année 2022
#us5: En tant qu'Agent je souhaite connaitre le nombre d'acquisitions de studios dans ma ville (Rennes) durant l'année 2022

@app.get("/transactions/count", description = 'Us3 et us5 : Retourne le nombre d\'acquisitions selon le type de bâtiment (optionnel us5)\
          dans une ville donnée durant l\'année donnée')
async def count(city: str, year, nb_piece: str =""):
    year = validate_year(year)
    req= f"SELECT COUNT(*) FROM transactions t WHERE ville LIKE '%{city}%' AND date_transaction LIKE '%{year}%'"
    if nb_piece != "":
        req+= f"AND n_pieces = {nb_piece};"
    return apply_request(req)


#us4: En tant qu'Agent je souhaite connaitre le prix au m2 moyen pour les maisons vendues l'année 2022
#us7: En tant qu'Agent je souhaite connaitre le prix au m2 moyen pour les maisons vendues à Avignon l'année 2022

@app.get("/transactions/prix-moyen", description= 'US4 et US7 : Retourne le prix moyen au m2 en fonction des villes (optionnel),\
          du type de batiment et de l\'année ')
async def prix_moy(type_batiment: TypeBatiment, year: str, city: str=""):
    year = validate_year(year)
    req=f"SELECT AVG(prix /surface_habitable) FROM transactions WHERE date_transaction LIKE '%{year}%' AND type_batiment = '{type_batiment.value}'"
    if city != "":
        req += f" AND ville LIKE '{city}%';"
    return apply_request(req)
   

#us6: En tant qu'Agent je souhaite connaitre la répartition des appartements vendus (à Marseille) durant l'année 2022 en fonction du nombre de pièces

@app.get("/transactions/repartition", description= 'US6 : Retourne la répartition des biens vendus \
         dans une ville données pour un type de batiment donnée durant l\'année 2022 en fonction du nombre de pièces')
async def repartition(type_batiment : TypeBatiment, city: str, year: str):
    year = validate_year(year)
    req=  f"SELECT n_pieces, count(*) FROM transactions WHERE ville LIKE '%{city}%' AND type_batiment = '{type_batiment.value}' AND \
    date_transaction LIKE '%{year}%' GROUP BY n_pieces;"
    return apply_request(req)


#us8: En tant que CEO, je veux consulter le nombre de transactions (tout type confondu) par département, ordonnées par ordre décroissant

@app.get("/transactions/departement", description= 'US8: Retourne le nombre de transactions (tout type confondu) par département,\
          ordonnées par ordre décroissant')
async def topdepartment(year: str = ''):
    if year == '':
        req=f"SELECT departement, COUNT(*) AS nb FROM transactions GROUP BY departement ORDER BY nb DESC;"
    else :
        year = validate_year(year)
        req=f"SELECT departement, COUNT(*) AS nb FROM transactions WHERE date_transaction LIKE '{year}%' \
            GROUP BY departement ORDER BY nb DESC;"
    answer=apply_request(req)
    return answer


#us9:En tant que CEO je souhaite connaitre le nombre total de vente d'appartements en 2022 dans toutes les villes où le revenu fiscal moyen en 2018 est supérieur à 70k

@app.get("/transactions/immo-fonction-revenu-fiscal", description= 'Us09 :Retourne le nombre total de vente d\
         \'un type de batiment (appartements ou maison) pour une année donnée dans \
         toutes les villes où le revenu fiscal moyen pour une année fiscale de référence donnée est supérieur à revenu fiscal donné')
async def total_vente_selon_parametre(type_batiment : TypeBatiment, year: str, fiscal_year: str, revenu_fiscal_moyen: int):
    year = validate_year(year)
    fiscal_year = validate_year(fiscal_year)
    req=f"SELECT t.ville, COUNT(t.id_transaction) AS n_total FROM transactions t\
        JOIN foyers_fiscaux ff ON t.ville = UPPER(ff.ville) \
        WHERE t.date_transaction LIKE '{year}%' AND type_batiment = '{type_batiment.value}' AND ff.revenu_fiscal_moyen > {revenu_fiscal_moyen} AND ff.date LIKE '%{fiscal_year}%'\
        GROUP BY t.ville ORDER BY n_total DESC;"
    answer=apply_request(req)

    return answer


# Us10 : En tant que CEO, je veux consulter le top 10 des villes les plus dynamiques en termes de transactions immobilières */ 

@app.get("/transactions/dynamisme", description= 'Us10 Retourne le top 10 des villes les plus dynamiques\
          en termes de transactions immobilières')
async def dynamisme(limit_top, year: str =""):
    if year == "":
        req=f"SELECT ville, COUNT(id_transaction) AS n_transac FROM transactions GROUP BY ville\
        ORDER BY n_transac DESC LIMIT {limit_top} ; "   
    else: 
        year = validate_year(year)
        req=f"SELECT ville, COUNT(id_transaction) AS n_transac FROM transactions\
        WHERE date_transaction LIKE '%{year}%' GROUP BY ville\
        ORDER BY n_transac DESC LIMIT {limit_top} ; "
    answer=apply_request(req)
    return answer


# us11 : En tant que CEO, je veux accéder aux 10 villes avec un prix au m2 moyen le plus bas pour les appartements 
# us12 : En tant que CEO, je veux accéder aux 10 villes avec un prix au m2 moyen le plus haut pour les maisons 

@app.get("/transactions/prix-moyen/top", description= 'Us11 ou US12 : Retourne le top + ou - des prix au m2\
          des Maisons ou Appartements')
async def top_prix_par_batiment(type_batiment : TypeBatiment, ascendant: bool, limit_top):
    if ascendant : order = 'ASC'
    else : order = 'DESC'
    req=f"SELECT ville, type_batiment, AVG(ROUND(prix/surface_habitable)) as prix_m2_moy FROM transactions\
        WHERE type_batiment = '{type_batiment.value}' GROUP BY ville  ORDER BY prix_m2_moy {order} LIMIT {limit_top}"
    answer=apply_request(req)
    return answer