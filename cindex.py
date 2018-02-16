import urllib
import os
import glob
import subprocess
import commands
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from dophot import *
from findSN import *

from astropy.time import Time

from moon import *
import csv
import json
from pprint import pprint
import os.path

sn_name="KSPN2188"

magB = np.load("phot_csv/compiledSN_" + "B" + "_" + sn_name + ".npy")
magB = magB.astype(np.float)

u_t = magB[:, 0]
u_t[u_t<370] = np.floor(u_t[u_t<370]*100)/100
u_t[u_t>370]=np.floor(u_t[u_t>370])
index=np.argsort(u_t)
u_t=u_t[index]
print u_t
u = magB[:, 3]
u=u[index]
u_e = magB[:, 4]
u_e=u_e[index]

magV = np.load("phot_csv/compiledSN_" + "V" + "_" + sn_name + ".npy")
magV = magV.astype(np.float)

v_t = magV[:, 0]
v_t[v_t<370] = np.floor(v_t[v_t<370]*100)/100
v_t[v_t>370] = np.floor(v_t[v_t>370])
index=np.argsort(v_t)
v_t=v_t[index]
v = magV[:, 3]
v=v[index]
v_e = magV[:, 4]
v_e=v_e[index]

magI = np.load("phot_csv/compiledSN_" + "I" + "_" + sn_name + ".npy")
magI = magI.astype(np.float)
i_t = magI[:, 0]
i_t[i_t<370] = np.floor(i_t[i_t<370]*100)/100
i_t[i_t>370] = np.floor(i_t[i_t>370])
index=np.argsort(i_t)
i_t=i_t[index]
i = magI[:, 3]
i=i[index]
i_e = magI[:, 4]
i_e=i_e[index]

bv_t = np.zeros(shape=(0, 1))
bv = np.zeros(shape=(0, 1))
bv_e = np.zeros(shape=(0, 1))
for index,j in enumerate(u_t):
    print j
    if np.min(np.abs(v_t-j))<=0.1:
        sub = np.argmin(np.abs(v_t - j))
        bv_t=np.concatenate((bv_t,v_t[sub].reshape((1,1))))
        bv=np.concatenate((bv,u[index]-v[sub].reshape((1,1))))
        bv_e=np.concatenate((bv_e,np.sqrt(np.square(v_e[sub].reshape((1,1)))+np.square(u_e[index].reshape((1,1))))))


vi_t = np.zeros(shape=(0, 1))
vi = np.zeros(shape=(0, 1))
vi_e = np.zeros(shape=(0, 1))
for index,j in enumerate(v_t):
    if np.min(np.abs(i_t-j))<=0.1:
        sub = np.argmin(np.abs(i_t - j))
        vi_t=np.concatenate((vi_t,i_t[sub].reshape((1,1))))
        vi=np.concatenate((vi,v[index]-i[sub].reshape((1,1))))
        vi_e=np.concatenate((vi_e,np.sqrt(np.square(i_e[sub].reshape((1,1)))+np.square(v_e[index].reshape((1,1))))))

cindex_t = np.zeros(shape=(0, 1))
cindex_vi = np.zeros(shape=(0, 1))
cindex_bv = np.zeros(shape=(0, 1))

for index,j in enumerate(vi_t):
    if np.min(np.abs(bv_t-j))<=0.1:
        sub = np.argmin(np.abs(bv_t - j))
        cindex_t=np.concatenate((cindex_t,bv_t[sub].reshape((1,1))))
        cindex_vi=np.concatenate((cindex_vi,bv[sub].reshape((1,1))))
        cindex_bv=np.concatenate((cindex_bv,vi[index].reshape((1,1))))

cindex_t=cindex_t-cindex_t[0]
ax=plt.subplot(111)

temp=np.genfromtxt("phot_csv/temperature.csv", delimiter=',')
temp_filter=np.genfromtxt("phot_csv/temps_filter.csv", delimiter=',')
BB_fluxB=np.genfromtxt("phot_csv/BB_fluxB_nofil.csv", delimiter=',')
BB_fluxV=np.genfromtxt("phot_csv/BB_fluxV_nofil.csv", delimiter=',')
BB_fluxI=np.genfromtxt("phot_csv/BB_fluxI_nofil.csv", delimiter=',')
flux_0 = [ 4023, 3562, 2814]
# BB_magB=-2.512*np.log10(BB_fluxB/flux_0[0])
# BB_magV=-2.512*np.log10(BB_fluxV/flux_0[1])
# BB_magI=-2.512*np.log10(BB_fluxI/flux_0[2])

BB_bv=-2.512*np.log10(BB_fluxB/BB_fluxV)
BB_vi=-2.512*np.log10(BB_fluxV/BB_fluxI)

from scipy.interpolate import UnivariateSpline
fit_temp = UnivariateSpline(temp[:,0] - temp[0,0], temp[:,1])
cindex_temp=fit_temp(cindex_t)
#plt.scatter(cindex_vi,cindex_bv, c=cindex_temp, cmap='jet')
plt.scatter(cindex_vi,cindex_bv, c=cindex_temp, cmap='jet_r',label='Observed')
plt.clim(4000, 15000)
plt.scatter(BB_vi,BB_bv, c=temp_filter, marker='s', cmap='jet_r',label='Blackbody')
plt.clim(4000, 15000)
plt.xlabel('V-I')
plt.ylabel('B-V')
cbar=plt.colorbar()
cbar.set_label('Temperature [k]', rotation=270)
#cbar.set_label('Time [day]', rotation=270)
ax.legend(loc='upper left', fancybox=True,fontsize=12)
plt.show()


# print bv_t
# plt.scatter(bv_t,bv,label='B-V',color='blue')
# plt.scatter(vi_t,vi,label='V-I',color='red')
# plt.xlabel('Time [days]')
# plt.ylabel('Color index')
# plt.tick_params(labelsize=20)


