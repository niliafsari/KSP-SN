import numpy as np
import csv
from astropy.time import Time
import matplotlib.pyplot as plt
import matplotlib



my_file = open("/home/afsari/PycharmProjects/kspSN/phot_csv/goodness_csm_niagara_0.1.csv", "r")
reader = csv.reader(my_file, delimiter=',')
my_list = list(reader)
my_file.close()
print my_list
my_list=[rows+[str(index)] for index,rows in enumerate(my_list)]
print my_list
mydict1 = {rows[3]:rows[0] for rows in my_list}
mydict_rev = {rows[0]:rows[3] for rows in my_list}

data = np.asarray(my_list)
data[:,0]=data[:,3]
data=np.delete(data,3,1)

data=np.array([np.array(xi,dtype=float) for xi in data])

z = np.zeros(shape=(np.shape(data)[0], 2))

data=np.c_[data, z]



for index,rows in enumerate(my_list):
    content=rows[0].split('_')
    #print content
    data[index, 3]=float(content[1])
    data[index, 4]=float(content[3])

#print data[np.argmin(data[:,1]),0],data[np.argmin(data[:,1]),2]



data=data[data[:,1].argsort()]

scale=data[0,1]
data[:,1]=data[:,1]/data[0,1]

solar_radius = 6.96e10
solar_mass = 1.99e33
#model_radius = 72567442288907.27
model_radius = 0.5694193820696878e014
model_radius = 86493739248921.08
model_radius =   72567442288907.27
model_radius_solar = model_radius / solar_radius
rad = np.arange(model_radius_solar + 2, 3800, 100)
rad_solar = rad * solar_radius
K = np.arange(1.0e17, 3.0e18, 1.0e17)

plt.rc('text', usetex=True)
plt.rc('font', family='serif')
print data
x1, y1 = np.meshgrid(rad,K)
from scipy.interpolate import griddata
grid = griddata(zip(data[:,3],data[:,4]),np.log10(data[:,1]), (x1, y1), method='nearest')
x=np.arange(model_radius_solar + 2, 3800, 100)
y=np.arange(1.0e17, 3.0e18, 1.0e17)
f3=np.argmin(data[:,1])
print data[f3,0],data[f3,1]*scale,data[f3,2],data[f3,3],data[f3,4], "hi"
#print mydict1[str(int(data[np.argmin(data[:,1]),0]))], data[np.argmin(data[:,1]),2]
#print mydict_rev
for u,i in enumerate(x):
    for v,j in enumerate(y):
        dir_name = 's%(num)2.1f_%(radius)i_K_%(cons).2E_mni0.1' % {"num": 18.8, "radius": np.floor(i), "cons": j}
        try:
            s= mydict_rev[str(dir_name)], dir_name
            if np.all(np.in1d( [int(mydict_rev[dir_name])],data[:, 0]))==False:
                grid[v, u] = np.nan
        except:
            grid[v, u] = np.nan

ax1 = plt.subplot(111)
sc=plt.pcolormesh(rad,K,grid, cmap='jet_r',vmin=np.nanmin(grid), vmax=np.nanmax(grid))
sc.cmap.set_under('white')
bbox_props = dict(boxstyle="rarrow,pad=0.3", fc="black", ec="black", lw=2)
t = ax1.text(data[f3,3],data[f3,4], "hey", ha="center", va="center", rotation=90,
            size=3,
            bbox=bbox_props)
bb = t.get_bbox_patch()
bb.set_boxstyle("square", pad=0.3)
import matplotlib.patches as mpatch




cb=plt.colorbar(sc)
cb.set_label(r'$\text{ln} \chi^2 / \chi_\min^2$', rotation=270)
#plt.title(r"^{56} \text{Ni}_\text{mixing}=3 [M_\odot]")
plt.xlabel(r'$R_{CSM} [R_\odot]$')
plt.ylabel('K')


plt.show()

