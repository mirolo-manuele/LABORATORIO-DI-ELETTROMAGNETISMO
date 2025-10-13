import ROOT
from array import array
import numpy as np
import pandas as pd

df = pd.read_excel("dati.xlsx")

V = array('d', df["V"].to_numpy(dtype=float))
I = array('d', df["I"].to_numpy(dtype=float))


eV = array('d', df["eV"].to_numpy(dtype=float))
eI = array('d', df["eI"].to_numpy(dtype=float))

c = ROOT.TCanvas("c", "Curva voltammetrica", 800, 600)

g=ROOT.TGraphErrors(len(V), V, I, eV, eI)

g.SetTitle("Curva voltammetrica;V[mV];I[mA]") 
g.SetMarkerStyle(21) 
g.SetMarkerColor(ROOT.kBlue) 
g.SetMarkerSize(0.5) 
g.SetLineColor(ROOT.kRed) 
g.SetLineWidth(1) 

g.Draw("APL")
c.Modified() 
c.Update()
c.Draw()
c.SaveAs("curva voltammetrica.png") 
input("Premi Invio per chiudere...") 