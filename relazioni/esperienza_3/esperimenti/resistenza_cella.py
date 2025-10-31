import ROOT
import pandas as pd
from array import array

# 1. Leggi il CSV specificando il separatore
df = pd.read_csv("squadra_Minnie_28_10.csv", sep=";")

# 2. Filtra solo le righe che ti servono
righe = [278,292,307,321,336,348,379,394,408,421,434,450,472,486,501,513,527,542,554,570,586,598,610,623,637,650,663,676,694,707,720,733,747,760,775,789]
df_filtrato = df.loc[righe, ["strum1", "strum2"]]

# 3. Converti in array numerici
I = array('d', df_filtrato["strum1"].to_numpy(dtype=float))
V = array('d', df_filtrato["strum2"].to_numpy(dtype=float))
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
fit = ROOT.TF1("fit", "[0]*x + [1]", -4.3, -3.15) # intervallo del fit, è scontato che prende minore e maggiore valore di x
fit.SetParNames("a", "b")
fit.SetLineColor(ROOT.kRed)

g.Fit(fit, "RQ")  # "Q" = quiet, rimuovi se vuoi output dettagliato ; "R" = fit nell'intervallo specificato 
fit.SetRange(-4.3, -3.15)
# 6. Visualizza risultati
fit.Draw("same")
c.Modified()
c.Update()

# 7. Salva grafico
c.SaveAs("Ohmicita_cella1_fit.pdf")

# 8. Stampa parametri a e b
a = fit.GetParameter(0)
b = fit.GetParameter(1)
ea = fit.GetParError(0)
eb = fit.GetParError(1)

R = 1 / a 
eR = ea / (a**2) 

print(f"Fit lineare: I = ({a:.3e} ± {ea:.3e}) * V + ({b:.3e} ± {eb:.3e})")

print(f"R= {R:.3e} ± {eR:.3e}")

input("Premi Invio per chiudere...")