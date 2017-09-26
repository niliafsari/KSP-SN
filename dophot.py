import os
import glob
import numpy as np
import matplotlib.pyplot as plt

def dophot(filename,verbosity=0, output=0):
    files_path = '/home/afsari/N2188/Q2'
    diffext='.nh.REF-SUB_v2.fits'
    outext = '.nh.apphot8_magcalc.cat'
    os.chdir(files_path)
    info = filename.split('.')
    band=info[2]
    files_sub=filename.replace('.nh.fits',diffext)
    print files_sub
    file_phot='temp.cat'
    #file_phot='N2188-1.Q2.V.170430_0926.A.056477.061035N3413.0060_tan.nh.phot.apass.csv'
    file_output=filename.replace('.nh.fits',outext)
    if output==1:
        file_output=' > ' +file_output
    else:
        file_output=''

    if verbosity==1:
        run_command = 'python ~/SNAP2/MagCalc.py -c  aavso -o  N2188-1.Q2.SN -b \'' + band + '\' -p 92.654754:-34.14111 -r 1000 -fwhm 5 -v -n 3.0 -psf 3 -y 2016 -a 8 -s 14.0 -r 1000 -f 19 --fit_sky ' + filename + ' -d ' + files_sub + ' ' + file_phot + file_output
    elif verbosity==2:
        run_command = 'python ~/SNAP2/MagCalc.py -c  aavso -o  N2188-1.Q2.SN -b \'' + band + '\' -p 92.654754:-34.14111 -r 1000 -fwhm 5 -vv -n 3.0 -psf 3 -y 2016 -a 8 -s 14.0 -r 1000 -f 19 --fit_sky ' + filename + ' -d ' + files_sub + ' ' + file_phot + file_output
    elif verbosity==3:
        run_command = 'python ~/SNAP2/MagCalc.py -c  aavso -o  N2188-1.Q2.SN -b \'' + band + '\' -p 92.654754:-34.14111 -r 1000 -fwhm 5 -vvv -n 3.0 -psf 3 -y 2016 -a 8 -s 14.0 -r 1000 -f 19 --fit_sky ' + filename + ' -d ' + files_sub + ' ' + file_phot + file_output
    elif verbosity==4:
        run_command = 'python ~/SNAP2/MagCalc.py -c  aavso -o  N2188-1.Q2.SN -b \'' + band + '\' -p 92.654754:-34.14111 -r 1000 -fwhm 5 -vvvv -n 3.0 -psf 3 -y 2016 -a 8 -s 14.0 -r 1000 -f 19 --fit_sky ' + filename + ' -d ' + files_sub + ' ' + file_phot + file_output
    else:
        run_command = 'python ~/SNAP2/MagCalc.py -c  aavso -o  N2188-1.Q2.SN -b \'' + band + '\' -p 92.654754:-34.14111 -r 1000 -fwhm 5 -n 3.0 -psf 3 -y 2016 -a 8 -s 14.0 -r 1000 -f 19 --fit_sky ' + filename + ' -d ' + files_sub + ' ' + file_phot + file_output


    # if verbosity==1:
    #     run_command = 'python ~/SNAP/MagCalc.py -c  aavso -o  N2188-1.Q2.SN -b \'' + band + '\' -p 92.654754:-34.14111 -r 1000 -fwhm 5 -v -n 3.0 -s 14.0 ' + filename + ' -d ' + files_sub + ' ' + file_phot + file_output
    # elif verbosity==2:
    #     run_command = 'python ~/SNAP/MagCalc.py -c  aavso -o  N2188-1.Q2.SN -b \'' + band + '\' -p 92.654754:-34.14111 -r 1000 -fwhm 5 -vv -n 3.0 -s 14.0 ' + filename + ' -d ' + files_sub + ' ' + file_phot + file_output
    # elif verbosity==3:
    #     run_command = 'python ~/SNAP/MagCalc.py -c  aavso -o  N2188-1.Q2.SN -b \'' + band + '\' -p 92.654754:-34.14111 -r 1000 -fwhm 5 -vvv -n 3.0 -s 14.0 ' + filename + ' -d ' + files_sub + ' ' + file_phot + file_output
    # elif verbosity==4:
    #     run_command = 'python ~/SNAP/MagCalc.py -c  aavso -o  N2188-1.Q2.SN -b \'' + band + '\' -p 92.654754:-34.14111 -r 1000 -fwhm 5 -vvvv -n 3.0 -s 14.0 ' + filename + ' -d ' + files_sub + ' ' + file_phot + file_output
    # else:
    #     run_command = 'python ~/SNAP/MagCalc.py -c  aavso -o  N2188-1.Q2.SN -b \'' + band + '\' -p 92.654754:-34.14111 -r 1000 -fwhm 5 -n 3.0 -s 14.0 ' + filename + ' -d ' + files_sub + ' ' + file_phot + file_output

    if verbosity>0:
        print run_command
    os.system(run_command)


if __name__ == "__main__":
    import argparse

    # command line arguments
    parser = argparse.ArgumentParser(description="do Photometry")
    parser.add_argument("filename", type=str, help="fits image containing source")
    parser.add_argument("-v", "--verbosity", action="count", default=0)
    parser.add_argument("-o", "--output", help="if identified, will output to a file",type=int, default=0)
    args = parser.parse_args()
    dophot(args.filename, verbosity=args.verbosity,output=args.output)
