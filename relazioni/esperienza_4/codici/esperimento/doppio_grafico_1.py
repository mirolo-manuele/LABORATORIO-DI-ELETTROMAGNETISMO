import ROOT
from array import array
import numpy as np
import pandas as pd

def fit_automatico_chi2_minimo():

    # Lettura dati
    df = pd.read_excel("Carica_scarica2.xlsx", sheet_name="1_PROVA")
    df = df.dropna(subset=["t", "log V"])

    # Dati
    t = array('d', df["t"].to_numpy(dtype=float))
    V = array('d', df["log V"].to_numpy(dtype=float))

    # Errori
    et = array('d', [0.0]*len(t))
    eV = array('d', [0.0]*len(V))

    # Canvas diviso in due pad
    c = ROOT.TCanvas("c", "log V vs t (due regioni)", 1700, 600)
    c.Divide(2, 1)

    # Definizione delle due regioni richieste
    region_bounds = [
        (0, 19e-6),     # Regione 1
        (20e-6, 33e-6)  # Regione 2
    ]

    num_fit_per_regione = 150
    risultati_tutti = []
    fit_graphs = []

    # Loop sulle due regioni
    for regione in range(2):

        start_reg, end_reg = region_bounds[regione]

        # Seleziona solo i punti della regione corrente
        mask_regione = (np.array(t) >= start_reg) & (np.array(t) <= end_reg)
        t_reg = array('d', np.array(t)[mask_regione])
        V_reg = array('d', np.array(V)[mask_regione])
        eV_reg = array('d', np.array(eV)[mask_regione])
        et_reg = array('d', [0.0]*len(t_reg))

        # Vai nel pad corretto
        pad = c.cd(regione+1)

        # Grafico della sola regione
        g = ROOT.TGraphErrors(len(t_reg), t_reg, V_reg, et_reg, eV_reg)
        g.SetTitle(f"Regione {regione+1}; t [s]; log V")
        g.SetMarkerStyle(21)
        g.SetLineColor(ROOT.kBlack)
        g.Draw("AL")

        fit_graphs.append(g)

        # Range di partenza e fine per i fit
        start_range = (start_reg, start_reg)  # fissato al minimo della regione
        end_range = (end_reg, end_reg)        # fissato al massimo della regione

        miglior_fit = None
        miglior_chi2 = 1000

        if regione == 0:
            start_range = (7.45000E-06, 7.45000E-06) 
            end_range = (10E-6, 12E-6)
        else:
            start_range = (2.01E-05, 2.01E-05) 
            end_range = (22E-6, 27E-6)

        # Eseguo tentativi casuali di fit
        for i in range(num_fit_per_regione):

            # Scelta casuale dei due estremi
            start_fit = np.random.uniform(start_range[0], start_range[1])
            end_fit = np.random.uniform(end_range[0], end_range[1])

            mask = (np.array(t) >= start_fit) & (np.array(t) <= end_fit)
            punti = sum(mask)
            if punti < 5:
                continue

            x_fit = array('d', np.array(t)[mask])
            y_fit = array('d', np.array(V)[mask])
            ey_fit = array('d', np.array(eV)[mask])

            g_fit = ROOT.TGraphErrors(len(x_fit), x_fit, y_fit,
                                      array('d', [0.0]*len(x_fit)), ey_fit)

            fit_func = ROOT.TF1(f"fit_temp_{regione}_{i}", "pol1", start_fit, end_fit)
            fit_result = g_fit.Fit(fit_func, "SQN")

            if fit_result.IsValid():
                chi2 = fit_func.GetChisquare()
                ndf = fit_func.GetNDF()
                chi2_ridotto = chi2/ndf if ndf > 0 else float('inf')

                risultato = {
                    'regione': regione,
                    'start': start_fit,
                    'end': end_fit,
                    'chi2': chi2,
                    'chi2_ridotto': chi2_ridotto,
                    'ndf': ndf,
                    'punti': punti,
                    'm': fit_func.GetParameter(1),
                    'em': fit_func.GetParError(1),
                    'q': fit_func.GetParameter(0),
                    'eq': fit_func.GetParError(0),
                    'fit_func': fit_func.Clone(f"best_fit_{regione}_{i}")
                }

                risultati_tutti.append(risultato)

                if chi2_ridotto < miglior_chi2 and ndf > 0:
                    miglior_chi2 = chi2_ridotto
                    miglior_fit = risultato

        # Disegno best fit della regione
        if miglior_fit:

            miglior_fit['fit_func'].SetLineColor(ROOT.kRed)
            miglior_fit['fit_func'].SetLineWidth(3)
            miglior_fit['fit_func'].Draw("SAME")

    c.Modified()
    c.Update()
    c.SaveAs("doppio_grafico_1.png")

    print("\nPremi Invio per chiudere...")
    input()

if __name__ == "__main__":
    fit_automatico_chi2_minimo()
