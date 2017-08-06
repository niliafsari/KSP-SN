from astropy.io import fits
from astropy.wcs import WCS
import numpy as np
import matplotlib.pyplot as plt
import os
import glob

current_path=os.path.dirname(os.path.abspath(__file__))
files_path='../../N2188/Q2'
os.chdir(files_path)
bands={0:'B',1:'I',2:'V'}
orig='.nh.fits'
outext='.nh.REF-SUB_v3.fits'
for i in xrange(0,len(bands)):
    filename_format = 'N2188-1.Q2.'+bands[i]+'.*.*.*.061035N3413.0060'+orig
    filename_done='N2188-1.Q2.'+bands[i]+'.*.*.*.061035N3413.0060'+outext
    files=glob.glob(filename_format)
    files_done = glob.glob(filename_done)
    files_done = [w.replace(outext,orig) for w in files_done]
    print len(files_done)
    print len(files)
    files= list(set(files) - set(files_done))
    print len(files)
    for j in xrange(0,len(files)):
        file_output = files[j].replace(orig, outext)
        run_command = 'python ~/SNAP2/CropIm.py '+files[j] + ' '+file_output+ ' -r 500'
        #print run_command
        os.system(run_command)