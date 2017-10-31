import os
import glob
import subprocess
import commands
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from dophot import *
from findSN import *
from SNAP import Astrometry
from astropy.time import Time
from moon import *
import csv
import itertools
matplotlib.rcParams.update({'font.size': 18})

band="B"
marker = itertools.cycle(('1', '+','8', 'p','.','>','^','x','v','d','s', 'o','h', '*','<'))
colors = itertools.cycle(("black","gray","red","olive","green",
                          "darkkhaki","peru","blue","m","salmon","gold","yellow","sienna","deepskyblue"))
with open("logs/sn_names.txt") as f:
    file_names = f.readlines()

file_names = [line.rstrip('\n') for line in file_names]
files_count=len(file_names)

# ax = plt.subplot(132)
# mag=np.load("phot_csv/compiledSN_"+band+"_"+"kspn2188"+".npy")
# ax.plot(mag[:,0],mag[:,3],linestyle = '',marker='*')
# ax.invert_yaxis()

ax1 = plt.subplot(311)
ax2 = plt.subplot(312)
ax3 = plt.subplot(313)
for i,sn_name in enumerate(file_names):
    mark=marker.next()
    col=colors.next()
    magB=np.load("phot_csv/compiledSN_"+"B"+"_"+sn_name+".npy")
    magB=magB.astype(np.float)
    u=np.argmin(magB[:, 3])
    ax1.plot(magB[:,0]-magB[u,0],magB[:,3], linestyle = '', marker=mark,color=col,label=sn_name)
    magV=np.load("phot_csv/compiledSN_"+"V"+"_"+sn_name+".npy")
    magV=magV.astype(np.float)
    ax2.plot(magV[:,0]-magV[u,0],magV[:,3], linestyle = '', marker=mark,color=col,label=sn_name)
    magI=np.load("phot_csv/compiledSN_"+"I"+"_"+sn_name+".npy")
    magI=magI.astype(np.float)
    if magI.size>0:
        ax3.plot(magI[:,0]-magI[0,0],magI[:,3], linestyle = '', marker=mark,color=col,label=sn_name)
plt.subplot(311)
plt.title("B")
plt.ylabel('Absolute Magnitude')
plt.xlabel('Time since max light [days]')
ax1.legend(loc='lower right',ncol=2, fancybox=True,fontsize=12)
ax1.invert_yaxis()

plt.subplot(312)
plt.title("V")
plt.ylabel('Absolute Magnitude')
plt.xlabel('Time since max light [days]')
#ax2.legend(loc='lower right',ncol=2, fancybox=True,fontsize=12)
ax2.invert_yaxis()

plt.subplot(313)
plt.title("I")
plt.ylabel('Absolute Magnitude')
plt.xlabel('Time since max light [days]')
#ax3.legend(loc='lower right',ncol=2, fancybox=True,fontsize=12)
ax3.invert_yaxis()


# ax4=plt.subplot(111)
# sn_name='KSPN2188'
# magB = np.load("phot_csv/compiledSN_" + "B" + "_" + sn_name + ".npy")
# magB = magB.astype(np.float)
# u = np.argmin(magB[:, 3])
# ax4.plot(magB[:, 0] - magB[u, 0], magB[:, 3], linestyle='', marker=mark, color=col, label=sn_name)
# magV = np.load("phot_csv/compiledSN_" + "V" + "_" + sn_name + ".npy")
# magV = magV.astype(np.float)
# ax4.plot(magV[:, 0] - magV[u, 0], magV[:, 3], linestyle='', marker=mark, color=col, label=sn_name)
# magI = np.load("phot_csv/compiledSN_" + "I" + "_" + sn_name + ".npy")
# magI = magI.astype(np.float)
# if magI.size > 0:
#     ax4.plot(magI[:, 0] - magI[0, 0], magI[:, 3], linestyle='', marker=mark, color=col, label=sn_name)
# ax4.invert_yaxis()
plt.show()

