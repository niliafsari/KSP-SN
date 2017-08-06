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
outext='.nh.relaxpsfnewsub_magcalc.cat'
subext='.nh.REF-SUB_v2.fits'
for i in xrange(0,len(bands)):
    filename_format = 'N2188-1.Q2.'+bands[i]+'.*.*.*.061035N3413.0060'+subext
    filename_done='N2188-1.Q2.'+bands[i]+'.*.*.*.061035N3413.0060'+outext
    files=glob.glob(filename_format)
    files_done = glob.glob(filename_done)
    files_done = [w.replace(outext, subext) for w in files_done]
    print len(files_done)
    print len(files)
    files= list(set(files) - set(files_done))
    print len(files)
    for j in xrange(0,len(files)):
        #print j
        file_original=files[j].replace(subext, '.nh.fits')
        file_phot='my_catname.cat'
        file_output = files[j].replace(subext, outext)
        #run_command='python ~/SNAP/MagCalc.py -c  aavso -o  N2188-1.Q2.SN -b \''+bands[i]+'\' -p 92.654754:-34.14111 -r 1000 -fwhm 5 -v -n 3.0 -s 14.0 '+file_original+' -d '+files[j]+' '+file_phot+' > '+ file_output
        run_command = 'python ~/SNAP/MagCalc.py -c  aavso -o  N2188-1.Q2.SN -b \'' + bands[
            i] + '\' -p 92.654754:-34.14111 -r 1000 -fwhm 5 -v -n 3.0 -s 14.0 -f 18.5 ' + file_original + ' '+'-d'+' '+files[j]+ ' ' + file_phot + ' > ' + file_output
        #print run_command
        os.system(run_command)

