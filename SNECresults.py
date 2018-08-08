import numpy as np
import csv
from astropy.time import Time
import matplotlib.pyplot as plt
import matplotlib

from matplotlib.ticker import AutoMinorLocator

matplotlib.rcParams.update({'font.size': 24})
matplotlib.rcParams['axes.linewidth'] = 1.5 #set the value globally
matplotlib.rcParams['xtick.major.size'] = 5
matplotlib.rcParams['xtick.major.width'] = 2
matplotlib.rcParams['xtick.minor.size'] = 2
matplotlib.rcParams['xtick.minor.width'] = 1.5
matplotlib.rcParams['ytick.major.size'] = 5
matplotlib.rcParams['ytick.major.width'] = 2
matplotlib.rcParams['ytick.minor.size'] = 2
matplotlib.rcParams['ytick.minor.width'] = 1.5
plt.rc('text', usetex=True)
my_file = open("/home/afsari/PycharmProjects/kspSN/phot_csv/goodness_niagara_0.1.csv", "r")
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

z = np.zeros(shape=(np.shape(data)[0], 3))

data=np.c_[data, z]



for index,rows in enumerate(my_list):
    content=rows[0].split('_')
    data[index, 3]=float(content[0].strip('s'))
    data[index, 4]=float(content[2])
    data[index, 5]=float(content[4])

print data[np.argmin(data[:,1]),0],data[np.argmin(data[:,1]),2]

data_3=data[data[:, 4]==3.0]
data_5=data[data[:, 4]==5.0]
data_7=data[data[:, 4]==7.0]

data_3=data_3[data_3[:,1].argsort()]
data_5=data_5[data_5[:,1].argsort()]
data_7=data_7[data_7[:,1].argsort()]

scale3=data_3[0,1]
scale5=data_5[0,1]
scale7=data_7[0,1]

data_3[:,1]=data_3[:,1]/data_5[0,1]
data_5[:,1]=data_5[:,1]
data_7[:,1]=data_7[:,1]/data_5[0,1]
temp=data_5[:,1]
temp = temp[~np.isnan(temp)]
temp = temp[~np.isinf(1/temp)]
print "quantile 98", 1/np.percentile(1/temp,98)
cut=1/np.percentile(1/temp,98)
cut=np.log10(cut/data_5[0,1])
plt.rc('font', family='serif')
data_5[:,1]=data_5[:,1]/data_5[0,1]

x1, y1 = np.meshgrid(np.arange(11,28,0.6),np.arange(4e49,1.95e51,0.06e51)/1.0e51)
from scipy.interpolate import griddata
grid_3 = griddata(zip(data_3[:,3],data_3[:,5]/1.0e51),np.log10(data_3[:,1]), (x1, y1), method='nearest')
x=np.arange(11,28,0.6)
y=np.arange(4e49,1.95e51,0.06e51)
f3=np.nanargmin(data_3[:,1])
print data_3[f3,1]*scale3,data_3[f3,3],data_3[f3,5]/1.0e51, data_3[f3,2]
f5=np.nanargmin(data_5[:,1])
print data_5[f5,1]*scale5,data_5[f5,3],data_5[f5,5]/1.0e51, data_5[f5,2]
f7=np.nanargmin(data_7[:,1])
print data_7[f7,1]*scale7,data_7[f7,3],data_7[f7,5]/1.0e51, data_7[f7,2]
print mydict1
print mydict1[str(int(data[np.nanargmin(data[:,1]),0]))], data[np.nanargmin(data[:,1]),2]
for u,i in enumerate(x):
    for v,j in enumerate(y):
        dir_name = 's%(num)2.1f_ni56_%(mixing)i_efin_%(efin).2E_mni0.1' % {"num": i, "mixing": 3, "efin": j}
        try:
            s= mydict_rev[dir_name], dir_name
            if np.all(np.in1d( [int(mydict_rev[dir_name])],data_3[:, 0]))==False:
                grid_3[v, u] = np.nan
        except:
            grid_3[v, u] = np.nan

grid_5 = griddata(zip(data_5[:,3],data_5[:,5]/1.0e51),np.log10(data_5[:,1]), (x1, y1), method='nearest')
for u,i in enumerate(x):
    for v,j in enumerate(y):
        dir_name = 's%(num)2.1f_ni56_%(mixing)i_efin_%(efin).2E_mni0.1' % {"num": i, "mixing": 5, "efin": j}
        try:
            s=mydict_rev[dir_name]
            if np.all(np.in1d( [int(mydict_rev[dir_name])],data_5[:, 0]))==False:
                grid_5[v, u] = np.nan
        except:
            grid_5[v, u] = np.nan

grid_7 = griddata(zip(data_7[:,3],data_7[:,5]/1.0e51),np.log10(data_7[:,1]), (x1, y1), method='nearest')
for u,i in enumerate(x):
    for v,j in enumerate(y):
        dir_name = 's%(num)2.1f_ni56_%(mixing)i_efin_%(efin).2E_mni0.1' % {"num": i, "mixing": 7, "efin": j}
        try:
            s=mydict_rev[dir_name]
            if np.all(np.in1d( [int(mydict_rev[dir_name])],data_7[:, 0]))==False:
                grid_7[v, u] = np.nan
        except:
            grid_7[v, u] = np.nan
#
# ax1 = plt.subplot(131)
# sc=plt.pcolormesh(np.arange(11,28,0.6),np.arange(4e49,1.95e51,0.06e51)/1.0e51,grid_3, cmap='jet_r',vmin=np.nanmin(grid_3), vmax=np.nanmax(grid_3))
# sc.cmap.set_under('white')
# bbox_props = dict(boxstyle="rarrow,pad=0.3", fc="black", ec="black", lw=2)
# t = ax1.text(data_3[f3,3],data_3[f3,5]/1.0e51, "hey", ha="center", va="center", rotation=90,
#             size=3,
#             bbox=bbox_props)
# bb = t.get_bbox_patch()
# bb.set_boxstyle("square", pad=0.3)
# import matplotlib.patches as mpatch
#
# plt.clim(0,2.75)


# cb=plt.colorbar(sc)
# cb.set_label(r'\text{ln} \chi^2 / \chi_\min^2', rotation=270)
# plt.title(r"$^{56} Ni_{mixing}=3 [M_\odot]$")
# plt.xlabel(r'M_{ZAMS} [M_\odot]')
# plt.clim(0,2.75)

# ax1.set_xlim([9.8, 28.2])
# ax1.yaxis.set_minor_locator(AutoMinorLocator(5))
# ax1.xaxis.set_minor_locator(AutoMinorLocator(10))
# ax1.xaxis.set_tick_params(width=1.5)
# ax1.yaxis.set_tick_params(width=1.5)
ax2 = plt.subplot(111)
plt.ylabel('E [foe]')
sc=plt.pcolormesh(np.arange(11,28,0.6),np.arange(4e49,1.95e51,0.06e51)/1.0e51,grid_5, cmap='jet_r',vmin=np.nanmin(grid_5), vmax=np.nanmax(grid_5))
sc.cmap.set_under('white')
#ax2.yaxis.set_ticklabels([])
# cb=plt.colorbar(sc)
bbox_props = dict(boxstyle="rarrow,pad=0.3", fc="black", ec="black", lw=2)
# t = ax2.text(data_5[f5,3],data_5[f5,5]/1.0e51, "hey", ha="center", va="center", rotation=90,
#             size=3,
#             bbox=bbox_props)
# bb = t.get_bbox_patch()
# bb.set_boxstyle("square", pad=0.3)
ax2.set_xlim([9.8, 28.2])
ax2.yaxis.set_minor_locator(AutoMinorLocator(5))
ax2.xaxis.set_minor_locator(AutoMinorLocator(10))
ax2.xaxis.set_tick_params(width=1.5)
ax2.yaxis.set_tick_params(width=1.5)
# cb.set_label(r'\text{ln}  \chi^2 / \chi_\min^2', rotation=270)
#plt.title(r"$^{56} \text{Ni}_\text{mixing}=5 [M_\odot]")
plt.xlabel(r'M$_{\rm ZAMS} [\rm M_\odot]$')
# ax3 = plt.subplot(133)
# sc=plt.pcolormesh(np.arange(11,28,0.6),np.arange(4e49,1.95e51,0.06e51)/1.0e51,grid_7, cmap='jet_r',vmin=np.nanmin(grid_7), vmax=np.nanmax(grid_7))
# sc.cmap.set_under('white')
cb=plt.colorbar(sc)
plt.clim(0,2.7)

grid_5[grid_5>cut]=np.nan
#sc=plt.pcolormesh(np.arange(11,28,0.6),np.arange(4e49,1.95e51,0.06e51)/1.0e51,grid_5, cmap='jet_r',hatch=['X'], alpha=0.,vmin=0, vmax=2.7)

#cs = plt.contourf(np.arange(11,28,0.6),np.arange(4e49,1.95e51,0.06e51)/1.0e51,grid_5, hatches=['/'],
                  # cmap=plt.get_cmap('jet_r'),
                  # extend='both', alpha=0.5
                  # )
matplotlib.rcParams['hatch.linewidth'] =1.5
plt.pcolor(np.arange(11,28,0.6),np.arange(4e49,1.95e51,0.06e51)/1.0e51,grid_5, hatch='/////', alpha=0.)
grid_5[grid_5>0]=np.nan
#
plt.pcolor(np.arange(11,28,0.6),np.arange(4e49,1.95e51,0.06e51)/1.0e51,grid_5,cmap="Greys",vmin=-1, vmax=0)

#plt.colorbar()


#cb=plt.colorbar(sc)
#plt.clim(0,0.052)

# bbox_props = dict(boxstyle="rarrow,pad=0.3", fc="black", ec="black", lw=2)
# t = ax3.text(data_7[f7,3],data_7[f7,5]/1.0e51, "hey", ha="center", va="center", rotation=90,
#             size=3,
#             bbox=bbox_props)
# bb = t.get_bbox_patch()
# ax3.yaxis.set_ticklabels([])
# ax3.set_xlim([9.8, 28.2])
# ax3.yaxis.set_minor_locator(AutoMinorLocator(5))
# ax3.xaxis.set_minor_locator(AutoMinorLocator(10))
# ax3.xaxis.set_tick_params(width=1.5)
# ax3.yaxis.set_tick_params(width=1.5)
# bb.set_boxstyle("square", pad=0.3)
cb.set_label(r'$\log (\chi^2 \chi_{\min}^{-2} )$', labelpad=23,rotation=270)
#plt.title(r"^{56} \text{Ni}_\text{mixing}=7 [M_\odot]")
#plt.ylabel('E [foe]')
plt.tight_layout()
#plt.subplots_adjust(hspace=0.1, wspace=0)
plt.show()

