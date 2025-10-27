import ROOT
from array import array
import numpy as np
import pandas as pd




c = ROOT.TCanvas("c", "Grafico I vs V", 800, 600)
c.cd()

all_V = array('d', [])
all_lnI = array('d', [])

tabella = ROOT.TLegend(0.70, 0.80, 1.00, 1.00) #creazione legenda in alto a destra
#coordinate: (x1, y1, x2, y2) dove (x1,y1) e' l'angolo in basso a sinistra, (x2,y2) l'angolo in alto a destra
tabella.SetBorderSize(1)
tabella.SetFillColor(0)
tabella.SetTextAlign(12)#codice di allineamento testo
#Codici di allineamento:
#Verticale: 1=sotto, 2=centro, 3=sopra
#Orizzontale: 1=sinistra, 2=centro, 3=destra
tabella.SetTextSize(0.025)

#uso fogli da processare per ciclare sui fogli
#questa parte di codice mi serve per creare la tavolozza su cui disegnare sennò è un casino mi sovrascrive
for j in range(1,7): #la funzione range prende crea un intervallo chiuso a sx e aperto a dx
    #nelle prossime righe faccio leggere tutti i dati da tutti i fogli(tolgo i NaN)
    s=str(j)
    foglio="Temp_"+s
    df = pd.read_excel("Esperienza_2.xlsx", sheet_name=foglio)
    df = df.dropna(subset=["Volt(mV)","Corr(mA)"])

    V = array('d', df["Volt(mV)"].to_numpy(dtype=float))
    lnI = array('d', df["Corr(mA)"].to_numpy(dtype=float))

    eV = array('d', [0.0]*len(V))
    elnI = array('d', [0.0]*len(lnI))

    all_V.extend(V) #array accumulatori che hanno tutti i dati
    all_lnI.extend(lnI)

#creazione grafico dummy, solo per disegnare la tavolozza con range completo ()
dummy_V = array('d', [min(all_V), max(all_V)])
dummy_lnI = array('d', [min(all_lnI), max(all_lnI)])
dummy_graph = ROOT.TGraph(2, dummy_V, dummy_lnI)
dummy_graph.SetTitle("Grafico I vs V;V(mV); I(mA)") 
dummy_graph.Draw("AP") #AP non solo A 

#N.B. TGraphErrors non viene conservato da ROOT (come fa per TF1), devo creare una lista dove salvare i grafici
grafici=[]
for j in range(1,7):
    s=str(j) #converte l'intero i in una stringa s, in modo da poterlo poi concatenare alla stringa foglio nella prossima riga 
    foglio="Temp_"+s
    df = pd.read_excel("Esperienza_2.xlsx", sheet_name=foglio) #legge il file excel
    df = df.dropna(subset=["Volt(mV)","Corr(mA)"]) #controlla solo le colonne V e I. Se una di queste contiene un valore mancante, elimina quella riga

    V = array('d', df["Volt(mV)"].to_numpy(dtype=float)) #df è il dataframe, "V" è il nome della colonna da leggere 
    lnI = array('d', df["Corr(mA)"].to_numpy(dtype=float))  #to_numpy converte la colonna in un array NumPy di tipo float.

    eV = array('d', [0.0]*len(V))
    elnI = array('d', [0.0]*len(lnI))
    tempK = df["Temp(K)"].iloc[1]
    T=str(tempK)


    g_name=f"g_{s}"
    g=ROOT.TGraphErrors(len(V), V, lnI, eV, elnI)
    g.SetName(f"g_{s}") #do un nome diverso ad ogni grafico
    g.SetMarkerStyle(21) 
    g.SetMarkerColor(ROOT.kBlack + (j%7)) 
    #ROOT associa ai colori un numero da 0 a 7
    #j%7 mi da il resto della divisione di j per 7, evito input non validi, se j=8 sono fuori range
    g.SetMarkerSize(0.5) 
    g.SetLineColor(ROOT.kBlack)
    g.SetLineWidth(1) 

    g.Draw("PL SAME") #non faccio ridisegnare gli assi!
    grafici.append(g)
    c.Update() #forzo l'aggiornamento del canvas

    colore=ROOT.kBlack + (j%7)
    testo = f"T= {T}#circ C" 
    entry = tabella.AddEntry(ROOT.nullptr, testo, "P") #crea una nuova voce nella legenda ogni ciclo
    entry.SetMarkerColor(colore)
    entry.SetMarkerStyle(20)  #P è il mio marker
    entry.SetMarkerSize(1.2)
    tabella.Draw()

c.RedrawAxis()
c.Modified() 
c.Update()
c.SaveAs("I_vs_V.pdf") 
input("Premi Invio per chiudere...")