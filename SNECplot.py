import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
import matplotlib
from matplotlib.ticker import AutoMinorLocator
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
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
def SNECplot(filename,offset=0,verbosity=0):
    files_path ='/home/afsari/gpc_SNEC/'
    os.chdir(files_path)
    #files_path ='/home/afsari/gpc_SNEC/'
    files_path='/home/afsari/gpc_SNEC/'
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
    f_info = open(output_info, 'r')
    for line in f_info:
        if 'Time of breakout' in line:
            line = line.strip('Time of breakout =')
            line = line.strip('seconds\n')
            line = line.strip()
            t_BO = float(line)
    t_BO=0
    mags[:,0]=mags[:,0]-t_BO
    files_path ='/home/afsari/gpc_SNEC/'
    os.chdir(files_path)
    #filename1='s14.6_1020_K_9.00E+17'
    filename1='s18.8_1644_K_4.00E+17_mni0.1'
    filename1='s18.8_1644_K_4.00E+17_mni0.1'
    output_path=filename1+'/output/magnitudes.dat'
    output_out = filename1 + '/output/magnitudes_output1.dat'
    output_info = filename1 + '/output/info.dat'
    try:
        fr = open(output_path, 'r')
        fw = open(output_out, 'w')
        for line in fr:
            fw.write(' '.join(line.split()) + '\n')
        fr.close()
        fw.close()
        mags1 = np.genfromtxt(output_out, delimiter=' ')
    except:
        print "error"
    f_info = open(output_info, 'r')
    for line in f_info:
        if 'Time of breakout' in line:
            line = line.strip('Time of breakout =')
            line = line.strip('seconds\n')
            line = line.strip()
            t_BO1 = float(line)
    t_BO1=0
    mags1[:,0]=mags1[:,0]-t_BO1

    ax=plt.subplot(211)

    plt.plot(mags[:,0]/84000.0-offset,mags[:,9],label=r'$B$ w/o CSM',color='blue',lw=2)
    plt.plot(mags[:,0]/84000.0-offset,mags[:,10],label=r'$V$ w/o CSM',color='green',lw=2)
    plt.plot(mags[:,0]/84000.0-offset,mags[:,12],label=r'$I$ w/o CSM',color='red',lw=2)
    plt.plot(mags1[:,0]/84000.0-offset,mags1[:,9],'--',label=r'$B$ w/ CSM',color='blue',lw=2)
    plt.plot(mags1[:,0]/84000.0-offset,mags1[:,10],'--',label=r'$V$ w/ CSM',color='green',lw=2)
    plt.plot(mags1[:,0]/84000.0-offset,mags1[:,12],'--',label=r'$I$ w/ CSM',color='red',lw=2)
    # tck = interpolate.splrep(mags[:,0]/84000.0-offset,mags[:,9], s=0)
    # tt = np.arange(0, 118, 0.2)
    # magnew = interpolate.splev(tt, tck, der=0)
    # plt.plot(tt, magnew, label='B fit', color='blue')
    files_path ='/home/afsari/PycharmProjects/kspSN'
    os.chdir(files_path)
    u_t, u, ue, v_t, v, ve, i_t, i, ie = getLC()
    plt.scatter(u_t,u,label=r'$B$ observed',marker='o',color='blue',s=50, facecolors='none', lw = 1.5)
    plt.scatter(v_t,v,label=r'$V$ observed',marker='o',color='green',s=50, facecolors='none', lw = 1.5)
    plt.scatter(i_t,i,label=r'$I$ observed',marker='o',color='red',s=50, facecolors='none', lw = 1.5)
    ax.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax.xaxis.set_minor_locator(AutoMinorLocator(10))
    ax.xaxis.set_tick_params(width=1.5)
    ax.yaxis.set_tick_params(width=1.5)
    ax.set_xlim([0, 105])
    ax.set_ylim([-18.5, -15])
    ax.invert_yaxis()


    #plt.title('Best fit model '+filename)
    # ax1 = inset_axes(ax, width="45%",  # width = 30% of parent_bbox
    #                 height=1.83,  # height : 1 inch
    #                 loc=3, bbox_to_anchor=(0.069, 0.03, 1, 1),
    #                 bbox_transform=ax.transAxes)
    ax1=plt.subplot(212)
    # label = ax.set_ylabel('Absolute Magnitude')
    # ax1.yaxis.set_label_coords(0,0)

    ax1.plot(mags[:,0]/84000.0-offset,mags[:,9],label=r'$B$ w/o CSM',color='blue',lw=1.5)
    ax1.plot(mags[:,0]/84000.0-offset,mags[:,10],label=r'$V$ w/o CSM',color='green',lw=1.5)
    ax1.plot(mags[:,0]/84000.0-offset,mags[:,12],label=r'$I$ w/o CSM',color='red',lw=1.5)
    ax1.plot(mags1[:,0]/84000.0-offset,mags1[:,9],'--',label=r'$B$ w/CSM',color='blue',lw=1.5)
    ax1.plot(mags1[:,0]/84000.0-offset,mags1[:,10],'--',label=r'$V$ w/ CSM',color='green',lw=1.5)
    ax1.plot(mags1[:,0]/84000.0-offset,mags1[:,12],'--',label=r'$I$ w/ CSM',color='red',lw=1.5)
    ax1.scatter(u_t,u,label=r'$B$ observed',marker='o',color='blue',s=50, facecolors='none', lw = 1.5)
    ax1.scatter(v_t,v,label=r'$V$ observed',marker='o',color='green',s=50, facecolors='none', lw = 1.5)
    ax1.scatter(i_t,i,label=r'$I$ observed',marker='o',color='red',s=50, facecolors='none', lw = 1.5)
    ax1.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax1.xaxis.set_minor_locator(AutoMinorLocator(10))
    ax1.xaxis.set_tick_params(width=1.5)
    ax1.yaxis.set_tick_params(width=1.5)
    # for item in ([ax1.title, ax1.xaxis.label, ax1.yaxis.label] +
    #                  ax1.get_xticklabels() + ax1.get_yticklabels()):
    #     item.set_fontsize(13)
    ax1.set_xlim([-1, 6])
    ax1.set_ylim([-18, -15])

    plt.xlabel('Time [days]')
    ax1.invert_yaxis()
    ax1.set_ylabel('Absolute Magnitude', y=1)
    plt.tight_layout()
    plt.subplots_adjust(wspace=0, hspace=0.2)
    ax1.legend(loc='lower right', ncol=3, fancybox=True, fontsize=12, frameon=False)
    #ax1.set_ylabel('Absolute Magnitude', y=1)
    plt.show()
    return

def SNEC_all(filename,offset=0,verbosity=0):
    #files_path ='/home/afsari/gpc_SNEC/'
    files_path='/home/afsari/gpc_SNEC/'
    os.chdir(files_path)
    output_path=filename+'/output/T_eff.dat'
    output_out = filename + '/output/T_eff_edit.dat'
    try:
        fr = open(output_path, 'r')
        fw = open(output_out, 'w')
        for line in fr:
            fw.write(' '.join(line.split()) + '\n')
        fr.close()
        fw.close()
        temp = np.genfromtxt(output_out, delimiter=' ')
    except:
        print "error"
    ax=plt.subplot(311)
    output_info = filename + '/output/info.dat'
    f_info = open(output_info, 'r')
    for line in f_info:
        if 'Time of breakout' in line:
            line = line.strip('Time of breakout =')
            line = line.strip('seconds\n')
            line = line.strip()
            t_BO = float(line)
    temp[:,0]=temp[:,0]-t_BO
    files_path = '/home/afsari/gpc_SNEC/'
    #files_path = '/home/afsari/gpc_SNEC/'
    os.chdir(files_path)
    #filename1='s14.6_1020_K_9.00E+17'
    filename1='s18.8_1644_K_4.00E+17_mni0.1'
    #files_path ='/home/afsari/gpc_SNEC/'
    #os.chdir(files_path)
    output_path=filename1+'/output/T_eff.dat'
    output_out = filename1 + '/output/T_eff_edit1.dat'
    try:
        fr = open(output_path, 'r')
        fw = open(output_out, 'w')
        for line in fr:
            fw.write(' '.join(line.split()) + '\n')
        fr.close()
        fw.close()
        temp1 = np.genfromtxt(output_out, delimiter=' ')
    except:
        print "error"
    files_path = '/home/afsari/gpc_SNEC/'
    #files_path = '/home/afsari/gpc_SNEC/'
    os.chdir(files_path)
    #filename1='s14.6_1020_K_9.00E+17'
    filename1='s18.8_1644_K_4.00E+17_mni0.1'
    output_info = filename1 + '/output/info.dat'
    f_info = open(output_info, 'r')
    for line in f_info:
        if 'Time of breakout' in line:
            line = line.strip('Time of breakout =')
            line = line.strip('seconds\n')
            line = line.strip()
            t_BO1 = float(line)
    temp1[:,0]=temp1[:,0]-t_BO1
    plt.plot(temp[:,0]/84000.0-offset,temp[:,1]/1000.0,label=r'Model without CSM',color='blue',lw=2)
    plt.plot(temp1[:, 0] / 84000.0 - offset, temp1[:, 1]/1000.0,'--', label=r'Model with CSM', color='green', lw=2)
    files_path ='/home/afsari/PycharmProjects/kspSN'
    os.chdir(files_path)
    temp_obs = np.genfromtxt("phot_csv/temperature.csv", delimiter=',')
    plt.scatter(temp_obs[:,0],temp_obs[:,1]/1000.0,label='SED Temperature',marker='o',s=55, facecolors='none',color='red', linewidth='2')
    ax.set_xlim([0, 105])
    ax.set_ylim([3, 18])
    ax.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax.xaxis.set_minor_locator(AutoMinorLocator(10))
    ax.xaxis.set_tick_params(width=1.5)
    ax.yaxis.set_tick_params(width=1.5)
    plt.subplots_adjust(wspace=0, hspace=0)
    plt.locator_params(axis='y', nbins=4)
    #plt.title('Model ' + filename)
    ax.legend(loc='upper right', ncol=1, fancybox=True, fontsize=12)
    plt.ylabel(r'$\rm{T}[10^{3} \ \rm{K}]$')
    #files_path ='/home/afsari/gpc_SNEC/'
    files_path='/home/afsari/gpc_SNEC/'
    os.chdir(files_path)
    output_path=filename+'/output/vel_photo.dat'
    output_out = filename + '/output/vel_photo_edit.dat'
    try:
        fr = open(output_path, 'r')
        fw = open(output_out, 'w')
        for line in fr:
            fw.write(' '.join(line.split()) + '\n')
        fr.close()
        fw.close()
        temp = np.genfromtxt(output_out, delimiter=' ')
    except:
        print "error"
    temp[:,0]=temp[:,0]-t_BO
    ax=plt.subplot(313)
    files_path = '/home/afsari/gpc_SNEC/'
    os.chdir(files_path)
    output_path=filename1+'/output/vel_photo.dat'
    output_out = filename1 + '/output/vel_photo_edit1.dat'
    try:
        fr = open(output_path, 'r')
        fw = open(output_out, 'w')
        for line in fr:
            fw.write(' '.join(line.split()) + '\n')
        fr.close()
        fw.close()
        temp1 = np.genfromtxt(output_out, delimiter=' ')
    except:
        print "error"
    temp1[:,0]=temp1[:,0]-t_BO1
    plt.plot(temp[:,0]/84000.0-offset,temp[:,1]/1e8,label='_nolegend_',color='blue',lw=2)
    plt.plot(temp1[:,0]/84000.0-offset,temp1[:,1]/1e8,'--',label='_nolegend_',color='green',lw=2)
    plt.errorbar(93, 7960.778936/1e3,yerr=  60.23038947/1e3,label=r'$\rm{H}\alpha$', color='yellow', fmt='d')
    plt.errorbar(93,5860.152232/1e3,yerr=  16.84773558/1e3,label=r'$\rm{H}\beta$', color='gray', fmt='p')
    plt.errorbar(93, 5452.050691/1e3,yerr=  45.91299733/1e3,label=r'$\rm{H}\gamma$', color='magenta', fmt='h')
    plt.errorbar(93, 2798.334687/1e3,yerr=  16.84773558/1e3,label='Fe II 4924', color='pink', fmt='v')
    plt.errorbar(93, 3133.97768/1e3,yerr=  84.5273615/1e3,label='Fe II 5018', color='green', fmt='^')
    plt.errorbar(93,3192.222867/1e3,yerr=  63.55/1e3,label='Fe II 5169', color='red', fmt='s')


    ax.set_xlim([0, 105])
    ax.set_ylim([0.2, 12.4])
    ax.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax.xaxis.set_minor_locator(AutoMinorLocator(10))
    ax.xaxis.set_tick_params(width=1.5)
    ax.yaxis.set_tick_params(width=1.5)
    ax.set_yticks(np.arange(2,12,4))
    plt.subplots_adjust(wspace=0, hspace=0)
    #plt.locator_params(axis='y', nbins=6)
    ax.legend(loc='upper right', ncol=3, fancybox=True, fontsize=12)
    plt.ylabel(r' $\rm{v}[10^{3} \ \rm{km}~\rm{s}^{-1}]$')
    plt.xlabel(r'Time [days]')

    files_path='/home/afsari/gpc_SNEC/'
    os.chdir(files_path)
    output_path=filename+'/output/lum_observed.dat'
    output_out = filename + '/output/lum_observed_edit.dat'
    try:
        fr = open(output_path, 'r')
        fw = open(output_out, 'w')
        for line in fr:
            fw.write(' '.join(line.split()) + '\n')
        fr.close()
        fw.close()
        temp = np.genfromtxt(output_out, delimiter=' ')
    except:
        print "error"
    ax=plt.subplot(312)
    temp[:,0]=temp[:,0]-t_BO
    files_path = '/home/afsari/gpc_SNEC/'
    #files_path = '/home/afsari/gpc_SNEC/'
    os.chdir(files_path)
    #filename1='s14.6_1020_K_9.00E+17'
    filename1='s18.8_1644_K_4.00E+17_mni0.1'
    output_path=filename1+'/output/lum_observed.dat'
    output_out = filename1 + '/output/lum_observed_edit.dat'
    try:
        fr = open(output_path, 'r')
        fw = open(output_out, 'w')
        for line in fr:
            fw.write(' '.join(line.split()) + '\n')
        fr.close()
        fw.close()
        temp1 = np.genfromtxt(output_out, delimiter=' ')
    except:
        print "error"
    temp1[:,0]=temp1[:,0]-t_BO1
    plt.plot(temp[:,0]/84000.0-offset,np.log10(temp[:,1]),label='Model without CSM',color='blue',lw=2)
    plt.plot(temp1[:, 0] / 84000.0 - offset, np.log10(temp1[:, 1]), '--',label='Model with CSM', color='green', lw=2)
    temp_obs = np.genfromtxt("/home/afsari/PycharmProjects/kspSN/phot_csv/Lbol.csv", delimiter=' ')
    print temp_obs
    plt.scatter(temp_obs[:,0],np.log10(temp_obs[:,1]),label='Observation',marker='o',s=55, facecolors='none',color='red', linewidth='2')
    ax.set_xlim([0, 105])
    ax.set_ylim([40, 43.7])
    ax.legend(loc='lower right', ncol=1, fancybox=True, fontsize=12)
    plt.ylabel(r'$\log \rm{L}[\rm{erg}~ \rm{s}^{-1}]$')
    #plt.xlabel('Time [days]')
    plt.locator_params(axis='y', nbins=4)
    ax = [plt.subplot(3, 1, i + 1) for i in range(3)]
    ax[0].set_xticklabels([])
    ax[1].set_xticklabels([])
    ax[2].yaxis.set_minor_locator(AutoMinorLocator(2))
    ax[1].yaxis.set_minor_locator(AutoMinorLocator(2))
    ax[0].yaxis.set_minor_locator(AutoMinorLocator(2))
    ax[2].xaxis.set_minor_locator(AutoMinorLocator(10))
    ax[2].xaxis.set_tick_params(width=1.5)
    ax[2].yaxis.set_tick_params(width=1.5)
    plt.tight_layout()
    plt.subplots_adjust(wspace=0, hspace=0)
    plt.show()
    return

def SNECtemp(filename,offset=0,verbosity=0):
    files_path ='/home/afsari/gpc_SNEC/'
    os.chdir(files_path)
    output_path=filename+'/output/T_eff.dat'
    output_out = filename + '/output/T_eff_edit.dat'
    try:
        fr = open(output_path, 'r')
        fw = open(output_out, 'w')
        for line in fr:
            fw.write(' '.join(line.split()) + '\n')
        fr.close()
        fw.close()
        temp = np.genfromtxt(output_out, delimiter=' ')
    except:
        print "error"
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
    plt.plot(temp[:,0]/84000.0-offset,temp[:,1],label='Model T_{\text{eff}}',color='blue')
    files_path ='/home/afsari/PycharmProjects/kspSN'
    os.chdir(files_path)
    temp_obs = np.genfromtxt("phot_csv/temperature.csv", delimiter=',')
    plt.scatter(temp_obs[:,0],temp_obs[:,1],label='SED Temperature',color='red',s=1.5)
    ax.set_xlim([0, 109])
    ax.set_ylim([3000, 18000])
    plt.ylabel(r'Temperature [k]')
    plt.xlabel('Time [days]')
    #plt.title('Model '+filename+'}')
    ax.legend(loc='upper right', ncol=1, fancybox=True, fontsize=12)
    plt.show()
    return

def SNECVelocity(filename,offset=0,verbosity=0):
    files_path ='/home/afsari/gpc_SNEC/'
    os.chdir(files_path)
    output_path=filename+'/output/vel_photo.dat'
    output_out = filename + '/output/vel_photo_edit.dat'
    try:
        fr = open(output_path, 'r')
        fw = open(output_out, 'w')
        for line in fr:
            fw.write(' '.join(line.split()) + '\n')
        fr.close()
        fw.close()
        temp = np.genfromtxt(output_out, delimiter=' ')
    except:
        print "error"
    ax=plt.subplot(111)
    output_info = filename + '/output/info.dat'
    f_info = open(output_info, 'r')
    for line in f_info:
        if 'Time of breakout' in line:
            line = line.strip('Time of breakout =')
            line = line.strip('seconds\n')
            line = line.strip()
            t_BO = float(line)
    print temp
    temp[:,0]=temp[:,0]-t_BO
    plt.plot(temp[:,0]/84000.0-offset,np.log10(temp[:,1]/1e5),label='Model v_{phot}',color='blue')
    ax.set_xlim([0, 110])
    ax.set_ylim([3, 4])
    plt.ylabel(r'\Log Velocity [cm/s]')
    plt.xlabel('Time [days]')
    #plt.title('Model '+filename)
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
    plt.rc('text', usetex=True)
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
    v = np.delete(v, np.where((v_t - v_t[0]) > 130))
    ve = np.delete(ve, np.where((v_t - v_t[0]) > 130))
    v_t = np.delete(v_t, np.where((v_t - v_t[0]) > 130))
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
    i = np.delete(i, np.where((i_t - i_t[0]) > 130))
    ie = np.delete(ie, np.where((i_t - i_t[0]) > 130))
    i_t = np.delete(i_t, np.where((i_t - i_t[0]) > 130))
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
    print
    files_path ='/home/afsari/gpc_SNEC/'
    os.chdir(files_path)
    mass = np.arange(11, 28, 0.6)
    ni56_mixing = [3, 5, 7]
    energy = np.arange(4e49, 1.96e51, 0.06e51)
    # mass=np.arange(11,28,0.6)
    # ni56_mixing=[3, 5, 7]
    # energy=np.arange(1.3e51,2e51,0.06e51)
    t_p=0
    t_end=110
    file_err=[]
    file_uncomp=[]
    file_offset=[]
    file_fit=[]
    # mass=[11]
    # ni56_mixing=[3, 7]
    # energy=[4e49]
    t_BO=0
    for z in mass:
        for j in ni56_mixing:
            for k in energy:
                chi2 = np.ones(shape=(1,3))*10000
                dir_name = 's%(num)2.1f_ni56_%(mixing)i_efin_%(efin).2E_mni0.1' % {"num": z, "mixing": j, "efin": k}
                output_path = dir_name + '/output/magnitudes.dat'
                output_out = dir_name + '/output/magnitudes_output.dat'
                output_info = dir_name + '/output/info.dat'
                try:
                    fr = open(output_path, 'r')
                    fw = open(output_out, 'w')
                    for line in fr:
                        fw.write(' '.join(line.split()) + '\n')
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
                mags = mags[~np.isnan(mags).any(axis=1)]
                mags[:, 0]=mags[:, 0]-t_BO
                # if np.max(mags[:,0]/84000.0) < np.max(u_t):
                #     print "B:", dir_name,np.max(mags[:,0]/84000.0)
                #     file_uncomp.append(dir_name)
                #     continue
                if np.max(mags[:,0]/84000.0) < np.max(v_t):
                    print "V:", dir_name
                    file_uncomp.append(dir_name)
                    continue
                if np.max(mags[:,0]/84000.0) < np.max(i_t):
                    file_uncomp.append(dir_name)
                    print "I:", dir_name
                    continue
                for count,offset in enumerate(np.arange(0,1.5,0.5)):
                    tt=(mags[:,0]/84000.0)-offset
                    # if np.max(tt) < np.max(u_t):
                    #     file_offset.append(dir_name)
                    #     continue
                    if np.max(tt) < np.max(v_t):
                        file_offset.append(dir_name)
                        continue
                    if np.max(tt) < np.max(i_t):
                        file_offset.append(dir_name)
                        continue
                    # try:
                    #     tck = interpolate.splrep(tt[tt>0], mags[:, 9][tt>0], s=0.00001)
                    # except:
                    #     file_fit.append(dir_name)
                    #     break
                    # magnew_u = interpolate.splev(u_t[u_t>t_p], tck, der=0)
                    try:
                        tck = interpolate.splrep(tt[tt>0], mags[:, 10][tt>0], s=0.1)
                    except:
                        file_err.append(dir_name)
                        print dir_name,offset
                        continue
                    magnew_v = interpolate.splev(v_t[(v_t>t_p) &  (v_t<t_end)], tck, der=0)
                    try:
                        tck = interpolate.splrep(tt[tt>0], mags[:, 12][tt>0], s=0.1)
                    except:
                        file_err.append(dir_name)
                        print dir_name,offset
                        continue
                    magnew_i = interpolate.splev(i_t[(i_t>t_p) & (i_t<t_end)], tck, der=0)
                    #chi2[0,count]=np.sum(np.divide(np.square(magnew_u-u),np.square(ue)))+ \
                    chi2[0, count] = \
                        np.sum(np.divide(np.square(magnew_v - v[(v_t>t_p) & (v_t<t_end)]), np.square(ve[(v_t>t_p) &  (v_t<t_end)])))+np.sum(np.divide(np.square(magnew_i - i[(i_t>t_p) &  (i_t<t_end)]), np.square(ie[(i_t>t_p) &  (i_t<t_end)])))
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
    errorfiles = open('/home/afsari/PycharmProjects/kspSN/logs/ErrorFile_chi.txt', 'w')
    for item in file_err:
        errorfiles.write("%s\n" % item)
    uncompfiles = open('/home/afsari/PycharmProjects/kspSN/logs/UnCompFile_chi.txt', 'w')
    for item in file_uncomp:
        uncompfiles.write("%s\n" % item)
    offsetfiles = open('/home/afsari/PycharmProjects/kspSN/logs/OffsetFile_chi.txt', 'w')
    for item in file_offset:
        offsetfiles.write("%s\n" % item)
    w = csv.writer(open("/home/afsari/PycharmProjects/kspSN/phot_csv/goodness_chi.csv", "w"))
    #print hash_chi.items()
    count=0
    for key, val in hash_chi.items():
        w.writerow([key, val, hash_offset[key]])
    print file_fit
    #print hash_offset['s18.8_ni56_7_efin_1.36E+51']
    return best_fit, best_offset

def SNEC_csm_analysis( verbosity=0 ):
    import csv
    t_offset=[]
    chi2_min=[]
    keys=[]
    t_end = 110
    t_p=0
    name = 's18.8'
    u_t, u, ue, v_t, v, ve, i_t, i, ie=getLC()
    files_path ='/home/afsari/gpc_SNEC/'
    os.chdir(files_path)
    solar_radius = 6.96e10
    solar_mass = 1.99e33
    #model_radius = 72567442288907.27
    #model_radius = 0.5694193820696878e014
    #model_radius=86493739248921.08
    model_radius = 72567442288907.27
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
            dir_name ='s%(num)2.1f_%(radius)i_K_%(cons).2E' % {"num": float(name.strip('s')), "radius": np.floor(z), "cons": j}
            print dir_name
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
                t_BO=0
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
            for count,offset in enumerate(np.arange(0,1.5,0.5)):
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
                magnew_v = interpolate.splev(v_t[(v_t>t_p) &  (v_t<t_end)], tck, der=0)
                tck = interpolate.splrep(tt[tt>0], mags[:, 12][tt>0], s=0.00001)
                magnew_i = interpolate.splev(i_t[(i_t>t_p) &  (i_t<t_end)], tck, der=0)
                #chi2[0,count]=np.sum(np.divide(np.square(magnew_u-u),np.square(ue)))+ \
                chi2[0, count] =(np.sum(np.divide(np.square(magnew_v - v[(v_t>t_p) &  (v_t<t_end)]), np.square(ve[(v_t>t_p) &  (v_t<t_end)])))+np.sum(np.divide(np.square(magnew_i - i[(i_t>t_p) &  (i_t<t_end)]), np.square(ie[(i_t>t_p) &  (i_t<t_end)]))))
            chi2_min.append(np.min(chi2))
            t_offset.append(np.argmin(chi2)*0.5)
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
    errorfiles = open('/home/afsari/PycharmProjects/kspSN/logs/ErrorFile_csm_niagara_0.1.txt', 'w')
    for item in file_err:
        errorfiles.write("%s\n" % item)
    uncompfiles = open('/home/afsari/PycharmProjects/kspSN/logs/UnCompFile_csm_niagara_0.1.txt', 'w')
    for item in file_uncomp:
        uncompfiles.write("%s\n" % item)
    offsetfiles = open('/home/afsari/PycharmProjects/kspSN/logs/OffsetFile_csm_niagara_0.1.txt', 'w')
    for item in file_offset:
        offsetfiles.write("%s\n" % item)
    w = csv.writer(open("/home/afsari/PycharmProjects/kspSN/phot_csv/goodness_csm_niagara_0.1.csv", "w"))
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
        best_fit, best_offset=SNECanalysis(verbosity=args.verbosity)
        print best_fit, best_offset
    else:
        parser.add_argument("filename", type=str, help="simulation name")
        parser.add_argument("-f", "--offset", type=float, default=0)
        parser.add_argument("-v", "--verbosity", action="count", default=0)
        args = parser.parse_args()
        SNECplot(args.filename,offset=args.offset)
