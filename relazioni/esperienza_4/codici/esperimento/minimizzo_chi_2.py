import ROOT
from array import array
import numpy as np
import pandas as pd

def fit_automatico_chi2_minimo(): #def si fa per funzioni, era figo metterlo
    # Lettura dati
    df = pd.read_excel("Carica_scarica2.xlsx", sheet_name="2_PROVA")
    df = df.dropna(subset=["t", "log V"])
    
    # Dati
    t = array('d', df["t"].to_numpy(dtype=float))
    V = array('d', df["log V"].to_numpy(dtype=float))
    
    # Errori
    et = array('d', [0.0]*len(t))
    eV = array('d', [0.0]*len(V)) 
    
    # Creazione canvas
    c = ROOT.TCanvas("c", "log V vs t", 1700, 600)
    g = ROOT.TGraphErrors(len(t), t, V, et, eV)
    
    # Stile grafico
    g.SetTitle("log V vs t; t[s]; log V") 
    g.SetLineColor(ROOT.kBlack)
    g.SetLineWidth(1)
    g.Draw("AL")
    
    # Range di ricerca per i fit
    t_min, t_max = min(t), max(t)
    
    # Parametri per la ricerca automatica
    num_fit_per_regione = 150  # Numero di fit da provare per ogni regione
    risultati_tutti = []
    
    for regione in range(2): 
        #range del fit
        if regione == 0:
            start_range = (7.45000E-06, 7.45000E-06) 
            end_range = (10E-6, 12E-6)
        else:
            start_range = (2.01E-05, 2.01E-05) 
            end_range = (22E-6, 27E-6)
        
        miglior_fit = None
        miglior_chi2 = 1000 #inizializzo le variabili, a questa do un valore perche mi serve dopo (riga 104)
        
        # Prova diverse combinazioni di inizio/fine
        for i in range(num_fit_per_regione):
            # Genera punti di inizio e fine casuali nei range definiti
            start_fit = np.random.uniform(start_range[0], start_range[1])
            end_fit = np.random.uniform(end_range[0], end_range[1])
            
            # Assicura che start < end e ci siano abbastanza punti
            if end_fit <= start_fit:
                continue
                
            # Seleziona dati nel range corrente
            mask = (np.array(t) >= start_fit) & (np.array(t) <= end_fit)
            #questa è una maschera booleana, prende tutti i dati che soddisfano la condizione >start_fit <end_fit
            punti_selezionati = sum(mask)
            #pyroot per una maschera booleana somma i punti che c sono dentro la maschera se gli dai funzione sum
            
            if punti_selezionati < 5:  # Almeno 5 punti 
                continue
            
            x_fit = array('d', np.array(t)[mask])
            y_fit = array('d', np.array(V)[mask])
            ey_fit = array('d', np.array(eV)[mask])
            
            # Crea grafico per il fit
            g_fit = ROOT.TGraphErrors(len(x_fit), x_fit, y_fit, 
                                     array('d', [0.0]*len(x_fit)), ey_fit)
            
            # Fit lineare
            fit_func = ROOT.TF1(f"fit_temp_{regione}_{i}", "pol1", start_fit, end_fit)
            
            # Esegui fit
            fit_result = g_fit.Fit(fit_func, "SQN")  # Q=quiet, N=non aggiungere alla lista
            
            if fit_result.IsValid():
                chi2 = fit_func.GetChisquare()
                ndf = fit_func.GetNDF()
                chi2_ridotto = chi2/ndf if ndf > 0 else float('inf')
                
                # Salva risultati
                risultato = {
                    'regione': regione,
                    'start': start_fit,
                    'end': end_fit,
                    'chi2': chi2,
                    'chi2_ridotto': chi2_ridotto,
                    'ndf': ndf,
                    'punti': punti_selezionati,
                    'm': fit_func.GetParameter(1),
                    'em': fit_func.GetParError(1),
                    'q': fit_func.GetParameter(0),
                    'eq': fit_func.GetParError(0),
                    'fit_func': fit_func.Clone(f"best_fit_{regione}_{i}")
                }
                
                risultati_tutti.append(risultato)
                
                # Controlla se è il miglior fit
                if chi2_ridotto < miglior_chi2 and ndf > 0:
                    miglior_chi2 = chi2_ridotto
                    miglior_fit = risultato
        
        # Disegna il miglior fit per questa regione
        if miglior_fit:
            print(f"\n*** MIGLIOR FIT REGIONE {regione+1} ***")
            print(f"Range: {miglior_fit['start']:.2e} - {miglior_fit['end']:.2e}")
            print(f"χ² = {miglior_fit['chi2']}")
            print(f"χ²/ndf = {miglior_fit['chi2']:.3f}/{miglior_fit['ndf']} = {miglior_fit['chi2_ridotto']:.3f}")
            print(f"Pendenza: {miglior_fit['m']:.3e} ± {miglior_fit['em']:.3e}")
            
            # Calcola RC
            rc = -1/miglior_fit['m']
            erc = abs(miglior_fit['em'] / (miglior_fit['m']**2))
            print(f"RC: {rc:.3e} ± {erc:.3e}")
            
            # Disegna il miglior fit
            miglior_fit['fit_func'].SetLineColor(ROOT.kRed)
            miglior_fit['fit_func'].SetLineWidth(3)
            miglior_fit['fit_func'].SetLineStyle(1)
            miglior_fit['fit_func'].Draw("SAME")
    
    
    c.Modified()
    c.Update()
    c.SaveAs("fit_automatico_chi2_minimo2.pdf")
    
    print("\nPremi Invio per chiudere...")
    input()


# Esecuzione
if __name__ == "__main__":
    risultati = fit_automatico_chi2_minimo()