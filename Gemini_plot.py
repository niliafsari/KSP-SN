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
matplotlib.rcParams.update({'font.size': 18})
coef = {'B': 3.626, 'V': 2.742, 'I': 1.505, 'i': 1.698}
coef = {'B': 4.315, 'V': 3.315, 'I': 1.940, 'i': 2.086}
data_B = np.genfromtxt(current_path+ '/phot_csv/N2188-B_v12_edit.csv', delimiter=',')
data_V = np.genfromtxt(current_path+'/phot_csv/N2188-V_v12_edit.csv', delimiter=',')
data_I = np.genfromtxt(current_path+'/phot_csv/N2188-I_v12_edit.csv', delimiter=',')


# ax = plt.subplot(111)
# plt.errorbar(data_B[:,4][(data_B[:,9] < data_B[:,11])],data_B[:,9][(data_B[:,9] < data_B[:,11])],yerr=data_B[:,10][(data_B[:,9] < data_B[:,11])]/5,color='blue',label='B',fmt='o')
# #plt.scatter(data_B[:,4][(data_B[:,9] > data_B[:,11])& (data_B[:,4]<723.5)],data_B[:,11][(data_B[:,9] > data_B[:,11])& (data_B[:,4]<723.5)],color='b', marker='D',label='B no detection')
# plt.errorbar(data_V[:,4][(data_V[:,9] < data_V[:,11])],data_V[:,9][(data_V[:,9] < data_V[:,11])],yerr=data_V[:,10][(data_V[:,9] < data_V[:,11])]/5,color='green',label='V',fmt='o')
# #plt.scatter(data_V[:,4][(data_V[:,9] > data_V[:,11])& (data_V[:,4]<723.5)],data_V[:,11][(data_V[:,9] > data_V[:,11])& (data_V[:,4]<723.5)],color='green', marker='D',label='V no detection')
# plt.errorbar(data_I[:,4][(data_I[:,9] < data_I[:,11])],data_I[:,9][(data_I[:,9] < data_I[:,11])],yerr=data_I[:,10][(data_I[:,9] < data_I[:,11])]/5,color='red',label='V',fmt='o')
# #plt.scatter(data_I[:,4][(data_I[:,9] > data_I[:,11])& (data_I[:,4]<723.5)],data_I[:,11][(data_I[:,9] > data_I[:,11])& (data_I[:,4]<723.5)],color='red', marker='D',label='V no detection')
# plt.axis([720-365,855-365,18,22])
#
# plt.ylabel('mag')
# ax.legend(loc='best',ncol=3, fancybox=True,fontsize=12)
# ax.invert_yaxis()


# ax = plt.subplot(312)
# plt.scatter(data_B[:,4],data_B[:,9],color='blue',label='B ',marker='o')
# plt.scatter(data_B[:,4],data_B[:,11],color='lightsteelblue', marker='.',label='B lim')
# plt.scatter(data_V[:,4],data_V[:,9],color='green',label='V ',marker='o')
# plt.scatter(data_V[:,4],data_V[:,11],color='lightgreen', marker='.',label='V lim')
# plt.scatter(data_I[:,4],data_I[:,9],color='red',label='V ',marker='o')
# plt.scatter(data_I[:,4],data_I[:,11],color='lightpink', marker='.',label='V lim')
#
# x=np.arange(650-365,855-365,0.5)
# y=(1+np.cos(2*np.pi*(x-742.881+365)/29.5306))/2
# ax.fill_between(x, 15,27, where= (y>0.8), facecolor='silver',alpha=0.5)
#
#
# plt.axis([650,855,15,27])
# plt.xlabel('time [days]')
# plt.ylabel('mag')
# ax.legend(loc='best',ncol=6, fancybox=True,fontsize=12)
# ax.invert_yaxis()
#



# ax = plt.subplot(312)
#
#
# plt.errorbar(data_B[:,4][(data_B[:,9] < data_B[:,11])],data_B[:,12][(data_B[:,9] < data_B[:,11])],yerr=data_B[:,13][(data_B[:,9] < data_B[:,11])]/5,color='blue',label='B mag',fmt='o')
# plt.errorbar(data_V[:,4][(data_V[:,9] < data_V[:,11])],data_V[:,12][(data_V[:,9] < data_V[:,11])],yerr=data_V[:,13][(data_V[:,9] < data_V[:,11])]/5,color='green',label='V mag',fmt='o')
# plt.errorbar(data_I[:,4][(data_I[:,9] < data_I[:,11])],data_I[:,12][(data_I[:,9] < data_I[:,11])],yerr=data_I[:,13][(data_I[:,9] < data_I[:,11])]/5,color='red',label='I mag',fmt='o')
# plt.axis([720-365,860-365,-18,-14])
# plt.gca().invert_yaxis()
#
# plt.ylabel('Absolute Mag')
# ax.legend(loc='best',ncol=3, fancybox=True,fontsize=12)

#for n in names[(M.T>Mlim.T) & (time.T>720)]:
#    findSN(n.replace('.nh.magcalc.cat','.nh.fits'),1,'/home/afsari/PycharmProjects/kspSN/corrupted/mgtmlim/')

#for n in names[(M.T<Mlim.T) & (time.T>720) &  (M.T<18.5)]:
#    findSN(n.replace('.nh.magcalc.cat', '.nh.fits'), 1, '/home/afsari/PycharmProjects/kspSN/corrupted/cantopen/')

#plt.tick_params(labelsize=20)


bin_factor = 2

data_Btobin = data_B[(data_B[:, 9] <= data_B[:, 11]) & (data_B[:, 4] >= 363)]
data_Bnobin = data_B[(data_B[:, 9] <= data_B[:, 11]) & (data_B[:, 4] < 363)]


data_Vtobin = data_V[(data_V[:, 9] <= data_V[:, 11]) & (data_V[:, 4] >= 363)]
data_Vnobin = data_V[(data_V[:, 9] <= data_V[:, 11]) & (data_V[:, 4] < 363)]

data_Itobin = data_I[(data_I[:, 9] <= data_I[:, 11]) & (data_I[:, 4] >= 363)]
data_Inobin = data_I[(data_I[:, 9] <= data_I[:, 11]) & (data_I[:, 4] < 363)]

fluxes = [1564, 4023, 3562, 2814, 2282]
fluxes = np.array([4023.0* 1000000.0, 3562.0 * 1000000.0, 2282.0 * 1000000.0])
binnedB=np.zeros(shape=(0,4))
binnedV=np.zeros(shape=(0,4))
binnedI=np.zeros(shape=(0,4))
t = 356
i_b = 1
i_v = 1
i_i = 1
print np.max(data_Itobin[:, 4])
while t <= (np.max(data_Itobin[:, 4])+bin_factor):
    dat = data_Btobin[(data_Btobin[:, 4] >= t) & (data_Btobin[:,4]< (t + bin_factor))]
    if dat.size != 0:
        I = dat[:, 7]
        time = np.mean(dat[:, 4])
        I_err = np.multiply(dat[:,10],I) * np.log(10) / 2.512
        I = np.mean(I)
        I_e = np.sqrt(np.sum(np.square(I_err))) / I_err.size
        mo = -2.512 * np.log10(I / fluxes[0])
        m_err = (2.512 / np.log(10)) * (I_e / I)
        binnedB=np.append(binnedB,np.array([time, I, mo, m_err]).reshape((1,4)),0)
    dat = data_Vtobin[(data_Vtobin[:, 4] >= t) & (data_Vtobin[:,4]< (t + bin_factor))]
    if dat.size != 0:
        I = dat[:, 7]
        time = np.mean(dat[:, 4])
        I_err = np.multiply(dat[:,10],I) * np.log(10) / 2.512
        I = np.mean(I)
        I_e = np.sqrt(np.sum(np.square(I_err))) / I_err.size
        mo = -2.512 * np.log10(I / fluxes[1])
        m_err = (2.512 / np.log(10)) * (I_e / I)
        binnedV=np.append(binnedV,np.array([time, I, mo, m_err]).reshape((1,4)),0)
    dat = data_Itobin[(data_Itobin[:, 4] >= t) & (data_Itobin[:,4]< (t + bin_factor))]
    if dat.size != 0:
        I = dat[:, 7]
        time = np.mean(dat[:, 4])
        I_err = np.multiply(dat[:,10],I) * np.log(10) / 2.512
        I = np.mean(I)
        I_e = np.sqrt(np.sum(np.square(I_err))) / I_err.size
        mo = -2.512 * np.log10(I / fluxes[2])
        m_err = (2.512 / np.log(10)) * (I_e / I)
        binnedI=np.append(binnedI,np.array([time, I, mo, m_err]).reshape((1,4)),0)
    t = t + bin_factor

ax1 = plt.subplot(111)
# plt.errorbar(data_Bnobin[:,4],data_Bnobin[:,9],yerr=data_Bnobin[:,10],color='blue',fmt='o')
# plt.errorbar(data_Vnobin[:,4],data_Vnobin[:,9],yerr=data_Vnobin[:,10],color='green',fmt='o')
# plt.errorbar(data_Inobin[:,4],data_Inobin[:,9],yerr=data_Inobin[:,10],color='red',fmt='o')
#
# plt.errorbar(binnedB[:,0],binnedB[:,2],yerr=binnedB[:,3],color='blue',label='B mag',fmt='o')
# plt.errorbar(binnedV[:,0],binnedV[:,2],yerr=binnedV[:,3],color='green',label='V mag',fmt='o')
# plt.errorbar(binnedI[:,0],binnedI[:,2],yerr=binnedI[:,3],color='red',label='I mag',fmt='o')

sn_name='KSPN2188_v1'
magB = np.load("phot_csv/compiledSN_" + "B" + "_" + sn_name + ".npy")
magB = magB.astype(np.float)
u = np.argmin(magB[:, 3])
ax1.errorbar(magB[:, 0] - magB[0, 0], magB[:, 3]+1, yerr= magB[:, 4], color='blue', label='B-band+1',fmt='o',markersize=10,markeredgecolor='black',
             markeredgewidth=1.2)
ax1.set_xlim([-10, 150])
ax1.set_ylim([-19.5, -14])
magV = np.load("phot_csv/compiledSN_" + "V" + "_" + sn_name + ".npy")
magV = magV.astype(np.float)
ax1.errorbar(magV[:, 0] - magV[0, 0], magV[:, 3],yerr=magV[:,4], color='green', label='V-band',fmt='o',markersize=10,markeredgecolor='black',
             markeredgewidth=1.2)
magI = np.load("phot_csv/compiledSN_" + "I" + "_" + sn_name + ".npy")
magI = magI.astype(np.float)
ax1.errorbar(magI[:, 0] - magI[0, 0], magI[:, 3]-1, yerr=magI[:, 4], color='red', label='I-band-1',fmt='o',markersize=10,markeredgecolor='black',
             markeredgewidth=1.2)
# filename='s14.6_ni56_5_efin_1.36E+51'
# offset=2
# files_path = '/home/afsari/gpc_SNEC/'
# os.chdir(files_path)
# output_path = filename + '/output/magnitudes.dat'
# output_out = filename + '/output/magnitudes_output.dat'
# output_info = filename + '/output/info.dat'
# try:
#     fr = open(output_path, 'r')
#     fw = open(output_out, 'w')
#     for line in fr:
#         fw.write(' '.join(line.split()) + '\n')
#     fr.close()
#     fw.close()
#     mags = np.genfromtxt(output_out, delimiter=' ')
# except:
#     print "error"
# output_info = filename + '/output/info.dat'
# f_info = open(output_info, 'r')
# for line in f_info:
#     if 'Time of breakout' in line:
#         line = line.strip('Time of breakout =')
#         line = line.strip('seconds\n')
#         line = line.strip()
#         t_BO = float(line)
# mags[:, 0] = mags[:, 0] - t_BO
#
# ax1.plot(mags[:, 0] / 84000.0 - offset, mags[:, 9]+1, color='blue')
# ax1.plot(mags[:, 0] / 84000.0 - offset, mags[:, 10], color='green')
# ax1.plot(mags[:, 0] / 84000.0 - offset, mags[:, 12]-1, color='red')
#
# filename='s14.6_1020_K_9.00E+17'
# offset=1.5
# files_path = '/home/afsari/gpc_SNEC/'
# os.chdir(files_path)
# output_path = filename + '/output/magnitudes.dat'
# output_out = filename + '/output/magnitudes_output.dat'
# output_info = filename + '/output/info.dat'
# try:
#     fr = open(output_path, 'r')
#     fw = open(output_out, 'w')
#     for line in fr:
#         fw.write(' '.join(line.split()) + '\n')
#     fr.close()
#     fw.close()
#     mags = np.genfromtxt(output_out, delimiter=' ')
# except:
#     print "error"
# output_info = filename + '/output/info.dat'
# f_info = open(output_info, 'r')
# for line in f_info:
#     if 'Time of breakout' in line:
#         line = line.strip('Time of breakout =')
#         line = line.strip('seconds\n')
#         line = line.strip()
#         t_BO = float(line)
# mags[:, 0] = mags[:, 0] - t_BO
#
# ax1.plot(mags[:, 0] / 84000.0 - offset, mags[:, 9]+1, color='blue',linestyle='--', linewidth=2)
# ax1.plot(mags[:, 0] / 84000.0 - offset, mags[:, 10], color='green',linestyle='--', linewidth=2)
# ax1.plot(mags[:, 0] / 84000.0 - offset, mags[:, 12]-1, color='red',linestyle='--', linewidth=2)

#plt.axis([720-365,860-365,18,23.2])

# y=np.arange(-20, -12, 0.5)
# ax1.fill_betweenx(y,x1=92,x2=93, color='y',alpha=0.5,zorder=0)
# #ax1.text(92.5, -16.5, ' ', fontsize=13, rotation='vertical',multialignment='center',va='center')


plt.gca().invert_yaxis()
plt.xlabel('Time [days]')
plt.ylabel('Absolute Magnitude (Vega)')
ax1.legend(loc='best',ncol=1, fancybox=True,fontsize=14, frameon=False)
#ax1.spines[side].set_linewidth(size)
ax1.yaxis.set_minor_locator(AutoMinorLocator(10))
ax1.xaxis.set_minor_locator(AutoMinorLocator(10))
ax1.xaxis.set_tick_params(width=1.5)
ax1.yaxis.set_tick_params(width=1.5)
plt.annotate('KSP-OT-2016kf', xy=(0.07, 0.05), xycoords='axes fraction')
plt.show()
plt.savefig(current_path+'/plots/LC.png')

