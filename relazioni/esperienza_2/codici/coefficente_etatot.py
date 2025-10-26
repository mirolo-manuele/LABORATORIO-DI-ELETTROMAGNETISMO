import ROOT
from array import array
import numpy as np
import pandas as pd

#piccola parte di codice per decidere se fittarle tutte, potrebbe essere utile per le prossime volte
print("Opzioni:")
print("1 - Tutti i fit")
print("2 - Fit singolo")
scelta = input("Scegli opzione (1 o 2): ")

if scelta == "2":
    foglio_singolo = input("Inserisci numero foglio (1-6): ")
    try: #try ed except servono per gestire gli errori
        foglio_singolo = int(foglio_singolo) #la stringa foglio_singolo viene convertita in intero
        if foglio_singolo < 1 or foglio_singolo > 6:
            print("Numero non valido. Usero' tutti i fogli.") #se numero fuori da 1-6 errore
            fogli_da_processare = range(1,7)
        else:
            fogli_da_processare = [foglio_singolo]
    except:
        print("Input non valido. Usero' tutti i fogli.") #gestione dell'errore che viene fatta in riga 18
else:
    fogli_da_processare = range(1,7)


c = ROOT.TCanvas("c", "Grafico semilogaritmico", 800, 600)
c.cd()

all_V = array('d', [])
all_lnI = array('d', [])


tabella = ROOT.TLegend(0.70, 0.84, 1.00, 1.0) #creazione legenda in alto a destra
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
for j in fogli_da_processare:
    #nelle prossime righe faccio leggere tutti i dati da tutti i fogli(tolgo i NaN)
    s=str(j)
    foglio="Temp_"+s
    df = pd.read_excel("Esperienza_2.xlsx", sheet_name=foglio)
    df = df.dropna(subset=["qV/kT","lnCorr(mA)"])

    V = array('d', df["qV/kT"].to_numpy(dtype=float))
    lnI = array('d', df["lnCorr(mA)"].to_numpy(dtype=float))

    eV = array('d', [0.0]*len(V))
    elnI = array('d', [0.0]*len(lnI))

    all_V.extend(V) #array accumulatori che hanno tutti i dati
    all_lnI.extend(lnI)

#creazione grafico dummy, solo per disegnare la tavolozza con range completo ()
dummy_V = array('d', [min(all_V), max(all_V)])
dummy_lnI = array('d', [min(all_lnI), max(all_lnI)])
dummy_graph = ROOT.TGraph(2, dummy_V, dummy_lnI)
dummy_graph.SetTitle("Grafico semilogaritmico;qV/kT;ln(I) ")
dummy_graph.Draw("AP") #AP non solo A 


for j in fogli_da_processare:
    s=str(j) #converte l'intero i in una stringa s, in modo da poterlo poi concatenare alla stringa foglio nella prossima riga 
    foglio="Temp_"+s
    df = pd.read_excel("Esperienza_2.xlsx", sheet_name=foglio) #legge il file excel
    df = df.dropna(subset=["qV/kT","lnCorr(mA)"]) #controlla solo le colonne V e I. Se una di queste contiene un valore mancante, elimina quella riga

    V = array('d', df["qV/kT"].to_numpy(dtype=float)) #df è il dataframe, "V" è il nome della colonna da leggere 
    lnI = array('d', df["lnCorr(mA)"].to_numpy(dtype=float))  #to_numpy converte la colonna in un array NumPy di tipo float.

    eV = array('d', [0.0]*len(V))
    elnI = array('d', [0.0]*len(lnI))

    v_max=max(V)
    v_min=min(V)
    
    g=ROOT.TGraphErrors(len(V), V, lnI, eV, elnI)
    g.SetName(f"g_{s}") #do un nome diverso ad ogni grafico
    g.SetMarkerStyle(21) 
    g.SetMarkerColor(ROOT.kBlue + (j%7)) 
    #ROOT associa ai colori un numero da 0 a 7
    #j%7 mi da il resto della divisione di j per 7, evito input non validi, se j=8 sono fuori range
    g.SetMarkerSize(0.5) 
    g.SetLineColor(ROOT.kRed) 
    g.SetLineWidth(1) 

    g.Draw("PL same") #non faccio ridisegnare gli assi!
    c.Update() #forzo l'aggiornamento del canvas

    indici_fit = [i for i in range(len(V)) if V[i] >= v_min and V[i]<= v_max] #sceglie l'intervallo in cui fare il fit (tra v_min e v_max)
    #in questo caso il cocie indici è inutile perchè li prendo tutti, l'unico modo per scegliere i dati e toglierli da Excel


    if len(indici_fit) > 0:
        V_fit = array('d', [V[i] for i in indici_fit])
        lnI_fit = array('d', [lnI[i] for i in indici_fit])
        elnI_fit = array('d', [elnI[i] for i in indici_fit]) #creo un array con solo i dati con x >= v_soglia
        eV_fit = array('d', [0.0]*len(V_fit))
        # Legge la cella alla colonna "Temp(K)" e riga 0 (prima riga dati)
        tempK = df["Temp(K)"].iloc[1]
        T=str(tempK)

        g_fit = ROOT.TGraphErrors(len(V_fit), V_fit, lnI_fit, eV_fit, elnI_fit)
        g_fit.SetName(f"g_fit_{s}") #nomi diversi a ciascun grafico fit

        ROOT.gStyle.SetOptFit(11)#stampa solo parametri fit ed errori

        fit_name = f"fit_{s}" #nomi diversi a ciascun fit
        fit_func = ROOT.TF1(fit_name, "pol1", min(V_fit), max(V_fit))
        #Rinomina dei parametri, mettere prima di fit_result (che fa il fit)
        fit_func.SetParName(0, "q")
        fit_func.SetParName(1, "m")

        fit_result = g_fit.Fit(fit_func, "S+", "", min(V_fit), max(V_fit))

        fit_func.SetLineColor(ROOT.kBlack + (j%7)) #cicli 7 colori
        fit_func.SetLineWidth(2)
        fit_func.Draw("SAME") #disegno sullo stesso grafico
        #mi salvo il colore, per dopo la legenda
        colore=fit_func.GetLineColor()
         #Rinomina dei parametri, mettere prima di fit_result (che fa il fit)
        m = fit_func.GetParameter(1)
        q = fit_func.GetParameter(0)
        eta = 1.0 / m
        testo = f"F{j}: #eta = {eta:.3f} T= {T}#circ C" #stringhe formattate
        #f mi permette di concatenare stringhe con variabili
        #:.3f mi permette di mostrare 3 cifre dopo la virgola
        entry = tabella.AddEntry(ROOT.nullptr, testo, "P") #crea una nuova voce nella legenda ogni ciclo
        #mostra il testo e P (pallino)
        #grazie a ROOT.nullptr non associo la legenda ad alcun grafico ma all'intero canvas
        entry.SetMarkerColor(colore)
        entry.SetMarkerStyle(20)  #P è il mio marker
        entry.SetMarkerSize(1.2)
        tabella.Draw()


c.RedrawAxis()
c.Modified() 
c.Update()
c.SaveAs("coefficente_eta.png") 
input("Premi Invio per chiudere...")