from astropy.io import fits
from astropy.wcs import WCS
import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import matplotlib.colors as colors


def findSN(filename,verbosity=0, directory='/home/afsari/PycharmProjects/kspSN/corrupted/'):
    files_path = '/home/afsari/N2188/Q2'
    os.chdir(files_path)
    filename_raw =  filename
    diffext='REF-SUB_v1.fits'
    filename = filename.replace('fits',diffext)
    diffext2='REF-SUB_v2.fits'
    filename2 = filename.replace(diffext,diffext2)
    info = filename.split('.')

    ax1=plt.subplot(1, 3, 1)
    hdulist = fits.open(filename_raw)
    image = hdulist[0].data
    image1 = hdulist[0].data
    header = hdulist[0].header
    coord = '92.654754:-34.14111'
    RA, DEC = [float(coord) for coord in coord.split(':')]
    hdulist.close()
    wcs = WCS(filename)
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

    ax2=plt.subplot(1, 3, 2)
    hdulist = fits.open(filename)
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

    ax3=plt.subplot(1, 3, 3)
    hdulist = fits.open(filename2)
    image = hdulist[0].data
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
    ax3.set_title("Subtracted 8*8")
    plt.gca().set_aspect('equal', adjustable='box')


    plt.suptitle('Name:' + info[0] + ' Filter:' + info[2] + ' Time:' + info[3])
    if directory != '':
        plt.savefig(directory+filename_raw.replace('.fits', '.png'))
    else:
        plt.show()
    fig = plt.figure()
    ax=plt.subplot(1, 3, 1)
    plt.imshow(image1, cmap='gray_r', vmax=150, vmin=0,label='original')
    ax.set_title("original")
    ax1=plt.subplot(1, 3, 2)
    plt.imshow(image2, cmap='gray_r', vmax=150, vmin=0)
    ax1.set_title("Subtracted 2*2")
    ax2=plt.subplot(1, 3, 3)
    plt.imshow(image, cmap='gray_r', vmax=150, vmin=0)
    ax2.set_title("Subtracted 8*8")
    if directory != '':
        plt.savefig(directory+filename_raw.replace('.fits', '.tot.png'))
    else:
        plt.show()


if __name__ == "__main__":
    import argparse

    # command line arguments
    parser = argparse.ArgumentParser(description="plot image")
    parser.add_argument("filename", type=str, help="fits image containing source")
    parser.add_argument("-v", "--verbosity", action="count", default=0)
    parser.add_argument("-d", "--directory", help="if identified, will output to a dir",type=str,default='')
    args = parser.parse_args()
    findSN(args.filename, verbosity=args.verbosity,directory=args.directory)