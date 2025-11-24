import ROOT
from ROOT import TLine
from array import array
import numpy as np
import pandas as pd

df = pd.read_excel("Esperienza_5.xlsx", sheet_name="Risonanza") #legge il file excel
df = df.dropna(subset=["ω", "V"]) #controlla solo le colonne V e I. Se una di queste contiene un valore mancante, elimina quella riga


t = array('d', df["ω"].to_numpy(dtype=float))
V = array('d', df["V"].to_numpy(dtype=float)) #df è il dataframe, "V" è il nome della colonna da leggere 


et = array('d', [0.0]*len(V))
eV = array('d', [0.0]*len(t))


c = ROOT.TCanvas("c", "c", 800, 600)

g = ROOT.TGraphErrors(len(V), t, V, et, eV)
g.SetTitle(" V vs #omega; #omega [rad/s]; V")
g.SetMarkerStyle(21)
g.SetMarkerColor(ROOT.kBlack)
g.SetLineColor(ROOT.kBlue)
g.SetMarkerSize(0.5)
g.SetLineWidth(1)
g.Draw("AP")


line1 = ROOT.TLine(49087.38521, 536, 49866.55006, 548)
line1.SetLineColor(ROOT.kBlue)
line1.SetLineWidth(1)
line1.Draw("same")


line2 = ROOT.TLine(61599.85595, 564,62209.75552, 524)
line2.SetLineColor(ROOT.kBlue)
line2.SetLineWidth(1)
line2.Draw("same")

line = ROOT.TLine(45*10**3, 545, 65*10**3, 545)
line.SetLineColor(ROOT.kRed)
line.SetLineWidth(1)
line.Draw("same")

y_line = 545

# --- Intersezione con line1 ---
x1a = line1.GetX1()
y1a = line1.GetY1()
x1b = line1.GetX2()
y1b = line1.GetY2()

t1 = (y_line - y1a) / (y1b - y1a)
x_int1 = x1a + t1 * (x1b - x1a)

print("Intersezione line1 con line:", x_int1, y_line)


# --- Intersezione con line2 ---
x2a = line2.GetX1()
y2a = line2.GetY1()
x2b = line2.GetX2()
y2b = line2.GetY2()

t2 = (y_line - y2a) / (y2b - y2a)
x_int2 = x2a + t2 * (x2b - x2a)

print("Intersezione line2 con line:", x_int2, y_line)


c.Modified()
c.Update()
c.Draw()

c.SaveAs("intersezione.pdf") 
input("Premi Invio per chiudere...") 