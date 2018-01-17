from astropy.io import fits
from astropy.wcs import WCS
import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import glob

def findSN(filename,verbosity=0, directory=''):
    filename_raw = filename
    info = filename.split('.')
    ref_format=info[0]+'.'+info[1]+'.'+info[2]+'*.REF.fits'
    reference=glob.glob(ref_format)
    ax1=plt.subplot(1, 2, 1)
    hdulist = fits.open(filename_raw)
    image = hdulist[0].data
    image1 = hdulist[0].data
    header = hdulist[0].header
    coord = '92.654754:-34.14111'
    RA, DEC = [float(coord) for coord in coord.split(':')]
    hdulist.close()
    wcs = WCS(filename_raw)
    Xo, Yo = wcs.all_world2pix(RA, DEC, 0)
    Xo, Yo = int(Xo), int(Yo)
    r = 100
    Y = np.linspace(Yo - r, Yo + r, 2 * r)
    X = np.linspace(Xo - r, Xo + r, 2 * r)
    y, x = np.meshgrid(Y, X)
    dat = image.T[Xo - r:Xo + r, Yo - r:Yo + r]
    #print np.max(dat)
    plt.pcolormesh(x, y, image.T[Xo - r:Xo + r, Yo - r:Yo + r],
                   cmap='gray_r', vmax=150, vmin=-40)
    ax1.set_title("original")
    plt.axis([Xo - r, Xo + r, Yo - r, Yo + r])
    plt.gca().set_aspect('equal', adjustable='box')

    ax2=plt.subplot(1, 2, 2)
    hdulist = fits.open(reference)
    image = hdulist[0].data
    image2 = hdulist[0].data
    header = hdulist[0].header
    coord = '92.654754:-34.14111'
    RA, DEC = [float(coord) for coord in coord.split(':')]
    hdulist.close()
    wcs = WCS(filename)
    Xo, Yo = wcs.all_world2pix(RA, DEC, 0)
    Xo, Yo = int(Xo), int(Yo)
    Y = np.linspace(Yo - r, Yo + r, 2 * r)
    X = np.linspace(Xo - r, Xo + r, 2 * r)
    y, x = np.meshgrid(Y, X)
    plt.pcolormesh(x, y, image.T[Xo - r:Xo + r, Yo - r:Yo + r],
                   cmap='gray_r', vmax=150, vmin=-40)
    plt.axis([Xo - r, Xo + r, Yo - r, Yo + r])
    ax2.set_title("subtracted 2*2")
    plt.gca().set_aspect('equal', adjustable='box')

    plt.suptitle('Name:' + info[0] + ' Filter:' + info[2] + ' Time:' + info[3])
    plt.show()
    plt.savefig(filename_raw.replace('.fits', '.png'))
    plt.cla()

if __name__ == "__main__":
    import argparse

    # command line arguments
    parser = argparse.ArgumentParser(description="plot image")
    parser.add_argument("filename", type=str, help="fits image containing source")
    parser.add_argument("-v", "--verbosity", action="count", default=0)
    parser.add_argument("-d", "--directory", help="if identified, will output to a dir",type=str,default='')
    args = parser.parse_args()
    findSN(args.filename, verbosity=args.verbosity,directory=args.directory)