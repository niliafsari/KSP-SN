import os
import glob
import subprocess
import commands
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from dophot import *
from findSN import *
import sys
sys.path.insert(0, '/home/afsari/')

from SNAP import Astrometry
from SNAP import Astrometry
from astropy.time import Time
from moon import *
import csv
current_path=os.path.dirname(os.path.abspath(__file__))
matplotlib.rcParams.update({'font.size': 18})


band='V'

files=['N2188-B_v2_edit.csv','N2188-V_v2_edit.csv','N2188-I_v2_edit.csv',
       'N2188-B_v11_edit.csv','N2188-V_v11_edit.csv','N2188-I_v11_edit.csv',
       'N2188-B_v10_edit.csv','N2188-V_v10_edit.csv','N2188-I_v10_edit.csv']
names=[]
for fil in files:
    data = np.genfromtxt(current_path + '/phot_csv/'+fil, delimiter=',')
    my_file = open('phot_csv/'+fil, 'r')
    reader = csv.reader(my_file, delimiter=',')
    my_list = list(reader)
    my_file.close()
    mydict1 = {int(float(rows[3])):rows[0] for rows in my_list}
    mydict2 = {int(float(rows[3])):rows[1] for rows in my_list}
    mydict3 = {int(float(rows[3])):rows[2] for rows in my_list}
    mydict_rev = {rows[0]:rows[3] for rows in my_list}
    i=0
    for l in my_list:
        if l[2]=='S':
            data[i,2]=0
        elif l[2]=='C':
            data[i,2]=1
        elif l[2]=='A':
            data[i,2]=2
        else:
            data[i,2]=-1
        i=i+1
        if fil==files[0]:
            data_B_v1=data
        elif fil==files[1]:
            data_V_v1 = data
        elif fil==files[2]:
            data_I_v1 = data
        elif fil == files[3]:
            data_B = data
        elif fil == files[4]:
            data_V = data
        elif fil == files[5]:
            data_I = data
        elif fil == files[6]:
            data_B_v3 = data
        elif fil == files[7]:
            data_V_v3 = data
        elif fil == files[8]:
            data_I_v3 = data

if band=='B':
    data_B_v1=data_B_v1
elif band=='V':
    data_B_v1=data_V_v1
elif band == 'I':
    data_B_v1 = data_I_v1
else:
    print "band doesn't exist"
data_B_v1[:,4]=data_B_v1[:,4]-365
ax = plt.subplot(311)
cond=((data_B_v1[:,9] < data_B_v1[:,11])& (data_B_v1[:,2]==0))
plt.errorbar(data_B_v1[:,4][cond],data_B_v1[:,9][cond],yerr=data_B_v1[:,10][cond],color='grey',label='S. Africa',fmt='v')
cond=((data_B_v1[:,9] < data_B_v1[:,11])& (data_B_v1[:,2]==1))
plt.errorbar(data_B_v1[:,4][cond],data_B_v1[:,9][cond],yerr=data_B_v1[:,10][cond],color='cyan',label='Chile',fmt='<')
cond=((data_B_v1[:,9] < data_B_v1[:,11])& (data_B_v1[:,2]==2))
plt.errorbar(data_B_v1[:,4][cond],data_B_v1[:,9][cond],yerr=data_B_v1[:,10][cond],color='yellow',label='Australia',fmt='^')

cond=((data_B_v1[:,9] < data_B_v1[:,11])& (data_B_v1[:,2]==0))
plt.scatter(data_B_v1[:,4][cond],data_B_v1[:,11][cond],color='grey', marker='.',label='lim S')
cond=((data_B_v1[:,9] < data_B_v1[:,11])& (data_B_v1[:,2]==1))
plt.scatter(data_B_v1[:,4][cond],data_B_v1[:,11][cond],color='cyan', marker='.',label='lim C')
cond=((data_B_v1[:,9] < data_B_v1[:,11])& (data_B_v1[:,2]==2))
plt.scatter(data_B_v1[:,4][cond],data_B_v1[:,11][cond],color='yellow', marker='.',label='lim A')
# plt.errorbar(data_V_v1[:,4][cond],data_V_v1[:,9][cond],yerr=data_V_v1[:,10][cond],color='green',label='V S. Africa',fmt='v')
# cond=((data_V_v1[:,9] < data_V_v1[:,11])& (data_V_v1[:,2]==1))
# plt.errorbar(data_V_v1[:,4][cond],data_V_v1[:,9][cond],yerr=data_V_v1[:,10][cond],color='green',label='V Chile',fmt='<')
# cond=((data_V_v1[:,9] < data_V_v1[:,11])& (data_V_v1[:,2]==2))
# plt.errorbar(data_V_v1[:,4][cond],data_V_v1[:,9][cond],yerr=data_V_v1[:,10][cond],color='green',label='V Australie',fmt='^')
# #plt.scatter(data_V_v1[:,4][(data_V_v1[:,9] > data_V_v1[:,11])& (data_V_v1[:,4]<723.5)],data_V_v1[:,11][(data_V_v1[:,9] > data_V_v1[:,11])& (data_V_v1[:,4]<723.5)],color='green', marker='D',label='V no detection')
# plt.scatter(data_V_v1[:,4],data_V_v1[:,11],color='lightgreen', marker='.',label='V lim')
#
# cond=((data_I_v1[:,9] < data_I_v1[:,11])& (data_I_v1[:,2]==0))
# plt.errorbar(data_I_v1[:,4][cond],data_I_v1[:,9][cond],yerr=data_I_v1[:,10][cond],color='red',label='I S. Africa ',fmt='v')
# cond=((data_I_v1[:,9] < data_I_v1[:,11])& (data_I_v1[:,2]==1))
# plt.errorbar(data_I_v1[:,4][cond],data_I_v1[:,9][cond],yerr=data_I_v1[:,10][cond],color='red',label='I Chile ',fmt='<')
# cond=((data_I_v1[:,9] < data_I_v1[:,11])& (data_I_v1[:,2]==2))
# plt.errorbar(data_I_v1[:,4][cond],data_I_v1[:,9][cond],yerr=data_I_v1[:,10][cond],color='red',label='I Australia ',fmt='^')
# # #plt.scatter(data_I_v1[:,4][(data_I_v1[:,9] > data_I_v1[:,11])& (data_I_v1[:,4]<723.5)],data_I_v1[:,11][(data_I_v1[:,9] > data_I_v1[:,11])& (data_I_v1[:,4]<723.5)],color='red', marker='D',label='V no detection')
# plt.scatter(data_I_v1[:,4],data_I_v1[:,11],color='lightpink', marker='.',label='V lim')
x=np.arange(650-365,870-365,0.5)
y=(1+np.cos(2*np.pi*(x-742.881+365)/29.5306))/2
ax.fill_between(x, 18,25, where= (y>0.8), facecolor='pink',alpha=0.5)


plt.axis([720-365,870-365,18,25])
#plt.xlabel('time [days]')
plt.ylabel('mag')

ax.legend(loc='best',ncol=6, fancybox=True,fontsize=12)
ax.invert_yaxis()

if band=='B':
    data_B_v1=data_B_v3
elif band=='V':
    data_B_v1=data_V_v3
elif band == 'I':
    data_B_v1 = data_I_v3
else:
    print "band doesn't exist"
#data_B_v1[:,4]=data_B_v1[:,4]+365
ax = plt.subplot(312)
cond=((data_B_v1[:,9] < data_B_v1[:,11])& (data_B_v1[:,2]==0))
plt.errorbar(data_B_v1[:,4][cond],data_B_v1[:,9][cond],yerr=data_B_v1[:,10][cond],color='grey',label='S. Africa',fmt='v')
cond=((data_B_v1[:,9] < data_B_v1[:,11])& (data_B_v1[:,2]==1))
plt.errorbar(data_B_v1[:,4][cond],data_B_v1[:,9][cond],yerr=data_B_v1[:,10][cond],color='cyan',label='Chile',fmt='<')
cond=((data_B_v1[:,9] < data_B_v1[:,11])& (data_B_v1[:,2]==2))
plt.errorbar(data_B_v1[:,4][cond],data_B_v1[:,9][cond],yerr=data_B_v1[:,10][cond],color='yellow',label='Australia',fmt='^')

cond=((data_B_v1[:,9] < data_B_v1[:,11])& (data_B_v1[:,2]==0))
plt.scatter(data_B_v1[:,4][cond],data_B_v1[:,11][cond],color='grey', marker='.',label='lim S')
cond=((data_B_v1[:,9] < data_B_v1[:,11])& (data_B_v1[:,2]==1))
plt.scatter(data_B_v1[:,4][cond],data_B_v1[:,11][cond],color='cyan', marker='.',label='lim C')
cond=((data_B_v1[:,9] < data_B_v1[:,11])& (data_B_v1[:,2]==2))
plt.scatter(data_B_v1[:,4][cond],data_B_v1[:,11][cond],color='yellow', marker='.',label='lim A')

x=np.arange(650-365,870-365,0.5)
y=(1+np.cos(2*np.pi*(x-742.881+365)/29.5306))/2
ax.fill_between(x, 18,25, where= (y>0.8), facecolor='pink',alpha=0.5)


plt.axis([720-365,870-365,18,25])
#plt.xlabel('time [days]')
plt.ylabel('mag')

ax.legend(loc='best',ncol=6, fancybox=True,fontsize=12)
ax.invert_yaxis()

if band=='B':
    data_B_v1=data_B
elif band=='V':
    data_B_v1=data_V
elif band == 'I':
    data_B_v1 = data_I
else:
    print "band doesn't exist"
data_B_v1[:,4]=data_B_v1[:,4]
ax = plt.subplot(313)
cond=( (data_B_v1[:,2]==0))
plt.errorbar(data_B_v1[:,4][cond],data_B_v1[:,9][cond],yerr=data_B_v1[:,10][cond]/3,color='grey',label='S. Africa',fmt='v')
cond=((data_B_v1[:,9] < data_B_v1[:,11])& (data_B_v1[:,2]==1))
plt.errorbar(data_B_v1[:,4][cond],data_B_v1[:,9][cond],yerr=data_B_v1[:,10][cond]/3,color='cyan',label='Chile',fmt='<')
cond=((data_B_v1[:,9] < data_B_v1[:,11])& (data_B_v1[:,2]==2))
plt.errorbar(data_B_v1[:,4][cond],data_B_v1[:,9][cond],yerr=data_B_v1[:,10][cond]/3,color='yellow',label='Australia',fmt='^')

# cond=((data_B_v1[:,9] < data_B_v1[:,11])& (data_B_v1[:,2]==0))
# plt.scatter(data_B_v1[:,4][cond],data_B_v1[:,9][cond],color='grey',label='S. Africa',marker='v',edgecolor='black')
# cond=((data_B_v1[:,9] < data_B_v1[:,11])& (data_B_v1[:,2]==1))
# plt.scatter(data_B_v1[:,4][cond],data_B_v1[:,9][cond],color='cyan',label='Chile',marker='<',edgecolor='black')
# cond=((data_B_v1[:,9] < data_B_v1[:,11])& (data_B_v1[:,2]==2))
# plt.scatter(data_B_v1[:,4][cond],data_B_v1[:,9][cond],color='yellow',label='Australia',marker='^',edgecolor='black')


cond=((data_B_v1[:,9] < data_B_v1[:,11])& (data_B_v1[:,2]==0))
plt.scatter(data_B_v1[:,4][cond],data_B_v1[:,11][cond],color='grey', marker='.',label='lim S')
cond=((data_B_v1[:,9] < data_B_v1[:,11])& (data_B_v1[:,2]==1))
plt.scatter(data_B_v1[:,4][cond],data_B_v1[:,11][cond],color='cyan', marker='.',label='lim C')
cond=((data_B_v1[:,9] < data_B_v1[:,11])& (data_B_v1[:,2]==2))
plt.scatter(data_B_v1[:,4][cond],data_B_v1[:,11][cond],color='yellow', marker='.',label='lim A')

#plt.scatter(data_B_v1[:,4][(data_B_v1[:,9] > data_B_v1[:,11])& (data_B_v1[:,4]<723.5)],data_B_v1[:,11][(data_B_v1[:,9] > data_B_v1[:,11])& (data_B_v1[:,4]<723.5)],color='b', marker='D',label='B no detection')
#plt.scatter(data_B_v1[:,4],data_B_v1[:,11],color='lightsteelblue', marker='.',label='B lim')
# cond=((data_V_v1[:,9] < data_V_v1[:,11])& (data_V_v1[:,2]==0))
# plt.errorbar(data_V_v1[:,4][cond],data_V_v1[:,9][cond],yerr=data_V_v1[:,10][cond],color='green',label='V S. Africa',fmt='v')
# cond=((data_V_v1[:,9] < data_V_v1[:,11])& (data_V_v1[:,2]==1))
# plt.errorbar(data_V_v1[:,4][cond],data_V_v1[:,9][cond],yerr=data_V_v1[:,10][cond],color='green',label='V Chile',fmt='<')
# cond=((data_V_v1[:,9] < data_V_v1[:,11])& (data_V_v1[:,2]==2))
# plt.errorbar(data_V_v1[:,4][cond],data_V_v1[:,9][cond],yerr=data_V_v1[:,10][cond],color='green',label='V Australie',fmt='^')
# #plt.scatter(data_V_v1[:,4][(data_V_v1[:,9] > data_V_v1[:,11])& (data_V_v1[:,4]<723.5)],data_V_v1[:,11][(data_V_v1[:,9] > data_V_v1[:,11])& (data_V_v1[:,4]<723.5)],color='green', marker='D',label='V no detection')
# plt.scatter(data_V_v1[:,4],data_V_v1[:,11],color='lightgreen', marker='.',label='V lim')
#
# cond=((data_I_v1[:,9] < data_I_v1[:,11])& (data_I_v1[:,2]==0))
# plt.errorbar(data_I_v1[:,4][cond],data_I_v1[:,9][cond],yerr=data_I_v1[:,10][cond],color='red',label='I S. Africa ',fmt='v')
# cond=((data_I_v1[:,9] < data_I_v1[:,11])& (data_I_v1[:,2]==1))
# plt.errorbar(data_I_v1[:,4][cond],data_I_v1[:,9][cond],yerr=data_I_v1[:,10][cond],color='red',label='I Chile ',fmt='<')
# cond=((data_I_v1[:,9] < data_I_v1[:,11])& (data_I_v1[:,2]==2))
# plt.errorbar(data_I_v1[:,4][cond],data_I_v1[:,9][cond],yerr=data_I_v1[:,10][cond],color='red',label='I Australia ',fmt='^')
# # #plt.scatter(data_I_v1[:,4][(data_I_v1[:,9] > data_I_v1[:,11])& (data_I_v1[:,4]<723.5)],data_I_v1[:,11][(data_I_v1[:,9] > data_I_v1[:,11])& (data_I_v1[:,4]<723.5)],color='red', marker='D',label='V no detection')
# plt.scatter(data_I_v1[:,4],data_I_v1[:,11],color='lightpink', marker='.',label='V lim')
x=np.arange(650-365,870-365,0.5)
y=(1+np.cos(2*np.pi*(x-742.881+365)/29.5306))/2
ax.fill_between(x, 18,25, where= (y>0.8), facecolor='pink',alpha=0.5)

plt.axis([720-365,870-365,18,25])
plt.xlabel('time [days]')
plt.ylabel('mag')

#plt.tight_layout()
ax.legend(loc='best',ncol=6, fancybox=True,fontsize=12)
ax.invert_yaxis()


plt.tick_params(labelsize=20)

plt.show()
plt.savefig(current_path+'/plots/LC_trends.png')

