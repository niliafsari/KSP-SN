from astropy.io import fits
from astropy.wcs import WCS
import numpy as np
#import matplotlib.pyplot as plt
import os
import glob
from findSN import *
import sys
from scipy.interpolate import UnivariateSpline

sys.path.insert(0, '/home/afsari/')
from SNAP2.Analysis import *

sn_name="KSPN2188"
magB = np.load("phot_csv/compiledSN_" + "B" + "_" + sn_name + ".npy")
magB = magB.astype(np.float)

u_t = magB[:, 0]
#u_t[u_t<370] = np.floor(u_t[u_t<370]*100)/100
#u_t[u_t>370]=np.floor(u_t[u_t>370])
index=np.argsort(u_t)
u_t=u_t[index]
u_t=np.delete(u_t,51)
u = magB[:, 3]
ue=magB[:, 4]
u=u[index]
ue=ue[index]
u=np.delete(u,51)
ue=np.delete(ue,51)
#z = np.polyfit(u_t-u_t[0], u, 10)
#fit_u = np.poly1d(z)
fit_u= UnivariateSpline(u_t-u_t[0], u, s=0.05)
magV = np.load("phot_csv/compiledSN_" + "V" + "_" + sn_name + ".npy")
magV = magV.astype(np.float)

v_t = magV[:, 0]
#v_t[v_t<370] = np.floor(v_t[v_t<370]*100)/100
#v_t[v_t>370] = np.floor(v_t[v_t>370])
index=np.argsort(v_t)
v_t=v_t[index]
v = magV[:, 3]
ve=magV[:, 4]
v=v[index]
ve=ve[index]
#z = np.polyfit(v_t-v_t[0], v, 10)
#fit_v = np.poly1d(z)

fit_v= UnivariateSpline(v_t-v_t[0], v, s=0.3)
#fit_v = np.poly1d(z)

magI = np.load("phot_csv/compiledSN_" + "I" + "_" + sn_name + ".npy")
magI = magI.astype(np.float)

magI = magI.astype(np.float)
i_t = magI[:, 0]
index=np.argsort(i_t)
i = magI[:, 3]
ie = magI[:, 4]

#i_t[i_t<370] = np.floor(i_t[i_t<370]*100)/100
#i_t[i_t>370] = np.floor(i_t[i_t>370])
index=np.argsort(i_t)
i_t=i_t[index]
i=i[index]
ie=ie[index]
i_t=np.delete(i_t,[68 ,69 ,70])
i=np.delete(i,[68 ,69 ,70])
ie=np.delete(ie,[68 ,69 ,70])
i = np.delete(i, np.where((i_t-i_t[0]) > 118))
ie = np.delete(ie, np.where((i_t-i_t[0]) > 118))
i_t = np.delete(i_t, np.where((i_t-i_t[0]) > 118))
print np.size(i)
#z = np.polyfit(i_t-i_t[0],i, 10)
#fit_i = np.poly1d(z)
fit_i= UnivariateSpline(i_t-i_t[0], i, s=0.2)

ax=plt.subplot(111)
plt.errorbar(u_t-u_t[0],u,yerr=ue,color='blue',label='B')
plt.errorbar(v_t-v_t[0],v,yerr=ve,color='green',label='V')
plt.errorbar(i_t-i_t[0],i,yerr=ie,color='red',label='I')

tt=np.linspace(0,110,110*2)
plt.plot(tt,fit_u(tt),color='blue',label='B fit')
tt=np.linspace(0,130,130*2)
plt.plot(tt,fit_v(tt),color='green',label='V fit')
tt=np.linspace(0,143,143*2)
plt.plot(tt,fit_i(tt),color='red',label='I fit')
plt.xlabel('Time [days]')
plt.ylabel('Abs. Mag.')
ax.invert_yaxis()
ax.legend(loc='best',ncol=6, fancybox=True,fontsize=12)
plt.show()

