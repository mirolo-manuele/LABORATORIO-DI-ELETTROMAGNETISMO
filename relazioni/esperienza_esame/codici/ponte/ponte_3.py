import ROOT
import pandas as pd
from array import array
import numpy as np
import math

# 1. Leggi il CSV specificando il separatore
df = pd.read_csv("/Users/alessiobrusini/Desktop/LABORATORIO-DI-ELETTROMAGNETISMO/relazioni/esperienza_esame/codici/file_csv/WaveData5911.csv", sep=",", comment='#')
df1 = pd.read_csv("/Users/alessiobrusini/Desktop/LABORATORIO-DI-ELETTROMAGNETISMO/relazioni/esperienza_esame/codici/file_csv/WaveData5910.csv", sep=",", comment='#')
n_soglia_inf = 0
n_soglia_sup = 2000
R_in= 830000
C_in = 0.00022

# valori buoni 626, 2535 

# Estrai i dati come array NumPy
t_np = df.iloc[n_soglia_inf:n_soglia_sup, 0].to_numpy(dtype=float)
V_np = df.iloc[n_soglia_inf:n_soglia_sup, 1].to_numpy(dtype=float)
# Estrai i dati come array NumPy
t_np1 = df1.iloc[n_soglia_inf+125:n_soglia_sup+2000, 0].to_numpy(dtype=float)
V_np1 = df1.iloc[n_soglia_inf+125:n_soglia_sup+2000, 1].to_numpy(dtype=float)


# --- APPLICAZIONE VETTORIZZATA (PIÙ VELOCE) ---
V_np += 0 # Aggiunge 6.240 a tutti gli elementi di V_np
V_np = V_np # Riscalo tutto perchè abbiamo preso dati sbagliati
t_np -= t_np[0] # Normalizzo t sottraendo primo elemento
# ---------------------------------------------
# --- APPLICAZIONE VETTORIZZATA (PIÙ VELOCE) ---
V_np1 += 0 # Aggiunge 6.240 a tutti gli elementi di V_np
V_np1 = V_np1 # Riscalo tutto perchè abbiamo preso dati sbagliati
t_np1 -= t_np1[0] # Normalizzo t sottraendo primo elemento






#c2 = ROOT.TCanvas("c2", "t vs ln(V)", 800, 600)
g = ROOT.TGraphErrors(len(t_np), t_np, V_np)
g2= ROOT.TGraphErrors(len(t_np1), t_np1, V_np1)
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

# 4. Usiamo TMultiGraph per sovrapporli
mg = ROOT.TMultiGraph()
mg.SetTitle("1#circ configurazione ponte;t[s]; V[V]") # Titolo globale;X;Y

    # Aggiungiamo i grafici al contenitore
    # "LP" significa disegna Linea e Punti per quel grafico
mg.Add(g, "L")
mg.Add(g2, "L")
    # 5. Disegniamo il tutto
    # "A" disegna gli assi attorno a tutti i grafici contenuti
mg.Draw("A") 
    
# 6. Aggiungiamo la legenda (fondamentale per capire chi è chi)
leg = ROOT.TLegend(0.75, 0.75, 0.9, 0.9) # Coordinate x1, y1, x2, y2
leg.AddEntry(g, "R= 830 k#Omega", "lp")
leg.AddEntry(g2, "C = 220 #muF", "lp")
leg.Draw()
    # Manteniamo la finestra aperta (necessario se esegui da script)
c.Update()
print("V_medio_maggiore =", np.mean(V_np1))
print("V_ripple_maggiore =", (np.max(V_np1)-np.min(V_np1)))
print("fattore di Ripple =", (np.max(V_np1)-np.min(V_np1))/np.mean(V_np1))

c.SaveAs("ponte_3.pdf")