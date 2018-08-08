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
sn_name='KSPN2188_v1'
magV = np.load("phot_csv/compiledSN_" + "V" + "_" + sn_name + ".npy")
magV = magV.astype(np.float)
u = 358.6
data=np.genfromtxt('/home/afsari/PycharmProjects/kspSN/phot_csv/anderson.csv', delimiter=',')
from scipy import interpolate

ax=plt.subplot(111)
#plt.rc('text', usetex=True)


ax.scatter(data[:,0],-(data[:,1]),s=0.5,color='black')
#ax.plot(-17.47,0.13, linestyle='',markersize=11,marker=(5, 1), color='red', label='KSP-SN-2016kf')
index=np.argsort(magV[:, 0])
magV=magV[index,:]


tck = interpolate.splrep(magV[:, 0], magV[:, 3], s=0.3)
magnew_v = interpolate.splev(magV[:, 0], tck, der=0)
ax.plot(magV[:, 0] - magV[0, 0], magnew_v , linestyle='-',lw=3, color='red',
         label='KSP-SN-2016kf')
#ax.set_ylim([0.0009, 0.2])
#ax.set_xlim([-18, -13])
#ax.set_yscale('log')
ax.invert_yaxis()
ax.yaxis.set_minor_locator(AutoMinorLocator(10))
ax.xaxis.set_minor_locator(AutoMinorLocator(5))
plt.ylabel('$V$-Band Magnitude')
plt.xlabel('Time since explosion [days]')
ax.legend(ncol=1, fancybox=True,fontsize=15,frameon=False,numpoints=1)
#plt.grid()
plt.tight_layout()
plt.savefig('/home/afsari/PycharmProjects/kspSN/plots/p_anderson.pdf')
plt.show()
