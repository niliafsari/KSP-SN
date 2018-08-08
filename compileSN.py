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
coef = {'B': 3.626, 'V': 2.742, 'I': 1.505, 'i': 1.698}
coef = {'B': 4.315, 'V': 3.315, 'I': 1.940, 'i': 2.086}
for i,sn_name in enumerate(file_names):
    print "name",sn_name
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
    # if sn_name == 'SN2014cx':
    #     print ebv
    ds=np.zeros(shape=(0,5))
    for dat in data[sn_name]["photometry"]:
        try:
            if sn_name=='SN1987A':
                ebv=0.19
            if "e_magnitude" in dat:
                error=float(dat["e_magnitude"])
            else:
                error=0
            if dat["band"]==Band and Band != 'I':
                if sn_name=='SN2014cx':
                    add = np.concatenate(([dat["time"], dat["magnitude"], error], [deredMag(float(dat["magnitude"]), float(ebv), coef[Band])-31.27,error]))
                if sn_name == 'SN1987A':
                    add = np.concatenate(([dat["time"], dat["magnitude"], error],
                                          [deredMag(float(dat["magnitude"]), float(ebv), coef[Band]) - 18.56, error]))
                elif sn_name=='SN199em' and dat["source"]=="1":
                    add = np.concatenate(([dat["time"], dat["magnitude"], error
                                      , deredMag(float(dat["magnitude"]), float(ebv), coef[Band])-29.46,error]))
                else:
                    add = np.concatenate(([dat["time"], dat["magnitude"], error]
                                      , absMag(deredMag(float(dat["magnitude"]), float(ebv), coef[Band]),
                                               float(redshift), error, 0)))
                print sn_name,add
                add=np.reshape(add,(1,5))
                if sn_name=='SN2004er':
                    print add
                mag=np.concatenate((mag,add),axis=0)
            elif Band == 'I':
                if sn_name!='SN1987A' and sn_name!='SN2004ek'  and sn_name!="SN1991al" and sn_name!="SN1992af" and sn_name!='SN1999em' and sn_name!='SN1999cr' and sn_name!='SN2009ib'  and sn_name!='SN2013ej' and sn_name!='SN2005cs' and sn_name!='SN20009bw' and sn_name!='SN2013fs' :
                    Band = 'i'
                if dat["band"]==Band :
                    if sn_name == 'SN2014cx':
                        add = np.concatenate(([dat["time"], dat["magnitude"], error],
                                               [deredMag(float(dat["magnitude"]), float(ebv), coef[Band]) - 31.27,
                                               error]))
                    if sn_name == 'SN1987A':
                        add = np.concatenate(([dat["time"], dat["magnitude"], error],
                                               [deredMag(float(dat["magnitude"]), float(ebv), coef[Band]) - 18.56,
                                               error]))
                    elif sn_name == 'SN1999em' and dat["source"]=="1":
                        add = np.concatenate(([dat["time"], dat["magnitude"], error
                            , deredMag(float(dat["magnitude"]), float(ebv), coef[Band]) -29.46, error]))
                    else:
                        add = np.concatenate(([dat["time"], dat["magnitude"], error]
                                          , absMag(deredMag(float(dat["magnitude"]), float(ebv), coef[Band]),
                                                   float(redshift), error, 0)))
                    add = np.reshape(add, (1, 5))
                    mag = np.concatenate((mag, add), axis=0)
                    Band='I'
        except:
            #print sn_name+" error in "
            #print dat
            continue
    #print mag.shape
    if Band == 'i':
        Band = 'I'
    np.save("phot_csv/compiledSN_"+Band+"_"+sn_name+".npy", mag)