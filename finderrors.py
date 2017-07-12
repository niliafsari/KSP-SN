import os
import glob
import subprocess
import commands

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

current_path=os.path.dirname(os.path.abspath(__file__))
files_path='/home/afsari/N2188/Q2'
os.chdir(files_path)

filename='N2188-1.Q2.*.*.*.*.061035N3413.0060.nh.magcalc.cat'
files = glob.glob(filename)
i=0
flag=0
for f in files:
    cmd='cat '+f+' | tail -n 1'
    last_line = subprocess.check_output(['tail', '-1', f])
    for line in last_line.split(' '):
#	print line
        if is_number(line)==False:
            print f, line
	    break

