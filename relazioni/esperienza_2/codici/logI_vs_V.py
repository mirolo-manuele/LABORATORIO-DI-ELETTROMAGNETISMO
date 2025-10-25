import ROOT
from array import array
import numpy as np
import pandas as pd

c = ROOT.TCanvas("c", "Grafico semilogaritmico", 800, 600) #tavolozza

for i in range(1,7): #la funzione range comprende l'estremo inferiore ma non quello superiore
    s=str(i) #converte l'intero i in una stringa s, in modo da poterlo poi concatenare alla stringa foglio nella prossima riga 
    foglio="Temp_"+s
    df = pd.read_excel("Esperienza_2.xlsx", sheet_name=foglio) #legge il file excel
    df = df.dropna(subset=["Volt(mV)","lnCorr(mA)"]) #controlla solo le colonne V e I. Se una di queste contiene un valore mancante, elimina quella riga

    V = array('d', df["Volt(mV)"].to_numpy(dtype=float)) #df è il dataframe, "V" è il nome della colonna da leggere 
    lnI = array('d', df["lnCorr(mA)"].to_numpy(dtype=float)) #to_numpy converte la colonna in un array NumPy di tipo float.

    eV = array('d', [0.0]*len(V))
    elnI = array('d', [0.0]*len(lnI))

    v_max=700
    v_min=300

    g=ROOT.TGraphErrors(len(V), V, lnI, eV, elnI) #len(V) è il numero di punti, V e I sono gli array dei dati, eV e eI sono gli errori associati 
    g.SetTitle("Grafico semilogaritmico;Tensione(V);ln(I)") 
    g.SetMarkerStyle(21) 
    g.SetMarkerColor(ROOT.kBlue) 
    g.SetMarkerSize(0.5) 
    g.SetLineColor(ROOT.kRed) 
    g.SetLineWidth(1) 

    g.Draw("APL") 
    ey = array('d', [0.00]*len(V))

    indici_fit = [i for i in range(len(V)) if V[i] >= v_min and V[i]<= v_max] #sceglie l'intervallo in cui fare il fit (tra v_min e v_max)

    V_fit = array('d', [V[i] for i in indici_fit])
    lnI_fit = array('d', [lnI[i] for i in indici_fit])
    ey_fit = array('d', [ey[i] for i in indici_fit]) #creo un array con solo i dati con x >= v_soglia

    g_fit = ROOT.TGraphErrors(len(V_fit), V_fit, lnI_fit, ey_fit) 

    ROOT.gStyle.SetOptFit(11) #stampa solo parametri m e q fit ed errori

    fit_func = ROOT.TF1("fit_func", "pol1", min(V_fit), max(V_fit)) #pol1 significa polinomio di grado 1

    #Rinomina dei parametri, mettere prima di fit_result (che fa il fit)
    fit_func.SetParName(0, "q")
    fit_func.SetParName(1, "m")

    # Eseguire il fit e poi calcolare eta usando il parametro di pendenza m
    fit_result = g_fit.Fit(fit_func, "S+", "", min(V_fit), max(V_fit))
  
    g_fit.Draw("Q")#mi serve per far comparire la tabella delle statistiche del fit, Q quiet
    fit_func.SetLineColor(ROOT.kBlack)
    fit_func.SetLineWidth(2)
    fit_func.Draw("SAME") #disegno sullo stesso grafico


#print("eta=",eta)
c.Modified() 
c.Update()
c.Draw()
c.SaveAs("scala_semilogaritmica.png") 
input("Premi Invio per chiudere...") 