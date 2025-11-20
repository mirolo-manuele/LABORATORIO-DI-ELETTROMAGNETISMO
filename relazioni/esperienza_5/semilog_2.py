import ROOT
from ROOT import TLine
from array import array
import numpy as np
import pandas as pd

df = pd.read_excel("Esperienza_5.xlsx", sheet_name="Dati_2") #legge il file excel
df = df.dropna(subset=["T", "LOG (V)"]) #controlla solo le colonne V e I. Se una di queste contiene un valore mancante, elimina quella riga


t = array('d', df["T"].to_numpy(dtype=float))
V = array('d', df["LOG (V)"].to_numpy(dtype=float)) #df è il dataframe, "V" è il nome della colonna da leggere 


et = array('d', [0.0]*len(V))
eV = array('d', [0.0]*len(t))



c = ROOT.TCanvas("c", "V vs T", 800, 600)

g=ROOT.TGraphErrors(len(V), t, V, et, eV)

g.SetTitle("log V vs T; T[s]; log V") 
g.SetMarkerStyle(21) 
g.SetMarkerColor(ROOT.kBlack) 
g.SetLineColor(ROOT.kBlue)
g.SetMarkerSize(0.5)
g.SetLineWidth(1) 
g.Draw("APL")

gfit = ROOT.TF1("gfit", "pol1", 0, max(t))
gfit.SetParName(0, "q")
gfit.SetParName(1, "m")
gfit.SetLineColor(ROOT.kRed)
gfit.Draw("same")
fit_result = g.Fit(gfit, "S+", "", 0, max(t))
ROOT.gStyle.SetOptFit(11) 

m=gfit.GetParameter(1)
q=gfit.GetParameter(0)
em=gfit.GetParError(1)
eq=gfit.GetParError(0)

Γ= -2*m
eΓ= 2*em

R=230


L=(R/Γ)*1000
eL=(R/(Γ**2))*eΓ*1000

real_L=43
percentual_error= (abs(L - real_L)/real_L)*100

print(" il valore dell'induttanza è:")
print(f"L = ({L:.3f} ± {eL:.3f}) mH")
print(f"L'errore è del: {percentual_error:.2f} %")

c.Modified() 
c.Update()
c.Draw()

c.SaveAs("semilog_2.pdf") 
input("Premi Invio per chiudere...") 