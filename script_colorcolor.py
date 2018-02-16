import numpy as np
import matplotlib.pyplot as plt
import U  # values for constants
B = lambda nu, T, muOnKT: nu**3 * 1./(np.exp(U.Hplanck/U.Kb*nu/T-muOnKT) - 1)
nu_B = U.Clight/(4378*U.Angstrom)
nu_V = U.Clight/(5466*U.Angstrom)
nu_I = U.Clight/(8565*U.Angstrom)
BminusV = lambda T,muOnKT: -2.5*np.log10(B(nu_B,T,muOnKT)/B(nu_V,T,muOnKT) )
VminusI = lambda T,muOnKT: -2.5*np.log10(B(nu_V,T,muOnKT)/B(nu_I,T,muOnKT) )
plt.figure()
for muOnKT in np.arange(0,1,.1):
    for T in np.arange(4000,15000,100):
        plt.plot(VminusI(T,0),BminusV(T,0),'s')
plt.show()