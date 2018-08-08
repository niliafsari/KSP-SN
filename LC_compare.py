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
matplotlib.rcParams.update({'font.size': 16})

band="B"
marker = itertools.cycle(('8', 'p','>','^','v','d','s', 'o','h','<'))
colors = itertools.cycle(("olive","yellow","salmon","green","m","sienna","gray","blue",
                          "darkkhaki","peru","gold","deepskyblue","black"))
with open("logs/sn_names.txt") as f:
    file_names = f.readlines()

file_names = [line.rstrip('\n') for line in file_names]
files_count=len(file_names)

# ax = plt.subplot(132)
# mag=np.load("phot_csv/compiledSN_"+band+"_"+"kspn2188"+".npy")
# ax.plot(mag[:,0],mag[:,3],linestyle = '',marker='*')
# ax.invert_yaxis()

ax1 = plt.subplot(221)
ax2 = plt.subplot(222)
ax3 = plt.subplot(223)
for i,sn_name in enumerate(file_names):
    print sn_name
    if sn_name!='KSPN2188_v1':
        mark=marker.next()
        col=colors.next()
    magB=np.load("phot_csv/compiledSN_"+"B"+"_"+sn_name+".npy")
    magB=magB.astype(np.float)
    u=np.argmin(magB[:, 3])
    print magB[:, 0]
    if sn_name=='KSPN2188_v1':
        ax1.plot(magB[:, 0] - magB[0, 0], magB[:, 3], linestyle='', markersize=11, marker=(5, 1), color='red', label='KSP-SN-2016kf',markeredgewidth=1, markeredgecolor='black')
    # elif sn_name == 'SN1999em':
    #     magB = np.genfromtxt('1999em_B.csv', delimiter=",")
    #     ax1.plot(magB[:, 0] , -1*magB[:, 1], linestyle='', marker=mark, color=col,label=sn_name)
    else:
        ax1.plot(magB[:,0]-magB[0,0],magB[:,3], linestyle = '', markersize=5, marker=mark,color=col,label=sn_name,markeredgewidth=0.5, markeredgecolor='black')
    ax1.set_xlim([-30, 250])
    ax1.set_ylim([-18, -11.5])
    magV=np.load("phot_csv/compiledSN_"+"V"+"_"+sn_name+".npy")
    magV=magV.astype(np.float)
    u = np.argmin(magV[:, 3])
    if sn_name=='SN2014cx':
        cx_t=magV[:,0]
        cx_m=magV[:,1]
    if sn_name=='KSPN2188_v1':
        ax2.plot(magV[:,0]-magV[0,0],magV[:,3], linestyle = '', markersize=11, marker=(5, 1), color='red',label='KSP-SN-2016kf',markeredgewidth=1, markeredgecolor='black')
    # elif sn_name == 'SN1999em':
    #     magV= np.genfromtxt('1999em_V.csv', delimiter=",")
    #     ax2.plot(magV[:, 0], -1 * magV[:, 1], linestyle='', marker=mark, color=col, label=sn_name)
    elif sn_name=='SN2005cs':
        ax2.plot(magV[:,0]-magV[u,0],magV[:,3], linestyle = '', markersize=5, marker=mark,color=col,label=sn_name,markeredgewidth=0.5, markeredgecolor='black')
    else:
        ax2.plot(magV[:,0]-magV[0,0],magV[:,3], linestyle = '', markersize=5, marker=mark,color=col,label=sn_name,markeredgewidth=0.5, markeredgecolor='black')
    ax2.set_xlim([-30, 250])
    ax2.set_ylim([-18, -13])
    magI=np.load("phot_csv/compiledSN_"+"I"+"_"+sn_name+".npy")
    magI=magI.astype(np.float)
    if magI.size>0:
        if sn_name == 'KSPN2188_v1':
            ind = np.where(( magI[:,3]< -16.2) & ((magI[:,0]-magI[0,0]) > 125))
            mag_abs = np.delete(magI[:,3], ind, 0)
            tt = np.delete(magI[:,0]-magI[0,0], ind, 0)
            ax3.plot(tt,mag_abs, linestyle = '', markersize=11,marker=(5, 1), color='red',label='KSP-SN-2016kf',markeredgewidth=1, markeredgecolor='black')
        # elif sn_name == 'SN1999em':
        #     magI = np.genfromtxt('1999em_I.csv', delimiter=",")
        #     ax3.plot(magI[:, 0], -1 * magI[:, 1], linestyle='', marker=mark, color=col, label=sn_name)
        else:
            ax3.plot(magI[:, 0] - magI[0, 0], magI[:, 3], linestyle='', markersize=5, marker=mark, color=col, label=sn_name,markeredgewidth=0.5, markeredgecolor='black')
        ax3.set_xlim([-30, 250])
        ax3.set_ylim([-18, -14])

plt.subplot(221)
label=ax1.set_ylabel('Absolute Magnitude')
ax1.yaxis.set_label_coords(-0.22, 0)
ax1.yaxis.set_minor_locator(AutoMinorLocator(10))
ax1.xaxis.set_minor_locator(AutoMinorLocator(10))
ax1.xaxis.set_tick_params(width=1.5)
ax1.yaxis.set_tick_params(width=1.5)
ax1.xaxis.set_ticklabels([])
plt.annotate('B', xy=(0.85, 0.85), color='black', xycoords='axes fraction')

#ax2.legend(loc='outside left',ncol=1, fancybox=True,fontsize=13,frameon=False,numpoints=1)
ax2.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2),
          fancybox=True, ncol=1, fontsize =11)
ax1.invert_yaxis()
plt.subplot(222)
ax2.grid()
ax2.invert_yaxis()
ax2.yaxis.set_minor_locator(AutoMinorLocator(10))
ax2.xaxis.set_minor_locator(AutoMinorLocator(10))
ax2.xaxis.set_tick_params(width=1.5)
ax2.yaxis.set_tick_params(width=1.5)
plt.annotate('V', xy=(0.85, 0.85), color='black', xycoords='axes fraction')

plt.subplot(223)
ax3.grid()
ax3.yaxis.set_minor_locator(AutoMinorLocator(10))
ax3.xaxis.set_minor_locator(AutoMinorLocator(10))
ax3.xaxis.set_tick_params(width=1.5)
ax3.yaxis.set_tick_params(width=1.5)
label=ax3.set_xlabel('Time [days]')
ax3.xaxis.set_label_coords(1, -0.21)
ax1.grid()
plt.yticks(np.arange(-18, -14, 1))
ax3.invert_yaxis()
plt.annotate('i/I', xy=(0.85, 0.85), color='black', xycoords='axes fraction')
plt.tight_layout()
plt.subplots_adjust(hspace=0, wspace=0.2)
#plt.savefig(current_path+'/plots/p_comp.pdf')
#plt.show()
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(8, 6.6, forward=True)
fig.savefig(current_path+'/plots/p_comp.pdf')
#plt.savefig(current_path+'/plots/p_comp.pdf')

