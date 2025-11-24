import ROOT
from ROOT import TLine
from array import array
import numpy as np
import pandas as pd

df = pd.read_excel("Esperienza_5.xlsx", sheet_name="Dati_2") #legge il file excel
df = df.dropna(subset=["T", "V"]) #controlla solo le colonne V e I. Se una di queste contiene un valore mancante, elimina quella riga


t = array('d', df["T"].to_numpy(dtype=float))
V = array('d', df["V"].to_numpy(dtype=float)) #df è il dataframe, "V" è il nome della colonna da leggere 


et = array('d', [0.0]*len(V))
eV = array('d', [0.0]*len(t))



c = ROOT.TCanvas("c", "V vs T", 1700, 600)

g=ROOT.TGraphErrors(len(V), t, V, et, eV)

g.SetTitle("V vs T; T[s]; Voltaggio[V]") 
g.SetMarkerStyle(21) 
g.SetMarkerColor(ROOT.kBlack) 
g.SetLineColor(ROOT.kBlue)
g.SetMarkerSize(0.5)
g.SetLineWidth(1) 
g.Draw("APC")

line= TLine(3.7*10E-5,0, 9*10E-5 ,0)
line.SetLineColor(ROOT.kBlack)
line.SetLineWidth(1)    
line.Draw("same")


c.Modified() 
c.Update()
c.Draw()

c.SaveAs("oscillazione_smorzata_2.pdf") 
input("Premi Invio per chiudere...") 