import ROOT
from array import array
import numpy as np
import pandas as pd

df = pd.read_excel("Esperienza_2.xlsx", sheet_name="Pol_inv") #legge il file excel
df = df.dropna(subset=["Volt(mV)", "Corr(μA)"]) #controlla solo le colonne V e I. Se una di queste contiene un valore mancante, elimina quella riga

V = array('d', df["Volt(mV)"].to_numpy(dtype=float)) #df è il dataframe, "V" è il nome della colonna da leggere 
I = array('d', df["Corr(μA)"].to_numpy(dtype=float)) #to_numpy converte la colonna in un array NumPy di tipo float.

eV = array('d', [0.0]*len(V))
eI = array('d', [0.0]*len(I))

v_min=-4500
v_max=-500



c = ROOT.TCanvas("c", "Polarizzazzione inversa", 800, 600)

g=ROOT.TGraphErrors(len(V), V, I, eV, eI)

g.SetTitle("Polarizzazzione inversa; Voltaggio (mV); I(#muA)") 
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

# IMPOSTA LA POSIZIONE PRIMA del fit
ROOT.gStyle.SetOptFit(11) #stampa solo parametri ed errori
ROOT.gStyle.SetStatX(0.9)  # Posizione X (0-1, da sinistra a destra)
ROOT.gStyle.SetStatY(0.4)  # Posizione Y (0-1, dal basso all'alto)
ROOT.gStyle.SetStatW(0.2)  # Larghezza della box
ROOT.gStyle.SetStatH(0.1)  # Altezza della box

fit_func = ROOT.TF1("fit_func", "pol1", min(x_fit), max(x_fit))

# Rinomina dei parametri, mettere prima di fit_result (che fa il fit)
fit_func.SetParName(0, "q")
fit_func.SetParName(1, "m")

# Eseguire il fit e poi calcolare eta usando il parametro di pendenza m
fit_result = g_fit.Fit(fit_func, "S+", "", min(x_fit), max(x_fit))

  
g_fit.Draw("Q")#mi serve per far comparire la tabella delle statistiche del fit, Q quiet
fit_func.SetLineColor(ROOT.kBlack)
fit_func.SetLineWidth(2)
fit_func.Draw("SAME")
c.Modified() 
c.Update()
c.Draw()
c.SaveAs("pol_inv.pdf") 
input("Premi Invio per chiudere...") 