import sys, os, time
import numpy as np
from subprocess import Popen, list2cmdline, PIPE
from shutil import copy2

# def cpu_count():
#     ''' Returns the number of CPUs in the system
#     '''
#     num = 1
#     try:
#         num = os.sysconf('SC_NPROCESSORS_ONLN')
#     except (ValueError, OSError, AttributeError):
#         pass
#     return num

# def exec_commands(cmds):
#     ''' Exec commands in parallel in multiple process
#     (as much as we have CPU)
#     '''
#     if not cmds: return # empty list
#
#     def done(p):
#         return p.poll() is not None
#     def success(p):
#         return p.returncode == 0
#     def fail():
#         sys.exit(1)
#
#     max_task = cpu_count()
#     processes = []
#     while True:
#         while cmds and len(processes) < max_task:
#             task = cmds.pop()
#             print task
#             processes.append(Popen(task, shell=True))
#
#         for p in processes:
#             if done(p):
#                 if success(p):
#                     print "success"
#                     processes.remove(p)
#                 else:
#                     print "fail"
#                     fail()
#
#         if not processes and not cmds:
#             break
#         else:
#             time.sleep(0.05)

def ReviseInlistFile(filename, profile, profile_comp, mixing, energy,mass,imax=999):
    m_ex=0.0414*mass+0.986
    tmp_filename = filename+'.tmp'
    fr = open(filename, 'r')
    fw = open(tmp_filename, 'w')
    print profile
    print profile_comp
    for line in fr:
        if ' profile_name' in line:
            new_content = ' profile_name = "%s" \n' % profile
            fw.write(new_content)
            print new_content
        elif 'comp_profile_name' in line:
            new_content = 'comp_profile_name = "%s" \n' % profile_comp
            fw.write(new_content)
        elif 'imax' in line:
            new_content = 'imax = %(max)i \n' % {'max':imax}
            fw.write(new_content)
        elif 'final_energy        =' in line:
            new_content = 'final_energy        =%(efin).2E \n' % {"efin":energy}
            fw.write(new_content)
        elif 'Ni_boundary_mass =' in line:
            new_content = 'Ni_boundary_mass =%(ni56).1E \n' % {"ni56":mixing}
            fw.write(new_content)
        elif 'mass_excised =' in line:
            new_content = 'mass_excised =%(ex).2E \n' % {"ex": m_ex}
            fw.write(new_content)
        elif 'bomb_mass_spread' in line:
            new_content = 'bomb_mass_spread =%(ex).2E \n' % {"ex": mass*0.02}
            fw.write(new_content)
        else:
            fw.write(line)
    fr.close()
    fw.close()
    command_mv = 'mv %s %s' % (tmp_filename, filename)
    os.system(command_mv)
    return

def main_loop():
    tasks=[]
    mass=np.arange(11,28,0.6)
    ni56_mixing=[3, 5, 7]
    energy=np.arange(1.3e51,2e51,0.06e51)
#energy=np.arange(4e49,1.3e51,0.06e51)
#    mass=[11]
#    ni56_mixing=[3, 7]
#    energy=[4e49]
    loc_bas='/scratch/m/matzner/afsari/SNEC/'
    #model_dir= '/home/afsari/PycharmProjects/kspSN/models/'
    for i in mass:
        for j in ni56_mixing:
            for k in energy:
                dir_name= 's%(num)2.1f_ni56_%(mixing)i_efin_%(efin).2E' %{"num":i,"mixing":j,"efin":k}
                try:
                    os.mkdir(loc_bas+dir_name)
                except OSError as err:
                    print err
                try:
                    os.mkdir(loc_bas+dir_name+'/output')
                except OSError as err:
                    print err
                print loc_bas+dir_name+'/output'
                copy2(loc_bas+'snec',loc_bas+dir_name)
                cmd='cp '+loc_bas + 'parameters '+loc_bas + dir_name
                print cmd
                os.system(cmd)
                src_comp='profile_s%(num)2.1f.iso.short' %{"num":i}
                cmd='cp '+loc_bas + 'profiles/'+src_comp+' '+loc_bas + dir_name
                print cmd
                os.system(cmd)
                src='profile_s%(num)2.1f.short' %{"num":i}
                cmd='cp '+loc_bas + 'profiles/'+src+' '+loc_bas + dir_name
                print cmd
                os.system(cmd)
                cmd='cp -r '+loc_bas+'tables '+loc_bas+dir_name
                print cmd
                os.system(cmd)
                cmd='cp '+loc_bas+'subfile '+loc_bas+dir_name
                print cmd
                os.system(cmd)
                ReviseInlistFile(loc_bas+dir_name+'/parameters',src,src_comp,j,k,i)
                task='(cd '+loc_bas+dir_name+' ; ./snec) &'
                tasks.append(task)
                if len(tasks)==8:
                    for count in range(0,8):
                        with open(loc_bas+dir_name+'/subfile', "a") as myfile:
                            myfile.write(tasks.pop()+' \n')
                    with open(loc_bas + dir_name + '/subfile', "a") as myfile:
                        myfile.write("wait")
                    cmd = 'cd ' + loc_bas + dir_name + ' && qsub ' + loc_bas + dir_name + '/subfile'
                    os.system(cmd)
                    tasks=[]
    if len(tasks)>0:
        for count in range(0, len(tasks)):
            with open(loc_bas + dir_name + '/subfile', "a") as myfile:
                myfile.write(tasks.pop()+' \n')
        with open(loc_bas + dir_name + '/subfile', "a") as myfile:
            myfile.write("wait")
        cmd = 'cd ' + loc_bas + dir_name + ' && qsub ' + loc_bas + dir_name + '/subfile'
        os.system(cmd)
        tasks = []
    return


def csm_loop():
    tasks=[]
    loc_bas='/scratch/m/matzner/afsari/SNEC/'
    best_model='s21.2_ni56_7_efin_7.60E+50'
    content = best_model.split('_')
    name= content[0].strip('s')
    mixing = float(content[2])
    energy = float(content[4])
    solar_radius = 6.96e10
    solar_mass = 1.99e33
    model_radius = 86493739248921.08
    model_radius_solar = model_radius / solar_radius
    rad = np.arange(model_radius_solar+2, 3800, 100)
    rad_solar = rad * solar_radius
    K = np.arange(1.0e17, 3.0e18, 1.0e17)
    #rad = [model_radius_solar + 100]
    #K = [1.0e17 + 1.0e17]
    for i, r in enumerate(rad):
        for j, k in enumerate(K):
            dir_name = 's%(num)2.1f_%(radius)i_K_%(cons).2E' % {"num": float(name), "radius": np.floor(r), "cons": k}
            try:
                os.mkdir(loc_bas+dir_name)
            except OSError as err:
                print err
            try:
                os.mkdir(loc_bas+dir_name+'/output')
            except OSError as err:
                print err
            print loc_bas+dir_name+'/output'
            copy2(loc_bas+'snec',loc_bas+dir_name)
            cmd='cp '+loc_bas + 'parameters '+loc_bas + dir_name
            print cmd
            os.system(cmd)
            src='profile_s%(num)2.1f.short' %{"num" : float(name)}
            cmd='cp '+loc_bas + 'profiles/'+src+' '+loc_bas + dir_name
            print cmd
            os.system(cmd)
            src_comp='profile_s%(num)2.1f.iso.short' %{"num":float(name)}
            cmd='cp '+loc_bas + 'profiles/'+src_comp+' '+loc_bas + dir_name
            os.system(cmd)
            fr = open(loc_bas + dir_name+ '/'+src , 'r')
            fw = open(loc_bas + dir_name+ '/'+'profile_'+dir_name+'.short', 'w')
            fr_iso = open(loc_bas + dir_name+ '/'+src_comp , 'r')
            fw_iso = open(loc_bas + dir_name+ '/'+'profile_'+dir_name+'.iso.short', 'w')
            for line in fr:
                fw.write(line)
            dat = line.split(' ')
            for line in fr_iso:
                fw_iso.write(line)
            dat_iso = line.split(' ')
            rad_csm = np.arange(model_radius_solar + 1, r, 1.5) * solar_radius
            radius_old = float(dat[2])
            mass_old = float(dat[1])
            print rad_csm
	    for u, csm in enumerate(rad_csm):
                rho = k / np.square(csm)
                mass_new = mass_old + (4 * np.pi * rho * (csm ** 3 - radius_old ** 3) / 3)
                dat_towrite = [int(dat[0]) + u + 1, mass_new, csm, float(dat[3]), rho, float(dat[5]), float(dat[6]),
                               float(dat[7])]
                dat_towrite_iso = [mass_new, csm, float(dat_iso[2]), float(dat_iso[3]),
                                   float(dat_iso[4]), float(dat_iso[5]), float(dat_iso[6]), float(dat_iso[7]),
                                   float(dat_iso[8]) , float(dat_iso[9]), float(dat_iso[10]), float(dat_iso[11]),
                                   float(dat_iso[12]), float(dat_iso[13]),float(dat_iso[14]), float(dat_iso[15]),
                                   float(dat_iso[16])]
                fw.writelines(["%s " % item for item in dat_towrite])
                fw.writelines(["\n"])
                fw_iso.writelines(["%s " % item for item in dat_towrite_iso])
                fw_iso.writelines(["\n"])
                mass_old = mass_new
                radius_old = csm
            csm_fac = 1 - (float(dat[1])) / mass_old
            prog_fac=(float(dat[1])) / mass_old
            fr.close()
            fw.close()
            fr_iso.close()
            fw_iso.close()
            with file(loc_bas + dir_name+ '/'+'profile_'+dir_name+'.short', 'r+') as modified:
                modified.write(str(int(dat[0]) + u +1))
            modified.close()
            with file(loc_bas + dir_name+ '/'+'profile_'+dir_name+'.iso.short', 'r+') as modified:
                modified.write(str(int(dat[0]) + u + 1) + '  15')
            modified.close()
            cmd='cp -r '+loc_bas+'tables '+loc_bas+dir_name
            print cmd
            os.system(cmd)
            file_grid = loc_bas+dir_name+'/tables/GridPattern.dat'
            dat_pattern = np.loadtxt(file_grid)
            dat_csm = dat_pattern[dat_pattern > prog_fac]
            dat_pattern = prog_fac * dat_pattern
            dat_pattern = np.concatenate([dat_pattern, dat_csm])
            np.savetxt(file_grid, dat_pattern)
            imax=np.shape(dat_pattern)[0]
            cmd='cp '+loc_bas+'subfile '+loc_bas+dir_name
            print cmd
            os.system(cmd)
            ReviseInlistFile(loc_bas+dir_name+'/parameters','profile_'+dir_name+'.short','profile_'+dir_name+'.iso.short',mixing,energy,float(name),imax)
            task='(cd '+loc_bas+dir_name+' ; ./snec) &'
            tasks.append(task)
            if len(tasks)==8:
                for count in range(0,8):
                    with open(loc_bas+dir_name+'/subfile', "a") as myfile:
                        myfile.write(tasks.pop()+' \n')
                with open(loc_bas + dir_name + '/subfile', "a") as myfile:
                    myfile.write("wait")
                cmd = 'cd ' + loc_bas + dir_name + ' && qsub ' + loc_bas + dir_name + '/subfile'
                os.system(cmd)
                tasks=[]
    if len(tasks)>0:
        for count in range(0, len(tasks)):
            with open(loc_bas + dir_name + '/subfile', "a") as myfile:
                myfile.write(tasks.pop()+' \n')
        with open(loc_bas + dir_name + '/subfile', "a") as myfile:
            myfile.write("wait")
        cmd = 'cd ' + loc_bas + dir_name + ' && qsub ' + loc_bas + dir_name + '/subfile'
        os.system(cmd)
        tasks = []
    return

def aux_csm_loop():
    tasks=[]
    loc_bas='/scratch/m/matzner/afsari/SNEC/'
    best_model='s21.2_ni56_7_efin_7.60E+50'
    content = best_model.split('_')
    name= content[0].strip('s')
    mixing = float(content[2])
    energy = float(content[4])
    solar_radius = 6.96e10
    solar_mass = 1.99e33
    model_radius = 86493739248921.08
    model_radius_solar = model_radius / solar_radius
    fname='/scratch/m/matzner/afsari/SNEC/UnCompFile.txt'
    with open(fname) as f:
        dirs = f.readlines()
    dirs = [x.strip() for x in dirs]
    loc_bas='/scratch/m/matzner/afsari/SNEC/'
    for dir_name in dirs:
        content = dir_name.split('_')
        r = float(content[1])
        k = float(content[3])
        try:
            os.mkdir(loc_bas+dir_name)
        except OSError as err:
            print err
        try:
            os.mkdir(loc_bas+dir_name+'/output')
        except OSError as err:
            print err
        print loc_bas+dir_name+'/output'
        copy2(loc_bas+'snec',loc_bas+dir_name)
        cmd='cp '+loc_bas + 'parameters '+loc_bas + dir_name
        print cmd
        os.system(cmd)
        src='profile_s%(num)2.1f.short' %{"num" : float(name)}
        cmd='cp '+loc_bas + 'profiles/'+src+' '+loc_bas + dir_name
        print cmd
        os.system(cmd)
        src_comp='profile_s%(num)2.1f.iso.short' %{"num":float(name)}
        cmd='cp '+loc_bas + 'profiles/'+src_comp+' '+loc_bas + dir_name
        os.system(cmd)
        fr = open(loc_bas + dir_name+ '/'+src , 'r')
        fw = open(loc_bas + dir_name+ '/'+'profile_'+dir_name+'.short', 'w')
        fr_iso = open(loc_bas + dir_name+ '/'+src_comp , 'r')
        fw_iso = open(loc_bas + dir_name+ '/'+'profile_'+dir_name+'.iso.short', 'w')
        for line in fr:
            fw.write(line)
        dat = line.split(' ')
        for line in fr_iso:
            fw_iso.write(line)
        dat_iso = line.split(' ')
        rad_csm = np.arange(model_radius_solar + 1, r, 1.5) * solar_radius
        radius_old = float(dat[2])
        mass_old = float(dat[1])
        print rad_csm
        for u, csm in enumerate(rad_csm):
            rho = k / np.square(csm)
            mass_new = mass_old + (4 * np.pi * rho * (csm ** 3 - radius_old ** 3) / 3)
            dat_towrite = [int(dat[0]) + u + 1, mass_new, csm, float(dat[3]), rho, float(dat[5]), float(dat[6]),
                           float(dat[7])]
            dat_towrite_iso = [mass_new, csm, float(dat_iso[2]), float(dat_iso[3]),
                               float(dat_iso[4]), float(dat_iso[5]), float(dat_iso[6]), float(dat_iso[7]),
                               float(dat_iso[8]) , float(dat_iso[9]), float(dat_iso[10]), float(dat_iso[11]),
                               float(dat_iso[12]), float(dat_iso[13]),float(dat_iso[14]), float(dat_iso[15]),
                               float(dat_iso[16])]
            fw.writelines(["%s " % item for item in dat_towrite])
            fw.writelines(["\n"])
            fw_iso.writelines(["%s " % item for item in dat_towrite_iso])
            fw_iso.writelines(["\n"])
            mass_old = mass_new
            radius_old = csm
        csm_fac = 1 - (float(dat[1])) / mass_old
        prog_fac=(float(dat[1])) / mass_old
        fr.close()
        fw.close()
        fr_iso.close()
        fw_iso.close()
        with file(loc_bas + dir_name+ '/'+'profile_'+dir_name+'.short', 'r+') as modified:
            modified.write(str(int(dat[0]) + u +1))
        modified.close()
        with file(loc_bas + dir_name+ '/'+'profile_'+dir_name+'.iso.short', 'r+') as modified:
            modified.write(str(int(dat[0]) + u + 1) + '  15')
        modified.close()
        cmd='cp -r '+loc_bas+'tables '+loc_bas+dir_name
        print cmd
        os.system(cmd)
        file_grid = loc_bas+dir_name+'/tables/GridPattern.dat'
        dat_pattern = np.loadtxt(file_grid)
        dat_csm = dat_pattern[dat_pattern > prog_fac]
        dat_pattern = prog_fac * dat_pattern
        dat_pattern = np.concatenate([dat_pattern, dat_csm])
        np.savetxt(file_grid, dat_pattern)
        imax=np.shape(dat_pattern)[0]
        cmd='cp '+loc_bas+'subfile '+loc_bas+dir_name
        print cmd
        os.system(cmd)
        ReviseInlistFile(loc_bas+dir_name+'/parameters','profile_'+dir_name+'.short','profile_'+dir_name+'.iso.short',mixing,energy,float(name),imax)
        task='(cd '+loc_bas+dir_name+' ; ./snec) &'
        tasks.append(task)
        if len(tasks)==8:
            for count in range(0,8):
                with open(loc_bas+dir_name+'/subfile', "a") as myfile:
                    myfile.write(tasks.pop()+' \n')
            with open(loc_bas + dir_name + '/subfile', "a") as myfile:
                myfile.write("wait")
            cmd = 'cd ' + loc_bas + dir_name + ' && qsub ' + loc_bas + dir_name + '/subfile'
            os.system(cmd)
            tasks=[]
    if len(tasks)>0:
        for count in range(0, len(tasks)):
            with open(loc_bas + dir_name + '/subfile', "a") as myfile:
                myfile.write(tasks.pop()+' \n')
        with open(loc_bas + dir_name + '/subfile', "a") as myfile:
            myfile.write("wait")
        cmd = 'cd ' + loc_bas + dir_name + ' && qsub ' + loc_bas + dir_name + '/subfile'
        os.system(cmd)
        tasks = []
    return

def aux_loop():
    tasks=[]
    fname='/scratch/m/matzner/afsari/SNEC/UnCompFile.txt'
    with open(fname) as f:
        dirs = f.readlines()
    dirs = [x.strip() for x in dirs]
    loc_bas='/scratch/m/matzner/afsari/SNEC/'
    for dir_name in dirs:
        content=dir_name.split('_')
        i=float(content[0].strip('s'))
        j=float(content[2])
        k=float(content[4])
        try:
            os.mkdir(loc_bas+dir_name)
        except OSError as err:
            print err
        try:
            os.mkdir(loc_bas+dir_name+'/output')
        except OSError as err:
            print err
        print loc_bas+dir_name+'/output'
        copy2(loc_bas+'snec',loc_bas+dir_name)
        cmd='cp '+loc_bas + 'parameters '+loc_bas + dir_name
        print cmd
        os.system(cmd)
        src_comp='profile_s%(num)2.1f.iso.short' %{"num":i}
        cmd='cp '+loc_bas + 'profiles/'+src_comp+' '+loc_bas + dir_name
        print cmd
        os.system(cmd)
        src='profile_s%(num)2.1f.short' %{"num":i}
        cmd='cp '+loc_bas + 'profiles/'+src+' '+loc_bas + dir_name
        print cmd
        os.system(cmd)
        cmd='cp -r '+loc_bas+'tables '+loc_bas+dir_name
        print cmd
        os.system(cmd)
        cmd='cp '+loc_bas+'subfile '+loc_bas+dir_name
        print cmd
        os.system(cmd)
        ReviseInlistFile(loc_bas+dir_name+'/parameters',src,src_comp,j,k,i)
        task='(cd '+loc_bas+dir_name+' ; ./snec) &'
        tasks.append(task)
        if len(tasks)==8:
            for count in range(0,8):
                with open(loc_bas+dir_name+'/subfile', "a") as myfile:
                    myfile.write(tasks.pop()+' \n')
            with open(loc_bas + dir_name + '/subfile', "a") as myfile:
                myfile.write("wait")
            cmd = 'cd ' + loc_bas + dir_name + ' && qsub ' + loc_bas + dir_name + '/subfile'
            os.system(cmd)
            tasks=[]
    if len(tasks)>0:
        for count in range(0, len(tasks)):
            with open(loc_bas + dir_name + '/subfile', "a") as myfile:
                myfile.write(tasks.pop()+' \n')
        with open(loc_bas + dir_name + '/subfile', "a") as myfile:
            myfile.write("wait")
        cmd = 'cd ' + loc_bas + dir_name + ' && qsub ' + loc_bas + dir_name + '/subfile'
        os.system(cmd)
        tasks = []
    return

if __name__ == '__main__':
    csm_loop()
