import ROOT
import pandas as pd
from array import array

# Leggi Excel con più opzioni di controllo
try:
    df = pd.read_excel("Esperienza_2.xlsx", sheet_name="Sheet1")
    print("Colonne trovate nel file Excel:", df.columns.tolist())
    print("Prime righe del dataframe:")
    print(df.head())
    print("\nInfo sul dataframe:")
    print(df.info())
except Exception as e:
    print(f"Errore nella lettura del file Excel: {e}")
    exit()

# Crea MultiGraph
mg = ROOT.TMultiGraph()

colors = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kMagenta, ROOT.kOrange]
markers = [20, 21, 22, 23, 24]

# Crea un grafico per ogni colonna Y - MODIFICA QUESTA RIGA IN BASE ALLE TUE COLONNE
# Cambia 'V' con il pattern giusto delle tue colonne Y
y_columns = [col for col in df.columns if col != 'T']  # Prova tutte le colonne eccetto T
print(f"Colonne Y trovate: {y_columns}")

graphs_created = 0

for i, y_col in enumerate(y_columns):
    # Verifica che esistano entrambe le colonne
    if 'T' not in df.columns:
        print("ERRORE: Colonna 'T' non trovata!")
        continue
        
    # Prendi i dati, rimuovi valori NaN
    valid_data = df[['T', y_col]].dropna()
    print(f"\nColonna {y_col}: {len(valid_data)} punti validi")
    
    if len(valid_data) > 0:
        try:
            x = array('d', valid_data['T'].values)
            y = array('d', valid_data[y_col].values)
            
            print(f"  Valori T: {x[:5]}...")  # Prime 5 x
            print(f"  Valori {y_col}: {y[:5]}...")  # Prime 5 y
            
            graph = ROOT.TGraph(len(x), x, y)
            graph.SetName(y_col)
            graph.SetMarkerColor(colors[i % len(colors)])
            graph.SetMarkerStyle(markers[i % len(markers)])
            graph.SetLineColor(colors[i % len(colors)])
            graph.SetLineWidth(2)
            
            mg.Add(graph)
            graphs_created += 1
            print(f"  ✓ Grafico {y_col} creato con successo")
            
        except Exception as e:
            print(f"  ✗ Errore creazione grafico {y_col}: {e}")
    else:
        print(f"  ✗ Nessun dato valido per {y_col}")

print(f"\nTotale grafici creati: {graphs_created}")

if graphs_created == 0:
    print("NESSUN GRAFICO CREATO! Controlla i nomi delle colonne.")
    print("Colonne disponibili:", df.columns.tolist())
    exit()

# Visualizza con più opzioni
c = ROOT.TCanvas("c1", "Multipli Dataset da Excel", 900, 600)
c.SetGrid()

# Disegna il MultiGraph
mg.Draw("APL")  # A=assi, P=punti, L=linee

# Personalizza gli assi
mg.SetTitle("Tensione vs Tempo;Tempo (s);Tensione (V)")
mg.GetXaxis().CenterTitle()
mg.GetYaxis().CenterTitle()

# Forza un range visibile se i dati sono molto piccoli
if graphs_created > 0:
    mg.GetXaxis().SetLimits(0, mg.GetXaxis().GetXmax() * 1.1)
    mg.SetMinimum(mg.GetYaxis().GetXmin() * 0.9)
    mg.SetMaximum(mg.GetYaxis().GetXmax() * 1.1)

# Legenda
legend = c.BuildLegend(0.75, 0.75, 0.9, 0.9)
legend.SetTextSize(0.03)

c.Update()
c.Draw()

# Salva
c.SaveAs("V_vs_T.png")
print("Grafico salvato come V_vs_T.png")

# Aspetta input
input("Premi Invio per chiudere...")