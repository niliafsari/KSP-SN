from astropy.io import fits
from astropy.wcs import WCS
import numpy as np
import matplotlib.pyplot as plt
import os
import glob

current_path=os.path.dirname(os.path.abspath(__file__))
files_path='../../N2188/Q2'

orig='.nh.cropped.fits'
outext='.nh.REF-SUB_v3.fits'
os.chdir(files_path)
filename_done = 'N2188-1.Q2*061035N3413.0060' + outext
files_done = glob.glob(filename_done)

for f in files_done:
    cmd='mv '+f+' '+ f.replace(outext,orig)
    print cmd
    os.system(cmd)