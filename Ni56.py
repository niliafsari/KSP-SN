from astropy.io import fits
from astropy.wcs import WCS
import numpy as np
import matplotlib
import os
import glob
from findSN import *
from matplotlib.ticker import AutoMinorLocator
import sys

sys.path.insert(0, '/home/afsari/')
from SNAP2.Analysis import *

matplotlib.rcParams['axes.linewidth'] = 1.5 #set the value globally
matplotlib.rcParams['xtick.major.size'] = 5
matplotlib.rcParams['xtick.major.width'] = 2
matplotlib.rcParams['xtick.minor.size'] = 2
matplotlib.rcParams['xtick.minor.width'] = 1.5
matplotlib.rcParams['ytick.major.size'] = 5
matplotlib.rcParams['ytick.major.width'] = 2
matplotlib.rcParams['ytick.minor.size'] = 2
matplotlib.rcParams['ytick.minor.width'] = 1.5
matplotlib.rcParams.update({'font.size': 18})


data=np.genfromtxt('/home/afsari/PycharmProjects/kspSN/phot_csv/Ni56_valenti.csv', delimiter=',')

ax=plt.subplot(111)
plt.rc('text', usetex=True)


ax.scatter(-data[:,0],10**(data[:,1]),color='black')
ax.plot(-17.47,0.10, linestyle='',markersize=11,marker=(5, 1), color='red', label='KSP-SN-2016kf')
ax.set_ylim([0.0009, 0.2])
ax.set_xlim([-18, -13])
ax.set_yscale('log')
ax.invert_xaxis()

ax.xaxis.set_minor_locator(AutoMinorLocator(10))
plt.xlabel(r'$V$-Band Magnitude at 50 days ')
plt.ylabel(r'M$_{\rm Ni}$ [M$_\odot$]')
ax.legend(ncol=1, fancybox=False,fontsize=15,frameon=True,numpoints=1)
#plt.grid()
plt.tight_layout()
plt.savefig('/home/afsari/PycharmProjects/kspSN/plots/p_ni56.pdf')
plt.show()
