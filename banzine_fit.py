import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import matplotlib
import os
import sys
sys.path.insert(0, '/home/afsari/')
from matplotlib.ticker import AutoMinorLocator


from scipy.optimize import curve_fit
from scipy.optimize import leastsq

#essential files
from SNAP4.Analysis.LCRoutines import*
from SNAP4.Analysis.LCFitting import*
from SNAP2.Analysis.Cosmology import*
#from ObjData import *
matplotlib.rcParams['axes.linewidth'] = 1.5 #set the value globally
matplotlib.rcParams['xtick.major.size'] = 5
matplotlib.rcParams['xtick.major.width'] = 2
matplotlib.rcParams['xtick.minor.size'] = 2
matplotlib.rcParams['xtick.minor.width'] = 1.5
matplotlib.rcParams['ytick.major.size'] = 5
matplotlib.rcParams['ytick.major.width'] = 2
matplotlib.rcParams['ytick.minor.size'] = 2
matplotlib.rcParams['ytick.minor.width'] = 1.5
matplotlib.rcParams.update({'font.size': 21})
matplotlib.rc('text', usetex=True)

def func(t, t0, a, n):
    return a*((t-t0)**n)

def benzine(t, tfall,trise, A,B):
    t0=0
    return A*(np.exp(-(t-t0)/tfall)/(np.exp((t-t0)/trise)+1))+B

t=np.linspace(0.5,55,10)
p=[  9.97527891e-03 , -1.58440654e+01 ,  3.07510967e-01 ,  7.68485856e-01]
print benzine(t,p[0],p[1],p[2],p[3])
# sn_name="KSPN2188_v1"
# magB = np.load("/home/afsari/PycharmProjects/kspSN/phot_csv/compiledSN_B_KSPN2188_v1.npy")
# magV = np.load("/home/afsari/PycharmProjects/kspSN/phot_csv/compiledSN_" + "V" + "_" + sn_name + ".npy")
# magI = np.load("/home/afsari/PycharmProjects/kspSN/phot_csv/compiledSN_" + "I" + "_" + sn_name + ".npy")


current_path=os.path.dirname(os.path.abspath(__file__))
magB = np.genfromtxt(current_path+ '/phot_csv/N2188-B_v12_edit.csv', delimiter=',')
magV = np.genfromtxt(current_path+'/phot_csv/N2188-V_v12_edit.csv', delimiter=',')
magI = np.genfromtxt(current_path+'/phot_csv/N2188-I_v12_edit.csv', delimiter=',')

coef = {0: 4.315, 1: 4.315, 2: 3.315, 3: 1.940, 4: 2.086}
coef = {1: 3.626, 2: 2.742, 3: 1.505, 4: 1.698}
magB[:,4]=magB[:,4]-3.58867256944e+02+0.12
magV[:,4]=magV[:,4]-3.58867256944e+02+0.12
magI[:,4]=magI[:,4]-3.58867256944e+02+0.12

# t1=-1
# t2=4

bands = {'U':0, 'B':1, 'V':2, 'R':3, 'I':4}
band_rev = {0:'U', 1:'B', 2:'V', 3:'R', 4:'I'}
fluxes = [1564, 4023, 3562, 2814, 2282]
fluxes = [flux*1e6 for flux in fluxes]

F=[magB[:,7]]
F.append(magV[:,7])
F.append(magI[:,7])

F_err=[np.divide(magB[:,7],magB[:,8])]
F_err.append(np.divide(magV[:,7],magV[:,8]))
F_err.append(np.divide(magI[:,7],magI[:,8]))

t=[magB[:,4]]
t.append(magV[:,4])
t.append(magI[:,4])

Mlim=[magB[:,11]]
Mlim.append(magV[:,11])
Mlim.append(magI[:,11])

band=[1, 2, 3]
maxes=[-17.40 , -17.6, -17.92]
print len(F)

EBVgal=0.029
z=0.042
zerr=0.002
Flim = Mlim
for i in range(len(F)):
    F[i] = deredFlux(F[i], EBVgal, coef[int(band[i])])
    F_err[i] = deredFlux(F_err[i], EBVgal, coef[int(band[i])])
    F[i], F_err[i] = absFlux(F[i]*10.0**-6, z, appFlux_err=F_err[i]*10.0**-6, z_err=zerr)
    F[i], F_err[i] = F[i]*10**6, F_err[i]*10**6
    Flim[i] = Mag_toFlux(band_rev[int(band[i])], absMag(deredMag(Mlim[i], EBVgal,coef[int(band[i])]), z))*10**6 #in uJy
    maxes[i] = Mag_toFlux(band_rev[int(band[i])],maxes[i])*10**6 #in uJy

print "Converting early LC to rest frame normalized luminosity"
#scale luminosity as fraction of max lum
L_err = [l/maxes[i] for i, l in enumerate(F_err)]
L = [l/maxes[i] for i, l in enumerate(F)]
Llim = [l/maxes[i] for i, l in enumerate(Flim)]


f = 0.5#fit up to 40% of maximum flux (Olling 2015)

L_err = [lerr[t[i]>=f] for i, lerr in enumerate(L_err)]
L = [l[t[i]>=f] for i,l in enumerate(L)]
Llim=[l[t[i]>=f] for i,l in enumerate(Llim)]
t = [time[time>=f] for time in t]


f = 80#fit up to 40% of maximum flux (Olling 2015)

L_err = [lerr[t[i]<f] for i, lerr in enumerate(L_err)]
L = [l[t[i]<f] for i,l in enumerate(L)]
Llim=[l[t[i]<f] for i,l in enumerate(Llim)]
t = [time[time<f] for time in t]

f = 35#fit up to 40% of maximum flux (Olling 2015)

L_err[0:2] = [lerr[t[i]<f] for i, lerr in enumerate(L_err[0:2])]
L[0:2] = [l[t[i]<f] for i,l in enumerate(L[0:2])]
Llim[0:2]=[l[t[i]<f] for i,l in enumerate(Llim[0:2])]
t[0:2] = [time[time<f] for time in t[0:2]]


t = [time[(L[i]>Llim[i]) ] for i, time in enumerate(t)]
L_err = [ lerr[(L[i]>Llim[i])] for i, lerr in enumerate(L_err)]
L = [l[(l>Llim[i])] for i,l in enumerate(L)]

t = [time[(L[i]<1.3) ] for i, time in enumerate(t)]
L_err = [ lerr[(L[i]<1.3)] for i, lerr in enumerate(L_err)]
L = [l[(l<1.3)] for i,l in enumerate(L)]
#
#
# f = -0.4#fit up to 40% of maximum flux (Olling 2015)
# t = [time[L[i]>f] for i, time in enumerate(t)]
# L_err = [lerr[L[i]>f] for i, lerr in enumerate(L_err)]
# #Llim = [lerr[L[i]>f] for i, lerr in enumerate(Llim)]
# L = [l[l>f] for l in L]
#
#
# f = 1 #fit up to 40% of maximum flux (Olling 2015)
# t = [time[L[i]<f] for i, time in enumerate(t)]
# L_err = [lerr[L[i]<f] for i, lerr in enumerate(L_err)]
# #Llim = [lerr[L[i]<f] for i, lerr in enumerate(Llim)]
# L = [l[l<f] for l in L]

for i,l in enumerate(t):
    ind=np.argsort(l)
    t[i]=t[i][ind]
    L[i]=L[i][ind]
    L_err[i]=L_err[i][ind]


# f, ax = plt.subplots(3, sharex=True)
# ax[-1].set_xlabel("t rest [days]")
# ax[1].set_ylabel("L/Lmax")
# print len(t)
# for i in range(len(t)):
#     #early light curve
#     ax[i].errorbar(t[i],L[i],L_err[i],fmt='g+')
#     #ax[i].scatter(t[i],Llim[i],c='r',marker='v')
# plt.show()

#for each band, perturb flux by flux errors
n = 10000 #number of perturbations
#randomdataY = [L]

#L_err=[np.ones(shape=l.shape)*0.05 for l in L_err]
# L_pert = []
# for j in range(n):
#     L_pert.append(L[0] + np.random.normal(0., L_err[0]/1.0, len(L[0])))

# randomdataY = L[0]
# print randomdataY, L_err[0].shape
randomdataY=[[L[0]]]
L_err=[np.ones(shape=l.shape)*0.1 for l in L_err]
for j in range(n):
    L_pert = []
    for i in [0]:
        L_pert.append(L[i] + np.random.normal(0., L_err[i]/1.0, len(L[i])))
    randomdataY.append(L_pert)
p0 = [10, 5, 1, 0.1]
print "Fitting bootstrap using 4 processes"
x, err_x = fit_bootstrap(p0, t[0], randomdataY, L_err[0], benzineErr, errfunc=True, perturb=False, n=3000, nproc=4)
print "Fitting bootstrap using better initial parameters"
x_B, err_x_B = fit_bootstrap(x, t[0],randomdataY, L_err[0], benzineErr, errfunc=True, perturb=False, n=3000, nproc=4)
print x_B
randomdataY=[[L[1]]]
for j in range(n):
    L_pert = []
    for i in [1]:
        L_pert.append(L[i] + np.random.normal(0., L_err[i]/1.0, len(L[i])))
    randomdataY.append(L_pert)

print "Fitting bootstrap using 4 processes"
x, err_x = fit_bootstrap(x_B, t[1], randomdataY, L_err[1], benzineErr, errfunc=True, perturb=False, n=3000, nproc=4)
print "Fitting bootstrap using better initial parameters"
x_V, err_x_V = fit_bootstrap(x, t[1], randomdataY, L_err[1], benzineErr, errfunc=True, perturb=False, n=3000, nproc=4)
print x_V


randomdataY=[[L[2]]]
for j in range(n):
    L_pert = []
    for i in [2]:
        L_pert.append(L[i] + np.random.normal(0., L_err[i]/1.0, len(L[i])))
    randomdataY.append(L_pert)


print "Fitting bootstrap using 4 processes"
x, err_x = fit_bootstrap(x_V, t[2], randomdataY, L_err[2], benzineErr, errfunc=True, perturb=False, n=3000, nproc=4)
print "Fitting bootstrap using better initial parameters"
x_I, err_x_I = fit_bootstrap(x, t[2], randomdataY, L_err[2], benzineErr, errfunc=True, perturb=False, n=3000, nproc=4)

tBaz_B=x_B[1]*np.log(-x_B[1]/(x_B[0]+x_B[1]))
tBaz_V=x_V[1]*np.log(-x_V[1]/(x_V[0]+x_V[1]))
tBaz_I=x_I[1]*np.log(-x_I[1]/(x_I[0]+x_I[1]))

def max_ben(trise,tfall,t0):
    return t0+trise*np.log(-trise/(trise+tfall))

print 0.07**2
print ((err_x_B[1]**2)*((np.log(-x_B[1]/(x_B[0]+x_B[1]))+(1-(x_B[1]/(x_B[0]+x_B[1]))))**2)),(err_x_B[1]**2),((np.log(-x_B[1]/(x_B[0]+x_B[1]))+(1-(x_B[1]/(x_B[0]+x_B[1]))))**2)
print ((err_x_B[0]**2)*(x_B[1]/(x_B[0]+x_B[1]))**2),(err_x_B[0]**2),(x_B[1]/(x_B[0]+x_B[1]))**2

print err_x_B
trise_B_pert=x_B[1] + np.random.normal(0.,err_x_B[1]/1.0,100000)
tfall_B_pert=x_B[0] + np.random.normal(0.,err_x_B[0]/1.0,100000)
tpeak=max_ben(trise_B_pert,tfall_B_pert,0)
tpeak=tpeak[~np.isnan(tpeak)]
print np.nanmedian(tpeak), np.nanstd(tpeak)

trise_B_pert=x_V[1] + np.random.normal(0.,err_x_V[1]/1.0,100000)
tfall_B_pert=x_V[0] + np.random.normal(0.,err_x_V[0]/1.0,100000)
tpeak=max_ben(trise_B_pert,tfall_B_pert,0)
print np.nanmedian(tpeak), np.nanstd(tpeak)

trise_B_pert=x_I[1] + np.random.normal(0.,err_x_I[1]/1.0,100000)
tfall_B_pert=x_I[0] + np.random.normal(0.,err_x_I[0]/1.0,100000)
tpeak=max_ben(trise_B_pert,tfall_B_pert,0)
print np.nanmedian(tpeak), np.nanstd(tpeak)

tBaz_B_err=np.sqrt(0.07**2+((err_x_B[1]**2)*((np.log(-x_B[1]/(x_B[0]+x_B[1]))+(1-(x_B[1]/(np.abs(x_B[0])+x_B[1]))))**2))+((err_x_B[0]**2)*(x_B[1]/(np.abs(x_B[0])+x_B[1]))**2))
print "tBaz_B",tBaz_B,"tBaz_V",tBaz_V,"tBaz_I",tBaz_I, tBaz_B_err

# #output data
# print ""
# print "Epoch of first light in rest frame:", t0, t0_err
# print "Epoch of first light in obs frame:", t0*(1.0+z), np.absolute(t0*(1.0+z)*np.sqrt(np.square(zerr/(1.0+z))+np.square(t0_err/t0)))
# print "Coefficient", C, C_err
# print "Power:", a, a_err
# print "Fit Chi2/dof", x2dof
# print ""
#
# print "Plotting early fit"
# #plot
# f, ax = plt.subplots(1, sharex=True)
# ax.set_xlabel("Time from first detection [days]", fontsize = 20)
# ax.set_ylabel("Normalized Flux", fontsize = 20)
# #best fit curves
tT = np.linspace(0, 80, 1000)
# LT = [earlyFit(tT,t0,C[0],a[0]),earlyFit(tT,t0,C[1],a[1]),earlyFit(tT,t0,C[2],a[2])]
# t1_early=-4
# t2_early=5.5
# #plot fit
#
#     #plot fluxes
ax=plt.subplot(111)
ax.errorbar(t[0],L[0],L_err[0],fmt='b+',label=r'$B$')
ax.plot(tT, benzine(tT,x_B[0],x_B[1],x_B[2],x_B[3]), 'b-')
ax.errorbar(t[1],L[1],L_err[1],fmt='g+',label=r'$V$')
ax.plot(tT, benzine(tT,x_V[0],x_V[1],x_V[2],x_V[3]), 'g-')
ax.errorbar(t[2],L[2],L_err[2],fmt='r+',label=r'$V$')
tT = np.linspace(0, 80, 1000)
ax.plot(tT, benzine(tT,x_I[0],x_I[1],x_I[2],x_I[3]), 'r-')
ax.set_xlabel("Time since SBO [days]", fontsize = 14)
ax.set_ylabel("Normalized Flux", fontsize = 14)
plt.tight_layout()
ax.yaxis.set_minor_locator(AutoMinorLocator(2))
ax.xaxis.set_minor_locator(AutoMinorLocator(10))
ax.xaxis.set_tick_params(width=1.5)
ax.yaxis.set_tick_params(width=1.5)
plt.legend(loc='best')
plt.show()
#ax.scatter(tc[0][tc[0]<0], Llimc[0][tc[0]<0], c='b', marker='v',s=9, alpha=0.6)
#
# ax.errorbar(t[1],L[1],L_err[1]*1.6,fmt='g+',label=r'$V$')
# ax.plot(tT, LT[1], 'g-')
# ax.scatter(tc[1][tc[1]<0], Llimc[1][tc[1]<0], c='g', marker='v',s=9, alpha=0.6)
#
# ax.errorbar(t[2],L[2],L_err[2]*1.6,fmt='r+',label=r'$I$')
# ax.plot(tT, LT[2], 'r-')
# ax.scatter(tc[2][tc[2]<0], Llimc[2][tc[2]<0], c='r', marker='v',s=9, alpha=0.6)
# ax.set_xlim(t1_early, t2_early)
# ax.set_ylim(-0.1,1.2)
# y=np.arange(-1, 1.3,0.01)
# ax.fill_betweenx(y, x1=-t0_err+t0, x2=t0_err+t0, color='yellow', alpha=0.35, zorder=0)
# ax.text(t0+0.05,0.9 ,r'$t_{\rm exp}$', fontsize=16,rotation=0,multialignment='center',va='center')
# #ax.text(0.5,0.1 ,r'$I=C(t-t_0)^{0.51\pm 0.17}$', fontsize=13,rotation=0,multialignment='center',va='center')
# ax.plot([t0,t0], [-10,30], 'k:', linewidth=2)
# # ax.plot([t0+t0_err,t0+t0_err], [-10,30], 'k:', linewidth=2)
# # ax.plot([t0-t0_err,t0-t0_err], [-10,30], 'k:', linewidth=2)
# ax.yaxis.set_minor_locator(AutoMinorLocator(5))
# ax.xaxis.set_minor_locator(AutoMinorLocator(10))
# ax.xaxis.set_tick_params(width=1.5)
# ax.yaxis.set_tick_params(width=1.5)
# ax.locator_params(axis='y', nbins=6)
# ax.locator_params(axis='x', nbins=10)
# plt.legend(fontsize=15)
# plt.tight_layout()
# plt.subplots_adjust(wspace=0, hspace=0)
# plt.show()

#plot residuals
# f, ax = plt.subplots(3, sharex=True)
# ax[-1].set_xlabel("Days from peak", fontsize = 14)
# ax[1].set_ylabel("Normalized Flux", fontsize = 14)
# for i in range(len(t)):
#     #plot residuals
#     ax[i].errorbar(t[i],L[i]-earlyFit(t[i],t0,C[i],a[i]),2*L_err[i],fmt='g+')
#     #ax[i].scatter(t[i],Llim[i]-earlyFit(t[i],*popts[i]),c='r',marker='v')
#     ax[i].plot(tT,[0]*len(tT),label='power fit')
#     ax[i].set_xlim(t1_early, t2_early)
#     ax[i].set_ylim(-0.095,0.095)
# ax[0].text(-18,0.05,'B', fontsize = 14, fontstyle='italic', fontweight='bold')
# ax[1].text(-18,0.05,'V', fontsize = 14, fontstyle='italic', fontweight='bold')
# ax[2].text(-18,0.05,'I', fontsize = 14, fontstyle='italic', fontweight='bold')
# f.subplots_adjust(hspace=0)
# plt.tight_layout()
# plt.show()



# magB[(magB[:,4]>t1) & (magB[:,4]<0),7]= fluxes[bands['B']]*np.power(10,-magB[(magB[:,4]>t1) & (magB[:,4]<0),11]/2.512)
# magB[(magB[:,4]>t1) & (magB[:,4]<0),8]=magB[(magB[:,4]>t1) & (magB[:,4]<0),7]
# print magB[(magB[:,4]>t1) & (magB[:,4]<0),7]
# print magB[(magB[:,4]>t1) & (magB[:,4]<0),8]
#
# print magB[:,4][(magB[:,4]>t1) & (magB[:,4]<t2)]
# print magB[:,7][(magB[:,4]>t1) & (magB[:,4]<t2)]
# print magB[:,8][(magB[:,4]>t1) & (magB[:,4]<t2)]

#print magB[(magB[:,4]>t1) & (magB[:,4]<2),7], magB[(magB[:,4]>t1) & (magB[:,4]<2),11]
#magB=np.deletmagB[(magB[:,4]>t1) & (magB[:,4]<0),7]e(magB,magB[:,7]<17,axis=0)
#print np.nanmax(magB[:,7][(magB[:,9] < magB[:,11])])
#magV[np.where(magB[:,7]<17)]=[]

# popt, pcov = curve_fit(func, magB[:,4][(magB[:,4]>t1) & (magB[:,4]<t2)],magB[:,7][(magB[:,4]>t1) & (magB[:,4]<t2)],sigma=np.divide(magB[:,7][(magB[:,4]>t1) & (magB[:,4]<t2)],magB[:,8][(magB[:,4]>t1) & (magB[:,4]<t2)]),
#                         p0=[-0.5, 1, 2], maxfev=1000000,bounds=([-10,-np.infty,0],[0,np.infty,10]))
# print popt
# t=np.linspace(-3,t2,200)
# plt.errorbar(magB[:,4][(magB[:,4]>t1) & (magB[:,4]<t2)& (magB[:,9] < magB[:,11])],magB[:,7][(magB[:,4]>t1) & (magB[:,4]<t2)& (magB[:,9] < magB[:,11])],yerr=np.sqrt(np.divide(magB[:,7][(magB[:,4]>t1) & (magB[:,4]<t2)& (magB[:,9] < magB[:,11])],magB[:,8][(magB[:,4]>t1) & (magB[:,4]<t2)& (magB[:,9] < magB[:,11])])),fmt='o',color='b',label='B data')
# plt.plot(t, func(t, *popt),color='lightblue',label='fit: t0=%5.3f, a=%5.3f, n=%5.3f' % tuple(popt))
#
# magB=magV
#
# popt, pcov = curve_fit(func, magB[:,4][(magB[:,4]>t1) & (magB[:,4]<t2)& (magB[:,9] < magB[:,11])],magB[:,7][(magB[:,4]>t1) & (magB[:,4]<t2)& (magB[:,9] < magB[:,11])],sigma=np.divide(magB[:,7][(magB[:,4]>t1) & (magB[:,4]<t2)& (magB[:,9] < magB[:,11])],magB[:,8][(magB[:,4]>t1) & (magB[:,4]<t2)& (magB[:,9] < magB[:,11])]),
#                         p0=[-0.5, 1, 2], maxfev=1000000,bounds=([-10,-np.infty,0],[0,np.infty,10]))
# print popt
# t=np.linspace(-3,t2,200)
# plt.errorbar(magB[:,4][(magB[:,4]>t1) & (magB[:,4]<t2)& (magB[:,9] < magB[:,11])],magB[:,7][(magB[:,4]>t1) & (magB[:,4]<t2)& (magB[:,9] < magB[:,11])],yerr=np.sqrt(np.divide(magB[:,7][(magB[:,4]>t1) & (magB[:,4]<t2)& (magB[:,9] < magB[:,11])],magB[:,8][(magB[:,4]>t1) & (magB[:,4]<t2)& (magB[:,9] < magB[:,11])])),fmt='o',color='g',label='V data')
# plt.plot(t, func(t, *popt),color='lightgreen',label='fit: t0=%5.3f, a=%5.3f, n=%5.3f' % tuple(popt))
#
# magB=magI
#
# popt, pcov = curve_fit(func, magB[:,4][(magB[:,4]>t1) & (magB[:,4]<t2)& (magB[:,9] < magB[:,11])],magB[:,7][(magB[:,4]>t1) & (magB[:,4]<t2)& (magB[:,9] < magB[:,11])],sigma=np.divide(magB[:,7][(magB[:,4]>t1) & (magB[:,4]<t2)& (magB[:,9] < magB[:,11])],magB[:,8][(magB[:,4]>t1) & (magB[:,4]<t2)& (magB[:,9] < magB[:,11])]),
#                         p0=[-0.5, 1, 2], maxfev=1000000,bounds=([-2,-np.infty,0],[0,np.infty,10]))
# print popt
# t=np.linspace(-3,t2,200)
# plt.errorbar(magB[:,4][(magB[:,4]>t1) & (magB[:,4]<t2)& (magB[:,9] < magB[:,11])],magB[:,7][(magB[:,4]>t1) & (magB[:,4]<t2)& (magB[:,9] < magB[:,11])],yerr=np.sqrt(np.divide(magB[:,7][(magB[:,4]>t1) & (magB[:,4]<t2)& (magB[:,9] < magB[:,11])],magB[:,8][(magB[:,4]>t1) & (magB[:,4]<t2)& (magB[:,9] < magB[:,11])])),fmt='o',color='r',label='I data')
# plt.plot(t, func(t, *popt),color='pink',label='fit: t0=%5.3f, a=%5.3f, n=%5.3f' % tuple(popt))



#plt.axis([-1,t2+1,0,100])
#
# plt.show()
