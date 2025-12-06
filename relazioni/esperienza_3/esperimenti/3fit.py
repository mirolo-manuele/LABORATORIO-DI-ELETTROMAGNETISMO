import ROOT
import pandas as pd
from array import array

# Classe per gestire gli eventi del mouse
# 1. Leggi il CSV specificando il separatore
df = pd.read_csv("dati_ristretti.csv", sep=";")

# 2. Filtra solo le righe che ti servono

# 3. Converti in array numerici
I = array('d', df["Amperom"].to_numpy(dtype=float))
V = array('d', df["Voltom"].to_numpy(dtype=float))
eV = array('d', [0.0]*len(V))
eI = array('d', [0.0]*len(I))

vmin=[-5,-3,-1.5]
vmax=[-3.5,-1.8,0]

fit_graphs = []
fit_functions = []

# 4. Crea grafico principale
c = ROOT.TCanvas("c", "I vs V", 800, 600)
g = ROOT.TGraphErrors(len(V), V, I, eV, eI)

g.SetTitle("I vs V;V [V];I [A]")
g.SetMarkerStyle(21)
g.SetMarkerColor(ROOT.kBlue)
g.SetMarkerSize(0.7)
g.Draw("AP")

# Array per memorizzare le pendenze
R = []

# Lista per mantenere i riferimenti ai grafici di fit


for j in range(0,3):
    indici_fit = [i for i in range(len(V)) if V[i] > vmin[j] and V[i] < vmax[j]]
    s=str(j)
    V_fit = array('d', [V[i] for i in indici_fit])
    I_fit = array('d', [I[i] for i in indici_fit])
    eV_fit = array('d', [0.0]*len(V_fit))
    eI_fit = array('d', [0.0]*len(V_fit))
    print(len(V_fit))

    g_fit = ROOT.TGraphErrors(len(V_fit), V_fit, I_fit, eV_fit, eI_fit)
    g_fit.SetName(f"g_fit_{s}")
    
    # Mantieni il riferimento al grafico
    fit_graphs.append(g_fit)
                        
    ROOT.gStyle.SetOptFit(11)

    fit_name = f"fit_{s}"
    fit_func = ROOT.TF1(fit_name, "pol1", min(V_fit), max(V_fit))
    fit_func.SetParName(0, "q")
    fit_func.SetParName(1, "m")

    fit_result = g_fit.Fit(fit_func, "S+", "", min(V_fit), max(V_fit))



    fit_func.SetLineColor(ROOT.kRed + j)  # Colori diversi per ogni fit
    fit_func.SetLineWidth(2)
    fit_func.Draw("SAME")
    

    a = fit_func.GetParameter(0)
    b = fit_func.GetParameter(1)
    ea = fit_func.GetParError(0)
    eb = fit_func.GetParError(1)

    R = 1 / b
    eR = ea / (b**2) 


    print(f"R= {R:.3e} ± {eR:.3e}")
    # Mantieni il riferimento alla funzione
    fit_functions.append(fit_func)


c.Update()
 


print("Resistenze calcolate R:", R)
c.SaveAs("3fit.pdf")


input("Premi Invio per chiudere...")
