import ROOT
from array import array
import numpy as np
import pandas as pd

df = pd.read_excel("faraday.xlsx", sheet_name="Dati") #legge il file excel
df = df.dropna(subset=["T", "R"]) #controlla solo le colonne V e I. Se una di queste contiene un valore mancante, elimina quella riga

I = array('d', df["R"].to_numpy(dtype=float))
V = array('d', df["T"].to_numpy(dtype=float)) #df è il dataframe, "V" è il nome della colonna da leggere 


eV = array('d', [0.0]*len(V))
eI = array('d', [0.0]*len(I))

vmin=200
vmax= 4000000

c = ROOT.TCanvas("c", "R vs t", 800, 600)

g=ROOT.TGraphErrors(len(V), V, I, eV, eI)

g.SetTitle("R vs t; t[s]; R[Ohm]") 
g.SetMarkerStyle(21) 
g.SetMarkerColor(ROOT.kBlue) 
g.SetMarkerSize(0.5) 
g.SetLineWidth(1) 

g.Draw("AP")




c.Modified() 
c.Update()
c.Draw()

c.SaveAs("Resistenza_nel_tempo.pdf") 
input("Premi Invio per chiudere...") 