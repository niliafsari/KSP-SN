import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

def SNECplot(filename,offset=0,verbosity=0):
    files_path ='/home/afsari/gpc_SNEC/'
    os.chdir(files_path)
    output_path=filename+'/output/magnitudes.dat'
    output_out = filename + '/output/magnitudes_output.dat'
    output_info = filename + '/output/info.dat'
    try:
        fr = open(output_path, 'r')
        fw = open(output_out, 'w')
        for line in fr:
            fw.write(' '.join(line.split()) + '\n')
        fr.close()
        fw.close()
        mags = np.genfromtxt(output_out, delimiter=' ')
    except:
        print "error"
    output_info = filename + '/output/info.dat'
    f_info = open(output_info, 'r')
    for line in f_info:
        if 'Time of breakout' in line:
            line = line.strip('Time of breakout =')
            line = line.strip('seconds\n')
            line = line.strip()
            t_BO = float(line)
    mags[:,0]=mags[:,0]-t_BO
    ax=plt.subplot(111)

    plt.plot(mags[:,0]/84000.0-offset,mags[:,9],label='B simulation',color='blue')
    plt.plot(mags[:,0]/84000.0-offset,mags[:,10],label='V simulation',color='green')
    plt.plot(mags[:,0]/84000.0-offset,mags[:,12],label='I simulation',color='red')
    # tck = interpolate.splrep(mags[:,0]/84000.0-offset,mags[:,9], s=0)
    # tt = np.arange(0, 118, 0.2)
    # magnew = interpolate.splev(tt, tck, der=0)
    # plt.plot(tt, magnew, label='B fit', color='blue')
    files_path ='/home/afsari/PycharmProjects/kspSN'
    os.chdir(files_path)
    u_t, u, ue, v_t, v, ve, i_t, i, ie = getLC()
    plt.scatter(u_t,u,label='B observed',marker='*',color='blue',s=1.5)
    plt.scatter(v_t,v,label='V observed',marker='*',color='green',s=1.5)
    plt.scatter(i_t,i,label='I observed',marker='*',color='red',s=1.5)
    ax.set_xlim([0, 119])
    ax.set_ylim([-19, -13])
    ax.invert_yaxis()
    plt.ylabel('Absolute Magnitude')
    plt.xlabel('Time [days]')
    plt.title('Best fit model '+filename)
    ax.legend(loc='lower left', ncol=2, fancybox=True, fontsize=12)
    plt.show()
    return

def SNECtemp(filename,offset=0,verbosity=0):
    files_path ='/home/afsari/gpc_SNEC/'
    os.chdir(files_path)
    output_path=filename+'/output/T_eff.dat'
    temp = np.genfromtxt(output_path, delimiter='  ')
    ax=plt.subplot(111)
    output_info = filename + '/output/info.dat'
    f_info = open(output_info, 'r')
    for line in f_info:
        if 'Time of breakout' in line:
            line = line.strip('Time of breakout =')
            line = line.strip('seconds\n')
            line = line.strip()
            t_BO = float(line)
    temp[:,0]=temp[:,0]-t_BO
    plt.plot(temp[:,0]/84000.0-offset,temp[:,1],label='Model T_{eff}',color='blue')
    files_path ='/home/afsari/PycharmProjects/kspSN'
    os.chdir(files_path)
    temp_obs = np.genfromtxt("phot_csv/temperature.csv", delimiter=',')
    plt.scatter(temp_obs[:,0],temp_obs[:,1],label='SED Temperature',color='red',s=1.5)
    ax.set_xlim([0, 109])
    ax.set_ylim([3000, 18000])
    plt.ylabel(r'Temperature [k]')
    plt.xlabel('Time [days]')
    plt.title('Model '+filename)
    ax.legend(loc='upper right', ncol=1, fancybox=True, fontsize=12)
    plt.show()
    return

def SNECluminosity(filename,offset=0,verbosity=0):
    files_path ='/home/afsari/gpc_SNEC/'
    os.chdir(files_path)
    output_path=filename+'/output/lum_observed.dat'
    temp = np.genfromtxt(output_path, delimiter='  ')
    ax=plt.subplot(111)
    output_info = filename + '/output/info.dat'
    f_info = open(output_info, 'r')
    for line in f_info:
        if 'Time of breakout' in line:
            line = line.strip('Time of breakout =')
            line = line.strip('seconds\n')
            line = line.strip()
            t_BO = float(line)
    temp[:,0]=temp[:,0]-t_BO
    plt.plot(temp[:,0]/84000.0-offset,np.log10(temp[:,1]),label='Model L_{phot}',color='blue')
    files_path ='/home/afsari/PycharmProjects/kspSN'
    # os.chdir(files_path)
    # temp_obs = np.genfromtxt("phot_csv/temperature.csv", delimiter=',')
    # plt.scatter(temp_obs[:,0],temp_obs[:,1],label='SED Temperature',color='red',s=1.5)
    ax.set_xlim([0, 110])
    ax.set_ylim([42, 43])
    plt.ylabel(r'Luminosity [ers/s]')
    plt.xlabel('Time [days]')
    plt.title('Model '+filename)
    ax.legend(loc='upper right', ncol=1, fancybox=True, fontsize=12)
    plt.show()
    return

def getLC():
    from scipy.interpolate import UnivariateSpline
    sn_name = "KSPN2188_v1"
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
    # i_t = np.delete(i_t, [68, 69, 70])
    # i = np.delete(i, [68, 69, 70])
    # ie = np.delete(ie, [68, 69, 70])
    i = np.delete(i, np.where((i_t - i_t[0]) > 118))
    ie = np.delete(ie, np.where((i_t - i_t[0]) > 118))
    i_t = np.delete(i_t, np.where((i_t - i_t[0]) > 118))
    # ie[:]=0.1
    # ve[:]=0.1
    # ue[:]=0.1
    return u_t-u_t[0],u,ue,v_t-v_t[0],v,ve,i_t-i_t[0],i,ie

def SNECanalysis( verbosity=0 ):
    import csv
    t_offset=[]
    chi2_min=[]
    keys=[]
    u_t, u, ue, v_t, v, ve, i_t, i, ie=getLC()
    files_path ='/home/afsari/gpc_SNEC/'
    os.chdir(files_path)
    mass = np.arange(11, 28, 0.6)
    ni56_mixing = [3, 5, 7]
    energy = np.arange(4e49, 1.96e51, 0.06e51)
    file_err=[]
    file_uncomp=[]
    file_offset=[]
    file_fit=[]
    # mass=[11]
    # ni56_mixing=[3, 7]
    # energy=[4e49]
    for z in mass:
        for j in ni56_mixing:
            for k in energy:
                chi2 = np.ones(shape=(1,5))*10000
                dir_name = 's%(num)2.1f_ni56_%(mixing)i_efin_%(efin).2E' % {"num": z, "mixing": j, "efin": k}
                output_path = dir_name + '/output/magnitudes.dat'
                output_info = dir_name + '/output/info.dat'
                try:
                    mags = np.genfromtxt(output_path, delimiter='  ')
                    f_info = open(output_info, 'r')
                    for line in f_info:
                        if 'Time of breakout' in line:
                            line = line.strip('Time of breakout =')
                            line = line.strip('seconds\n')
                            line = line.strip()
                            t_BO = float(line)
                except:
                    file_err.append(dir_name)
                    continue
                mags[:, 0]=mags[:, 0]-t_BO
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
                for count,offset in enumerate(np.arange(0,2.5,0.5)):
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
                    try:
                        tck = interpolate.splrep(tt[tt>0], mags[:, 9][tt>0], s=0.00001)
                    except:
                        file_fit.append(dir_name)
                        break
                    magnew_u = interpolate.splev(u_t, tck, der=0)
                    tck = interpolate.splrep(tt[tt>0], mags[:, 10][tt>0], s=0.00001)
                    magnew_v = interpolate.splev(v_t, tck, der=0)
                    tck = interpolate.splrep(tt[tt>0], mags[:, 12][tt>0], s=0.00001)
                    magnew_i = interpolate.splev(i_t, tck, der=0)
                    #chi2[0,count]=np.sum(np.divide(np.square(magnew_u-u),np.square(ue)))+ \
                    chi2[0, count] = \
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
    w = csv.writer(open("/home/afsari/PycharmProjects/kspSN/phot_csv/goodness_1.csv", "w"))
    print hash_chi.items()
    count=0
    for key, val in hash_chi.items():
        w.writerow([key, val, hash_offset[key]])
    print file_fit
    print hash_offset['s18.8_ni56_7_efin_1.36E+51']
    return best_fit, best_offset

def SNEC_csm_analysis( verbosity=0 ):
    import csv
    t_offset=[]
    chi2_min=[]
    keys=[]
    name = 's18.8'
    u_t, u, ue, v_t, v, ve, i_t, i, ie=getLC()
    files_path ='/home/afsari/gpc_SNEC/'
    os.chdir(files_path)
    solar_radius = 6.96e10
    solar_mass = 1.99e33
    #model_radius = 72567442288907.27
    model_radius = 0.5694193820696878e014
    model_radius_solar = model_radius / solar_radius
    rad = np.arange(model_radius_solar+2, 3800, 100)
    rad_solar = rad * solar_radius
    K = np.arange(1.0e17, 3.0e18, 1.0e17)
    file_err=[]
    file_uncomp=[]
    file_offset=[]
    file_fit=[]
    # mass=[11]
    # ni56_mixing=[3, 7]
    # energy=[4e49]
    for z in rad:
        for j in K:
            chi2 = np.ones(shape=(1,5))*10000
            dir_name ='s%(num)2.1f_%(radius)i_K_%(cons).2E' % {"num": 14.6, "radius": np.floor(z), "cons": j}
            output_path = dir_name + '/output/magnitudes.dat'
            output_out = dir_name + '/output/magnitudes_output.dat'
            output_info = dir_name + '/output/info.dat'
            try:
                fr = open(output_path, 'r')
                fw = open(output_out, 'w')
                for line in fr:
                    fw.write(' '.join(line.split( ))+'\n')
                fr.close()
                fw.close()
                mags = np.genfromtxt(output_out, delimiter=' ')
                f_info = open(output_info, 'r')
                for line in f_info:
                    if 'Time of breakout' in line:
                        line = line.strip('Time of breakout =')
                        line = line.strip('seconds\n')
                        line = line.strip()
                        t_BO = float(line)
            except:
                file_err.append(dir_name)
                continue
            mags=mags[~np.isnan(mags).any(axis=1)]
            mags[:,0]=mags[:,0]-t_BO
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
            for count,offset in enumerate(np.arange(0,2.5,0.5)):
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

                try:
                    tck = interpolate.splrep(tt[tt>0], mags[:, 9][tt>0], s=0.00001)
                except:
                    file_fit.append(dir_name)
                    break
                magnew_u = interpolate.splev(u_t, tck, der=0)
                tck = interpolate.splrep(tt[tt>0], mags[:, 10][tt>0], s=0.00001)
                magnew_v = interpolate.splev(v_t, tck, der=0)
                tck = interpolate.splrep(tt[tt>0], mags[:, 12][tt>0], s=0.00001)
                magnew_i = interpolate.splev(i_t, tck, der=0)
                #chi2[0,count]=np.sum(np.divide(np.square(magnew_u-u),np.square(ue)))+ \
                chi2[0, count] =(np.sum(np.divide(np.square(magnew_v - v), np.square(ve)))+np.sum(np.divide(np.square(magnew_i - i), np.square(ie))))
            chi2_min.append(np.nanmin(chi2))
            t_offset.append(np.nanargmin(chi2)*0.5)
            keys.append(dir_name)
    print keys
    hash_chi = {k: v for k, v in zip(keys, chi2_min)}
    print hash_chi
    hash_offset = {k: v for k, v in zip(keys, t_offset)}
    best_fit=min(hash_chi, key=hash_chi.get)
    best_offset=hash_offset[best_fit]
    print "error files:",len(file_err)
    print "uncomplete:", len(file_uncomp)
    print "offsetshort:",len(file_offset)
    errorfiles = open('/home/afsari/PycharmProjects/kspSN/logs/ErrorFile_csm.txt', 'w')
    for item in file_err:
        errorfiles.write("%s\n" % item)
    uncompfiles = open('/home/afsari/PycharmProjects/kspSN/logs/UnCompFile_csm.txt', 'w')
    for item in file_uncomp:
        uncompfiles.write("%s\n" % item)
    offsetfiles = open('/home/afsari/PycharmProjects/kspSN/logs/OffsetFile_csm.txt', 'w')
    for item in file_offset:
        offsetfiles.write("%s\n" % item)
    w = csv.writer(open("/home/afsari/PycharmProjects/kspSN/phot_csv/goodness_csm.csv", "w"))
    print hash_chi.items()
    count=0
    for key, val in hash_chi.items():
        w.writerow([key, val, hash_offset[key]])
    print file_fit
    return best_fit, best_offset


if __name__ == "__main__":
    import argparse
    import sys
    parser = argparse.ArgumentParser(description="plot simulation")
    # parser.add_argument("filename", type=str, help="simulation name")
    # parser.add_argument("-f", "--offset", type=float, default=0)
    # parser.add_argument("-v", "--verbosity", action="count", default=0)
    # args = parser.parse_args()
    # SNECluminosity(args.filename,offset=args.offset)
    if len(sys.argv)==1:
        parser.add_argument("-v", "--verbosity", action="count", default=0)
        args = parser.parse_args()
        best_fit, best_offset=SNEC_csm_analysis(verbosity=args.verbosity)
        print best_fit, best_offset
    else:
        parser.add_argument("filename", type=str, help="simulation name")
        parser.add_argument("-f", "--offset", type=float, default=0)
        parser.add_argument("-v", "--verbosity", action="count", default=0)
        args = parser.parse_args()
        SNECplot(args.filename,offset=args.offset)
