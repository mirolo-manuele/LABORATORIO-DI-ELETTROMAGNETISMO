import math
import matplotlib.pyplot as plt
import numpy as np

def intersezioni_parabola_retta(a, b, c, m, q):
    """
    Calcola i punti di intersezione tra la parabola y = ax^2 + bx + c 
    e la retta y = mx + q.
    """
    
    # Coefficienti dell'equazione quadratica risolvente A*x^2 + B*x + C = 0
    # Dove A = a, B = b - m, C = c - q
    A = a
    B = b - m
    C = c - q
    
    # Calcolo del discriminante Delta = B^2 - 4*A*C
    discriminante = B**2 - 4 * A * C
    
    print(f"Equazione risolvente: {A}x^2 + ({B})x + ({C}) = 0")
    print(f"Discriminante (Δ): {discriminante}")
    
    if discriminante > 0:
        # Due intersezioni reali distinte
        # 



        print("\n=> Due punti di intersezione (Retta Secante)")
        
        # Calcolo delle due soluzioni per x
        x1 = (-B + math.sqrt(discriminante)) / (2 * A)
        x2 = (-B - math.sqrt(discriminante)) / (2 * A)
        
        # Calcolo delle corrispondenti y usando l'equazione della retta (più semplice)
        y1 = m * x1 + q
        y2 = m * x2 + q
        
        punti = [(x1, y1), (x2, y2)]
        
    elif discriminante == 0:
        # Una singola intersezione reale (punto di tangenza)
        # 
        print("\n=> Un solo punto di intersezione (Retta Tangente)")
        
        # Calcolo della singola soluzione per x
        x_tangente = -B / (2 * A)
        
        # Calcolo della corrispondente y
        y_tangente = m * x_tangente + q
        
        punti = [(x_tangente, y_tangente)]
        
    else:
        # Nessuna intersezione reale
        # 
        print("\n=> Nessun punto di intersezione reale (Retta Esterna)")
        punti = []
        
    return punti

# --- Esempio d'uso ---

# Esempio Parabola: y = x^2 - 3x + 4 (a=1, b=-3, c=4)
a_par = - 0.00000058
b_par = 0.04075137
c_par = 55.1579


m_retta = 0
q_retta = 545.1550931

x = np.linspace(-17000, 90000, 20000)

risultato = intersezioni_parabola_retta(a_par, b_par, c_par, m_retta, q_retta)

y_par=a_par*x**2+b_par*x+c_par
y_retta=m_retta*x+q_retta

plt.plot(x, y_par, label='Parabola')
plt.plot(x, m_retta*x + q_retta, label='Retta')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.show()

plt.figure(figsize=(10,6))

# Disegno parabola e retta
plt.plot(x, y_par)
plt.plot(x, y_retta)

# Disegno eventuali punti di intersezione
for (x, y) in risultato:
    plt.scatter(x, y, color='red')
    plt.text(x, y, f"({x:.2f}, {y:.2f})", fontsize=9, color='red')

plt.xlabel('x')
plt.ylabel('y')
plt.title('Intersezione tra Parabola e Retta')
plt.grid(True)
plt.legend()
plt.show()

print("\n--- Risultato ---")
if risultato:
    print("I punti di intersezione sono:")
    for i, (x, y) in enumerate(risultato):
        print(f"Punto {i+1}: X={x:.4f}, Y={y:.4f}")
else:
    print("Non ci sono intersezioni reali.")