import os
import glob
import subprocess
import commands
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.ticker import AutoMinorLocator
from dophot import *
from findSN import *
from astropy.time import Time
from moon import *
import csv
import sys
sys.path.insert(0, '/home/afsari/')

from SNAP import Astrometry
from SNAP.Analysis import *
current_path=os.path.dirname(os.path.abspath(__file__))
matplotlib.rcParams.update({'font.size': 18})
matplotlib.rcParams['axes.linewidth'] = 1.5 #set the value globally
# matplotlib.rcParams['xtick.major.size'] = 5
# matplotlib.rcParams['xtick.major.width'] = 2
# matplotlib.rcParams['xtick.minor.size'] = 2
# matplotlib.rcParams['xtick.minor.width'] = 1.5
# matplotlib.rcParams['ytick.major.size'] = 5
# matplotlib.rcParams['ytick.major.width'] = 2
# matplotlib.rcParams['ytick.minor.size'] = 2
# matplotlib.rcParams['ytick.minor.width'] = 1.5


# coef = {'B': 3.626, 'V': 2.742, 'I': 1.505, 'i': 1.698}
# coef = {'B': 4.315, 'V': 3.315, 'I': 1.940, 'i': 2.086}
spec_SN = np.genfromtxt(current_path+ '/KSP-N2997-1-2018oh-Gemini.flm', delimiter='  ')
spec_Nova= np.genfromtxt(current_path+'/KSP-N300-2017iv.flm', delimiter='  ')

#data_I[data_I[:,9] < 18.3,:]=[]
# data_I=np.delete(data_I, np.where(data_I[:,9] < 18.3), axis=0)
ax = plt.subplot(111)
plt.plot(spec_SN[:,0],spec_SN[0,1],color='black')
plt.plot(spec_Nova[:,0],spec_Nova[0,1],color='black')
# u=np.argmin(data_B[:,4])
# plt.errorbar(data_B[:,4][(data_B[:,9] < data_B[:,11])]-data_B[u,4],data_B[:,9][(data_B[:,9] < data_B[:,11])],yerr=data_B[:,10][(data_B[:,9] < data_B[:,11])],color='blue',label='B-band',fmt='o',markersize=10,markeredgecolor='black',
#              markeredgewidth=1.2)
# plt.errorbar(data_V[:,4][(data_V[:,9] < data_V[:,11])]-data_B[u,4],data_V[:,9][(data_V[:,9] < data_V[:,11])],yerr=data_V[:,10][(data_V[:,9] < data_V[:,11])],color='green',label='V-band',fmt='o',markersize=10,markeredgecolor='black',
#              markeredgewidth=1.2)
# plt.errorbar(data_I[:,4][(data_I[:,9] < data_I[:,11])]-data_B[u,4],data_I[:,9][(data_I[:,9] < data_I[:,11])],yerr=data_I[:,10][(data_I[:,9] < data_I[:,11])],color='red',label='I-band',fmt='o',markersize=10,markeredgecolor='black',
#              markeredgewidth=1.2)
#plt.axis([720-365,855-365,18,23.2])
# ax.set_xlim([-1, 10])
# ax.set_ylim([18, 20.7])
#plt.gca().invert_yaxis()
plt.xlabel('Rest Wavelength [Ang]')
plt.ylabel('Counts [Arbitrary Units]')
# ax.legend(loc='best',ncol=1, fancybox=True,fontsize=14, frameon=False)
#ax1.spines[side].set_linewidth(size)
# ax.yaxis.set_minor_locator(AutoMinorLocator(10))
# ax.xaxis.set_minor_locator(AutoMinorLocator(10))
ax.xaxis.set_tick_params(width=1.5)
ax.yaxis.set_tick_params(width=1.5)
# plt.xticks(np.arange(-1, 10, 1.0))
#y=np.arange(18, 21,0.2)
# ax.fill_betweenx(y,x1=4,x2=5, color='y',alpha=0.5,zorder=0)
# plt.annotate('KSP-N2997-1_2018oh', xy=(0.3, 0.05), xycoords='axes fraction')
# ax.text(4.4, 20, '2018A', fontsize=17, rotation='vertical',multialignment='center',va='center')
plt.tight_layout()
plt.show()