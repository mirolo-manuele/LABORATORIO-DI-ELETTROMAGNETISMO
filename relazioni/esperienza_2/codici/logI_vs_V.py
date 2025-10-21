import ROOT
from array import array
import numpy as np
import pandas as pd

df = pd.read_excel("Esperienza_2.xlsx", sheet_name="Temp_1") #legge il file excel
df = df.dropna(subset=["Volt(mV)","lnCorr(mA)"]) #controlla solo le colonne V e I. Se una di queste contiene un valore mancante, elimina quella riga

V = array('d', df["Volt(mV)"].to_numpy(dtype=float)) #df è il dataframe, "V" è il nome della colonna da leggere 
lnI = array('d', df["lnCorr(mA)"].to_numpy(dtype=float)) #to_numpy converte la colonna in un array NumPy di tipo float.

eV = array('d', [0.0]*len(V))
elnI = array('d', [0.0]*len(lnI))

v_max=700
v_min=300


c = ROOT.TCanvas("c", "coefficiente eta", 800, 600) #tavolozza

g=ROOT.TGraphErrors(len(V), V, lnI, eV, elnI) #len(V) è il numero di punti, V e I sono gli array dei dati, eV e eI sono gli errori associati 
g.SetTitle("Grafico semilogaritmico;Tensione(V);ln(I)") 
g.SetMarkerStyle(21) 
g.SetMarkerColor(ROOT.kBlue) 
g.SetMarkerSize(0.5) 
g.SetLineColor(ROOT.kRed) 
g.SetLineWidth(1) 

g.Draw("APL") 

indici_fit = [i for i in range(len(V)) if V[i] >= v_min and V[i]<= v_max] #sceglie l'intervallo in cui fare il fit (tra v_min e v_max)

x_fit = array('d', [V[i] for i in indici_fit])
y_fit = array('d', [lnI[i] for i in indici_fit])

g_fit = ROOT.TGraphErrors(len(x_fit), x_fit, y_fit,) 

ROOT.gStyle.SetOptFit(11) #stampa solo parametri m e q fit ed errori

fit_func = ROOT.TF1("fit_func", "pol1", min(x_fit), max(x_fit)) #pol1 significa polinomio di grado 1

#Rinomina dei parametri, mettere prima di fit_result (che fa il fit)
fit_func.SetParName(0, "q")
fit_func.SetParName(1, "m")

# Eseguire il fit e poi calcolare eta usando il parametro di pendenza m
fit_result = g_fit.Fit(fit_func, "S+", "", min(x_fit), max(x_fit))
  
g_fit.Draw("Q")#mi serve per far comparire la tabella delle statistiche del fit, Q quiet
fit_func.SetLineColor(ROOT.kBlack)
fit_func.SetLineWidth(2)
fit_func.Draw("SAME") #disegno sullo stesso grafico


#print("eta=",eta)
c.Modified() 
c.Update()
c.Draw()
c.SaveAs("scala_semilogaritmica.png") 
input("Premi Invio per chiudere...") 