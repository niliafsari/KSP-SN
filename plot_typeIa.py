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
import sys
sys.path.insert(0, '/home/afsari/')
from matplotlib.ticker import AutoMinorLocator
from SNAP import Astrometry
from SNAP.Analysis import *
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

matplotlib.rcParams['axes.linewidth'] = 1.5 #set the value globally
matplotlib.rcParams['xtick.major.size'] = 5
matplotlib.rcParams['xtick.major.width'] = 2
matplotlib.rcParams['xtick.minor.size'] = 2
matplotlib.rcParams['xtick.minor.width'] = 1.5
matplotlib.rcParams['ytick.major.size'] = 5
matplotlib.rcParams['ytick.major.width'] = 2
matplotlib.rcParams['ytick.minor.size'] = 2
matplotlib.rcParams['ytick.minor.width'] = 1.5
current_path=os.path.dirname(os.path.abspath(__file__))
matplotlib.rcParams.update({'font.size': 17})
coef = {'B': 3.626, 'V': 2.742, 'I': 1.505, 'i': 1.698}
coef = {'B': 4.315, 'V': 3.315, 'I': 1.940, 'i': 2.086}

direc='/data/afsari/SNAP/cockpit-lc/'
fname_B=direc+'KSP-N2997-1-2018oh.B.lc.CN_180627.txt'
fname_V=direc+'KSP-N2997-1-2018oh.V.lc.CN_180627.txt'
fname_I=direc+'KSP-N2997-1-2018oh.I.lc.CN_180627.txt'

f_list=[fname_B,fname_V,fname_I]

for i,filename in enumerate(f_list):
    tmp_filename = filename + '.tmp'
    fr = open(filename, 'r')
    fw = open(tmp_filename, 'w')
    for j,line in enumerate(fr):
        if j<5:
            continue
        newline=' '.join(line.split())
        fw.write(newline+'\n')
    fr.close()
    fw.close()


data_B = np.genfromtxt(fname_B+'.tmp', delimiter=' ')
data_V = np.genfromtxt(fname_V+'.tmp', delimiter=' ')
data_I = np.genfromtxt(fname_I+'.tmp', delimiter=' ')
#
# print data_B[90,:]
ax1=plt.subplot(111)
ax1.errorbar(data_B[:,0][data_B[:,6]<data_B[:,8]]-64, data_B[:,6][data_B[:,6]<data_B[:,8]]+1, yerr= data_B[:, 7][data_B[:,6]<data_B[:,8]], color='blue', label='B+1',fmt='o',markersize=6,markeredgecolor='black',
              markeredgewidth=1.2)
ax1.errorbar(data_V[:,0][data_V[:,6]<data_V[:,8]]-64, data_V[:,6][data_V[:,6]<data_V[:,8]], yerr= data_V[:, 7][data_V[:,6]<data_V[:,8]], color='green', label='V',fmt='o',markersize=6,markeredgecolor='black',
              markeredgewidth=1.2)
ax1.errorbar(data_I[:,0][data_I[:,6]<data_I[:,8]]-64, data_I[:,6][data_I[:,6]<data_I[:,8]]-2, yerr= data_I[:, 7][data_I[:,6]<data_I[:,8]], color='red', label='I-2',fmt='o',markersize=6,markeredgecolor='black',
              markeredgewidth=1.2)

# ax1.scatter(data_B[:,0][data_B[:,6]<data_B[:,8]], data_B[:,8][data_B[:,6]<data_B[:,8]], color='lightblue', label='B+1')
# ax1.scatter(data_V[:,0][data_V[:,6]<data_V[:,8]], data_V[:,8][data_V[:,6]<data_V[:,8]], color='lightgreen', label='V')
# ax1.scatter(data_I[:,0][data_I[:,6]<data_I[:,8]], data_I[:,8][data_I[:,6]<data_I[:,8]], color='pink', label='I-2')

plt.xlabel('Time [days]')
plt.ylabel('Apparent Magnitude [mag]')
ax1.legend(loc='best',ncol=1, fancybox=True,fontsize=14, frameon=False)
ax1.yaxis.set_minor_locator(AutoMinorLocator(10))
ax1.xaxis.set_minor_locator(AutoMinorLocator(10))
ax1.xaxis.set_tick_params(width=1.5)
ax1.yaxis.set_tick_params(width=1.5)

ax1.set_xlim([-4,120])
ax1.set_ylim([16,26])
# plt.xticks(np.arange(-4, 5, 1.0))
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

