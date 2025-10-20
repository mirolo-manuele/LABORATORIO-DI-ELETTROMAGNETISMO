import ROOT
from array import array
import numpy as np
import pandas as pd

df = pd.read_excel("prova1.xlsx", sheet_name="Sheet2") 
df = df.dropna(subset=["V", "Rd"])

V = array('d', df["V"].to_numpy(dtype=float)) 
Rd = array('d', df["Rd"].to_numpy(dtype=float)) 

eV = array('d', df["eV"].to_numpy(dtype=float))

c = ROOT.TCanvas("c", "Curva resistenza dinamica", 800, 600)

g=ROOT.TGraphErrors(len(V), V, Rd, eV)

g.SetTitle("Resistenza dinamica;V[mV];Rd[Ohm]") 
g.SetMarkerStyle(21) 
g.SetMarkerColor(ROOT.kBlue) 
g.SetMarkerSize(0.5) 
g.SetLineColor(ROOT.kRed) 
g.SetLineWidth(1) 

g.Draw("APL")
c.Modified() 
c.Update()
c.Draw()
c.SaveAs("resistenza_dinamica_zoom.png") 
input("Premi Invio per chiudere...") 