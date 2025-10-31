import pandas as pd
from array import array
import numpy as np

Area= 0.0041440932  # m^2
Diff_m= -2.35e-03  #kg


# 1. Leggi il CSV specificando il separatore
df = pd.read_csv("squadra_Minnie_28_10.csv", sep=";")

# 3. Converti in array numerici
I = np.array(df["Amperom"].to_numpy(dtype=float))  # usa direttamente numpy
I_media = (I[:-1] + I[1:]) / 2

# Matrice dei tempi (esempio)
t_matrix = df[["giorno", "ora", "minuti", "secondi", "msec"]].to_numpy(dtype=float)

# Differenze tra righe
diff_matrix = np.diff(t_matrix, axis=0)

# Pesi (scegli tu in base all'unità, ad esempio per convertire tutto in secondi)
weights = np.array([24*3600, 3600, 60, 1, 1e-3])  # giorno→s, ora→s, min→s, sec→s, msec→s

# Somma pesata
weighted_sum = np.sum(diff_matrix * weights, axis=1)

Q=np.dot(weighted_sum, I_media)
F= Area / (2*Diff_m) * Q
print(Q)
print(F)