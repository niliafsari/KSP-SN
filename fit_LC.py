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

sn_name="KSPN2188_v1"
magB = np.load("/home/afsari/PycharmProjects/kspSN/phot_csv/compiledSN_B_KSPN2188_v1.npy")
magV = np.load("/home/afsari/PycharmProjects/kspSN/phot_csv/compiledSN_" + "V" + "_" + sn_name + ".npy")
magI = np.load("/home/afsari/PycharmProjects/kspSN/phot_csv/compiledSN_" + "I" + "_" + sn_name + ".npy")

#plt.scatter(magB[:,0],magB[:,1])
magB[:,0]=magB[:,0]-3.588672569440000188e+02
magV[:,0]=magV[:,0]-3.588672569440000188e+02
magI[:,0]=magI[:,0]-3.588672569440000188e+02

t1=30
t2=75
[z,v]=np.polyfit(magB[:,0][(magB[:,0]>t1) & (magB[:,0]<t2)],magB[:,1][(magB[:,0]>t1) & (magB[:,0]<t2)],1,cov=True)
print z,v
p = np.poly1d(z)
plt.scatter(magB[:,0],magB[:,1])
x=magB[:,0][(magB[:,0]>t1) & (magB[:,0]<t2)]

plt.scatter(x,p(x))

magB=magV
[z,v]=np.polyfit(magB[:,0][(magB[:,0]>t1) & (magB[:,0]<t2)],magB[:,1][(magB[:,0]>t1) & (magB[:,0]<t2)],1,cov=True)
print z,v
p = np.poly1d(z)
plt.scatter(magB[:,0],magB[:,1])
x=magB[:,0][(magB[:,0]>t1) & (magB[:,0]<t2)]

plt.scatter(x,p(x))

magB=magI
[z,v]=np.polyfit(magB[:,0][(magB[:,0]>t1) & (magB[:,0]<t2)],magB[:,1][(magB[:,0]>t1) & (magB[:,0]<t2)],1,cov=True)
print z,v
p = np.poly1d(z)
plt.scatter(magB[:,0],magB[:,1])
x=magB[:,0][(magB[:,0]>t1) & (magB[:,0]<t2)]

plt.scatter(x,p(x))

plt.show()