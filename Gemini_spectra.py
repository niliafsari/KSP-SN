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
matplotlib.rcParams.update({'font.size': 20})
matplotlib.rcParams['axes.linewidth'] = 1.5 #set the value globally
# matplotlib.rcParams['xtick.major.size'] = 5
# matplotlib.rcParams['xtick.major.width'] = 2
matplotlib.rcParams['xtick.minor.size'] = 2
matplotlib.rcParams['xtick.minor.width'] = 1.5
# matplotlib.rcParams['ytick.major.size'] = 5
# matplotlib.rcParams['ytick.major.width'] = 2
# matplotlib.rcParams['ytick.minor.size'] = 2
# matplotlib.rcParams['ytick.minor.width'] = 1.5


# coef = {'B': 3.626, 'V': 2.742, 'I': 1.505, 'i': 1.698}
# coef = {'B': 4.315, 'V': 3.315, 'I': 1.940, 'i': 2.086}
spec_SN = np.genfromtxt('/home/afsari/snandhostgalaxyspectrum/spectrum.text', delimiter=' ')
SN1999em= np.genfromtxt('SN1999em_94.txt', delimiter=',')
SN2009ib= np.genfromtxt('SN2009ib_103.txt', delimiter=',')
SN2013fs= np.genfromtxt('SN2013fs_81.txt', delimiter=',')
SN2012aw= np.genfromtxt('SN2012aw_91.txt', delimiter=',')
#spec_Nova= np.genfromtxt(current_path+'/KSP-N300-2017iv.flm', delimiter='  ')

#plt.rc('text', usetex=True)
#data_I[data_I[:,9] < 18.3,:]=[]
# data_I=np.delete(data_I, np.where(data_I[:,9] < 18.3), axis=0)
ax = plt.subplot(211)
plt.plot(spec_SN[:,0],spec_SN[:,1]*10,color='red')
print SN1999em[:,0]
SN2013fs_z=	0.011855
SN1999em_z=0.002392
SN2009ib_z=0.00482
SN2012aw_z=0.002595

SN1999em[:,0]=SN1999em[:,0]- (SN1999em_z*SN1999em[:,0])
SN2009ib[:,0]=SN2009ib[:,0]-(SN2009ib_z*SN2009ib[:,0])
SN2013fs[:,0]=SN2013fs[:,0]-(SN2013fs_z*SN2013fs[:,0])
SN2012aw[:,0]=SN2012aw[:,0]-(SN2012aw_z*SN2012aw[:,0])
print np.nanmax(SN1999em[:,1]),np.nanmax(SN2009ib[:,1]),np.nanmax(SN2012aw[:,1])
plt.plot(SN1999em[:,0],(SN1999em[:,1]/np.nanmax(SN1999em[:,1]))+1,color='black',label='SN1999em')
plt.plot(SN2009ib[:,0],SN2009ib[:,1]/np.nanmax(SN2009ib[:,1])+2,color='black',label='SN2009ib')
#plt.plot(SN2013fs[:,0],SN2013fs[:,1]/np.nanmax(SN2013fs[:,1])+2,color='black',label='SN2013fs')
plt.plot(SN2012aw[:,0],SN2012aw[:,1]/np.nanmax(SN2012aw[:,1])+3,color='black',label='SN2012aw')
# plt.plot(spec_Nova[:,0],spec_Nova[:,1]/np.max(spec_Nova[:,1]),color='black')
# u=np.argmin(data_B[:,4])
# plt.errorbar(data_B[:,4][(data_B[:,9] < data_B[:,11])]-data_B[u,4],data_B[:,9][(data_B[:,9] < data_B[:,11])],yerr=data_B[:,10][(data_B[:,9] < data_B[:,11])],color='blue',label='B-band',fmt='o',markersize=10,markeredgecolor='black',
#              markeredgewidth=1.2)
# plt.errorbar(data_V[:,4][(data_V[:,9] < data_V[:,11])]-data_B[u,4],data_V[:,9][(data_V[:,9] < data_V[:,11])],yerr=data_V[:,10][(data_V[:,9] < data_V[:,11])],color='green',label='V-band',fmt='o',markersize=10,markeredgecolor='black',
#              markeredgewidth=1.2)
# plt.errorbar(data_I[:,4][(data_I[:,9] < data_I[:,11])]-data_B[u,4],data_I[:,9][(data_I[:,9] < data_I[:,11])],yerr=data_I[:,10][(data_I[:,9] < data_I[:,11])],color='red',label='I-band',fmt='o',markersize=10,markeredgecolor='black',
#              markeredgewidth=1.2)
#plt.axis([720-365,855-365,18,23.2])
ax.set_xlim([3500, 8900])
#ax.set_ylim([-0.7, 3])
#plt.gca().invert_yaxis()
label=ax.set_ylabel(r'Scaled Flux$_\lambda$ + Constant')
ax.yaxis.set_label_coords(-0.1, 0)
# ax.legend(loc='best',ncol=1, fancybox=True,fontsize=14, frameon=False)
#ax1.spines[side].set_linewidth(size)
ax.yaxis.set_minor_locator(AutoMinorLocator(5))
ax.xaxis.set_minor_locator(AutoMinorLocator(5))
ax.xaxis.set_tick_params(width=1.5)
ax.yaxis.set_tick_params(width=1.5)

#y=np.arange(18, 21,0.2)
# ax.fill_betweenx(y,x1=4,x2=5, color='y',alpha=0.5,zorder=0)
# plt.annotate('KSP-N2997-1_2018oh', xy=(0.3, 0.05), xycoords='axes fraction')
#ax.text(7100,0.5, 'KSP-N2997-1-2018oh (SNIa)', fontsize=16,multialignment='center',va='center')
ax.text(6800,0.85, 'KSP-OT-2016kf (+96)', fontsize=17,multialignment='center',va='center')
ax.text(7050,1.86, 'SN1999em (+94)', fontsize=17,multialignment='center',va='center')
ax.text(7050,2.83, 'SN2009ib (+103)', fontsize=17,multialignment='center',va='center')
#ax.text(9000,1.9, 'SN2013fs (+81)', fontsize=13,multialignment='center',va='center')
ax.text(7050,3.83, 'SN2012aw (+91)', fontsize=17,multialignment='center',va='center')

my_file = open('lines.csv', 'r')
reader = csv.reader(my_file, delimiter=' ')
my_list = list(reader)
my_file.close()
lines= np.genfromtxt ('lines.csv', delimiter=" ")
print my_list[0]
#mydict1 = {rows[0]:rows[1] for rows in my_list}
y=np.arange(-1, 4,0.2)
for l in my_list:
    print l[0], l[1]
    #ax.axvline(x=float(l[0]), ymax=1, color='black',lw=1)
    ax.fill_betweenx(y, x1=float(l[0])-35, x2=float(l[0])+9, color='gray', alpha=0.5, zorder=0)
    ax.text(float(l[0])-45,-0.2, l[1], fontsize=11,rotation=90,multialignment='center',va='center')
# ax.text( 5500, -0.07, 'KSP-N300-2017iv (Nova)', fontsize=16,multialignment='center',va='center')
ax.xaxis.set_ticklabels([])
ax2 = plt.subplot(212)
host= np.genfromtxt('host_spectrum.csv', delimiter=' ')
ax2.plot(host[:,0],host[:,1]/np.nanmax(host[:,1]),color='black',label='Host Galaxy')
print host[:,0]
ax2.yaxis.set_minor_locator(AutoMinorLocator(5))
ax2.xaxis.set_minor_locator(AutoMinorLocator(10))
ax2.xaxis.set_tick_params(width=1.5)
ax2.yaxis.set_tick_params(width=1.5)
ax2.set_ylim([-0.2, 1.1])
plt.xticks(np.arange(3500, 8900, 1000))
ax2.xaxis.set_ticklabels(np.arange(3500, 8900, 1000))
ax2.set_xlim([3500, 8900])
ax2.text( 7000, 0.8, 'Host Galaxy', fontsize=17,multialignment='center',va='center')
my_file = open('host_lines.csv', 'r')
reader = csv.reader(my_file, delimiter=' ')
my_list = list(reader)
my_file.close()
for l in my_list:
    print l[1]
    if l[1]=='[NII]':
        ax2.axvline(x=6584, ls='--', ymax=1, color='black', lw=1)
        ax2.text(float(l[0])+20, 0.6, '[NII]', fontsize=12, rotation=90, multialignment='center', va='center')
    elif  l[1]=='[OII]':
        ax2.axvline(x=l[0], ls='--', ymax=1, color='black', lw=1)
        ax2.text(float(l[0])+20, 0.8, l[1], fontsize=12, rotation=90, multialignment='center', va='center')
    elif  float(l[0])==6560:
        ax2.axvline(x=float(l[0]),ls='--', ymax=1, color='black',lw=1)
        ax2.text(6500,0, l[1], fontsize=12,rotation=90,multialignment='center',va='center')
    elif float(l[0]) == 4959:
        ax2.axvline(x=float(l[0]), ls='--', ymax=1, color='black', lw=1)
        ax2.text(4959-70, 0.7, l[1], fontsize=12, rotation=90, multialignment='center', va='center')
    else:
        ax2.axvline(x=float(l[0]),ls='--', ymax=1, color='black',lw=1)
        ax2.text(float(l[0])+20,0, l[1], fontsize=12,rotation=90,multialignment='center',va='center')

plt.xlabel('Rest Wavelength [Ang]')
matplotlib.rcParams.update({'font.size': 18})
matplotlib.rcParams['axes.linewidth'] = 1.5
plt.tight_layout()
plt.subplots_adjust(hspace=0, wspace=0.2)
plt.show()