from array import array
from ROOT import TCanvas, TGraphErrors, TLatex, TF1, TLine, gStyle
import ROOT

# Dati esempio (sostituisci con i tuoi)
I = [ 0.0000211, 0.000130, 0.000433, 0.001293, 0.002147, 0.003467, 0.007000, 0.011280, 0.017300, 0.028850]      # Voltaggio [V]
V = [1.302, 1.302, 1.300,1.298,1.295, 1.291, 1.279, 1.265, 1.248, 1.217]      # Corrente [mA]
n = len(V)
I_soglia = 0.005

# Crea il grafico
g = ROOT.TGraph(n)
ROOT.gStyle.SetOptFit(11)
for i in range(n):
    g.SetPoint(i, I[i], V[i])

g.SetTitle("Intensita' di corrente vs Voltaggio;Corrente [A];Voltaggio [V]")

# Definisci la funzione di fit: y = m*x + q
f = ROOT.TF1("f", "[0]*x + [1]", min(I), I_soglia)
f.SetParNames("m", "q")

# Fit
g.Fit(f, "Q", "", min(I), I_soglia)  # "Q" = quiet (non stampa troppo)

# Disegna
c = ROOT.TCanvas("c", "V-I Fit", 800, 600)
g.SetMarkerStyle(20)
g.Draw("AP")
f.Draw("same")

# Mostra i risultati
m = f.GetParameter(0)
q = f.GetParameter(1)
em = f.GetParError(0)
eq = f.GetParError(1)
print(f"Fit: V = ({m:.3f} ± {em:.3f}) * I + ({q:.3f} ± {eq:.3f})")

c.Update()
input("Premi invio per uscire...")