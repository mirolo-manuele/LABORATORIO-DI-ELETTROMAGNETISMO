import ROOT
from array import array
import numpy as np
import pandas as pd

df = pd.read_excel("Carica_scarica2.xlsx", sheet_name="1_PROVA") #legge il file excel
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
g.SetMarkerSize(0.3)
g.SetLineWidth(1) 

v_soglia=[0, 2.03E-5]
v_sup=[1.4E-5, 2.8E-5]

fit_graphs = []
fit_functions = []

g.Draw("AL")

for j in range(0,2):
    s=str(j)
    indici_fit = [i for i in range(len(t)) if t[i] >= v_soglia[j] and t[i] <=v_sup[j]] 

    x_fit = array('d', [t[i] for i in indici_fit])
    y_fit = array('d', [V[i] for i in indici_fit])
    ey_fit = array('d', [eV[i] for i in indici_fit]) 

    g_fit = ROOT.TGraphErrors(len(x_fit), x_fit, y_fit, et, ey_fit)
    g_fit.SetName(f"g_fit_{s}") 
    

    fit_graphs.append(g_fit)
    ROOT.gStyle.SetOptFit(11) 

    fit_name = f"fit_{s}"
    fit_func = ROOT.TF1(fit_name, "pol1", min(x_fit), max(x_fit))
    fit_func.SetParName(0, "q")
    fit_func.SetParName(1, "m")
    fit_result = g_fit.Fit(fit_func, "S+", "",min(x_fit), max(x_fit)) 

    fit_func.SetLineColor(ROOT.kRed)
    fit_func.SetLineWidth(2)

    fit_func.Draw("SAME") 
    fit_functions.append(fit_func)
    c.Update()
    
    m=fit_func.GetParameter(1)
    em=fit_func.GetParError(1)
    rc= -1/m
    erc = em / (m**2) 
    print(f"RC fit {s}: {rc:.3e} ± {erc:.3e}")

c.Modified() 
c.Update()
c.Draw()

c.SaveAs("log_V_vs_t_1.pdf") 
input("Premi Invio per chiudere...") 