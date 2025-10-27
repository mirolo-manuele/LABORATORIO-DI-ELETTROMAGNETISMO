import ROOT
import pandas as pd
from array import array

df = pd.read_excel("Esperienza_2.xlsx", sheet_name="Sheet1")

mg = ROOT.TMultiGraph() #multigraph mi permette di disegnare più rette in un unico canvas
colors = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kMagenta, ROOT.kOrange]
y_columns = [col for col in df.columns if col.startswith('V')] #prova tutte le colonne che cominciano con V
nomilegenda = ["I1=4mA", "I2=5mA", "I3=6mA", "I4=7mA", "I5=8mA"] #multigraph crea una legenda in automatico, mi serve per dare i nomi diversi

fits = [] #array creati per salvare grafici e fit
graphs = []  # tieni traccia dei grafici per la legenda

for i, y_col in enumerate(y_columns): #y_col diventa il mio numero finale per l'indice grazie ad enumerate
    valid_data = df[['T', y_col]].dropna() #rimuovi valori NaN
    if len(valid_data) == 0:
        continue

    x = array('d', valid_data['T'].values)
    y = array('d', valid_data[y_col].values)

    graph = ROOT.TGraph(len(x), x, y)
    graph.SetMarkerColor(colors[i % len(colors)])
    graph.SetMarkerStyle(20)
    graph.SetMarkerSize(0.6)
    graph.SetLineColor(ROOT.kWhite)
    graph.SetTitle(nomilegenda[i])#per avere nomi diversi ogni set di punti, così li vedo diversi nella legenda

    fit = ROOT.TF1(f"fit_{y_col}", "pol1", 0, max(x) + 20)
    fit.SetLineColor(colors[i % len(colors)])
    fit.SetLineWidth(2)

    graph.Fit(fit, "Q")
    fit.SetRange(0, max(x) + 20)

    mg.Add(graph)
    fits.append(fit)
    graphs.append(graph)

    print(f"{nomilegenda[i]}: y = {fit.GetParameter(1):.3f}x + {fit.GetParameter(0):.3f}")

# Disegno del multigrafico
c = ROOT.TCanvas("c1", "Multipli Dataset da Excel", 900, 900)
mg.Draw("APL")
mg.SetTitle("V vs T;T[K];Voltaggio(V)")
mg.GetXaxis().SetLimits(0, max(df['T'].dropna()) + 20)
mg.GetYaxis().SetRangeUser(0.53, 1.25)

# Ridisegna i fit
for f in fits:
    f.Draw("same")

# Crea legenda solo per i punti
legend = ROOT.TLegend(0.75, 0.75, 0.9, 0.9)
for g, label in zip(graphs, nomilegenda): #Itera su ogni grafico (g) nella lista graphs e sulla corrispondente etichetta (label) in nomilegenda
    legend.AddEntry(g, label, "p")  # "p" = solo marker (nessuna linea del fit), in pratica metto una legenda solo per i punti altrimenti mi fa anche per i fit
legend.Draw()

c.Update()
c.SaveAs("V_vs_T.pdf")

input("Premi Invio per chiudere...")