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
matplotlib.rcParams.update({'font.size': 20})

marker = itertools.cycle(('8', 'p','>','^','v','<','s', 'o','h','<'))
colors = itertools.cycle(("black","gold","darkgray","green","m","sienna","salmon","blue",
                          "darkkhaki","peru","yellow","deepskyblue","olive"))
with open("logs/sn_names_color.txt") as f:
    file_names = f.readlines()

file_names = [line.rstrip('\n') for line in file_names]
files_count=len(file_names)

# ax = plt.subplot(132)
# mag=np.load("phot_csv/compiledSN_"+band+"_"+"kspn2188"+".npy")
# ax.plot(mag[:,0],mag[:,3],linestyle = '',marker='*')
# ax.invert_yaxis()
if 0:
    ax1 = plt.subplot(311)
    ax2 = plt.subplot(312)
    ax3 = plt.subplot(313)
else :
    ax1 = plt.subplot(211)
    ax2 = plt.subplot(212)
dict1={'SN1999em':51475.87,'SN1987A':46849,'SN2014cx':56901.89,'SN2016esw':57607.83,'SN2013fs':56571.12,'KSPN2188_v1':358.867-0.12, 'SN2012aw':56002,'SN2005cs':53548.5}
#dict1={'SN2014cx':56901.89}
file_names=['SN2014cx','SN1999em','SN2016esw','SN2013fs','SN2005cs','KSPN2188_v1']
#file_names=['SN2005cs']
bands=['B','V','I']
marker = itertools.cycle(('<', '*','>','^','v','o','s', 'x','h','<','p'))
colors = itertools.cycle(('blue','green', 'purple',"gold","salmon","red","orange","sienna","black","gray","sienna",
                          "darkkhaki","peru","gold","deepskyblue","olive"))
for k,sn_name in enumerate(file_names):
    mark =marker.next()
    color=colors.next()
    magB=np.load("phot_csv/compiledSN_"+bands[0]+"_"+sn_name+".npy")
    magB = magB.astype(np.float)
    magB[:,0]=magB[:, 0] - dict1[sn_name]
    magV=np.load("phot_csv/compiledSN_"+bands[1]+"_"+sn_name+".npy")
    magV = magV.astype(np.float)
    magV[:,0]=magV[:, 0] - dict1[sn_name]
    magI=np.load("phot_csv/compiledSN_"+bands[2]+"_"+sn_name+".npy")
    magI = magI.astype(np.float)
    magI[:,0]=magI[:, 0] - dict1[sn_name]
    # mark =marker.next()
    # color=colors.next()
    if 0:
        ax3.errorbar(magB[:, 0], magB[:, 3], yerr=magB[:, 2], fmt=mark, color=color)
        mark = marker.next()
        color = colors.next()
        ax3.errorbar(magV[:, 0], magV[:, 3], yerr=magV[:, 2], fmt=mark, color=color)
        mark =marker.next()
        color=colors.next()
        ax3.errorbar(magI[:, 0], magI[:, 3], yerr=magI[:, 2], fmt=mark, color=color)
    u_t = magB[:, 0]
    index=np.argsort(u_t)
    u_t=u_t[index]
    u = magB[:, 3]
    u=u[index]
    u_e = magB[:, 4]
    u_e=u_e[index]
    v_t = magV[:, 0]
    index=np.argsort(v_t)
    v_t=v_t[index]
    v = magV[:, 3]
    v=v[index]
    v_e = magV[:, 4]
    v_e=v_e[index]
    i_t = magI[:, 0]
    index=np.argsort(i_t)
    i_t=i_t[index]
    i = magI[:, 3]
    i=i[index]
    i_e = magI[:, 4]
    i_e=i_e[index]
    bv_t = np.zeros(shape=(0, 1))
    bv = np.zeros(shape=(0, 1))
    bv_e = np.zeros(shape=(0, 1))
    if sn_name=='SN2005cs':
        dist=0.02
    else:
        dist=0.1
    for index,j in enumerate(u_t):
        if np.min(np.abs(v_t-j))<=dist:
            sub = np.argmin(np.abs(v_t - j))
            bv_t=np.concatenate((bv_t,v_t[sub].reshape((1,1))))
            bv=np.concatenate((bv,u[index]-v[sub].reshape((1,1))))
            bv_e=np.concatenate((bv_e,np.sqrt(np.square(v_e[sub].reshape((1,1)))+np.square(u_e[index].reshape((1,1))))))
    print bv
    vi_t = np.zeros(shape=(0, 1))
    vi = np.zeros(shape=(0, 1))
    vi_e = np.zeros(shape=(0, 1))
    for index, j in enumerate(v_t):
        if np.min(np.abs(i_t - j)) <= dist:
            sub = np.argmin(np.abs(i_t - j))
            vi_t = np.concatenate((vi_t, i_t[sub].reshape((1, 1))))
            vi = np.concatenate((vi, v[index] - i[sub].reshape((1, 1))))
            vi_e = np.concatenate((vi_e, np.sqrt(np.square(i_e[sub].reshape((1, 1))) + np.square(v_e[index].reshape((1, 1))))))
    if sn_name=='KSPN2188_v1':
        sn_name = 'KSPN2188'
    ax1.errorbar(bv_t, bv, yerr=bv_e, fmt=mark, color=color, markersize=5,
                 label=sn_name, markeredgewidth=0.5, markeredgecolor='black',linestyle='-')
    ax2.errorbar(vi_t, vi, yerr=vi_e, fmt=mark, color=color, markersize=5,
                 label=sn_name, markeredgewidth=0.5, markeredgecolor='black',linestyle='-')

# color=colors.next()
# mag=np.load("phot_csv/model.npy")
# ax1.plot(mag[:,0],mag[:,1],lw=3,label='model w/o CSM',color=color)
# ax2.plot(mag[:,0],mag[:,2],lw=3,label='model w/o CSM',color=color)
#
# color=colors.next()
# mag=np.load("phot_csv/model_csm.npy")
# ax1.plot(mag[:,0],mag[:,1],lw=3,label='model w/ CSM',color=color)
# ax2.plot(mag[:,0],mag[:,2],lw=3,label='model w/ CSM',color=color)
#ax3.invert_yaxis()
# plt.show()

label=ax1.set_ylabel('B-V')
label=ax2.set_ylabel('V-i/I')
ax2.yaxis.set_label_coords(-0.16, 0.5)
ax1.yaxis.set_label_coords(-0.16, 0.5)
# #ax1.grid()
# # plt.yticks([0,1,2])
# ax1.set_xlim([0, 120])
# ax1.set_ylim([-0.4,  1.8])
# # #
# ax2.set_xlim([0, 120])
# # ax3.set_xlim([0, 100])
# ax2.set_ylim([-0.5, 1.7])

ax1.set_xlim([0, 5])
ax1.set_ylim([-0.4,  0.75])
# #
ax2.set_xlim([0, 5])
# ax3.set_xlim([0, 100])
ax2.set_ylim([-0.5, 0.5])

ax1.legend(loc='best',ncol=2, fancybox=True,fontsize=11,frameon=True,numpoints=1,columnspacing=0.2)
ax1.yaxis.set_minor_locator(AutoMinorLocator(5))
ax1.xaxis.set_minor_locator(AutoMinorLocator(10))
ax1.xaxis.set_tick_params(width=1.5)
ax1.yaxis.set_tick_params(width=1.5)
ax1.xaxis.set_ticklabels([])



ax2.set_xlabel('Time since SBO [days]')
ax2.yaxis.set_minor_locator(AutoMinorLocator(5))
ax2.xaxis.set_minor_locator(AutoMinorLocator(5))
ax2.xaxis.set_tick_params(width=1.5)
ax2.yaxis.set_tick_params(width=1.5)

plt.tight_layout()
plt.subplots_adjust(hspace=0, wspace=0.1)
plt.show()

