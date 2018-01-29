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

from SNAP import Astrometry
from SNAP.Analysis import *
current_path=os.path.dirname(os.path.abspath(__file__))
matplotlib.rcParams.update({'font.size': 18})
coef = {'B': 3.626, 'V': 2.742, 'I': 1.505, 'i': 1.698}
coef = {'B': 4.315, 'V': 3.315, 'I': 1.940, 'i': 2.086}
data_B = np.genfromtxt(current_path+ '/phot_csv/N2188-B_v11_edit.csv', delimiter=',')
data_V = np.genfromtxt(current_path+'/phot_csv/N2188-V_v11_edit.csv', delimiter=',')
data_I = np.genfromtxt(current_path+'/phot_csv/N2188-I_v11_edit.csv', delimiter=',')

# files=['N2188-B_v2_edit.csv','N2188-V_v2_edit.csv','N2188-I_v2_edit.csv']
# names=[]
# for fil in files:
#     data = np.genfromtxt(current_path + '/phot_csv/'+fil, delimiter=',')
#     my_file = open('phot_csv/'+fil, 'r')
#     reader = csv.reader(my_file, delimiter=',')
#     my_list = list(reader)
#     my_file.close()
#     mydict1 = {int(float(rows[3])):rows[0] for rows in my_list}
#     mydict2 = {int(float(rows[3])):rows[1] for rows in my_list}
#     mydict3 = {int(float(rows[3])):rows[2] for rows in my_list}
#     mydict_rev = {rows[0]:rows[3] for rows in my_list}
#
#     for dat in data[:,3][(data[:,9] < data[:,11]) & (data[:,4]<723.5)]:
#         names.append(mydict1[dat])
#
# for name in names:
#     findSN(name,1,'/home/afsari/PycharmProjects/kspSN/corrupted/preSNdet/')


ax = plt.subplot(311)
plt.errorbar(data_B[:,4][(data_B[:,9] < data_B[:,11])],data_B[:,9][(data_B[:,9] < data_B[:,11])],yerr=data_B[:,10][(data_B[:,9] < data_B[:,11])]/5,color='blue',label='B',fmt='v')
#plt.scatter(data_B[:,4][(data_B[:,9] > data_B[:,11])& (data_B[:,4]<723.5)],data_B[:,11][(data_B[:,9] > data_B[:,11])& (data_B[:,4]<723.5)],color='b', marker='D',label='B no detection')
plt.errorbar(data_V[:,4][(data_V[:,9] < data_V[:,11])],data_V[:,9][(data_V[:,9] < data_V[:,11])],yerr=data_V[:,10][(data_V[:,9] < data_V[:,11])]/5,color='green',label='V',fmt='<')
#plt.scatter(data_V[:,4][(data_V[:,9] > data_V[:,11])& (data_V[:,4]<723.5)],data_V[:,11][(data_V[:,9] > data_V[:,11])& (data_V[:,4]<723.5)],color='green', marker='D',label='V no detection')
plt.errorbar(data_I[:,4][(data_I[:,9] < data_I[:,11])],data_I[:,9][(data_I[:,9] < data_I[:,11])],yerr=data_I[:,10][(data_I[:,9] < data_I[:,11])]/5,color='red',label='V',fmt='^')
#plt.scatter(data_I[:,4][(data_I[:,9] > data_I[:,11])& (data_I[:,4]<723.5)],data_I[:,11][(data_I[:,9] > data_I[:,11])& (data_I[:,4]<723.5)],color='red', marker='D',label='V no detection')
plt.axis([720-365,855-365,18,23.2])

plt.ylabel('mag')
ax.legend(loc='best',ncol=3, fancybox=True,fontsize=12)
ax.invert_yaxis()


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



ax = plt.subplot(312)


plt.errorbar(data_B[:,4][(data_B[:,9] < data_B[:,11])],data_B[:,12][(data_B[:,9] < data_B[:,11])],yerr=data_B[:,13][(data_B[:,9] < data_B[:,11])]/5,color='blue',label='B mag',fmt='o')
plt.errorbar(data_V[:,4][(data_V[:,9] < data_V[:,11])],data_V[:,12][(data_V[:,9] < data_V[:,11])],yerr=data_V[:,13][(data_V[:,9] < data_V[:,11])]/5,color='green',label='V mag',fmt='o')
plt.errorbar(data_I[:,4][(data_I[:,9] < data_I[:,11])],data_I[:,12][(data_I[:,9] < data_I[:,11])],yerr=data_I[:,13][(data_I[:,9] < data_I[:,11])]/5,color='red',label='I mag',fmt='o')
plt.axis([720-365,860-365,-18,-14])
plt.gca().invert_yaxis()

plt.ylabel('Absolute Mag')
ax.legend(loc='best',ncol=3, fancybox=True,fontsize=12)

#for n in names[(M.T>Mlim.T) & (time.T>720)]:
#    findSN(n.replace('.nh.magcalc.cat','.nh.fits'),1,'/home/afsari/PycharmProjects/kspSN/corrupted/mgtmlim/')

#for n in names[(M.T<Mlim.T) & (time.T>720) &  (M.T<18.5)]:
#    findSN(n.replace('.nh.magcalc.cat', '.nh.fits'), 1, '/home/afsari/PycharmProjects/kspSN/corrupted/cantopen/')

plt.tick_params(labelsize=20)


bin_factor = 2

data_Btobin = data_B[(data_B[:, 9] <= data_B[:, 11]) & (data_B[:, 4] >= 363)]
data_Bnobin = data_B[(data_B[:, 9] <= data_B[:, 11]) & (data_B[:, 4] < 363)]


data_Vtobin = data_V[(data_V[:, 9] <= data_V[:, 11]) & (data_V[:, 4] >= 363)]
data_Vnobin = data_V[(data_V[:, 9] <= data_V[:, 11]) & (data_V[:, 4] < 363)]

data_Itobin = data_I[(data_I[:, 9] <= data_I[:, 11]) & (data_I[:, 4] >= 363)]
data_Inobin = data_I[(data_I[:, 9] <= data_I[:, 11]) & (data_I[:, 4] < 363)]

#fluxes = [1564, 4023, 3562, 2814, 2282]
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

ax = plt.subplot(313)
plt.errorbar(data_Bnobin[:,4],data_Bnobin[:,9],yerr=data_Bnobin[:,10]/5,color='blue',fmt='v')
plt.errorbar(data_Vnobin[:,4],data_Vnobin[:,9],yerr=data_Vnobin[:,10]/5,color='green',fmt='>')
plt.errorbar(data_Inobin[:,4],data_Inobin[:,9],yerr=data_Inobin[:,10]/5,color='red',fmt='^')

plt.errorbar(binnedB[:,0],binnedB[:,2],yerr=binnedB[:,3]/5,color='blue',label='B mag',fmt='v')
plt.errorbar(binnedV[:,0],binnedV[:,2],yerr=binnedV[:,3]/5,color='green',label='V mag',fmt='>')
plt.errorbar(binnedI[:,0],binnedI[:,2],yerr=binnedI[:,3]/5,color='red',label='I mag',fmt='^')
ebv=0.0290
mag = np.zeros(shape=(0, 5))
for i,dat in enumerate(data_Bnobin[:,4]):
    add = np.concatenate(([data_Bnobin[i,4], deredMag(data_Bnobin[i,9], ebv, coef["B"]), data_Bnobin[i,10]],absMag(deredMag(data_Bnobin[i,9], ebv, coef["B"]), 0.043,data_Bnobin[i,10],0.002)))
    add = np.reshape(add, (1, 5))
    mag = np.concatenate((mag, add), axis=0)

for i,dat in enumerate(binnedB[:,0]):
    add = np.concatenate(([binnedB[i,0], deredMag(binnedB[i,2], ebv, coef["B"]), binnedB[i,3]],
                          absMag(deredMag(binnedB[i,2], ebv, coef["B"]), 0.043,binnedB[i,3],0.002)))
    add = np.reshape(add, (1, 5))
    mag = np.concatenate((mag, add), axis=0)
mag=mag[mag[:,0]>357]
np.save("phot_csv/compiledSN_"+"B"+"_"+"KSPN2188"+".npy", mag)
np.savetxt("phot_csv/compiledSN_"+"B"+"_"+"KSPN2188"+".csv", mag)

mag = np.zeros(shape=(0, 5))
for i,dat in enumerate(data_Vnobin[:,4]):
    add = np.concatenate(([dat, deredMag(data_Vnobin[i,9], ebv, coef["V"]), data_Vnobin[i,10]],
                          absMag(deredMag(data_Vnobin[i,9], ebv, coef["V"]), 0.043,data_Vnobin[i,10],0.002)))
    add = np.reshape(add, (1, 5))
    mag = np.concatenate((mag, add), axis=0)

for i,dat in enumerate(binnedV[:,0]):
    add = np.concatenate(([binnedV[i,0],deredMag(binnedV[i,2], ebv, coef["V"]), binnedV[i,3]],
                          absMag(deredMag(binnedV[i,2], ebv, coef["V"]), 0.043,binnedV[i,3],0.002)))
    add = np.reshape(add, (1, 5))
    mag = np.concatenate((mag, add), axis=0)
mag=mag[mag[:,0]>357]
np.save("phot_csv/compiledSN_"+"V"+"_"+"KSPN2188"+".npy", mag)
np.savetxt("phot_csv/compiledSN_"+"V"+"_"+"KSPN2188"+".csv", mag)

mag = np.zeros(shape=(0, 5))
for i,dat in enumerate(data_Inobin[:,4]):
    add = np.concatenate(([dat, deredMag(data_Inobin[i,9], ebv, coef["I"]), data_Inobin[i,10]],
                          absMag(deredMag(data_Inobin[i,9], ebv, coef["I"]), 0.043,data_Inobin[i,10],0.002)))
    add = np.reshape(add, (1, 5))
    mag = np.concatenate((mag, add), axis=0)

for i,dat in enumerate(binnedI[:,0]):
    add = np.concatenate(([binnedI[i,0], deredMag(binnedI[i,2], ebv, coef["I"]), binnedI[i,3]],
                          absMag(deredMag(binnedI[i,2], ebv, coef["I"]), 0.043,binnedI[i,3],0.002)))
    add = np.reshape(add, (1, 5))
    mag = np.concatenate((mag, add), axis=0)
mag=mag[mag[:,0]>357]
np.save("phot_csv/compiledSN_"+"I"+"_"+"KSPN2188"+".npy", mag)
np.savetxt("phot_csv/compiledSN_"+"I"+"_"+"KSPN2188"+".csv", mag)

plt.axis([720-365,860-365,18,23.2])
plt.gca().invert_yaxis()
plt.xlabel('time [days]')
plt.ylabel('Binned LC')
ax.legend(loc='best',ncol=3, fancybox=True,fontsize=12)

plt.show()
plt.savefig(current_path+'/plots/LC.png')


#names=np.array([names])
#name= names[(M.T>17.4) & (M.T<17.75) & (time.T>689) & (time.T<692)]
#findSN(name[0].replace('.nh.magcalc.cat', '.nh.fits'), 1, '/home/afsari/PycharmProjects/kspSN/corrupted/')

# names=np.array([names])
# for n in names[(time.T>723.5) & (time.T<724)]:
#     print n.replace('nh.magcalc.cat','nh.fits')

# qb= np.percentile(M[(band == 0) & (M < Mlim) & (time>732)],2)
# qi= np.percentile(M[(band == 1) & (M < Mlim) & (time>732)],2)
# qv= np.percentile(M[(band == 2) & (M < Mlim) & (time>732)],2)
#
# names=np.array([names])
# name=names[(M.T < qb) & (M.T < Mlim.T)]
# print np.shape(name)
# for n in names[(band.T == 0) & (M.T < qb) & (M.T < Mlim.T) & (time.T>732)]:
#      print n.replace('nh.magcalc.cat','nh.fits')
#      findSN(n.replace('.nh.magcalc.cat', '.nh.fits'), 1, '/home/afsari/PycharmProjects/kspSN/corrupted/brightB/')
#
# for n in names[(band.T == 1) & (M.T<qi)& (M.T < Mlim.T)& (time.T>732)]:
#      print n.replace('nh.magcalc.cat','nh.fits')
#      findSN(n.replace('.nh.magcalc.cat', '.nh.fits'), 1, '/home/afsari/PycharmProjects/kspSN/corrupted/brightI/')
#
# for n in names[(band.T == 2) & (M.T<qv) & (M.T < Mlim.T)& (time.T>732)]:
#      print n.replace('nh.magcalc.cat','nh.fits')
#      findSN(n.replace('.nh.magcalc.cat', '.nh.fits'), 1, '/home/afsari/PycharmProjects/kspSN/corrupted/brightV/')
