import numpy as np
import csv
from astropy.time import Time
from moon import *

in_filename='N2188-V_v2.csv'
out_filename="N2188-V_v2_edit.csv"
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
# ,'N2188-1.Q2.V.170402_1925.S.001873.061035N3413.0060.nh.fits']
#
# for file in torem:
#     index=mydict_rev[file]
#     data=data[data[:,3] != int(index)]

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

tt=[l[1] for l in data_list]
T=[moon_illumination(Time(t, format='isot', scale='utc')) for t in tt]
i=0

for l in data_list:
    l.append(str(T[i]))
    i=i+1


with open("phot_csv/"+out_filename, "wb") as f:
    writer = csv.writer(f)
    writer.writerows(data_list)

f.close()