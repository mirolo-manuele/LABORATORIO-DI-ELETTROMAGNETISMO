import ROOT
from array import array
import numpy as np
import pandas as pd

df = pd.read_excel("Carica_scarica.xlsx", sheet_name="WaveData541") #legge il file excel
df = df.dropna(subset=["Column1", "log"]) #controlla solo le colonne V e I. Se una di queste contiene un valore mancante, elimina quella riga

t = array('d', df["Column1"].to_numpy(dtype=float))
V = array('d', df["log"].to_numpy(dtype=float)) #df è il dataframe, "V" è il nome della colonna da leggere 


et = array('d', [0.0]*len(V))
eV = array('d', [0.0]*len(t))



c = ROOT.TCanvas("c", "V vs t", 1700, 600)

g=ROOT.TGraphErrors(len(V), t, V, et, eV)

g.SetTitle("Q vs t;t[s]Q[C]") 
g.SetMarkerStyle(21) 
g.SetMarkerColor(ROOT.kBlue) 
g.SetMarkerSize(0.3)
g.SetLineWidth(1) 

v_soglia=8.64E-6
v_sup=1.2E-5
indici_fit = [i for i in range(len(t)) if t[i] >= v_soglia and t[i] <=v_sup] #creo un array con gli indici dei punti con x >= v_soglia
#metto nella lista i (primo i) (potevo mettere per esempio i^2)
#questo i (o i^2) è associato ad ogni posizione dell'array (for i in range(len(x))
#ma tutto ciò solo se x[i] >= v_soglia

x_fit = array('d', [t[i] for i in indici_fit])
y_fit = array('d', [V[i] for i in indici_fit])
ey_fit = array('d', [eV[i] for i in indici_fit]) #creo un array con solo i dati con x >= v_soglia

g_fit = ROOT.TGraphErrors(len(x_fit), x_fit, y_fit, et, ey_fit) #Crea un nuovo grafico con solo i punti filtrati (x ≥ v_soglia)
ROOT.gStyle.SetOptFit(1111) #mostra le statistiche del fit sul grafico (parametri, chi2, ndf, probabilità)

fit_func = ROOT.TF1("fit_func", "pol1",min(x_fit), max(x_fit))



fit_result = g_fit.Fit(fit_func, "S+", "",min(x_fit), max(x_fit)) #esegue il fit su g_fit

#v_soglia, max(x) = intervallo del fit

# Parametri del fit (posso farlo perchè ho messo "S" nelle opzioni del fit)
m = fit_func.GetParameter(1)
q = fit_func.GetParameter(0)
dm = fit_func.GetParError(1)
dq = fit_func.GetParError(0)



fit_func.SetLineColor(ROOT.kBlack)
fit_func.SetLineWidth(2)
g.Draw("AP")

fit_func.Draw("SAME") #disegna la funzione di fit sullo stesso grafico






c.Modified() 
c.Update()
c.Draw()

c.SaveAs("Q_vs_t.pdf") 
input("Premi Invio per chiudere...") 