import ROOT
from array import array
import numpy as np
import pandas as pd

df = pd.read_excel("faraday.xlsx", sheet_name="Ohmicita_cella") #legge il file excel
df = df.dropna(subset=["T", "R"]) #controlla solo le colonne V e I. Se una di queste contiene un valore mancante, elimina quella riga

I = array('d', df["R"].to_numpy(dtype=float))
V = array('d', df["T"].to_numpy(dtype=float)) #df è il dataframe, "V" è il nome della colonna da leggere 


eV = array('d', [0.0]*len(V))
eI = array('d', [0.0]*len(I))

vmax=[350, 1200, 1800]
vmin=[200, 600, 1300]

c = ROOT.TCanvas("c", "R vs t", 800, 600)

g=ROOT.TGraphErrors(len(V), V, I, eV, eI)

g.SetTitle("R vs t; t[s]; R[Ohm]") 
g.SetMarkerStyle(21) 
g.SetMarkerColor(ROOT.kBlue) 
g.SetMarkerSize(0.5) 
g.SetLineWidth(1) 

g.Draw("AP")

for j in range(0,3):
    indici_fit = [i for i in range(len(V)) if V[i] > vmin[j] and V[i] < vmax[j]]
    s=str(j)
    V_fit = array('d', [V[i] for i in indici_fit])
    I_fit = array('d', [I[i] for i in indici_fit])
    eV_fit = array('d', [0.0]*len(V_fit))
    eI_fit = array('d', [0.0]*len(V_fit))
    print(len(V_fit))

    g_fit = ROOT.TGraphErrors(len(V_fit), V_fit, I_fit, eV_fit, eI_fit)
    g_fit.SetName(f"g_fit_{s}") #nomi diversi a ciascun grafico fi
                        
    ROOT.gStyle.SetOptFit(11)#stampa solo parametri fit ed errori

    fit_name = f"fit_{s}" #nomi diversi a ciascun fit
    fit_func = ROOT.TF1(fit_name, "pol1", min(V_fit), max(V_fit))
                        #Rinomina dei parametri, mettere prima di fit_result (che fa il fit)
    fit_func.SetParName(0, "q")
    fit_func.SetParName(1, "m")

    fit_result = g_fit.Fit(fit_func, "S+", "", min(V_fit), max(V_fit))

    R=[]

    Rx=1/fit_func.GetParameter(1)
    R.append(Rx)

    fit_func.SetLineColor(ROOT.kBlack) #cicli 7 colori
    fit_func.SetLineWidth(1)
    fit_func.Draw("SAME") #disegno sullo stesso grafico

print(R)

c.Modified() 
c.Update()
c.Draw()

c.SaveAs("Resistenza_nel_tempo.pdf") 
input("Premi Invio per chiudere...") 