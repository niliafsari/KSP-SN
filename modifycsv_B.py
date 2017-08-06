import numpy as np
import csv
from astropy.time import Time
from moon import *

in_filename='N2188-B_v7.csv'
out_filename="N2188-B_v7_edit.csv"
my_file = open('phot_csv/'+in_filename, 'r')
reader = csv.reader(my_file, delimiter=',')
my_list = list(reader)
my_file.close()
mydict1 = {rows[3]:rows[0] for rows in my_list}
mydict2 = {rows[3]:rows[1] for rows in my_list}
mydict3 = {rows[3]:rows[2] for rows in my_list}
mydict_rev = {rows[0]:rows[3] for rows in my_list}
data = np.genfromtxt ('phot_csv/'+in_filename, delimiter=",")
print data.shape
data=data[1:][:]

in_filename_v2='N2188-B_v2_edit.csv'
my_file = open('phot_csv/'+in_filename_v2, 'r')
reader = csv.reader(my_file, delimiter=',')
my_list_v2 = list(reader)
my_file.close()
mydict1_v2 = {rows[3]:rows[0] for rows in my_list_v2}
mydict2_v2 = {rows[3]:rows[1] for rows in my_list_v2}
mydict3_v2 = {rows[3]:rows[2] for rows in my_list_v2}
mydict4_v2 = {rows[0]:float(rows[7]) for rows in my_list_v2}
mydict5_v2 = {rows[0]:float(rows[8]) for rows in my_list_v2}
mydict_rev_v2 = {rows[0]:rows[3] for rows in my_list_v2}
data_v2 = np.genfromtxt ('phot_csv/'+in_filename_v2, delimiter=",")

data_list_v2=data_v2.tolist()
for l in data_list_v2:
    try:
        l[0] = mydict1_v2[str(int(l[3]))]
        l[1] = mydict2_v2[str(int(l[3]))]
        l[2] = mydict3_v2[str(int(l[3]))]
    except:
        l[0] =0
        l[1] = 0
        l[2] = 0


# torem=['N2188-1.Q2.B.170116_2031.S.050939.061035N3413.0060.nh.fits','N2188-1.Q2.B.170223_1936.S.057837.061035N3413.0060.nh.fits',
# 'N2188-1.Q2.B.170131_1109.A.043571.061035N3413.0060.nh.fits','N2188-1.Q2.B.170309_0213.C.060754.061035N3413.0060.nh.fits',
# 'N2188-1.Q2.B.170223_1936.S.057837.061035N3413.0060.nh.fits','N2188-1.Q2.B.161104_1542.A.031460.061035N3413.0060.nh.fits',
# 'N2188-1.Q2.B.170315_0952.A.049328.061035N3413.0060.nh.fits','N2188-1.Q2.B.161213_1700.A.037688.061035N3413.0060.nh.fits',
#        'N2188-1.Q2.B.170114_0238.C.049289.061035N3413.0060.nh.fits']
#
# for file in torem:
#     index=mydict_rev[file]
#     data=data[data[:,3] != int(index)]

torem=[]
for i, index in enumerate(data[:,3]):
    I=data[i,7]
    I_err=I/data[i,8]
    I_orig=mydict4_v2[mydict1[str(int(index))]]
    I_orig_err=I_orig/mydict5_v2[mydict1[str(int(index))]]
    if I>(I_orig+I_orig_err):
        torem.append(mydict1[str(int(index))])

rem=['N2188-1.Q2.B.161227_2045.S.048536.061035N3413.0060.nh.fits'
     ,'N2188-1.Q2.B.170218_1148.A.044953.061035N3413.0060.nh.fits'
     ,'N2188-1.Q2.B.170218_1043.A.044923.061035N3413.0060.nh.fits'
     ,'N2188-1.Q2.B.170219_1143.A.045219.061035N3413.0060.nh.fits'
     ,'N2188-1.Q2.B.170219_1249.A.045249.061035N3413.0060.nh.fits'
     ,'N2188-1.Q2.B.170219_1401.A.045281.061035N3413.0060.nh.fits'
     ,'N2188-1.Q2.B.170219_1035.A.045189.061035N3413.0060.nh.fits'
     ,'N2188-1.Q2.B.170116_2031.S.050939.061035N3413.0060.nh.fits'
     ,'N2188-1.Q2.B.170130_1917.S.053586.061035N3413.0060.nh.fits'
     ,'N2188-1.Q2.B.170112_0706.C.048932.061035N3413.0060.nh.fits'
     ,'N2188-1.Q2.B.170202_1917.S.054285.061035N3413.0060.nh.fits']


torem=torem+rem

# for file in torem:
#      index=mydict_rev[file]
#      data=data[data[:,3] != int(index)]

print data.shape

data_list=data.tolist()
for l in data_list:
    try:
        l[0] = mydict1[str(int(l[3]))]
        l[1] = mydict2[str(int(l[3]))]
        l[2] = mydict3[str(int(l[3]))]
    except:
        l[0] =0
        l[1] = 0
        l[2] = 0

tt=[l[1] for l in data_list]
T=[moon_illumination(Time(t, format='isot', scale='utc')) for t in tt]
i=0



with open("phot_csv/"+out_filename, "wb") as f:
    writer = csv.writer(f)
    writer.writerows(data_list)

f.close()