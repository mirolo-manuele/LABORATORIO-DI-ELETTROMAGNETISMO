import ROOT
from array import array
import numpy as np
import pandas as pd

df = pd.read_excel("Esperienza_2.xlsx", sheet_name="Temp_5") #legge il file excel
df = df.dropna(subset=["qV/kT", "lnCorr(mA)"]) #controlla solo le colonne V e I. Se una di queste contiene un valore mancante, elimina quella riga

V = array('d', df["qV/kT"].to_numpy(dtype=float)) #df è il dataframe, "V" è il nome della colonna da leggere 
I = array('d', df["lnCorr(mA)"].to_numpy(dtype=float)) #to_numpy converte la colonna in un array NumPy di tipo float.

eV = array('d', [0.0]*len(V))
eI = array('d', [0.0]*len(I))

v_max=25
v_min=12


c = ROOT.TCanvas("c", "coefficiente eta", 800, 600)

g=ROOT.TGraphErrors(len(V), V, I, eV, eI)

g.SetTitle("coefficiente eta;qV/kT;I") 
g.SetMarkerStyle(21) 
g.SetMarkerColor(ROOT.kBlue) 
g.SetMarkerSize(0.5) 
g.SetLineColor(ROOT.kRed) 
g.SetLineWidth(1) 

g.Draw("APL")

indici_fit = [i for i in range(len(V)) if V[i] >= v_min and V[i]<= v_max]

x_fit = array('d', [V[i] for i in indici_fit])
y_fit = array('d', [I[i] for i in indici_fit])

g_fit = ROOT.TGraphErrors(len(x_fit), x_fit, y_fit,) 

ROOT.gStyle.SetOptFit(11)#stampa solo parametri fit ed errori

fit_func = ROOT.TF1("fit_func", "pol1", min(x_fit), max(x_fit))

# Rinomina dei parametri, mettere prima di fit_result (che fa il fit)
fit_func.SetParName(0, "q")
fit_func.SetParName(1, "m")

# Eseguire il fit e poi calcolare eta usando il parametro di pendenza m
fit_result = g_fit.Fit(fit_func, "S+", "", min(x_fit), max(x_fit))
eta = 1.0 / fit_func.GetParameter(1)

  
g_fit.Draw("Q")#mi serve per far comparire la tabella delle statistiche del fit, Q quiet
fit_func.SetLineColor(ROOT.kBlack)
fit_func.SetLineWidth(2)
fit_func.Draw("SAME")


print("eta=",eta)
c.Modified() 
c.Update()
c.Draw()
c.SaveAs("coefficiente_eta5.png") 
input("Premi Invio per chiudere...") 
