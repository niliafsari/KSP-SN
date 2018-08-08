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
data_B = np.genfromtxt(current_path+ '/phot_csv/N2188-B_v12_edit.csv', delimiter=',')
data_V = np.genfromtxt(current_path+'/phot_csv/N2188-V_v12_edit.csv', delimiter=',')
data_I = np.genfromtxt(current_path+'/phot_csv/N2188-I_v12_edit.csv', delimiter=',')



bin_factor = 2

#data_Btobin = data_B[(data_B[:, 9] <= data_B[:, 11]) & (data_B[:, 4] >= 363)]
data_Bnobin = data_B[(data_B[:, 9] <= data_B[:, 11]) & (data_B[:, 4] < 500)]

limB=data_B[ (data_B[:, 4] <358.8672) & (data_B[:, 4] >350) ]
print np.shape(limB)
#data_Vtobin = data_V[(data_V[:, 9] <= data_V[:, 11]) & (data_V[:, 4] >= 363)]
data_Vnobin = data_V[(data_V[:, 9] <= data_V[:, 11]) & (data_V[:, 4] < 500)]
limV = data_V[(data_V[:, 4] < 358.8672) &  (data_V[:, 4] >350) ]
#data_Itobin = data_I[(data_I[:, 9] <= data_I[:, 11]) & (data_I[:, 4] >= 363)]
data_Inobin = data_I[(data_I[:, 9] <= data_I[:, 11]) & (data_I[:, 4] < 500)]
limI = data_I[(data_I[:, 4] < 358.8672) & (data_I[:, 4] >350)]
fluxes = [1564, 4023, 3562, 2814, 2282]
fluxes = np.array([4023.0* 1000000.0, 3562.0 * 1000000.0, 2282.0 * 1000000.0])
# binnedB=np.zeros(shape=(0,5))
# binnedV=np.zeros(shape=(0,5))
# binnedI=np.zeros(shape=(0,5))
# t = 356
# i_b = 1
# i_v = 1
# i_i = 1
# print np.max(data_Itobin[:, 4])
# while t <= (np.max(data_Itobin[:, 4])+bin_factor):
#     dat = data_Btobin[(data_Btobin[:, 4] >= t) & (data_Btobin[:,4]< (t + bin_factor))]
#     if dat.size != 0:
#         I = dat[:, 7]
#         time = np.mean(dat[:, 4])
#         I_err = np.multiply(dat[:,10],I) * np.log(10) / 2.512
#         I = np.mean(I)
#         I_e = np.sqrt(np.sum(np.square(I_err))) / I_err.size
#         mo = -2.512 * np.log10(I / fluxes[0])
#         m_err = (2.512 / np.log(10)) * (I_e / I)
#         binnedB=np.append(binnedB,np.array([time, I, mo, m_err,dat[:, 2]]).reshape((1,5)),0)
#     dat = data_Vtobin[(data_Vtobin[:, 4] >= t) & (data_Vtobin[:,4]< (t + bin_factor))]
#     if dat.size != 0:
#         I = dat[:, 7]
#         time = np.mean(dat[:, 4])
#         I_err = np.multiply(dat[:,10],I) * np.log(10) / 2.512
#         I = np.mean(I)
#         I_e = np.sqrt(np.sum(np.square(I_err))) / I_err.size
#         mo = -2.512 * np.log10(I / fluxes[1])
#         m_err = (2.512 / np.log(10)) * (I_e / I)
#         binnedV=np.append(binnedV,np.array([time, I, mo, m_err,dat[:, 2]]).reshape((1,5)),0)
#     dat = data_Itobin[(data_Itobin[:, 4] >= t) & (data_Itobin[:,4]< (t + bin_factor))]
#     if dat.size != 0:
#         I = dat[:, 7]
#         time = np.mean(dat[:, 4])
#         I_err = np.multiply(dat[:,10],I) * np.log(10) / 2.512
#         I = np.mean(I)
#         I_e = np.sqrt(np.sum(np.square(I_err))) / I_err.size
#         mo = -2.512 * np.log10(I / fluxes[2])
#         m_err = (2.512 / np.log(10)) * (I_e / I)
#         binnedI=np.append(binnedI,np.array([time, I, mo, m_err,dat[:, 2]]).reshape((1,5)),0)
#     t = t + bin_factor

ax1 = plt.subplot(111)

ebv=0.0290
mag = np.zeros(shape=(0, 6))
for i,dat in enumerate(data_Bnobin[:,4]):
    add = np.concatenate(([data_Bnobin[i,4], deredMag(data_Bnobin[i,9], ebv, coef["B"]), data_Bnobin[i,10],data_Bnobin[i,2]],absMag(deredMag(data_Bnobin[i,9], ebv, coef["B"]), 0.043,data_Bnobin[i,10],0.002)))
    add = np.reshape(add, (1, 6))
    mag = np.concatenate((mag, add), axis=0)

# for i,dat in enumerate(binnedB[:,0]):
#     add = np.concatenate(([binnedB[i,0], deredMag(binnedB[i,2], ebv, coef["B"]), binnedB[i,3],binnedB[i,4]],
#                           absMag(deredMag(binnedB[i,2], ebv, coef["B"]), 0.043,binnedB[i,3],0.002)))
#     add = np.reshape(add, (1, 6))
#     mag = np.concatenate((mag, add), axis=0)
mag=mag[mag[:,0]>357]
magB=mag

mag = np.zeros(shape=(0, 6))
for i,dat in enumerate(data_Vnobin[:,4]):
    add = np.concatenate(([dat, deredMag(data_Vnobin[i,9], ebv, coef["V"]), data_Vnobin[i,10],data_Vnobin[i,2]],
                          absMag(deredMag(data_Vnobin[i,9], ebv, coef["V"]), 0.043,data_Vnobin[i,10],0.002)))
    add = np.reshape(add, (1, 6))
    mag = np.concatenate((mag, add), axis=0)

# for i,dat in enumerate(binnedV[:,0]):
#     add = np.concatenate(([binnedV[i,0],deredMag(binnedV[i,2], ebv, coef["V"]), binnedV[i,3],binnedV[i,4]],
#                           absMag(deredMag(binnedV[i,2], ebv, coef["V"]), 0.043,binnedV[i,3],0.002)))
#     add = np.reshape(add, (1, 6))
#     mag = np.concatenate((mag, add), axis=0)
mag=mag[mag[:,0]>357]

magV=mag

mag = np.zeros(shape=(0, 6))
for i,dat in enumerate(data_Inobin[:,4]):
    add = np.concatenate(([dat, deredMag(data_Inobin[i,9], ebv, coef["I"]), data_Inobin[i,10],data_Inobin[i,2]],
                          absMag(deredMag(data_Inobin[i,9], ebv, coef["I"]), 0.043,data_Inobin[i,10],0.002)))
    add = np.reshape(add, (1, 6))
    mag = np.concatenate((mag, add), axis=0)

# for i,dat in enumerate(binnedI[:,0]):
#     add = np.concatenate(([binnedI[i,0], deredMag(binnedI[i,2], ebv, coef["I"]), binnedI[i,3],binnedI[i,4]],
#                           absMag(deredMag(binnedI[i,2], ebv, coef["I"]), 0.043,binnedI[i,3],0.002)))
#     add = np.reshape(add, (1, 6))
#     mag = np.concatenate((mag, add), axis=0)
mag=mag[mag[:,0]>357]

magI=mag



u = np.min(magB[:, 0])-0.68
print u
ax1.errorbar(magB[:, 0][magB[:, 3]==0] - u, magB[:, 1][magB[:, 3]==0] +1, yerr= magB[:, 2][magB[:, 3]==0] , color='blue', label='B+1',fmt='o',markersize=6,markeredgecolor='black',
             markeredgewidth=1.2)
ax1.errorbar(magB[:, 0][magB[:, 3]==1] - u, magB[:, 1][magB[:, 3]==1] +1, yerr= magB[:, 2][magB[:, 3]==1] , color='blue',label='_nolegend_',fmt='d',markersize=6,markeredgecolor='black',
             markeredgewidth=1.2)
ax1.errorbar(magB[:, 0][magB[:, 3]==2] - u, magB[:, 1][magB[:, 3]==2] +1, yerr= magB[:, 2][magB[:, 3]==2] , color='blue',label='_nolegend_',fmt='s',markersize=6,markeredgecolor='black',
             markeredgewidth=1.2)
#ax1.scatter(limB[:, 4] - u, limB[:, 11]+1, color='blue',facecolors='none',label='_nolegend_',marker='v',s=18, lw=1.2)
#ax1.scatter(limB[:, 4] - u, limB[:, 9]+1, color='blue',facecolors='none',label='_nolegend_',marker='o',s=18, lw=1.2)

ax1.errorbar(magV[:, 0][magV[:, 3]==0] - u, magV[:, 1][magV[:, 3]==0], yerr= magV[:, 2][magV[:, 3]==0] , color='green', label='V',fmt='o',markersize=6,markeredgecolor='black',
             markeredgewidth=1.2)
ax1.errorbar(magV[:, 0][magV[:, 3]==1] - u, magV[:, 1][magV[:, 3]==1], yerr= magV[:, 2][magV[:, 3]==1] , color='green',label='_nolegend_',fmt='d',markersize=6,markeredgecolor='black',
             markeredgewidth=1.2)
ax1.errorbar(magV[:, 0][magV[:, 3]==2] - u, magV[:, 1][magV[:, 3]==2], yerr= magV[:, 2][magV[:, 3]==2] , color='green',label='_nolegend_',fmt='s',markersize=6,markeredgecolor='black',
             markeredgewidth=1.2)
#ax1.scatter(limV[:, 4] - u, limV[:, 11] , color='green',facecolors='none',label='_nolegend_',marker='v',s=18, lw=1.2)
#ax1.scatter(limV[:, 4] - u, limV[:, 9] , color='green',facecolors='none',label='_nolegend_',marker='o',s=18, lw=1.2)

magI=np.delete(magI[:],np.where(magI[:,1]<18.5),0)
magI=np.delete(magI[:],np.where((magI[:,1]>18.89) & ((magI[:, 0] - u)<72 ) & ((magI[:, 0] - u)>30)),0)

ax1.errorbar(magI[:, 0][magI[:, 3]==0] - u, magI[:, 1][magI[:, 3]==0] -1, yerr= magI[:, 2][magI[:, 3]==0] , color='red', label='I-1',fmt='o',markersize=6,markeredgecolor='black',
             markeredgewidth=1.2)
ax1.errorbar(magI[:, 0][magI[:, 3]==1] - u, magI[:, 1][magI[:, 3]==1] -1, yerr= magI[:, 2][magI[:, 3]==1] , color='red',label='_nolegend_',fmt='d',markersize=6,markeredgecolor='black',
             markeredgewidth=1.2)
ax1.errorbar(magI[:, 0][magI[:, 3]==2] - u, magI[:, 1][magI[:, 3]==2] -1, yerr= magI[:, 2][magI[:, 3]==2] , color='red',label='_nolegend_',fmt='s',markersize=6,markeredgecolor='black',
             markeredgewidth=1.2)
#ax1.scatter(limI[:, 4] - u, limI[:, 11]-1 , color='red',facecolors='none',label='_nolegend_',marker='v',s=18, lw=1.2)
y=np.arange(16, 28,0.2)
ax1.fill_betweenx(y,x1=93,x2=94, color='y',alpha=0.5,zorder=0)
ax1.axvline(x=0,color='k', linestyle='--',lw=0.8)
ax1.set_xlim([-10, 150])
ax1.set_ylim([17, 26])
plt.gca().invert_yaxis()
plt.tight_layout()
plt.xlabel('MJD-57746.18 [days]')
plt.ylabel('Apparent Magnitude')
ax1.legend(loc='lower right',ncol=1, fancybox=True,fontsize=14, frameon=False)
#ax1.spines[side].set_linewidth(size)
ax1.yaxis.set_minor_locator(AutoMinorLocator(10))
ax1.xaxis.set_minor_locator(AutoMinorLocator(10))
ax1.xaxis.set_tick_params(width=1.5)
ax1.yaxis.set_tick_params(width=1.5)

ax = inset_axes(ax1, width="45%", # width = 30% of parent_bbox
                    height=1.83, # height : 1 inch
                    loc=3,  bbox_to_anchor=(0.035, 0.03, 1, 1),
                   bbox_transform=ax1.transAxes)

ax.errorbar(magB[:, 0][(magB[:, 3]==0) ] - u, magB[:, 1][magB[:, 3]==0] +1, yerr= magB[:, 2][magB[:, 3]==0] , color='blue', label='B+1',fmt='o',markersize=6,markeredgecolor='black',
             markeredgewidth=1.2)
ax.errorbar(magB[:, 0][magB[:, 3]==1] - u, magB[:, 1][magB[:, 3]==1] +1, yerr= magB[:, 2][magB[:, 3]==1] , color='blue',label='_nolegend_',fmt='d',markersize=6,markeredgecolor='black',
             markeredgewidth=1.2)
ax.errorbar(magB[:, 0][magB[:, 3]==2] - u, magB[:, 1][magB[:, 3]==2] +1, yerr= magB[:, 2][magB[:, 3]==2] , color='blue',label='_nolegend_',fmt='s',markersize=6,markeredgecolor='black',
             markeredgewidth=1.2)
ax.scatter(limB[:, 4] - u, limB[:, 11]+1, color='blue',facecolors='none',label='_nolegend_',marker='v',s=18, lw=1.2)
#ax1.scatter(limB[:, 4] - u, limB[:, 9]+1, color='blue',facecolors='none',label='_nolegend_',marker='o',s=18, lw=1.2)

ax.errorbar(magV[:, 0][magV[:, 3]==0] - u, magV[:, 1][magV[:, 3]==0], yerr= magV[:, 2][magV[:, 3]==0] , color='green', label='V',fmt='o',markersize=6,markeredgecolor='black',
             markeredgewidth=1.2)
ax.errorbar(magV[:, 0][magV[:, 3]==1] - u, magV[:, 1][magV[:, 3]==1], yerr= magV[:, 2][magV[:, 3]==1] , color='green',label='_nolegend_',fmt='d',markersize=6,markeredgecolor='black',
             markeredgewidth=1.2)
ax.errorbar(magV[:, 0][magV[:, 3]==2] - u, magV[:, 1][magV[:, 3]==2], yerr= magV[:, 2][magV[:, 3]==2] , color='green',label='_nolegend_',fmt='s',markersize=6,markeredgecolor='black',
             markeredgewidth=1.2)
ax.scatter(limV[:, 4] - u, limV[:, 11] , color='green',facecolors='none',label='_nolegend_',marker='v',s=18, lw=1.2)
#ax1.scatter(limV[:, 4] - u, limV[:, 9] , color='green',facecolors='none',label='_nolegend_',marker='o',s=18, lw=1.2)


ax.errorbar(magI[:, 0][magI[:, 3]==0] - u, magI[:, 1][magI[:, 3]==0] -1, yerr= magI[:, 2][magI[:, 3]==0] , color='red', label='I-1',fmt='o',markersize=6,markeredgecolor='black',
             markeredgewidth=1.2)
ax.errorbar(magI[:, 0][magI[:, 3]==1] - u, magI[:, 1][magI[:, 3]==1] -1, yerr= magI[:, 2][magI[:, 3]==1] , color='red',label='_nolegend_',fmt='d',markersize=6,markeredgecolor='black',
             markeredgewidth=1.2)
ax.errorbar(magI[:, 0][magI[:, 3]==2] - u, magI[:, 1][magI[:, 3]==2] -1, yerr= magI[:, 2][magI[:, 3]==2] , color='red',label='_nolegend_',fmt='s',markersize=6,markeredgecolor='black',
             markeredgewidth=1.2)
ax.scatter(limI[:, 4] - u, limI[:, 11]-1 , color='red',facecolors='none',label='_nolegend_',marker='v',s=18, lw=1.2)
ax.axvline(x=0,color='k', linestyle='--',lw=0.8)
ax.set_xlim([-4, 4.5])
ax.set_ylim([17.6,22.5])
plt.xticks(np.arange(-4, 5, 1.0))
plt.gca().invert_yaxis()
# plt.xlabel('Time [days]')
# plt.ylabel('Absolute Magnitude')
# ax1.legend(loc='upper right',ncol=1, fancybox=True,fontsize=14, frameon=False)
#ax1.spines[side].set_linewidth(size)
ax.yaxis.set_minor_locator(AutoMinorLocator(10))
ax.xaxis.set_minor_locator(AutoMinorLocator(10))
ax.xaxis.set_tick_params(width=1.5)
ax.yaxis.set_tick_params(width=1.5)

for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
             ax.get_xticklabels() + ax.get_yticklabels()):
    item.set_fontsize(12)

# plt.annotate('i/I', xy=(0.85, 0.75), color='red', xycoords='axes fraction')
# plt.annotate('V', xy=(0.85, 0.45), color='green', xycoords='axes fraction')
# plt.annotate('B', xy=(0.85, 0.15), color='blue', xycoords='axes fraction')
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(9, 5.7, forward=True)
plt.tight_layout()
fig.savefig(current_path+'/plots/p_lc.pdf')
plt.show()

