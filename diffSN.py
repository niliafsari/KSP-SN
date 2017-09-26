def diffSN(verbosity=0, band='B'):
    from astropy.io import fits
    from astropy.wcs import WCS
    import numpy as np
    import matplotlib.pyplot as plt
    import os
    import glob

    current_path=os.path.dirname(os.path.abspath(__file__))
    files_path='../../N2188/Q2'
    os.chdir(files_path)
    if band=='B':
        bands={band:0}
    elif band=='I':
        bands={band:1}
    elif band=='V':
        bands = {band:2}
    outext='.nh.REF-SUB_v2.fits'
    REF_images=['REF_Images/N2188-1.Q2.B.161023_1618-161025_0816.XCXA.061035N3413.00005.00005.FM48.BS0512.coadd.REF.fits',
    'REF_Images/N2188-1.Q2.I.161023_1622-161025_0820.XCXA.061035N3413.00005.00005.FM40.BS0512.coadd.REF.fits',
    'REF_Images/N2188-1.Q2.V.161023_1729-161025_0818.XCXA.061035N3413.00005.00005.FM43.BS0512.coadd.REF.fits']

    filename_format = 'N2188-1.Q2.'+band+'.*.*.*.061035N3413.0060.nh.fits.fz'
    filename_done='N2188-1.Q2.'+band+'.*.*.*.061035N3413.0060'+outext
    files=glob.glob(filename_format)
    files_done = glob.glob(filename_done)
    files_done = [w.replace(outext, '.nh.fits.fz') for w in files_done]
    print len(files_done)
    print len(files)
    files= list(set(files) - set(files_done))
    print len(files)
    for f in files:
        run_command='funpack -O '+f.replace('.fz','')+' '+f
        #os.system(run_command)
        #print run_command
        #os.system(run_command)
        run_command='python ~/SNAP2/DiffIm.py '+f.replace('.fz','')+' '+REF_images[bands[band]]+' '+ f.replace('.nh.fits.fz',outext)
        #print run_command
        #os.system(run_command)

if __name__ == "__main__":
    import argparse

    # command line arguments
    parser = argparse.ArgumentParser(description="do Photometry")
    parser.add_argument("-v", "--verbosity", action="count", default=0)
    parser.add_argument("-b", "--band", help="band",type=str)
    args = parser.parse_args()
    diffSN( verbosity=args.verbosity,band=args.band)

