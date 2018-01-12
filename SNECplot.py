import os
import glob
import numpy as np
import matplotlib.pyplot as plt

def SNECplot(filename,verbosity=0):
    files_path ='/home/afsari/gpc_SNEC/'
    os.chdir(files_path)
    output_path=filename+'/output/magnitudes.dat'
    mags = np.genfromtxt(output_path, delimiter='  ')
    ax=plt.subplot(111)
    plt.plot(mags[:,0]/84000.0,mags[:,9],label='B',color='blue')
    plt.plot(mags[:,0]/84000.0,mags[:,10],label='V',color='green')
    plt.plot(mags[:,0]/84000.0,mags[:,12],label='I',color='red')
    ax.invert_yaxis()
    plt.ylabel('Absolute Magnitude')
    plt.xlabel('Time [days]')
    plt.show()
if __name__ == "__main__":
    import argparse

    # command line arguments
    parser = argparse.ArgumentParser(description="plot simulation")
    parser.add_argument("filename", type=str, help="simulation name")
    parser.add_argument("-v", "--verbosity", action="count", default=0)
    #parser.add_argument("-n", "--name", help="if identified, will output to a file",type=int, default=0)
    args = parser.parse_args()
    SNECplot(args.filename, verbosity=args.verbosity)
