import ROOT
import pandas as pd
from array import array
import numpy as np
import math

# 1. Leggi il CSV specificando il separatore
df = pd.read_csv("/Users/alessiobrusini/Desktop/LABORATORIO-DI-ELETTROMAGNETISMO/relazioni/esperienza_esame/codici/file_csv/WaveData5912.csv", sep=",", comment='#')
df1 = pd.read_csv("/Users/alessiobrusini/Desktop/LABORATORIO-DI-ELETTROMAGNETISMO/relazioni/esperienza_esame/codici/file_csv/WaveData5913.csv", sep=",", comment='#')
df2 = pd.read_csv("/Users/alessiobrusini/Desktop/LABORATORIO-DI-ELETTROMAGNETISMO/relazioni/esperienza_esame/codici/file_csv/WaveData5914.csv", sep=",", comment='#')
n_soglia_inf = 4
n_soglia_sup = 2500
R_in= 693
C_in = 0.00047

# valori buoni 626, 2535 

# Estrai i dati come array NumPy
t_np = df.iloc[n_soglia_inf:n_soglia_sup, 0].to_numpy(dtype=float)
V_np = df.iloc[n_soglia_inf:n_soglia_sup, 1].to_numpy(dtype=float)
# Estrai i dati come array NumPy
t_np1 = df1.iloc[n_soglia_inf+150:n_soglia_sup+150, 0].to_numpy(dtype=float)
V_np1 = df1.iloc[n_soglia_inf+150:n_soglia_sup+150, 1].to_numpy(dtype=float)

t_np2 = df2.iloc[n_soglia_inf+142:n_soglia_sup+142, 0].to_numpy(dtype=float)
V_np2 = df2.iloc[n_soglia_inf+142:n_soglia_sup+142, 1].to_numpy(dtype=float)

# --- APPLICAZIONE VETTORIZZATA (PIÙ VELOCE) ---
V_np += 0 # Aggiunge 6.240 a tutti gli elementi di V_np
V_np = V_np # Riscalo tutto perchè abbiamo preso dati sbagliati
t_np -= t_np[0] # Normalizzo t sottraendo primo elemento
# ---------------------------------------------
# --- APPLICAZIONE VETTORIZZATA (PIÙ VELOCE) ---
V_np1 += 0 # Aggiunge 6.240 a tutti gli elementi di V_np
V_np1 = V_np1 # Riscalo tutto perchè abbiamo preso dati sbagliati
t_np1 -= t_np1[0] # Normalizzo t sottraendo primo elemento

V_np2 += 0 # Aggiunge 6.240 a tutti gli elementi di V_np
V_np2 = V_np2 # Riscalo tutto perchè abbiamo preso dati sbagliati
t_np2 -= t_np2[0] # Normalizzo t sottraendo primo elemento


# Trova dove il prodotto di elementi consecutivi è negativo
# Verrà creato un array di booleani (True/False)
crossings_bool = np.sign(V_np[:-1]) != np.sign(V_np[1:])

# Ottiene gli indici del *primo* elemento di ogni coppia che attraversa lo zero.
# Questi indici sono i punti immediatamente *prima* del crossing.
indices_before = np.where(crossings_bool)[0]
closest_time_points = t_np[indices_before]
mask_t = (closest_time_points > 0.00005) & (closest_time_points < 0.0004)
t_periodi= closest_time_points[mask_t]
t_periodi_diff = np.diff(t_periodi)
mask_t_2 = t_periodi_diff > 1E-05
t_periodi_diff = t_periodi_diff[mask_t_2]
t_periodi_1 = t_periodi_diff *2
t_medio = np.mean(t_periodi_1)
v_ang = 2*math.pi / t_medio




#c2 = ROOT.TCanvas("c2", "t vs ln(V)", 800, 600)
g = ROOT.TGraphErrors(len(t_np), t_np, V_np)
g2= ROOT.TGraphErrors(len(t_np1), t_np1, V_np1)
g3= ROOT.TGraphErrors(len(t_np2), t_np2, V_np2)
# 6. Crea il Canvas e Dividilo
# Un canvas più largo è utile per due grafici affiancati (es. 1200x600)
c = ROOT.TCanvas("c", "Grafico Lineare e Semilogaritmico", 1200, 600)

ROOT.gPad.SetGrid() #comando per comparire griglia 

# Imposta il titolo per il grafico lineare
g.SetTitle("Scala Lineare;t [s];V [V]")
g.SetMarkerStyle(21)
g.SetMarkerColor(ROOT.kBlue)
g.SetLineColor(ROOT.kBlue)
g.SetMarkerSize(0.5)

g2.SetTitle("Scala Lineare;t [s];V [V]")
g2.SetMarkerStyle(21)
g2.SetMarkerColor(ROOT.kRed)
g2.SetLineColor(ROOT.kRed)
g2.SetMarkerSize(0.5)

g3.SetTitle("Scala Lineare;t [s];V [V]")
g3.SetMarkerStyle(21)
g3.SetMarkerColor(ROOT.kRed)
g3.SetLineColor(ROOT.kMagenta)
g3.SetMarkerSize(0.5)
# 4. Usiamo TMultiGraph per sovrapporli
mg = ROOT.TMultiGraph()
mg.SetTitle("Confronto tra due CSV; t [s]; Voltaggio [V]") # Titolo globale;X;Y

    # Aggiungiamo i grafici al contenitore
    # "LP" significa disegna Linea e Punti per quel grafico
mg.Add(g, "L")
mg.Add(g3, "L")
mg.Add(g2, "L")
    # 5. Disegniamo il tutto
    # "A" disegna gli assi attorno a tutti i grafici contenuti
mg.Draw("A") 
    
# 6. Aggiungiamo la legenda (fondamentale per capire chi è chi)
leg = ROOT.TLegend(0.75, 0.75, 0.9, 0.9) # Coordinate x1, y1, x2, y2
leg.AddEntry(g, "R= 693 #Omega", "lp")
leg.AddEntry(g3, "C = 22 #muF", "lp")
leg.AddEntry(g2, "C = 470 #muF", "lp")

leg.Draw()
    # Manteniamo la finestra aperta (necessario se esegui da script)
c.Update()
print("V_medio_maggiore =", np.mean(V_np1))
print("V_ripple_maggiore =", (np.max(V_np1)-np.min(V_np1)))
print("fattore di Ripple =", (np.max(V_np1)-np.min(V_np1))/np.mean(V_np1))
print("Abbassamento tensione =", max(V_np)-max(V_np1))
c.SaveAs("ponte_invertito.pdf")
