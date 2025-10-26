import ROOT
import pandas as pd
from array import array


df = pd.read_excel("Esperienza_2.xlsx", sheet_name="Sheet1")

# Crea MultiGraph
mg = ROOT.TMultiGraph()

colors = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kMagenta, ROOT.kOrange]
# Crea un grafico per ogni colonna Y
y_columns = [col for col in df.columns if col.startswith('V')]

nomilegenda=["I1=4mA", "I2=5mA", "I3=6mA", "I4=7mA", "I5=8mA"]

for i, y_col in enumerate(y_columns):
    # Prendi i dati, rimuovi valori NaN
    valid_data = df[['T', y_col]].dropna()
    if len(valid_data) > 0:
        x = array('d', valid_data['T'].values)
        y = array('d', valid_data[y_col].values)
        
        graph = ROOT.TGraph(len(x), x, y)
        graph.SetName(y_col)
        graph.SetMarkerColor(colors[i % len(colors)])
        graph.SetMarkerStyle(20)
        graph.SetMarkerSize(0.5)
        graph.SetLineColor(ROOT.kWhite)
        graph.SetTitle(nomilegenda[i])

        fit=ROOT.TF1(f"fit_{y_col}", "pol1")
      
        fit.SetLineColor(colors[i % len(colors)])
        fit.SetLineWidth(2)
        graph.Fit(fit, "Q")
        mg.Add(graph)

        print(f"Dataset {i+1}: y = {fit.GetParameter(1):.3f}x + {fit.GetParameter(0):.3f}")

# Visualizza

c = ROOT.TCanvas("c1", "Multipli Dataset da Excel", 900, 600)
mg.Draw("APL")
mg.SetTitle("V vs T;T[K];Voltaggio(V)")
c.BuildLegend(0.75, 0.75, 0.9, 0.9)
c.Update()
c.Draw()
c.SaveAs("V_vs_T.png") 
input("Premi Invio per chiudere...")