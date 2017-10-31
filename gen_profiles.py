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
from SNAP.Analysis import *
import itertools
import zipfile
import urllib

models=np.arange(11,28,0.6)
for i in models:
    location = '/home/afsari/PycharmProjects/kspSN/models/'
    file_model=location +'s%(num)2.1f.gz' %{"num":i}
    print os.path.isfile(file_model)
    if os.path.isfile(file_model) == False:
        url = 'https://2sn.org/stellarevolution/solar/s%(num)2.1f.gz' %{"num":i}
        urllib.urlretrieve(url,file_model)
    cmd='gunzip '+file_model
    os.system(cmd)

os.chdir(location)
filename_format = 's*.?'
files_found = glob.glob(filename_format)
print files_found
for i,f in enumerate(files_found):
    ff = open('/home/afsari/SNEC-1.01/profiles/profile_'+files_found[i]+'.short', 'w')
    ff.write('20 \n \n')
    writer = csv.writer(ff,delimiter =' ')
    ff_iso = open('/home/afsari/SNEC-1.01/profiles/profile_'+files_found[i]+'.iso.short', 'w')
    ff_iso.write('20 \n ')
    ff_iso.write('20 \n')
    ff_iso.write('1 3 4 12 16 20 24 28 32 36 40 44 48 52 56 \n')
    ff_iso.write('1 2 2 6 8 10 12 14 16 18 20 22 24 26 28 \n')
    writer_iso = csv.writer(ff_iso,delimiter =' ')
    with open(files_found[i], 'r') as fff:
        for j,line in enumerate(itertools.islice(fff, 2, None)):
            line=line.replace(':','')
            line=' '.join(line.split())
            print line
            dat=line.split(' ')
            dat=[0 if x =='---' else x for x in dat]
            writer.writerow((int(dat[0]),float(dat[1]),float(dat[2]),
                                                     float(dat[5]),float(dat[4]),float(dat[3]),float(dat[11]),0))
            writer_iso.writerow((float(dat[1]), float(dat[2]),
                             float(dat[15]), float(dat[16]), float(dat[17]),float(dat[18]),
                                 float(dat[20]), float(dat[21]), float(dat[22]),float(dat[23]), float(dat[24]), float(dat[25]),
                                 float(dat[26]), float(dat[27]), float(dat[28]), float(dat[29]),float(dat[31]) ))

    fff.close()
    ff.close()
    ff_iso.close()

    with file('/home/afsari/SNEC-1.01/profiles/profile_'+files_found[i]+'.short', 'r+') as modified:
        modified.write(str(j+1))
    modified.close()
    with file('/home/afsari/SNEC-1.01/profiles/profile_'+files_found[i]+'.iso.short', 'r+') as modified:
        modified.write(str(j + 1) + '  15')
    modified.close()