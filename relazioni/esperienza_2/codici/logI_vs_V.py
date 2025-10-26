import ROOT
from array import array
import numpy as np
import pandas as pd


print("Opzioni:")
print("1 - Tutti i fit (fogli 1-6)")
print("2 - Fit singolo")
scelta = input("Scegli opzione (1 o 2): ")

if scelta == "2":
    foglio_singolo = input("Inserisci numero foglio (1-6): ")
    try:
        foglio_singolo = int(foglio_singolo)
        if foglio_singolo < 1 or foglio_singolo > 6:
            print("Numero non valido. Usero' tutti i fogli.")
            fogli_da_processare = range(1,7)
        else:
            fogli_da_processare = [foglio_singolo]
    except:
        print("Input non valido. Usero' tutti i fogli.")
else:
    fogli_da_processare = range(1,7)

print(f"Processando fogli: {list(fogli_da_processare)}")

c = ROOT.TCanvas("c", "Grafico semilogaritmico", 1000, 600)
c.cd()

all_V = array('d', [])
all_lnI = array('d', [])


tabella = ROOT.TLegend(0.70, 0.84, 1.00, 1.0)
tabella.SetBorderSize(1)
tabella.SetFillColor(0)
tabella.SetTextAlign(12)
tabella.SetTextSize(0.025)

# AGGIUNGI: lista per memorizzare i risultati dei fit
risultati_fit = []
grafici = []




# MODIFICA: usa fogli_da_processare invece di range(1,7)
for j in fogli_da_processare:
    s=str(j)
    foglio="Temp_"+s
    df = pd.read_excel("Esperienza_2.xlsx", sheet_name=foglio)
    df = df.dropna(subset=["Volt(mV)","lnCorr(A)"])

    V = array('d', (df["Volt(mV)"].to_numpy(dtype=float) / 1000))
    lnI = array('d', df["lnCorr(A)"].to_numpy(dtype=float))

    eV = array('d', [0.0]*len(V))
    elnI = array('d', [0.0]*len(lnI))

    v_max=max(V)
    v_min=min(V)

    all_V.extend(V)
    all_lnI.extend(lnI)

# Resto del codice invariato...
dummy_V = array('d', [min(all_V), max(all_V)])
dummy_lnI = array('d', [min(all_lnI), max(all_lnI)])
dummy_graph = ROOT.TGraph(2, dummy_V, dummy_lnI)
dummy_graph.SetTitle("Grafico semilogaritmico;Tensione (V);ln(I) (A)")
dummy_graph.Draw("AP")



# MODIFICA: usa fogli_da_processare invece di range(1,7)
for j in fogli_da_processare:
    s=str(j)
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
    g.SetName(f"g_{s}")
    g.SetMarkerStyle(21) 
    g.SetMarkerColor(ROOT.kBlue + (j%7)) 
    g.SetMarkerSize(0.5) 
    g.SetLineColor(ROOT.kRed) 
    g.SetLineWidth(1) 

    grafici.append(g)

    g.Draw("PE same")
    c.Update()

    indici_fit = [i for i in range(len(V)) if V[i] >= v_min and V[i]<= v_max]

    if len(indici_fit) > 0:
        V_fit = array('d', [V[i] for i in indici_fit])
        lnI_fit = array('d', [lnI[i] for i in indici_fit])
        elnI_fit = array('d', [elnI[i] for i in indici_fit])
        eV_fit = array('d', [0.0]*len(V_fit))

        g_fit = ROOT.TGraphErrors(len(V_fit), V_fit, lnI_fit, eV_fit, elnI_fit)
        g_fit.SetName(f"g_fit_{s}")

        ROOT.gStyle.SetOptFit(11)#stampa solo parametri fit ed errori

        fit_name = f"fit_{s}"
        fit_func = ROOT.TF1(fit_name, "pol1", min(V_fit), max(V_fit))

        fit_func.SetParName(0, "q")
        fit_func.SetParName(1, "m")

        fit_result = g_fit.Fit(fit_func, "S+", "", min(V_fit), max(V_fit))

        fit_func.SetLineColor(ROOT.kBlack + (j%7))
        fit_func.SetLineWidth(2)
        fit_func.Draw("SAME")
    

 # AGGIUNGI: prendi i parametri dal fit e aggiungi alla tabella
        m = fit_func.GetParameter(1)
        q = fit_func.GetParameter(0)
        
        # Crea il testo con il pallino colorato
        testo = f"F{j}: y = {m:.3f}x + {q:.2f}"
        entry = tabella.AddEntry(g, testo, "P")
        entry.SetMarkerColor(j%7)
        entry.SetMarkerStyle(20)  # 20 = pallino pieno
        entry.SetMarkerSize(1.2)
        tabella.Draw()


c.RedrawAxis()
c.Modified() 
c.Update()
c.SaveAs("scala_semilogaritmica.png") 
input("Premi Invio per chiudere...")