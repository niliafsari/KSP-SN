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

f_B = open('phot_csv/N2188-B_v12.csv', 'w')
f_I = open('phot_csv/N2188-I_v12.csv', 'w')
f_V = open('phot_csv/N2188-V_v12.csv', 'w')

writer_B = csv.writer(f_B)
writer_B.writerow( ('Name','KSPtime','Location','index', 'time', 'RA', 'DEC','I', 'SN', 'M', 'Merr', 'Mlim' ))

writer_I = csv.writer(f_I)
writer_I.writerow( ('Name','KSPtime','Location', 'index','time', 'RA', 'DEC','I', 'SN', 'M', 'Merr', 'Mlim' ))

writer_V = csv.writer(f_V)
writer_V.writerow( ('Name','KSPtime','Location','index', 'time', 'RA', 'DEC','I', 'SN', 'M', 'Merr', 'Mlim' ))


current_path=os.path.dirname(os.path.abspath(__file__))
files_path='/home/afsari/N2188/Q2'
outext='.nh.psfconv10_magcalc.cat'
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
            #dophot(f.replace(outext,'.nh.fits'),1,1)
            cmd='rm ~/N2188/Q2/'+f
            os.system(cmd)
            flag=1
            break
    if flag==1:
        flag=0
        continue
    else:
        info = f.split('.')
        names.append(f)
        if len(last_line.split(' '))==8:
            timeksp=Astrometry.ksp_isot(info[3])
            location=info[4]
            time,RA, DEC,I, SN, M, Merr, Mlim = [float(last_line) for last_line in last_line.split(' ')]
            if info[2]=='B':
                #if (time > 462 and time<466 and M<Mlim):
                #    print names[i].replace(outext,'.nh.fits')
                writer_B.writerow((names[i].replace(outext,'.nh.fits'),timeksp,location,i,time,RA, DEC,I, SN, M, Merr, Mlim))
            elif info[2]=='I':
                #if ( time < 357.0 and  M<Mlim ):
                #    print names[i].replace(outext,'.nh.fits')
                  #dophot(names[i].replace(outext,'.nh.fits'),1,1)
                writer_I.writerow((names[i].replace(outext,'.nh.fits'),timeksp,location,i,time,RA, DEC,I, SN, M, Merr, Mlim))
            else:
                # if (M<18.4 and M<Mlim) or (Merr>1 and M<Mlim):
                #       print names[i].replace(outext, '.nh.fits')
                # #    findSN(names[i].replace(outext,'.nh.fits'),1,'/home/afsari/PycharmProjects/kspSN/corrupted/varhighV/')
                writer_V.writerow((names[i].replace(outext,'.nh.fits'),timeksp,location,i,time,RA, DEC,I, SN, M, Merr, Mlim))
            i=i+1
        else:
            print f, last_line
            dophot(f.replace(outext,'.nh.fits'),1,1)

f_B.close()
f_V.close()
f_I.close()
