import os
import glob
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from dophot import *
from findSN import *
from SNAP import Astrometry
import csv
import sys

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

f_B = open('phot_csv/N2188metadata-B_v3.csv', 'w')
f_I = open('phot_csv/N2188metadata-I_v3.csv', 'w')
f_V = open('phot_csv/N2188metadata-V_v3.csv', 'w')

writer_B = csv.writer(f_B)
writer_B.writerow( ('Name','KSPtime','Location','index', 'time', 'RA', 'DEC','I', 'SN', 'M', 'Merr', 'Mlim','FWHM','r_opt','Io_err','I_rand' ))

writer_I = csv.writer(f_I)
writer_I.writerow( ('Name','KSPtime','Location', 'index','time', 'RA', 'DEC','I', 'SN', 'M', 'Merr', 'Mlim','FWHM','r_opt','Io_err','I_rand' ))

writer_V = csv.writer(f_V)
writer_V.writerow( ('Name','KSPtime','Location','index', 'time', 'RA', 'DEC','I', 'SN', 'M', 'Merr', 'Mlim','FWHM','r_opt','Io_err','I_rand' ))


current_path=os.path.dirname(os.path.abspath(__file__))
files_path='/home/afsari/N2188/Q2'
outext='.nh.newsub_magcalc.cat'
os.chdir(files_path)
filename='N2188-1.Q2.*.*.*.*.061035N3413.0060'+outext
bands={'B':0,'I':1,'V':2}
files = glob.glob(filename)
i=0
flag=0
names=[]
j=0
matplotlib.rcParams.update({'font.size': 18})
for f in files:
    last_line = subprocess.check_output(['tail', '-1', f])
    for line in last_line.split(' '):
        if is_number(line)==False:
            print f, line,j
            j=j+1
            #findSN(f.replace('.nh.magcalc.cat', '.nh.fits'), 1, '/home/afsari/PycharmProjects/kspSN/corrupted/cantopen/')
            #dophot(f.replace('nh.magcalc.cat','nh.fits'),0,1)
            flag=1
            break
    if flag==1:
        flag=0
        continue
    else:
        with open(f) as fil:
            for line in fil:
                if 'full width half maximum:' in line:
                    l=line.split(' ')
                    FWHM=float(l[4])
                elif 'optimal at aperture:' in line:
                    l=line.split(' ')
                    r_opt=float(l[3].replace('FWHM',''))
                elif 'Contribution of intrinsic error:' in line:
                    l=line.split(' ')
                    Io_err=float(l[4])
                elif 'Contribution of ref star scatter:' in line:
                    l = line.split(' ')
                    I_rand = float(l[5])
        info = f.split('.')
        names.append(f)
        if len(last_line.split(' '))==8:
            timeksp=Astrometry.ksp_isot(info[3])
            location=info[4]
            time,RA, DEC,I, SN, M, Merr, Mlim = [float(last_line) for last_line in last_line.split(' ')]
            if info[2]=='B':
                writer_B.writerow((names[i].replace(outext,'.nh.fits'),timeksp,location,i,time,RA, DEC,I, SN, M, Merr, Mlim,FWHM,r_opt,Io_err,I_rand))
            elif info[2]=='I':
                writer_I.writerow((names[i].replace(outext,'.nh.fits'),timeksp,location,i,time,RA, DEC,I, SN, M, Merr, Mlim,FWHM,r_opt,Io_err,I_rand))
            else:
                writer_V.writerow((names[i].replace(outext,'.nh.fits'),timeksp,location,i,time,RA, DEC,I, SN, M, Merr, Mlim,FWHM,r_opt,Io_err,I_rand))
            i=i+1
        else:
            print f, last_line
            #dophot(f.replace(outext,'.nh.fits'),1,1)
f_B.close()
f_V.close()
f_I.close()
