import numpy as np
import pandas as pd
import requests
import sqlite3

"""
con = sqlite3.connect("Chinook.db")


except sqlite3.Error:"""
# Récupérer la DB de Kaggle via l'URL
kaggle_url = "https://www.kaggle.com/datasets/benoitfavier/immobilier-france/download?datasetVersionNumber=3"
response=requests.get(kaggle_url)
print(response.content)

arrays = dict(np.load(response.content))
data = {k: [s.decode("utf-8") for s in v.tobytes().split(b"\x00")] if v.dtype == np.uint8 else v for k, v in arrays.items()}
transactions = pd.DataFrame.from_dict(data)

#database = response.content.json()
#df= pd.DataFrame()




arrays = dict(np.load(r"C:\Users\Utilisateur\Downloads\transactions.npz"))
data = {k: [s.decode("utf-8") for s in v.tobytes().split(b"\x00")] if v.dtype == np.uint8 else v for k, v in arrays.items()}
transactions = pd.DataFrame.from_dict(data)

transactions.to_csv(r"C:\Users\Utilisateur\Downloads\transactions.csv", header=True)