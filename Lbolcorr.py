from astropy.io import fits
from astropy.wcs import WCS
import numpy as np
#import matplotlib.pyplot as plt
import os
import glob
from findSN import *

import sys

sys.path.insert(0, '/home/afsari/')
from SNAP2.Analysis import *

sys.path.insert(0, '/home/afsari/SuperBoL-master/')
from superbol.luminosity import calc_Lbol
coef = {'B': 4.107, 'V': 2.682, 'I': 1.516, 'i': 1.698}
fluxes = np.array([4023.0* 1000000.0, 3562.0 * 1000000.0, 2282.0 * 1000000.0])

ebv=0.029
dis=5.6153658728e+26 #cm
sn_name="KSPN2188"

magB = np.load("phot_csv/compiledSN_" + "B" + "_" + sn_name + ".npy")
magB = magB.astype(np.float)

u_t = magB[:, 0]
u_t[u_t<370] = np.floor(u_t[u_t<370]*100)/100
u_t[u_t>370]=np.floor(u_t[u_t>370])
index=np.argsort(u_t)
u_t=u_t[index]
print u_t
u = magB[:, 3]
u=u[index]
u_e = magB[:, 4]
u_e=u_e[index]
u_app=magB[:, 1]
u_app_err=magB[:, 2]
u_app=u_app[index]
u_app_err=u_app_err[index]


magV = np.load("phot_csv/compiledSN_" + "V" + "_" + sn_name + ".npy")
magV = magV.astype(np.float)

v_t = magV[:, 0]
v_t[v_t<370] = np.floor(v_t[v_t<370]*100)/100
v_t[v_t>370] = np.floor(v_t[v_t>370])
index=np.argsort(v_t)
v_t=v_t[index]
v = magV[:, 3]
v_app=magV[:, 1]
v_app_err=magV[:, 2]
v_app=v_app[index]
v_app_err=v_app_err[index]

v_e = magV[:, 4]
v_e=v_e[index]

magI = np.load("phot_csv/compiledSN_" + "I" + "_" + sn_name + ".npy")
magI = magI.astype(np.float)
i_t = magI[:, 0]
i_t[i_t<370] = np.floor(i_t[i_t<370]*100)/100
i_t[i_t>370] = np.floor(i_t[i_t>370])
index=np.argsort(i_t)
i_t=i_t[index]
i = magI[:, 3]
i_app=magI[:, 1]
i_app_err=magI[:, 2]
i_app=i_app[index]
i_app_err=i_app_err[index]
i=i[index]
i_e = magI[:, 4]
i_e=i_e[index]

bv_t = np.zeros(shape=(0, 1))
vv = np.zeros(shape=(0, 1))
ve = np.zeros(shape=(0, 1))
bv = np.zeros(shape=(0, 1))
bv_e = np.zeros(shape=(0, 1))
for index,j in enumerate(u_t):
    print j
    if np.min(np.abs(v_t-j))<=0.1:
        sub = np.argmin(np.abs(v_t - j))
        bv_t=np.concatenate((bv_t,v_t[sub].reshape((1,1))))
        bv=np.concatenate((bv,deredMag(u_app[index], ebv, coef["B"])-deredMag(v_app[sub].reshape((1,1)), ebv, coef["V"])))
        vv=np.concatenate((vv,deredMag(v_app[sub].reshape((1,1)), ebv, coef["V"])))
        ve = np.concatenate((ve, v_app_err[sub].reshape((1, 1))))
        bv_e=np.concatenate((bv_e,np.sqrt(np.square(v_e[sub].reshape((1,1)))+np.square(u_e[index].reshape((1,1))))))

vi_t = np.zeros(shape=(0, 1))
vi = np.zeros(shape=(0, 1))
vi_e = np.zeros(shape=(0, 1))
Mv= np.zeros(shape=(0, 1))
Mi= np.zeros(shape=(0, 1))
Mv_err = np.zeros(shape=(0, 1))
for index,j in enumerate(v_t):
    if (np.min(np.abs(i_t-j))<=1 and j>475) or (np.min(np.abs(i_t-j))<=0.1 and j<=475) :
        sub = np.argmin(np.abs(i_t - j))
        vi_t=np.concatenate((vi_t,i_t[sub].reshape((1,1))))
        vi=np.concatenate((vi,v[index].reshape((1,1))-i[sub].reshape((1,1))))
        Mv=np.concatenate((Mv,v[index].reshape((1,1))))
        Mi=np.concatenate((Mi,i[sub].reshape((1,1))))
        vv = np.concatenate((vv, deredMag(v_app[index].reshape((1, 1)), ebv, coef["V"])))
        ve = np.concatenate((ve, v_app_err[index].reshape((1, 1))))
        Mv_err = np.concatenate((Mv_err, v_e[index].reshape((1,1))))
        vi_e=np.concatenate((vi_e,np.sqrt(np.square(i_e[sub].reshape((1,1)))+np.square(v_e[index].reshape((1,1))))))

bi_t = np.zeros(shape=(0, 1))
bi = np.zeros(shape=(0, 1))
bi_e = np.zeros(shape=(0, 1))
Mb = np.zeros(shape=(0, 1))
Mb_err = np.zeros(shape=(0, 1))
for index, j in enumerate(u_t):
    if np.min(np.abs(i_t - j)) <= 0.1:
        sub = np.argmin(np.abs(i_t - j))
        bi_t = np.concatenate((bi_t, i_t[sub].reshape((1, 1))))
        bi = np.concatenate((bi, u[index] - i[sub].reshape((1, 1))))
        Mb = np.concatenate((Mb, u[index].reshape((1, 1))))
        Mb_err = np.concatenate((Mb_err, u_e[index].reshape((1, 1))))
        bi_e = np.concatenate(
            (bi_e, np.sqrt(np.square(i_e[sub].reshape((1, 1))) + np.square(u_e[index].reshape((1, 1))))))

# bv_t_early=bv_t[bv_t<363]
# bv_early=bv[bv_t<363]
# vv_early=vv[bv_t<363]
# z = np.polyfit(bv_t_early, bv_early, 3)
# fit = np.poly1d(z)
# bv_new=fit(bv_t_early)
# z = np.polyfit(bv_t_early, vv_early, 3)
# fit = np.poly1d(z)
# vv_new=fit(bv_t_early)
# print bv_new, vv[bv_t<363]
# bv[bv_t<363]=bv_new
#
# length=np.shape(ve)
# lbol_bc=np.zeros(shape=(length[0],1))
# lbol_bc_err=np.zeros(shape=(length[0],1))
# for k,v_mag in enumerate(vv):
#     lbol_bc[k], lbol_bc_err[k] = calc_Lbol(bv[5], bv_e[k],'BminusV', vv[k],ve[k], dis, 0)
#     print bv[k], lbol_bc[k],v_mag, bv_t[k]
# ax=plt.subplot(111)
#
# plt.scatter(bv_t,lbol_bc,color='blue')
# plt.xlabel('Time [days]')
# plt.ylabel('L_{bol}[erg/s]')
#
# plt.tick_params(labelsize=20)
# plt.show()

length=np.shape(Mv)
lbol_bc=np.zeros(shape=(length[0],1))
Mbol=np.zeros(shape=(length[0],1))
lbol_bc_err=np.zeros(shape=(length[0],1))
Msun=4.83
Lsun=3.9e33
# for k, M_mag in enumerate(Mb):
#     if (bi_t[k]>=363):
#         Mbol[k] = M_mag + 0.004 - 0.297 * (bi[k]) - 0.149 * (np.square(bi[k]))
#     else:
#         Mbol[k] = M_mag - 0.473 + 0.830*bi[k] - 1.064*(np.square(bi[k]))
#     print Mbol[k]
#     lbol_bc[k]=Lsun*np.power(10,((Msun-Mbol[k])/2.5))

vi_t_late=vi_t[vi_t>=474.5]
Mv_late=Mv[vi_t>=474.5]
Mi_late=Mi[vi_t>=474.5]
z = np.polyfit(vi_t_late, Mv_late, 1)
fit = np.poly1d(z)

zz = np.polyfit(vi_t_late, Mi_late, 1)
fit_1 = np.poly1d(zz)
print zz
Mv_new=fit(vi_t_late)
Mi_new=fit_1(vi_t_late)
vi[vi_t>=474.5]=Mv_new-Mi_new
Mv[vi_t>=474.5]=Mv_new

# z = np.polyfit(bv_t_early, vv_early, 3)
# fit = np.poly1d(z)
# vv_new=fit(bv_t_early)
# print bv_new, vv[bv_t<363]
# bv[bv_t<363]=bv_new

#Sn1987a

l1=41.55
l2=41.45

t1=0
t2=20

alpha=(l1-l2)/(t1-t2)
beta=l2+(-alpha*t2)
zz[1]=beta
zz[0]=alpha
fit_2 = np.poly1d(zz)


for k, M_mag in enumerate(Mv):
    if (1):
        Mbol[k] = M_mag + 0.057 + 0.708 * (vi[k]) - 0.912 * (np.square(vi[k]))
#        Mbol[k] = M_mag + 0.059 + 0.744 * (vi[k]) - 0.953 * (np.square(vi[k]))
        Mbol[k] = M_mag -1.3555 + 6.262 * (vi[k]) - 2.676 * (np.square(vi[k])) -22.973*np.power(vi[k],3) +35.542*np.power(vi[k],4)-15.34*np.power(vi[k],5)
        #Mbol[k] = M_mag
        #lbol_bc[k], lbol_bc_err[k] = calc_Lbol(vi[k], vi_e[k],'VminusI', vv[k],ve[k], dis, 0)
    else:
        Mbol[k] = M_mag - 0.610 + 2.244 * vi[k] - 2.107 * (np.square(vi[k]))
    lbol_bc[k]=Lsun*np.power(10,((Msun-Mbol[k])/2.5))
    print vi_t[k],vi[k],Mbol[k],Mv[k],M_mag-vi[k],Mbol[k]-M_mag,lbol_bc[k],vi[k]
app=Lsun*np.power(10,((Msun+16.4)/2.5))
M_56=7.866e-44*np.multiply(lbol_bc[vi_t>=474.5],np.exp(((vi_t[vi_t>=474.5]-vi_t[0])/(1+0.043)-6.1)/111.26))
x=vi_t[vi_t>=474.5]-474.5
M_56_new=0.075*(lbol_bc[vi_t>=474.5]/np.power(10,fit_2(x)))
print "M_ni56",np.mean(M_56), "M_ni_sn87",np.mean(M_56_new)
plt.scatter(vi_t,lbol_bc,color='blue')
plt.xlabel('Time [days]')
plt.ylabel('$L_{bol}$[erg/s]')

plt.tick_params(labelsize=20)
plt.show()