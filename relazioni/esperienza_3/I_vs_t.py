import ROOT
from array import array
import numpy as np
import pandas as pd

df = pd.read_excel("faraday.xlsx", sheet_name="I_vs_t") #legge il file excel
df = df.dropna(subset=["T", "I"]) #controlla solo le colonne V e I. Se una di queste contiene un valore mancante, elimina quella riga

I = array('d', df["I"].iloc[236:40318].to_numpy(dtype=float))
V = array('d', df["T"].iloc[236:40318].to_numpy(dtype=float)) #df è il dataframe, "V" è il nome della colonna da leggere 


eV = array('d', [0.0]*len(V))
eI = array('d', [0.0]*len(I))



c = ROOT.TCanvas("c", "I vs t", 800, 600)

g=ROOT.TGraphErrors(len(V), V, I, eV, eI)

g.SetTitle("I vs t;t[s];I[A]") 
g.SetMarkerStyle(21) 
g.SetMarkerColor(ROOT.kBlue) 
g.SetMarkerSize(0.5) 
g.SetLineWidth(1) 

g.Draw("AP")




c.Modified() 
c.Update()
c.Draw()

c.SaveAs("I_vs_t.pdf") 
input("Premi Invio per chiudere...") 
