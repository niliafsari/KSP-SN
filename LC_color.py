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
import itertools
from scipy import interpolate
from matplotlib.ticker import AutoMinorLocator
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
matplotlib.rcParams.update({'font.size': 22})

marker = itertools.cycle(('8', 'p','>','^','v','<','s', 'o','h','<'))
colors = itertools.cycle(("black","yellow","salmon","green","m","sienna","gray","blue",
                          "darkkhaki","peru","gold","deepskyblue","olive"))
with open("logs/sn_names_color.txt") as f:
    file_names = f.readlines()

file_names = [line.rstrip('\n') for line in file_names]
files_count=len(file_names)

# ax = plt.subplot(132)
# mag=np.load("phot_csv/compiledSN_"+band+"_"+"kspn2188"+".npy")
# ax.plot(mag[:,0],mag[:,3],linestyle = '',marker='*')
# ax.invert_yaxis()

ax1 = plt.subplot(211)
ax2 = plt.subplot(212)
dict1={'SN1999em':0,'ASASSN-14dq':56841,'SN1987A':46849,'SN2014cx':56900,'SN2013fs':56422,'KSPN2188_v1':358.1, 'SN2012aw':56002,'SN2005cs':53548}
for i,sn_name in enumerate(file_names):
    print sn_name
    if sn_name!='KSPN2188_v1':
        mark=marker.next()
        col=colors.next()
    magB=np.load("phot_csv/compiledSN_"+"B"+"_"+sn_name+".npy")
    if 1:
        magB=magB.astype(np.float)
        magB = magB[np.argsort(magB[:, 0]), :]
        u=np.argmin(magB[:, 1])
    if  sn_name=='SN1987A':
        u=0
######################
    magV = np.load("phot_csv/compiledSN_" + "V" + "_" + sn_name + ".npy")
    magV=magV.astype(np.float)
    magV = magV[np.argsort(magV[:, 0]), :]
    ind = np.where(((magV[:, 0] - magV[0, 0]) > 150))
    magV = np.delete(magV, ind, 0)
####################
    magI=np.load("phot_csv/compiledSN_"+"I"+"_"+sn_name+".npy")
    magI=magI.astype(np.float)
    magI=magI[np.argsort(magI[:,0]),:]
    ind = np.where(((magI[:, 0] - magI[0, 0]) > 150))
    magI = np.delete(magI, ind, 0)
    if magI.size>0:
        if sn_name == 'KSPN2188_v1':
            ind = np.where(( magI[:,3]< -16.2) & ((magI[:,0]-magI[0,0]) > 125))
            magI= np.delete(magI, ind, 0)
    if  1:
        tck = interpolate.splrep(magV[:,0]-dict1[sn_name], magV[:, 3], s=0.05)
        magnew_v = interpolate.splev(magB[:,0]-dict1[sn_name], tck, der=0)
        bv=magB[:, 3]-magnew_v
        bv_t=magB[:,0]-dict1[sn_name]
        # if sn_name == 'SN1999em1':
        #     z = np.polyfit(magV[:, 0] - magB[u, 0], magV[:, 3], 6)
        #     p = np.poly1d(z)
        #     tck = interpolate.splrep(magV[:, 0] - magB[u, 0], p(magV[:, 0] - magB[u, 0]), s=0.02)
        #     magnew_v = interpolate.splev(magB[:, 0] - magB[u, 0], tck, der=0)
        #     # z = np.polyfit(magB[:, 0] - magB[u, 0], magV[:, 3], 5)
        #     # p = np.poly1d(z)
        #     bv = magB[:, 3] - magnew_v
        #     bv_t = magB[:, 0] - magB[u, 0]
    if sn_name != 'KSPN2188_v1':
        ax1.errorbar(bv_t, bv,linestyle='', fmt=mark, color=col, label=sn_name,markersize=6,markeredgewidth=0.5, markeredgecolor='black')
        print bv_t
    else:
        bv=np.load('phot_csv/bv.npy')
        ax1.errorbar(bv[:,0]-dict1[sn_name], bv[:,1],yerr=bv[:,2],fmt='H',color='r',markersize=5, label='KSP-SN-2016kf',markeredgewidth=0.5, markeredgecolor='black')
    #####
    if  1:
        if sn_name=='SN2012aw':
            tck = interpolate.splrep(magI[:,0]-dict1[sn_name], magI[:, 3], s=0.001)
        else:
            tck = interpolate.splrep(magI[:,0]-dict1[sn_name], magI[:, 3], s=0.2)
        magnew_i = interpolate.splev(magV[:,0]-dict1[sn_name], tck, der=0)
        vi=magV[:, 3]-magnew_i
    vi_t=magV[:,0]-dict1[sn_name]
    #print vi_t, vi
    if (sn_name != 'KSPN2188_v1' and sn_name!='SN2012aw'):
        ax2.plot(vi_t, vi,linestyle='', marker=mark, color=col, label=sn_name,markersize=6,markeredgewidth=0.5, markeredgecolor='black')
    elif (sn_name == 'KSPN2188_v1'):
        vi=np.load('phot_csv/vi.npy')
        ax2.errorbar(vi[:,0]-dict1[sn_name], vi[:,1],yerr=vi[:,2],fmt='H',linestyle='',markersize=5, color='r', label='KSP-SN-2016kf',markeredgewidth=0.5, markeredgecolor='black')


label=ax1.set_ylabel('B-V')
label=ax2.set_ylabel('V-i/I')
ax2.yaxis.set_label_coords(-0.09, 0.5)
#ax1.grid()
# plt.yticks([0,1,2])
ax1.set_xlim([-15, 150])
ax1.set_ylim([-0.4, 2])

ax2.set_xlim([-15, 150])
ax2.set_ylim([-0.7, 1.3])

ax1.yaxis.set_minor_locator(AutoMinorLocator(10))
ax1.xaxis.set_minor_locator(AutoMinorLocator(10))
ax1.xaxis.set_tick_params(width=1.5)
ax1.yaxis.set_tick_params(width=1.5)
ax1.xaxis.set_ticklabels([])
#plt.annotate('B', xy=(0.85, 0.85), color='black', xycoords='axes fraction')
#bbox_to_anchor=(0.5, -0.2),
#ax2.legend(loc='outside left',ncol=1, fancybox=True,fontsize=13,frameon=False,numpoints=1)
ax1.legend(loc='best', fancybox=True, ncol=2, fontsize =8,frameon=True)
#ax1.invert_yaxis()

ax2.set_xlabel('Time since explosion [days]')
#ax2.grid()
#ax2.invert_yaxis()
ax2.yaxis.set_minor_locator(AutoMinorLocator(10))
ax2.xaxis.set_minor_locator(AutoMinorLocator(5))
ax2.xaxis.set_tick_params(width=1.5)
ax2.yaxis.set_tick_params(width=1.5)
#plt.annotate('V', xy=(0.85, 0.85), color='black', xycoords='axes fraction')

# plt.subplot(223)
# plt.xlabel('Time [days]')
# ax3.grid()
# ax3.yaxis.set_minor_locator(AutoMinorLocator(10))
# ax3.xaxis.set_minor_locator(AutoMinorLocator(10))
# ax3.xaxis.set_tick_params(width=1.5)
# ax3.yaxis.set_tick_params(width=1.5)
# plt.yticks(np.arange(-18, -14, 1))
# ax3.invert_yaxis()
# plt.annotate('i/I', xy=(0.85, 0.85), color='black', xycoords='axes fraction')
plt.tight_layout()
plt.subplots_adjust(hspace=0, wspace=0.1)
plt.show()

