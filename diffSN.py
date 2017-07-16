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
outext='.nh.REF-SUB_v1.fits'
REF_images=['REF_Images/N2188-1.Q2.B.161023_1618-161025_0816.XCXA.061035N3413.00005.00005.FM48.BS0512.coadd.REF.fits',
'REF_Images/N2188-1.Q2.I.161023_1622-161025_0820.XCXA.061035N3413.00005.00005.FM40.BS0512.coadd.REF.fits',
'REF_Images/N2188-1.Q2.V.161023_1729-161025_0818.XCXA.061035N3413.00005.00005.FM43.BS0512.coadd.REF.fits']
for i in xrange(0,len(bands)):
    filename_format = 'N2188-1.Q2.'+bands[i]+'.*.*.*.061035N3413.0060.nh.fits'
    filename_done='N2188-1.Q2.'+bands[i]+'.*.*.*.061035N3413.0060'+outext
    files=glob.glob(filename_format)
    files_done = glob.glob(filename_done)
    files_done = [w.replace(outext, '.nh.fits') for w in files_done]
    print len(files_done)
    print len(files)
    files= list(set(files) - set(files_done))
    print len(files)
    for f in files:
        run_command='python ~/SNAP/DiffIm.py '+f+' '+REF_images[i]+' '+ f.replace('.nh.fits',outext)
        #print run_command
        #os.system(run_command)
