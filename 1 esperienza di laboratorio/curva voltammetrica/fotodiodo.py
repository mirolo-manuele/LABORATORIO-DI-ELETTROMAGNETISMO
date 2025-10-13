import ROOT
from array import array
import numpy as np
import pandas as pd

df = pd.read_excel("prova1.xlsx") 
df = df.dropna(subset=["V", "I"])

V = array('d', df["V"].to_numpy(dtype=float)) 
Tfd = array('d', df["Tfd"].to_numpy(dtype=float)) 

eV = array('d', df["eV"].to_numpy(dtype=float))

c = ROOT.TCanvas("c", "Fotodiodo", 800, 600)

g=ROOT.TGraphErrors(len(V), V, Tfd, eV)

g.SetTitle("Fotodiodo;V[mV];Tfd[mV]") 
g.SetMarkerStyle(21) 
g.SetMarkerColor(ROOT.kBlue) 
g.SetMarkerSize(0.5) 
g.SetLineColor(ROOT.kRed) 
g.SetLineWidth(1) 

g.Draw("APL")
c.Modified() 
c.Update()
c.Draw()
c.SaveAs("fotodiodo.png") 
input("Premi Invio per chiudere...") 