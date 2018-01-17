import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

def SNECplot(filename,verbosity=0):
    files_path ='/home/afsari/gpc_SNEC/'
    os.chdir(files_path)
    output_path=filename+'/output/magnitudes.dat'
    mags = np.genfromtxt(output_path, delimiter='  ')
    ax=plt.subplot(111)
    plt.scatter(mags[:,0]/84000.0,mags[:,9],label='B',color='blue')
    plt.scatter(mags[:,0]/84000.0,mags[:,10],label='V',color='green')
    plt.scatter(mags[:,0]/84000.0,mags[:,12],label='I',color='red')
    tck = interpolate.splrep(mags[:,0]/84000.0,mags[:,9], s=0)
    tt = np.arange(0, 118, 0.2)
    magnew = interpolate.splev(tt, tck, der=0)
    plt.plot(tt, magnew, label='B fit', color='blue')
    ax.invert_yaxis()
    plt.ylabel('Absolute Magnitude')
    plt.xlabel('Time [days]')
    plt.show()
    return


def getLC():
    from scipy.interpolate import UnivariateSpline
    sn_name = "KSPN2188"
    magB = np.load("phot_csv/compiledSN_" + "B" + "_" + sn_name + ".npy")
    magB = magB.astype(np.float)
    u_t = magB[:, 0]
    index = np.argsort(u_t)
    u_t = u_t[index]
    u_t = np.delete(u_t, 51)
    u = magB[:, 3]
    ue = magB[:, 4]
    u = u[index]
    ue = ue[index]
    u = np.delete(u, 51)
    ue = np.delete(ue, 51)
    fit_u = UnivariateSpline(u_t - u_t[0], u, s=0.05)
    magV = np.load("phot_csv/compiledSN_" + "V" + "_" + sn_name + ".npy")
    magV = magV.astype(np.float)
    v_t = magV[:, 0]
    index = np.argsort(v_t)
    v_t = v_t[index]
    v = magV[:, 3]
    ve = magV[:, 4]
    v = v[index]
    ve = ve[index]
    v = np.delete(v, np.where((v_t - v_t[0]) > 118))
    ve = np.delete(ve, np.where((v_t - v_t[0]) > 118))
    v_t = np.delete(v_t, np.where((v_t - v_t[0]) > 118))
    fit_v = UnivariateSpline(v_t - v_t[0], v, s=0.3)
    magI = np.load("phot_csv/compiledSN_" + "I" + "_" + sn_name + ".npy")
    magI = magI.astype(np.float)
    magI = magI.astype(np.float)
    i_t = magI[:, 0]
    index = np.argsort(i_t)
    i = magI[:, 3]
    ie = magI[:, 4]
    index = np.argsort(i_t)
    i_t = i_t[index]
    i = i[index]
    ie = ie[index]
    i_t = np.delete(i_t, [68, 69, 70])
    i = np.delete(i, [68, 69, 70])
    ie = np.delete(ie, [68, 69, 70])
    i = np.delete(i, np.where((i_t - i_t[0]) > 118))
    ie = np.delete(ie, np.where((i_t - i_t[0]) > 118))
    i_t = np.delete(i_t, np.where((i_t - i_t[0]) > 118))
    return u_t-u_t[0],u,ue,v_t-v_t[0],v,ve,i_t-i_t[0],i,ie

def SNECanalysis( verbosity=0 ):
    t_offset=[]
    chi2_min=[]
    keys=[]
    u_t, u, ue, v_t, v, ve, i_t, i, ie=getLC()
    files_path ='/home/afsari/gpc_SNEC/'
    os.chdir(files_path)
    mass = np.arange(11, 28, 0.6)
    ni56_mixing = [3, 5, 7]
    energy = np.arange(4e49, 1.3e51, 0.06e51)
    file_err=[]
    file_uncomp=[]
    file_offset=[]
    # mass=[11]
    # ni56_mixing=[3, 7]
    # energy=[4e49]
    for z in mass:
        for j in ni56_mixing:
            for k in energy:
                chi2 = np.zeros(shape=(1,10))
                dir_name = 's%(num)2.1f_ni56_%(mixing)i_efin_%(efin).2E' % {"num": z, "mixing": j, "efin": k}
                output_path = dir_name + '/output/magnitudes.dat'
                try:
                    mags = np.genfromtxt(output_path, delimiter='  ')
                except:
                    file_err.append(dir_name)
                    continue
                if np.max(mags[:,0]/84000.0) < np.max(u_t):
                    print "B:", dir_name,np.max(mags[:,0]/84000.0)
                    file_uncomp.append(dir_name)
                    continue
                if np.max(mags[:,0]/84000.0) < np.max(v_t):
                    print "V:", dir_name
                    file_uncomp.append(dir_name)
                    continue
                if np.max(mags[:,0]/84000.0) < np.max(i_t):
                    file_uncomp.append(dir_name)
                    print "I:", dir_name
                    continue
                for count,offset in enumerate(np.arange(0,5,0.5)):
                    tt=(mags[:,0]/84000.0)-offset
                    if np.max(tt) < np.max(u_t):
                        file_offset.append(dir_name)
                        continue
                    if np.max(tt) < np.max(v_t):
                        file_offset.append(dir_name)
                        continue
                    if np.max(tt) < np.max(i_t):
                        file_offset.append(dir_name)
                        continue
                    tck = interpolate.splrep(tt, mags[:, 9], s=0)
                    magnew_u = interpolate.splev(u_t, tck, der=0)
                    tck = interpolate.splrep(tt, mags[:, 10], s=0)
                    magnew_v = interpolate.splev(v_t, tck, der=0)
                    tck = interpolate.splrep(tt, mags[:, 12], s=0)
                    magnew_i = interpolate.splev(i_t, tck, der=0)
                    chi2[0,count]=np.sum(np.divide(np.square(magnew_u-u),np.square(ue)))+ \
                    np.sum(np.divide(np.square(magnew_v - v), np.square(ve)))+np.sum(np.divide(np.square(magnew_i - i), np.square(ie)))
                chi2_min.append(np.min(chi2))
                t_offset.append(np.argmin(chi2)*0.5)
                keys.append(dir_name)
    hash_chi = {k: v for k, v in zip(keys, chi2_min)}
    hash_offset = {k: v for k, v in zip(keys, t_offset)}
    best_fit=min(hash_chi, key=hash_chi.get)
    best_offset=hash_offset[best_fit]
    print "error files:",len(file_err)
    print "uncomplete:", len(file_uncomp)
    print "offsetshort:",len(file_offset)
    errorfiles = open('/home/afsari/PycharmProjects/kspSN/logs/ErrorFile.txt', 'w')
    for item in file_err:
        errorfiles.write("%s\n" % item)
    uncompfiles = open('/home/afsari/PycharmProjects/kspSN/logs/UnCompFile.txt', 'w')
    for item in file_uncomp:
        uncompfiles.write("%s\n" % item)
    offsetfiles = open('/home/afsari/PycharmProjects/kspSN/logs/OffsetFile.txt', 'w')
    for item in file_offset:
        offsetfiles.write("%s\n" % item)
    return best_fit, best_offset

if __name__ == "__main__":
    import argparse

    # command line arguments
    parser = argparse.ArgumentParser(description="plot simulation")
    #parser.add_argument("filename", type=str, help="simulation name")
    parser.add_argument("-v", "--verbosity", action="count", default=0)
    #parser.add_argument("-n", "--name", help="if identified, will output to a file",type=int, default=0)
    args = parser.parse_args()
    best_fit, best_offset=SNECanalysis(verbosity=args.verbosity)
    #SNECplot(args.filename)
    print best_fit, best_offset
