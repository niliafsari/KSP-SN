import numpy as np
import sys
sys.path.insert(0, '/home/afsari/')
from SNAP2.Analysis import *
import csv

file_name="phot_csv/N2188-I_v12_edit.csv"
my_file = open(file_name, 'r')
reader = csv.reader(my_file, delimiter=',')
my_list = list(reader)
my_file.close()

data = np.genfromtxt (file_name, delimiter=",")

print data.shape
#data=data[1:][:]
mydict1 = {int(float(rows[3])):rows[0] for rows in my_list}
mydict2 = {int(float(rows[3])):rows[1] for rows in my_list}
mydict3 = {int(float(rows[3])):rows[2] for rows in my_list}
mydict_rev = {rows[0]:rows[3] for rows in my_list}

abs_mag=np.zeros((data.shape[0],2))


for i in xrange(0,data.shape[0]):
    abs_mag[i,0], abs_mag[i,1] = absMag(data[i,9],0.043,data[i,10],0.002)

print abs_mag.shape

data=np.append(data[:,0:12], abs_mag, axis=1)

print data.shape

data_list=data.tolist()
for l in data_list:
    try:
        l[0] = mydict1[int(l[3])]
        l[1] = mydict2[int(l[3])]
        l[2] = mydict3[int(l[3])]
    except:
        l[0] =0
        l[1] = 0
        l[2] = 0




with open(file_name, "wb") as f:
    writer = csv.writer(f)
    writer.writerows(data_list)

f.close()