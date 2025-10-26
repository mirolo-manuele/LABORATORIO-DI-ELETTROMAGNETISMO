import ROOT
import pandas as pd
from array import array

# Carica dati
df = pd.read_excel("Esperienza_2.xlsx", sheet_name="Sheet2")

mg = ROOT.TMultiGraph()
colors = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kMagenta, ROOT.kOrange]
y_columns = [col for col in df.columns if col.startswith('V')]
nomilegenda = ["I1=4mA", "I2=5mA", "I3=6mA", "I4=7mA", "I5=8mA"]

fits = []  # memorizza i fit per ridisegnarli dopo
graphs = []  # tieni traccia dei grafici per la legenda

for i, y_col in enumerate(y_columns):
    valid_data = df[['T', y_col]].dropna()
    if len(valid_data) == 0:
        continue

    x = array('d', valid_data['T'].values)
    y = array('d', valid_data[y_col].values)

    graph = ROOT.TGraph(len(x), x, y)
    graph.SetMarkerColor(colors[i % len(colors)])
    graph.SetMarkerStyle(20)
    graph.SetMarkerSize(0.6)
    graph.SetLineColor(ROOT.kWhite)
    graph.SetTitle(nomilegenda[i])

    fit = ROOT.TF1(f"fit_{y_col}", "pol1")
    fit.SetLineColor(colors[i % len(colors)])
    fit.SetLineWidth(2)

    graph.Fit(fit, "Q")       # Fit silenzioso

    mg.Add(graph)
    fits.append(fit)
    graphs.append(graph)

    print(f"{nomilegenda[i]}: y = {fit.GetParameter(1):.3f}x + {fit.GetParameter(0):.3f}")

# Disegno del multigrafico
c = ROOT.TCanvas("c1", "Multipli Dataset da Excel", 900, 900)
mg.Draw("APL")
mg.SetTitle("V vs T;T[K];Voltaggio(V)")

# Ridisegna le rette di fit sopra il multigrafico
for f in fits:
    f.Draw("same")

# Crea legenda solo per i punti
legend = ROOT.TLegend(0.75, 0.75, 0.9, 0.9)
for g, label in zip(graphs, nomilegenda):
    legend.AddEntry(g, label, "p")  # "p" = solo marker (nessuna linea del fit)
legend.Draw()
c.Update()
c.SaveAs("V_vs_T_lim.pdf")

input("Premi Invio per chiudere...")