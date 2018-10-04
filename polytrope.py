import numpy as np
from scipy.integrate import simps, cumtrapz, trapz
import scipy.io as io
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit



n = 1.5
nn=1000
r = np.linspace(0, 1, nn) + 0.5 / nn
rho = r.copy() * 0. + 1;
G = 1.  # keep symbol; value not important.

for i in range(100):
    m = cumtrapz(4 * np.pi * r ** 2 * rho, r, initial=0)

    mmax = np.max(m)  ## normalize density and mass to unit mass.
    rho = rho / mmax
    plt.plot(r, rho)
    m = m / mmax

    g = -G * m / r ** 2
    Phi = cumtrapz(-g, r, initial=0)
    rho = (np.max(Phi) - Phi) ** n

rho = rho / mmax
print np.shape(rho),rho
np.savetxt('polytrope15.txt',np.concatenate((np.reshape(r,[nn,1]), np.reshape(rho,[nn, 1])),axis=1),delimiter=',')
plt.plot(r,rho)
plt.show()