import numpy as np
import pandas as pd

arrays = dict(np.load(r"C:\Users\Utilisateur\Downloads\transactions.npz"))
data = {k: [s.decode("utf-8") for s in v.tobytes().split(b"\x00")] if v.dtype == np.uint8 else v for k, v in arrays.items()}
transactions = pd.DataFrame.from_dict(data)

transactions.to_csv(r"C:\Users\Utilisateur\Downloads\transactions.csv", header=True)