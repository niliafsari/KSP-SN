def diffSN(verbosity=0, band='B'):
    from astropy.io import fits
    from astropy.wcs import WCS
    import numpy as np
    import matplotlib.pyplot as plt
    import os
    import glob

    current_path=os.path.dirname(os.path.abspath(__file__))
    files_path='../../N300'
    os.chdir(files_path)
    if band=='B':
        bands={band:0}
    elif band=='I':
        bands={band:1}
    elif band=='V':
        bands = {band:2}
    outext='.nh.REF-SUB.fits'
    REF_images=['REF_Images/N300-1.Q2.B.150626_1842-151019_1231.XCSA.005608N3754.00094.00094.FM30.BS0512.ALL.coadd.REF.fits',
'REF_Images/N300-1.Q2.I.150625_1033-151019_1303.XCSA.005608N3754.00294.00294.FM30.BS0512.ALL.coadd.REF.fits',
'REF_Images/N300-1.Q2.V.150625_1010-151019_1300.XCSA.005608N3754.00181.00181.FM30.BS0512.ALL.coadd.REF.fits']
    filename_format = 'N300-1.Q2.'+band+'.*.*.*.*.0060.nh.fits'
    filename_done='N300-1.Q2.'+band+'.*.*.*.*.0060'+outext
    files=glob.glob(filename_format)
    files_done = glob.glob(filename_done)
    files_done = [w.replace(outext, '.nh.fits') for w in files_done]
    print len(files_done)
    print len(files)
    files= list(set(files) - set(files_done))
    print len(files)
    for f in files:
        #run_command='funpack -O '+f.replace('.fz','')+' '+f
        #os.system(run_command)
        #print run_command
        #os.system(run_command)
        run_command='python ~/SNAP2/DiffIm.py '+f+' '+REF_images[bands[band]]+' '+ f.replace('.nh.fits',outext)
        print run_command
        os.system(run_command)

if __name__ == "__main__":
    import argparse

    # command line arguments
    parser = argparse.ArgumentParser(description="do Photometry")
    parser.add_argument("-v", "--verbosity", action="count", default=0)
    parser.add_argument("-b", "--band", help="band",type=str)
    args = parser.parse_args()
    diffSN( verbosity=args.verbosity,band=args.band)

