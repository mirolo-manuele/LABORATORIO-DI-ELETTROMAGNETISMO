import ROOT
from array import array
import numpy as np
import pandas as pd

df = pd.read_excel("Carica_scarica.xlsx", sheet_name="WaveData540") #legge il file excel
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

g.Draw("AL")




c.Modified() 
c.Update()
c.Draw()

c.SaveAs("Q_vs_t.pdf") 
input("Premi Invio per chiudere...") 