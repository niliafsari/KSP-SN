from astropy.io import fits
from astropy.wcs import WCS
import numpy as np
#import matplotlib.pyplot as plt
import os
import glob
from findSN import *

import sys
sys.path.insert(0, '/home/afsari/')

from SNAP2.Analysis import *
coef = {'B': 4.107, 'V': 2.682, 'I': 1.516, 'i': 1.698}


location_sexagesimal='-34:08:28.22'
location_deg='92.653175:-34.141172'
rad_pixel=10
rad_arcsec=9.36

ebv=0.029
redshift=0.043
dz=0.002
rad_rad=(rad_arcsec/3600)*(np.pi/180.0) #degrees

gal_rad=sepDistProj(rad_rad, redshift)
print rad_rad,gal_rad/1e3 #kpc
print intDc(redshift)/1e6 #mpc
print intDc(redshift)*3.086e18 #cm

file_original='/home/afsari/N2188/Q2/Hostgal_V/coadd.fits'
#file_original='/home/afsari/N2188/Q2/REF_Images/N2188-1.Q2.V.161023_1729-161025_0818.XCXA.061035N3413.00005.00005.FM43.BS0512.coadd.REF.fits'
file_output='/home/afsari/N2188/Q2/Hostgal_V/coadd.phot'
file_phot='temp_3.cat'
#run_command = 'python ~/SNAP2/MagCalc.py -c  aavso -o  N2188-1.Q2.HOST -b \'' + 'B' + '\' -p 92.653175:-34.141172 -a 12 -fwhm 5 -v -n 3.0  -y 2016 -s 14.0 -r 1000 -f 19 ' + file_original + ' ' + file_phot + ' > ' + file_output

run_command = 'python ~/SNAP2/MagCalc.py -c  aavso -o  N2188-1.Q2.HOST -b \'' + 'V' + '\' -p 92.652976:-34.14109 -a 12.6 -fwhm 5 -v -n 3.0  -y 2016 -s 14.0 -r 1000 -f 19 ' + file_original + ' ' + file_phot + ' > ' + file_output

print run_command
os.system(run_command)

# run_command = 'python ~/SNAP2/MagCalc.py -c  aavso -o  N2188-1.Q2.HOST -b \'' + 'B' + '\' -p 92.653308:-34.141172 -a 13 -fwhm 5 -v -n 3.0  -y 2016 -s 14.0 -r 1000 -f 19 ' + file_original + ' ' + file_phot + ' > ' + file_output
# print run_command
# os.system(run_command)

m_I=17.6034133279
dm_I=0.0575434796098

m_B=19.1628860013
dm_B=0.122631640404

m_V = 18.4531865948
dm_V = 0.0651456553194

M_I,dM_I=absMag(deredMag(m_I, ebv, coef["I"]), redshift,dm_I,dz)
M_B,dM_B=absMag(deredMag(m_B, ebv, coef["B"]), redshift,dm_B,dz)
M_V,dM_V=absMag(deredMag(m_V, ebv, coef["V"]), redshift,dm_V,dz)

print "Abs. Mag. I:", M_I, dM_I
print "Abs. Mag. B:", M_B, dM_B
print "Abs. Mag. V:", M_V, dM_V
print 'B-I',M_B-M_I
print 'B-V',M_B-M_V
print 'V-I',M_V-M_I


