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


c = ROOT.TCanvas("c", "Grafico semilogaritmico", 900, 600)
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

# AGGIUNGI: lista per memorizzare i risultati dei fit e del TGraph
risultati_fit = []
grafici = []


#uso fogli da processare per ciclare sui fogli
#questa parte di codice mi serve per creare la tavolozza su cui disegnare sennò è un casino mi sovrascrive
for j in fogli_da_processare:
    #nelle prossime righe faccio leggere tutti i dati da tutti i fogli(tolgo i NaN)
    s=str(j) #converte l'intero i in una stringa s, in modo da poterlo poi concatenare alla stringa foglio nella prossima riga 
    foglio="Temp_"+s
    df = pd.read_excel("Esperienza_2.xlsx", sheet_name=foglio)
    df = df.dropna(subset=["Volt(mV)","lnCorr(A)"])

    V = array('d', (df["Volt(mV)"].to_numpy(dtype=float) / 1000)) #convert i mV in V
    lnI = array('d', df["lnCorr(A)"].to_numpy(dtype=float))

    eV = array('d', [0.0]*len(V)) #array con floting point (d=doubble) di zeri 
    elnI = array('d', [0.0]*len(lnI))

    all_V.extend(V) #array accumulatori che hanno tutti i dati
    all_lnI.extend(lnI)

#creazione grafico dummy, solo per disegnare la tavolozza con range completo ()
dummy_V = array('d', [min(all_V), max(all_V)])
dummy_lnI = array('d', [min(all_lnI), max(all_lnI)])
dummy_graph = ROOT.TGraph(2, dummy_V, dummy_lnI)
dummy_graph.SetTitle("Grafico semilogaritmico;Tensione (V);ln(I)")
dummy_graph.Draw("AP")



for j in fogli_da_processare:
    s=str(j) #converte l'intero i in una stringa s, in modo da poterlo poi concatenare alla stringa foglio nella prossima riga 
    foglio="Temp_"+s
    df = pd.read_excel("Esperienza_2.xlsx", sheet_name=foglio)
    df = df.dropna(subset=["Volt(mV)","lnCorr(A)"])

    V = array('d', (df["Volt(mV)"].to_numpy(dtype=float) / 1000))
    lnI = array('d', df["lnCorr(A)"].to_numpy(dtype=float))

    eV = array('d', [0.0]*len(V))
    elnI = array('d', [0.0]*len(lnI))

    v_max=max(V)
    v_min=min(V)
    
    g=ROOT.TGraphErrors(len(V), V, lnI, eV, elnI)
    g.SetName(f"g_{s}") #do un nome diverso ad ogni grafico
    g.SetMarkerStyle(21) 
    g.SetMarkerColor((ROOT.kBlack + (j%7)))
    #ROOT associa ai colori un numero da 0 a 7
    #j%7 mi da il resto della divisione di j per 7, evito input non validi, se j=8 sono fuori range
    g.SetMarkerSize(0.5) 
    g.SetLineColor(ROOT.kRed) 
    g.SetLineWidth(1) 

    grafici.append(g)

    g.Draw("PE same") #non faccio ridisegnare assi
    c.Update() #forzo l'aggiornamento del canvas

    indici_fit = [i for i in range(len(V)) if V[i] >= v_min and V[i]<= v_max] #sceglie l'intervallo in cui fare il fit (tra v_min e v_max)
    #in questo caso il cocie indici è inutile perchè li prendo tutti, l'unico modo per scegliere i dati e toglierli da Excel


    if len(indici_fit) > 0:
        V_fit = array('d', [V[i] for i in indici_fit])
        lnI_fit = array('d', [lnI[i] for i in indici_fit])
        elnI_fit = array('d', [elnI[i] for i in indici_fit]) #creo un array con solo i dati con x >= v_soglia
        eV_fit = array('d', [0.0]*len(V_fit))

        g_fit = ROOT.TGraphErrors(len(V_fit), V_fit, lnI_fit, eV_fit, elnI_fit)
        g_fit.SetName(f"g_fit_{s}") #nomi diversi a ciascun grafico fit

        ROOT.gStyle.SetOptFit(11)#stampa solo parametri fit ed errori

        fit_name = f"fit_{s}" #nomi diversi a ciascun fit
        fit_func = ROOT.TF1(fit_name, "pol1", min(V_fit), max(V_fit))
        #Rinomina dei parametri, mettere prima di fit_result (che fa il fit)
        fit_func.SetParName(0, "q")
        fit_func.SetParName(1, "m")

        fit_result = g_fit.Fit(fit_func, "S+", "", min(V_fit), max(V_fit))
        
        
        fit_func.SetLineColor(ROOT.kBlack) #cicli 7 colori
        fit_func.SetLineWidth(1)
        fit_func.Draw("SAME") #disegno sullo stesso grafico
        #mi salvo il colore, per dopo la legenda
        colore=fit_func.GetLineColor()
         #Rinomina dei parametri, mettere prima di fit_result (che fa il fit)
        m = fit_func.GetParameter(1)
        q = fit_func.GetParameter(0)
        
        testo = f"T{j}: y = {m:.3f}x {q:.2f} "
        entry = tabella.AddEntry(g, testo, "P") #crea una nuova voce nella legenda ogni ciclo
        #mostra il testo e P (pallino)
        #grazie a ROOT.nullptr non associo la legenda ad alcun grafico ma all'intero canvas
        entry.SetMarkerColor(colore)
        entry.SetMarkerStyle(20)  #P è il mio marker
        entry.SetMarkerSize(1.2)
        entry.SetTextFont(132) # font che supporta simboli greci
        tabella.Draw()


c.RedrawAxis()
c.Modified() 
c.Update()
c.SaveAs("scala_semilogaritmica.png") 
input("Premi Invio per chiudere...")