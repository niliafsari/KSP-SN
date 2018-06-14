from astropy.io import fits
from astropy.wcs import WCS
import numpy as np
#import matplotlib.pyplot as plt
import os
import glob
from findSN import *
import sys
from scipy.interpolate import UnivariateSpline
sys.path.insert(0, '/home/afsari/')
from SNAP2.Analysis import *

magB = np.genfromtxt('phot_csv/B.csv', delimiter=",")
magV = np.genfromtxt('phot_csv/V.csv', delimiter=",")
magI = np.genfromtxt('phot_csv/I.csv', delimiter=",")

magB[:,1]=-magB[:,1]+28
magV[:,1]=-magV[:,1]+28
magI[:,1]=-magI[:,1]+28
sn_name="SN1999em"
error=np.zeros(shape=[np.shape(magB)[0],1])
magB=np.concatenate((magB,error),axis=1)
abs=np.reshape((magB[:,1]-30.56),np.shape(error))
print np.shape(abs)
magB=np.concatenate((magB,abs),axis=1)
magB=np.concatenate((magB,error),axis=1)
print magB
np.save("phot_csv/compiledSN_"+"B"+"_"+sn_name+".npy",magB)


magB=magV
error=np.zeros(shape=[np.shape(magB)[0],1])
magB=np.concatenate((magB,error),axis=1)
abs=np.reshape((magB[:,1]-30.56),np.shape(error))
magB=np.concatenate((magB,abs),axis=1)
magB=np.concatenate((magB,error),axis=1)
print magB
np.save("phot_csv/compiledSN_"+"V"+"_"+sn_name+".npy",magB)

magB=magI
error=np.zeros(shape=[np.shape(magB)[0],1])
magB=np.concatenate((magB,error),axis=1)
abs=np.reshape((magB[:,1]-30.56),np.shape(error))
magB=np.concatenate((magB,abs),axis=1)
magB=np.concatenate((magB,error),axis=1)
np.save("phot_csv/compiledSN_"+"I"+"_"+sn_name+".npy",magB)
# plt.scatter(magB[:,0],magB[:,1])
# plt.gca().invert_yaxis()
# plt.show()