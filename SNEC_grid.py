import sys, os, time
import numpy as np
from subprocess import Popen, list2cmdline, PIPE
from shutil import copy2

def cpu_count():
    ''' Returns the number of CPUs in the system
    '''
    num = 1
    try:
        num = os.sysconf('SC_NPROCESSORS_ONLN')
    except (ValueError, OSError, AttributeError):
        pass
    return num

def exec_commands(cmds):
    ''' Exec commands in parallel in multiple process 
    (as much as we have CPU)
    '''
    if not cmds: return # empty list

    def done(p):
        return p.poll() is not None
    def success(p):
        return p.returncode == 0
    def fail():
        sys.exit(1)

    max_task = cpu_count()
    processes = []
    while True:
        while cmds and len(processes) < max_task:
            task = cmds.pop()
            print task
            processes.append(Popen(task, shell=True))

        for p in processes:
            if done(p):
                if success(p):
                    print "success"
                    processes.remove(p)
                else:
                    print "fail"
                    fail()

        if not processes and not cmds:
            break
        else:
            time.sleep(0.05)

def ReviseInlistFile(filename, profile, profile_comp, mixing, energy,mass):
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
    energy=np.arange(4e49,1.3e51,0.06e51)
#     mass=[11]
#     ni56_mixing=[3, 7]
#     energy=[4e49]
    loc_bas='/home/afsari/SNEC-1.01/'
    model_dir= '/home/afsari/PycharmProjects/kspSN/models/'
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
                ReviseInlistFile(loc_bas+dir_name+'/parameters',src,src_comp,j,k,i)
                task='cd '+loc_bas+dir_name+' && '+loc_bas+dir_name+'/snec'
                tasks.append(task)
    return tasks


if __name__ == '__main__':
    cmds=main_loop()
    exec_commands(cmds)
