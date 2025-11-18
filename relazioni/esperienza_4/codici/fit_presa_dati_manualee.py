import ROOT
from array import array
import numpy as np
import pandas as pd

df = pd.read_excel("Circuito_RC.xlsx", sheet_name="Carica condensatore") #legge il file excel
df = df.dropna(subset=["t", "log V"]) #controlla solo le colonne V e I. Se una di queste contiene un valore mancante, elimina quella riga

t = array('d', df["t"].to_numpy(dtype=float))
V = array('d', df["log V"].to_numpy(dtype=float)) #df è il dataframe, "V" è il nome della colonna da leggere 


et = array('d', [0.0]*len(V))
eV = array('d', [0.0]*len(t))

c = ROOT.TCanvas("c", "log V vs t", 1700, 600)

g=ROOT.TGraphErrors(len(V), t, V, et, eV)

g.SetTitle("log V vs t; t[s]; log V") 
g.SetMarkerStyle(21) 
g.SetMarkerColor(ROOT.kBlue) 
g.SetMarkerSize(1)
g.SetLineWidth(1) 

v_soglia=0
v_sup=10000

g.Draw("APL")

indici_fit = [i for i in range(len(t)) if t[i] >= v_soglia and t[i] <=v_sup] 

x_fit = array('d', [t[i] for i in indici_fit])
y_fit = array('d', [V[i] for i in indici_fit])
ey_fit = array('d', [eV[i] for i in indici_fit]) 

g_fit = ROOT.TGraphErrors(len(x_fit), x_fit, y_fit, et, ey_fit)



ROOT.gStyle.SetOptFit(11) 

fit_func = ROOT.TF1("fit", "pol1", min(x_fit), max(x_fit))
fit_func.SetParName(0, "q")
fit_func.SetParName(1, "m")
fit_result = g_fit.Fit(fit_func, "S+", "",min(x_fit), max(x_fit)) 

fit_func.SetLineColor(ROOT.kRed)
fit_func.SetLineWidth(2)

fit_func.Draw("SAME") 

c.Update()

m=fit_func.GetParameter(1)
em=fit_func.GetParError(1)
rc= -1/m
erc = em / (m**2) 
print(f"RC fit: {rc:.3e} ± {erc:.3e}")

c.Modified() 
c.Update()
c.Draw()

c.SaveAs("fit_presa_dati_manuale.pdf") 
input("Premi Invio per chiudere...") 