import urllib
import os
import glob
import subprocess
import commands
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from astropy.time import Time

from moon import *
import csv
import json
from pprint import pprint
import os.path
import sys

sys.path.insert(0, '/home/afsari/')
from SNAP2.Analysis import *

with open("logs/sn_names.txt") as f:
    file_names = f.readlines()

file_names = [line.rstrip('\n') for line in file_names]
files_count=len(file_names)
Band='I'
coef = {'B': 4.107, 'V': 2.682, 'I': 1.516, 'i': 1.698}
for i,sn_name in enumerate(file_names):
    mag = np.zeros(shape=(0, 5))
    location='/home/afsari/PycharmProjects/kspSN/SN_json/'
    print os.path.isfile(location+sn_name+'.json')
    if os.path.isfile(location+sn_name+'.json')==False:
        url='https://sne.space/astrocats/astrocats/supernovae/output/json/'+sn_name+'.json'
        urllib.urlretrieve(url,location+sn_name+'.json')

    with open(location+sn_name+'.json') as data_file:
        print data_file
        data = json.load(data_file)

    redshift=data[sn_name]["redshift"][0]["value"]
    ebv=data[sn_name]["ebv"][0]["value"]
    # if sn_name == 'SN2009bw':
    #     print data[sn_name]["redshift"][2]["value"]
    ds=np.zeros(shape=(0,5))
    for dat in data[sn_name]["photometry"]:
        try:
            if dat["band"]==Band:
                add = np.concatenate(([dat["time"], dat["magnitude"], dat["e_magnitude"]]
                                      , absMag(deredMag(float(dat["magnitude"]), float(ebv), coef[Band]),
                                               float(redshift), float(dat["e_magnitude"]), 0)))
                add=np.reshape(add,(1,5))
                mag=np.concatenate((mag,add),axis=0)
            else:
                if Band == 'I' and sn_name!='SN2013ej' and sn_name!='SN2005cs' and sn_name!='SN20009bw' and sn_name!='SN2013fs' :
                    Band = 'i'
                if dat["band"] == Band:
                    add = np.concatenate(([dat["time"], dat["magnitude"], dat["e_magnitude"]]
                                          , absMag(deredMag(float(dat["magnitude"]), float(ebv), coef[Band]),
                                                   float(redshift), float(dat["e_magnitude"]), 0)))
                    add = np.reshape(add, (1, 5))
                    mag = np.concatenate((mag, add), axis=0)
                Band='I'
        except:
            print sn_name+" error in "
            print dat
            continue
    print mag.shape
    if Band == 'i':
        Band = 'I'
    np.save("phot_csv/compiledSN_"+Band+"_"+sn_name+".npy", mag)