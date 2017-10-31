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

ax=plt.subplot(111)
print bv_t
plt.scatter(bv_t,bv,label='B-V',color='blue')
plt.scatter(vi_t,vi,label='V-I',color='red')
plt.xlabel('Time [days]')
plt.ylabel('Color index')
plt.tick_params(labelsize=20)
ax.legend(loc='lower right', fancybox=True,fontsize=12)

plt.show()