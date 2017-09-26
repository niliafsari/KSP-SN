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


bin_factor = 4

data_B = np.genfromtxt(current_path+ '/phot_csv/N2188-B_v9_edit.csv', delimiter=',')
data_V = np.genfromtxt(current_path+'/phot_csv/N2188-V_v9_edit.csv', delimiter=',')
data_I = np.genfromtxt(current_path+'/phot_csv/N2188-I_v9_edit.csv', delimiter=',')



data_Btobin = data_B[(data_B[:, 9] <= data_B[:, 11]) & (data_B[:, 4] >= 363)]
data_Bnobin = data_B[(data_B[:, 9] <= data_B[:, 11]) & (data_B[:, 4] < 363)]


data_Vtobin = data_V[(data_V[:, 9] <= data_V[:, 11]) & (data_V[:, 4] >= 363)]
data_Vnobin = data_V[(data_V[:, 9] <= data_V[:, 11]) & (data_V[:, 4] < 363)]

data_Itobin = data_I[(data_I[:, 9] <= data_I[:, 11]) & (data_I[:, 4] >= 363)]
data_Inobin = data_I[(data_I[:, 9] <= data_I[:, 11]) & (data_I[:, 4] < 363)]


fluxes = np.array([4260.0* 1000000.0, 3640.0 * 1000000.0, 2550.0 * 1000000.0])
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
        binnedV=np.append(binnedV,np.array([time, I, mo, m_err]).reshape((1,4)),0)
    t = t + bin_factor



