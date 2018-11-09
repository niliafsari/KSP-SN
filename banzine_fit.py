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

def func(t, t0, tfall,trise, A,B):
    return A*(np.exp(-(t-t0)/tfall)/(np.exp((t-t0)/trise)+1))+B

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
magB[:,4]=magB[:,4]-3.58867256944e+02-0.12
magV[:,4]=magV[:,4]-3.58867256944e+02-0.12
magI[:,4]=magI[:,4]-3.58867256944e+02-0.12

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
    #need to correct for K correction
    # kcorr, mask = s.model.kcorr(band[i],t[i]-s.Tmax)
    # kcorr_val = kcorr[mask]
    # kcorr_inval = np.zeros(len(kcorr[np.invert(mask)]))
    # kcorr = np.concatenate([kcorr_inval, kcorr_val], axis=0)
    F[i], F_err[i] = absFlux(F[i]*10.0**-6, z, appFlux_err=F_err[i]*10.0**-6, z_err=zerr)
    F[i], F_err[i] = F[i]*10**6, F_err[i]*10**6
    Flim[i] = Mag_toFlux(band_rev[int(band[i])], absMag(deredMag(Mlim[i], EBVgal,coef[int(band[i])]), z))*10**6 #in uJy
    #peak abs fluxes
    maxes[i] = Mag_toFlux(band_rev[int(band[i])],maxes[i])*10**6 #in uJy
    #get Max centered dilated time
    #t[i] = absTime(t[i]-s.Tmax, z)
#
print "Converting early LC to rest frame normalized luminosity"
#scale luminosity as fraction of max lum
L_err = [l/maxes[i] for i, l in enumerate(F_err)]
L = [l/maxes[i] for i, l in enumerate(F)]
Llim = [l/maxes[i] for i, l in enumerate(Flim)]
#
# print "plotting early data"
# #plot

#
# print "Fitting power law to section of early light curve"
# # #for each band crop to right section
f = 55#fit up to 40% of maximum flux (Olling 2015)

L_err = [lerr[t[i]<f] for i, lerr in enumerate(L_err)]
L = [l[t[i]<f] for i,l in enumerate(L)]
Llim=[l[t[i]<f] for i,l in enumerate(Llim)]
t = [time[time<f] for time in t]

f = 0#fit up to 40% of maximum flux (Olling 2015)

L_err = [lerr[t[i]>f] for i, lerr in enumerate(L_err)]
L = [l[t[i]>f] for i,l in enumerate(L)]
Llim=[l[t[i]>f] for i,l in enumerate(Llim)]
t = [time[time>f] for time in t]

# tc=t
# Llimc=Llim
# LL=L
# #fit up to 40% of maximum flux (Olling 2015)
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
randomdataY = [L]

#L_err=[np.ones(shape=l.shape)*0.05 for l in L_err]
p0 = [-0.5, 0.14790311668495584, 0.13297572161885188, 0.075625766346250234, 1.5252380308464539]
for j in range(n):
    print str(j+1)+"/"+str(n)
    L_pert = []
    for i in range(len(t)):
        L_pert.append(L[i] + np.random.normal(0., L_err[i]/1.0, len(L[i])))
    randomdataY.append(L_pert)
print "Fitting bootstrap using 4 processes"
x, err_x = fit_bootstrap(p0, t, randomdataY, L_err, earlyMultiErr, errfunc=True, perturb=False, n=3000, nproc=4)
print "Fitting bootstrap using better initial parameters"
x, err_x = fit_bootstrap(x, t, randomdataY, L_err, earlyMultiErr, errfunc=True, perturb=False, n=3000, nproc=4)
#
# #interpret results
# t0, t0_err = x[0], err_x[0]
# C = [x[1],x[2],x[3]]
# C_err = [err_x[1],err_x[2],err_x[3]]
# a = [x[4],x[4],x[4]]
# a_err = [err_x[4],err_x[4],err_x[4]]
# x2dof = np.sqrt(np.square(earlyMultiErr(x, t, L, L_err)).sum())/(len(L[0])+len(L[1])+len(L[2])-len(x))
#
#
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
# tT = np.linspace(t[0][0]-10, t[0][-1]+10, 1000)
# LT = [earlyFit(tT,t0,C[0],a[0]),earlyFit(tT,t0,C[1],a[1]),earlyFit(tT,t0,C[2],a[2])]
# t1_early=-4
# t2_early=5.5
# #plot fit
#
#     #plot fluxes
# ax.errorbar(t[0],L[0],L_err[0]*1.6,fmt='b+',label=r'$B$')
# ax.plot(tT, LT[0], 'b-')
# ax.scatter(tc[0][tc[0]<0], Llimc[0][tc[0]<0], c='b', marker='v',s=9, alpha=0.6)
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
# plt.legend()
# plt.show()
