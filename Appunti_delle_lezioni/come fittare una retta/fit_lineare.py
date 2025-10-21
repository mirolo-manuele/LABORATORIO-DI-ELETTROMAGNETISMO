import ROOT #importo la libreria ROOT
import numpy as np #importo numpy come np, mi serve per fare i calcoli
from array import array #importo array per creare gli array di dati (mi serve perchè root non riconosce le liste di python)


x = array('d', [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
y = array('d', [2.42,4.00,7.02,8.0,10,12.91,15.99,16.12,19.21,21.35,
                23.45,25.58,27.68,29.79,31.88,34.02,36.11,38.25,40.34,42.48])
ey = array('d', [0.15]*len(x))
ex = array('d', [0.0]*len(x))
v_soglia = 1.0

c = ROOT.TCanvas("c", "Grafico con errori", 800, 600) #creo il canvas
#c nome del canvas
#titolo del canvas
#dimensioni (in pixel)



g=ROOT.TGraphErrors(len(x), x, y, ex, ey) #creo il grafico con gli errori (lunghezza len(x), x, y, errori x=0, errori y=dati forniti)

#con TH1F non serve convertire in array perchè lo crea lui (C++)

g.SetTitle("Grafico con errori;X[M];Y[S]") #titolo del grafico e degli assi
g.SetMarkerStyle(21) #stile dei punti
g.SetMarkerColor(ROOT.kBlue) #colore dei punti
g.SetMarkerSize(0.5) #dimensione dei punti
g.SetLineColor(ROOT.kRed) #colore della linea
g.SetLineWidth(1) #larghezza della linea

g.Draw("APL") #disegna 
#ho diverse opzioni (unisco le lettere per fare più cose insieme):
#"A" solo gli assi
#"P" solo i punti
#"L" solo la linea che congiungono i punti

indici_fit = [i for i in range(len(x)) if x[i] >= v_soglia] #creo un array con gli indici dei punti con x >= v_soglia
#metto nella lista i (primo i) (potevo mettere per esempio i^2)
#questo i (o i^2) è associato ad ogni posizione dell'array (for i in range(len(x))
#ma tutto ciò solo se x[i] >= v_soglia

x_fit = array('d', [x[i] for i in indici_fit])
y_fit = array('d', [y[i] for i in indici_fit])
ey_fit = array('d', [ey[i] for i in indici_fit]) #creo un array con solo i dati con x >= v_soglia




g_fit = ROOT.TGraphErrors(len(x_fit), x_fit, y_fit, ex, ey_fit) #Crea un nuovo grafico con solo i punti filtrati (x ≥ v_soglia)
ROOT.gStyle.SetOptFit(1111) #mostra le statistiche del fit sul grafico (parametri, chi2, ndf, probabilità)
#altre combinazioni: 
#1       Solo χ²
#10      Solo NDF  
#100     Solo Probabilità
#1000    Solo valori parametri
#10000   Solo errori parametri
#100000  Solo matrix correlazione

#IN QUESTA PARTE DEL CODICE ROOT VA A STIMARE I PARAMETRI INIZIALI DEL FIT (m,q) se non vanno bene lo rifà (in base a chi)



fit_func = ROOT.TF1("fit_func", "pol1",min(x_fit), max(x_fit))
#Cosa fa: Crea una funzione lineare per fit
# "fit_func" = nome
#"pol1" = polinomio di grado 1 (retta)
#v_soglia, max(x) = intervallo del fit


fit_result = g_fit.Fit(fit_func, "S+", "",min(x_fit), max(x_fit)) #esegue il fit su g_fit
#"S" = Salva il risultato del fit
# opzioni:
#"S"    Salva il risultato del fit (puoi fare GetFunction()), posso rendere i parametri
#"Q"    Quiet mode (non stampa output)
#"V"    Verbose mode (stampa più dettagli)
#"R"    Usa range della funzione TF1 invece di specificare xmin,xmax
#"M"    Usa Minuit invece di Fumili
#"E"    Considera errori statistici


#"+" = Aggiungi alla lista delle funzioni 
 

#"" = Nessuna opzione aggiuntiva per il disegno
#opzioni:
# "0" non disegnare
# "L" disegna solo la linea
# "P" disegna solo i punti


#v_soglia, max(x) = intervallo del fit

# Parametri del fit (posso farlo perchè ho messo "S" nelle opzioni del fit)
m = fit_func.GetParameter(1)
q = fit_func.GetParameter(0)
dm = fit_func.GetParError(1)
dq = fit_func.GetParError(0)



fit_func.SetLineColor(ROOT.kBlack)
fit_func.SetLineWidth(2)
fit_func.Draw("SAME") #disegna la funzione di fit sullo stesso grafico

c.Modified() #aggiorna il canvas       #QUESTI non servono se metto c.Draw() alla fine
c.Update() #applica le modifiche
c.Draw() #disegna il canvas
c.SaveAs("grafico_con_errori.png") #salva il canvas come immagine png
input("Premi Invio per chiudere...") #mantiene aperta la finestra del grafico finchè non premo invio