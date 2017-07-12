import numpy as np
import csv
from astropy.time import Time
from moon import *

in_filename='N2188-I_v2.csv'
out_filename="N2188-I_v2_edit.csv"
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

# torem=['N2188-1.Q2.I.170131_1113.A.043573.061035N3413.0060.nh.fits'
# ,'N2188-1.Q2.I.170211_1346.A.044455.061035N3413.0060.nh.fits'
# ,'N2188-1.Q2.I.170309_0217.C.060756.061035N3413.0060.nh.fits'
# ,'N2188-1.Q2.I.170315_0959.A.049330.061035N3413.0060.nh.fits'
# ,'N2188-1.Q2.I.170315_1107.A.049361.061035N3413.0060.nh.fits'
# , 'N2188-1.Q2.I.161121_1724.A.034145.061035N3413.0060.nh.fits'
# ,'N2188-1.Q2.I.161121_1726.A.034146.061035N3413.0060.nh.fits'
# ,'N2188-1.Q2.I.170223_1941.S.057839.061035N3413.0060.nh.fits'
# ,'N2188-1.Q2.I.161116_0132.S.041475.061035N3413.0060.nh.fits'
# ,'N2188-1.Q2.I.161120_0033.S.042069.061035N3413.0060.nh.fits'
# ,'N2188-1.Q2.V.170121_2020.S.052068.061035N3413.0060.nh.fits']
#
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