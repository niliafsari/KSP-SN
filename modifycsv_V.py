import numpy as np
import csv
from astropy.time import Time
from moon import *

in_filename='N2188-V_v12.csv'
out_filename="N2188-V_v12_edit.csv"
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
#data=data[data[:,7]<= data[:,9]]

# torem=['N2188-1.Q2.V.170114_0504.C.049355.061035N3413.0060.nh.fits'
# ,'N2188-1.Q2.V.170123_0245.C.051298.061035N3413.0060.nh.fits'
# ,'N2188-1.Q2.V.170131_1111.A.043572.061035N3413.0060.nh.fits'
# ,'N2188-1.Q2.V.170408_0943.A.052640.061035N3413.0060.nh.fits'
# ,'N2188-1.Q2.V.161026_1622.A.029736.061035N3413.0060.nh.fits'
# ,'N2188-1.Q2.V.170119_1906.S.051583.061035N3413.0060.nh.fits'
# ,'N2188-1.Q2.V.170223_1939.S.057838.061035N3413.0060.nh.fits'
# ,'N2188-1.Q2.V.161221_1129.A.038753.061035N3413.0060.nh.fits'
# ,'N2188-1.Q2.V.170402_1925.S.001873.061035N3413.0060.nh.fits'
# ,'N2188-1.Q2.V.170115_1931.S.050842.061035N3413.0060.nh.fits']

in_filename_v2='N2188-V_v12_edit.csv'
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

torem=[]
# for i, index in enumerate(data[:,3]):
#     I=data[i,7]
#     I_err=I/data[i,8]
#     try:
#         I_orig=mydict4_v2[mydict1[str(int(index))]]
#     except:
#         continue
#     I_orig_err=I_orig/mydict5_v2[mydict1[str(int(index))]]
#     if (I)>(I_orig+I_orig_err):
#         torem.append(mydict1[str(int(index))])

# for i, index in enumerate(data[:,3]):
#     I=data[i,7]
#     tt=data[i,4]
#     m=data[i,9]
#     I_err=I/data[i,8]
#     try:
#         name_orig=mydict1[str(int(index))]
#     except:
#         continue
#     if tt>491:
#         torem.append(name_orig)
#     if tt > 454 and m<19.35:
#         torem.append(name_orig)
#     if tt > 484 and m < 21.12:
#         torem.append(name_orig)
#
# print len(torem),torem

rem=['N2188-1.Q2.V.170123_0245.C.051298.061035N3413.0060.nh.fits'
     ,'N2188-1.Q2.V.170115_1931.S.050842.061035N3413.0060.nh.fits'
     ,'N2188-1.Q2.V.170119_2014.S.051613.061035N3413.0060.nh.fits'
     ,'N2188-1.Q2.V.170123_0245.C.051298.061035N3413.0060.nh.fits'
     ,'N2188-1.Q2.V.170211_1344.A.044454.061035N3413.0060.nh.fits'
     ,'N2188-1.Q2.V.170423_0004.C.006241.061035N3413.0060.nh.fits'
     ,'N2188-1.Q2.V.170420_0857.A.055385.061035N3413.0060.nh.fits'
     ,'N2188-1.Q2.V.170408_0943.A.052640.061035N3413.0060.nh.fits'
     ,'N2188-1.Q2.V.170208_1918.S.055443.061035N3413.0060.nh.fits'
     ,'N2188-1.Q2.V.170223_2050.S.057869.061035N3413.0060.nh.fits'
     ,'N2188-1.Q2.V.170330_0946.A.051073.061035N3413.0060.nh.fits'
     ,'N2188-1.Q2.V.170303_1856.S.059847.061035N3413.0060.nh.fits'
     ,'N2188-1.Q2.V.170219_1403.A.045282.061035N3413.0060.nh.fits'
     ,'N2188-1.Q2.V.170218_1150.A.044954.061035N3413.0060.nh.fits'
     ,'N2188-1.Q2.V.170218_1414.A.045020.061035N3413.0060.nh.fits'
     ,'N2188-1.Q2.V.170219_1037.A.045190.061035N3413.0060.nh.fits'
     ,'N2188-1.Q2.V.170218_1046.A.044924.061035N3413.0060.nh.fits'
     ,'N2188-1.Q2.V.170219_1145.A.045220.061035N3413.0060.nh.fits'
     ,'N2188-1.Q2.V.170219_1251.A.045250.061035N3413.0060.nh.fits'
     ,'N2188-1.Q2.V.170120_2001.S.051848.061035N3413.0060.nh.fits'
     ,'N2188-1.Q2.V.170119_1906.S.051583.061035N3413.0060.nh.fits'
     ,'N2188-1.Q2.V.170116_2033.S.050940.061035N3413.0060.nh.fits'
     ,'N2188-1.Q2.V.170120_1852.S.051817.061035N3413.0060.nh.fits'
     ,'N2188-1.Q2.V.170307_1132.A.048078.061035N3413.0060.nh.fits'
     ,'N2188-1.Q2.V.170309_1227.A.048492.061035N3413.0060.nh.fits'
     ,'N2188-1.Q2.V.170309_1945.S.061645.061035N3413.0060.nh.fits'
     ,'N2188-1.Q2.V.170303_1146.A.047416.061035N3413.0060.nh.fits'
     ,'N2188-1.Q2.V.170309_1223.A.048490.061035N3413.0060.nh.fits'
     ,'N2188-1.Q2.V.170309_1219.A.048488.061035N3413.0060.nh.fits'
     ,'N2188-1.Q2.V.170309_2051.S.061675.061035N3413.0060.nh.fits'
     ,'N2188-1.Q2.V.170309_1231.A.048494.061035N3413.0060.nh.fits'
     ,'N2188-1.Q2.V.170112_0352.C.048843.061035N3413.0060.nh.fits']

rem=['N2188-1.Q2.V.170430_1745.S.008590.061035N3413.0060.nh.fits',
     'N2188-1.Q2.V.170514_1720.S.012022.061035N3413.0060.nh.fits',
     'N2188-1.Q2.V.170412_1021.A.053336.061035N3413.0060.nh.fits']

torem=torem+rem

for file in torem:
     index=mydict_rev[file]
     data=data[data[:,3] != int(index)]

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

print data_list

# tt=[l[1] for l in data_list]
# T=[moon_illumination(Time(t, format='isot', scale='utc')) for t in tt]
# i=0

# for l in data_list:
#     l.append(str(T[i]))
#     i=i+1


with open("phot_csv/"+out_filename, "wb") as f:
    writer = csv.writer(f)
    writer.writerows(data_list)

f.close()