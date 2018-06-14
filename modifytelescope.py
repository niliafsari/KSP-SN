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


files=['N2188-B_v12_edit.csv','N2188-V_v12_edit.csv','N2188-I_v12_edit.csv']
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
        print l
        if l[2]=='S':
            data[i,2]=0
        elif l[2]=='C':
            data[i,2]=1
        elif l[2]=='A':
            data[i,2]=2
        else:
            data[i,2]=-1
        i=i+1
    data_list=data.tolist()
    for l in data_list:
        l[0] = mydict1[int(l[3])]
        l[1] = mydict2[int(l[3])]
    with open("phot_csv/"+fil, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(data_list)