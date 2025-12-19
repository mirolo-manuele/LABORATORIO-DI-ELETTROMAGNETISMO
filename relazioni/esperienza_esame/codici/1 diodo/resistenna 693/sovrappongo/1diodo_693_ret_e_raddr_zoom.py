import ROOT
from array import array
import numpy as np
import pandas as pd

df = pd.read_csv("WaveData593.csv") #legge il file excel
df = df.dropna(subset=["t", "V"]) #controlla solo le colonne V e I. Se una di queste contiene un valore mancante, elimina quella riga


t = array('d', df["t"].to_numpy(dtype=float))
V = array('d', df["V"].to_numpy(dtype=float)) #df è il dataframe, "V" è il nome della colonna da leggere 


et = array('d', [0.0]*len(V))
eV = array('d', [0.0]*len(t))

c = ROOT.TCanvas("c", "t vs V", 1700, 600)

g=ROOT.TGraphErrors(len(V), t, V, et, eV)


g.SetTitle("Diodo rettificato e raddrizzato; t[s]; Voltaggio[V]") 
g.SetMarkerStyle(21) 
g.SetMarkerColor(ROOT.kBlack) 
g.SetMarkerSize(0.3)
g.SetLineWidth(1) 

g.Draw("AL")

linea1 = ROOT.TLine(0, 10.4, 0.085, 10.4) 

linea1.SetLineColor(ROOT.kRed)
linea1.SetLineWidth(2)
linea1.SetLineStyle(2)
linea1.Draw() # Non serve specificare opzioni per TLine


linea = ROOT.TLine(0, 12, 0.085, 12) 

linea.SetLineColor(ROOT.kRed)
linea.SetLineWidth(2)
linea.SetLineStyle(2)

linea.Draw() # Non serve specificare opzioni per TLine

c.Modified() 
c.Update()
c.Draw()

c.SaveAs("1diodo_ret_e_raddr_zoom.pdf") 
input("Premi Invio per chiudere...")