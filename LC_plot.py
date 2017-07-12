import os
import glob
import subprocess
import commands
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from dophot import *
from findSN import *
from SNAP import Astrometry
from astropy.time import Time
from moon import *
import csv
current_path=os.path.dirname(os.path.abspath(__file__))
matplotlib.rcParams.update({'font.size': 18})

data_B = np.genfromtxt(current_path+ '/phot_csv/N2188-B_v2_edit.csv', delimiter=',')
data_V = np.genfromtxt(current_path+'/phot_csv/N2188-V_v2_edit.csv', delimiter=',')
data_I = np.genfromtxt(current_path+'/phot_csv/N2188-I_v2_edit.csv', delimiter=',')

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
plt.errorbar(data_B[:,4][(data_B[:,9] < data_B[:,11])],data_B[:,9][(data_B[:,9] < data_B[:,11])],yerr=data_B[:,10][(data_B[:,9] < data_B[:,11])],color='blue',label='B',fmt='o')
plt.scatter(data_B[:,4][(data_B[:,9] > data_B[:,11])& (data_B[:,4]<723.5)],data_B[:,11][(data_B[:,9] > data_B[:,11])& (data_B[:,4]<723.5)],color='b', marker='D',label='B no detection')
plt.errorbar(data_V[:,4][(data_V[:,9] < data_V[:,11])],data_V[:,9][(data_V[:,9] < data_V[:,11])],yerr=data_V[:,10][(data_V[:,9] < data_V[:,11])],color='green',label='V',fmt='o')
plt.scatter(data_V[:,4][(data_V[:,9] > data_V[:,11])& (data_V[:,4]<723.5)],data_V[:,11][(data_V[:,9] > data_V[:,11])& (data_V[:,4]<723.5)],color='green', marker='D',label='V no detection')
plt.errorbar(data_I[:,4][(data_I[:,9] < data_I[:,11])],data_I[:,9][(data_I[:,9] < data_I[:,11])],yerr=data_I[:,10][(data_I[:,9] < data_I[:,11])],color='red',label='V',fmt='o')
plt.scatter(data_I[:,4][(data_I[:,9] > data_I[:,11])& (data_I[:,4]<723.5)],data_I[:,11][(data_I[:,9] > data_I[:,11])& (data_I[:,4]<723.5)],color='red', marker='D',label='V no detection')
plt.axis([650,855,18,25])
plt.xlabel('time [days]')
plt.ylabel('mag')
ax.legend(loc='best',ncol=3, fancybox=True,fontsize=12)
ax.invert_yaxis()


ax = plt.subplot(312)
plt.scatter(data_B[:,4],data_B[:,9],color='blue',label='B ',marker='o')
plt.scatter(data_B[:,4],data_B[:,11],color='lightsteelblue', marker='.',label='B lim')
plt.scatter(data_V[:,4],data_V[:,9],color='green',label='V ',marker='o')
plt.scatter(data_V[:,4],data_V[:,11],color='lightgreen', marker='.',label='V lim')
plt.scatter(data_I[:,4],data_I[:,9],color='red',label='V ',marker='o')
plt.scatter(data_I[:,4],data_I[:,11],color='lightpink', marker='.',label='V lim')

x=np.arange(650,855,0.5)
y=(1+np.cos(2*np.pi*(x-742.881)/29.5306))/2
ax.fill_between(x, 15,27, where= (y>0.8), facecolor='silver',alpha=0.5)


plt.axis([650,855,15,27])
plt.xlabel('time [days]')
plt.ylabel('mag')
ax.legend(loc='best',ncol=6, fancybox=True,fontsize=12)
ax.invert_yaxis()




ax = plt.subplot(313)
# plt.scatter(x,y)
# x=np.arange(650,855,0.5)
# y=(1+np.cos(2*np.pi*(x-742.881)/29.5306))/2
# plt.scatter(x,y,color='r')
# theta=0.75
# ax.fill_between(x, 0,1, where=y > theta, facecolor='silver',alpha=0.5)



plt.errorbar(data_B[:,4][(data_B[:,9] < data_B[:,11])],data_B[:,13][(data_B[:,9] < data_B[:,11])],yerr=data_B[:,14][(data_B[:,9] < data_B[:,11])],color='blue',label='B mag',fmt='o')
plt.errorbar(data_V[:,4][(data_V[:,9] < data_V[:,11])],data_V[:,13][(data_V[:,9] < data_V[:,11])],yerr=data_V[:,14][(data_V[:,9] < data_V[:,11])],color='green',label='V mag',fmt='o')
plt.errorbar(data_I[:,4][(data_I[:,9] < data_I[:,11])],data_I[:,13][(data_I[:,9] < data_I[:,11])],yerr=data_I[:,14][(data_I[:,9] < data_I[:,11])],color='red',label='V mag',fmt='o')
plt.axis([720,860,-18,-14])
plt.gca().invert_yaxis()
plt.xlabel('time [days]')
plt.ylabel('Absolute Mag')
ax.legend(loc='best',ncol=3, fancybox=True,fontsize=12)

#for n in names[(M.T>Mlim.T) & (time.T>720)]:
#    findSN(n.replace('.nh.magcalc.cat','.nh.fits'),1,'/home/afsari/PycharmProjects/kspSN/corrupted/mgtmlim/')

#for n in names[(M.T<Mlim.T) & (time.T>720) &  (M.T<18.5)]:
#    findSN(n.replace('.nh.magcalc.cat', '.nh.fits'), 1, '/home/afsari/PycharmProjects/kspSN/corrupted/cantopen/')

plt.tick_params(labelsize=20)

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
