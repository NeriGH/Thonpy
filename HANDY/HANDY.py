import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# Paramètres du modèle
s = 0.1
lambda_E = 100
lambda_W = 100
pi = 0.1
kappa = 0.1
delta = 0.1
r = 0.1
K = 100

# Fonction définissant les équations différentielles du modèle HANDY
def handy(y, t):
    E, W, Y, N = y
    x = pi*Y
    dEdt = s*x - E/lambda_E
    dWdt = (1-s)*x - W/lambda_W
    dYdt = pi*Y - kappa*(E+W) - delta*Y
    dNdt = r*N*(1 - N/K) - Y/(1 + Y/N)
    return [dEdt, dWdt, dYdt, dNdt]

# Conditions initiales
E0 = 1
W0 = 1
Y0 = 1
N0 = 1
y0 = [E0, W0, Y0, N0]

# Intervalle de temps
t = np.linspace(0, 100, 1000)

# Résoudre les équations différentielles
sol = odeint(handy, y0, t)

# Tracer les résultats
plt.figure(figsize=(8,6))
plt.plot(t, sol[:, 0], label='Elites (E)')
plt.plot(t, sol[:, 1], label='Travailleurs (W)')
plt.plot(t, sol[:, 2], label='Richesse (Y)')
plt.plot(t, sol[:, 3], label='Nature (N)')
plt.legend()
plt.xlabel('Temps')
plt.ylabel('Population / Richesse / Nature')
plt.title('Modèle HANDY')
plt.grid(True)
plt.show()