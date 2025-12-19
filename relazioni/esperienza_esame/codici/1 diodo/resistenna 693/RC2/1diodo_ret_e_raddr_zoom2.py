import ROOT
from array import array
import numpy as np
import pandas as pd

df = pd.read_csv("WaveData594.csv") #legge il file excel
df = df.dropna(subset=["t", "V"]) #controlla solo le colonne V e I. Se una di queste contiene un valore mancante, elimina quella riga


t = array('d', df["t"].to_numpy(dtype=float))
V = array('d', df["V"].to_numpy(dtype=float)) #df è il dataframe, "V" è il nome della colonna da leggere 


et = array('d', [0.0]*len(V))
eV = array('d', [0.0]*len(t))

c = ROOT.TCanvas("c", "t vs V", 1700, 600)

g=ROOT.TGraphErrors(len(V), t, V, et, eV)

g.SetMinimum(-0.5)

g.SetTitle("Diodo rettificato e raddrizzato; t[s]; Voltaggio[V]") 
g.SetMarkerStyle(21) 
g.SetMarkerColor(ROOT.kBlack) 
g.SetMarkerSize(0.3)
g.SetLineWidth(1) 

g.Draw("AL")

c.Modified() 
c.Update()
c.Draw()

c.SaveAs("1diodo_ret_e_raddr_zoom2.pdf") 
input("Premi Invio per chiudere...") 