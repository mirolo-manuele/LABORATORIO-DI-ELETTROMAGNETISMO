import ROOT
import pandas as pd
from array import array

# 1. Leggi il CSV specificando il separatore
df = pd.read_excel("faraday.xslx", sheet_name="Dati filtrati")

df = df.dropna(subset=["V", "I"]) 

# 3. Converti in array numerici
I = array('d', df["V"].to_numpy(dtype=float))
V = array('d', df["I"].to_numpy(dtype=float)) 
eV = array('d', [0.0]*len(V))
eI = array('d', [0.0]*len(I))

# 4. Crea grafico
c = ROOT.TCanvas("c", "I vs V", 800, 600)
g = ROOT.TGraphErrors(len(V), V, I, eV, eI)

g.SetTitle("I vs V;V [V];I [A]")
g.SetMarkerStyle(21)
g.SetMarkerColor(ROOT.kBlue)
g.SetMarkerSize(0.7)
g.Draw("AP")

# 5. Fit lineare: I = a·V + b
fit = ROOT.TF1("fit", "[0]*x + [1]", min(V), max(V)) # intervallo del fit, è scontato che prende minore e maggiore valore di x
fit.SetParNames("m", "q")
fit.SetLineColor(ROOT.kRed)

g.Fit(fit, "RQ")  # "Q" = quiet, rimuovi se vuoi output dettagliato ; "R" = fit nell'intervallo specificato 

# 6. Visualizza risultati
fit.Draw("same")
c.Modified()
c.Update()

# 7. Salva grafico
c.SaveAs("Resistenza filtrata.pdf")

# 8. Stampa parametri a e b
m = fit.GetParameter(0)
q = fit.GetParameter(1)
em = fit.GetParError(0)
eq = fit.GetParError(1)

R = 1 / m 
eR = em / (m**2) 

print(f"Fit lineare: I = ({m:.3e} ± {em:.3e}) * V + ({q:.3e} ± {eq:.3e})")

print(f"R= {R:.3e} ± {eR:.3e}")

input("Premi Invio per chiudere...")