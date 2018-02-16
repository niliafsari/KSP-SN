import numpy as np
import csv

model='models/s18.8'
name='s18.8'
solar_radius=6.96e10
solar_mass=1.99e33
model_radius=72567442288907.27
model_radius_solar=model_radius/solar_radius
rad = np.arange(model_radius_solar, 3800, 100)
rad_solar=rad*solar_radius
K=np.arange(1.0e17, 3.0e18, 1.0e17)
rad=[model_radius_solar+100]
K=[1.0e17+1.0e17]
for i,r in enumerate(rad):
    for j,k in enumerate(K):
        name_file='s%(num)2.1f_%(radius)i_efin_%(cons).2E' % {"num": 18.8, "radius": np.floor(r), "cons": k}
        fr = open('/home/afsari/SNEC-1.01/profiles/profile_' + name + '.short', 'r')
        fr_iso = open('/home/afsari/SNEC-1.01/profiles/profile_' + name + '.iso.short', 'r')
        fw = open('profile_' + name_file + '.short', 'w')
        for line in fr:
                fw.write(line)
        dat = line.split(' ')
        fw_iso = open('profile_' + name_file + '.iso.short', 'w')
        for line in fr_iso:
            fw_iso.write(line)
        dat_iso = line.split(' ')
        rad_csm=np.arange(model_radius_solar+1, r, 1.5)*solar_radius
        print model_radius_solar*solar_radius
        print rad_csm
        radius_old=float(dat[2])
        mass_old=float(dat[1])
        for u,csm in enumerate(rad_csm):
            rho=k/np.square(csm)
            mass_new=mass_old+(4*np.pi*rho*(csm**3-radius_old**3)/3)
            dat_towrite=[int(dat[0])+u+1, mass_new, csm, float(dat[3]) ,rho ,float(dat[5]), float(dat[6]) ,float(dat[7])]
            dat_towrite_iso=[mass_new, csm, float(dat_iso[2]) ,float(dat_iso[3]) ,
                             float(dat_iso[4]), float(dat_iso[5]) ,float(dat_iso[6]),float(dat_iso[7]),float(dat_iso[8])
                , float(dat_iso[9]),float(dat_iso[10]),float(dat_iso[11]),float(dat_iso[12]),float(dat_iso[13]),float(dat_iso[14])
                , float(dat_iso[15]),float(dat_iso[16])]
            fw.writelines(["%s " % item for item in dat_towrite])
            fw.writelines(["\n"])
            fw_iso.writelines(["%s " % item for item in dat_towrite_iso])
            fw_iso.writelines(["\n"])
            mass_old=mass_new
            radius_old=csm
        print (mass_old-float(dat[1]))/solar_mass
        csm_fac =1-(float(dat[1]))/mass_old
        prog_fac=(float(dat[1]))/mass_old
        print 1-csm_fac
        fw_iso.close()
        fw.close()
        fr.close()
        fr_iso.close()
        with file('profile_' + name_file + '.short', 'r+') as modified:
            modified.write(str(int(dat[0]) + u + 1))
        modified.close()
        with file('profile_' + name_file + '.iso.short', 'r+') as modified:
            modified.write(str(int(dat[0]) + u + 1) + '  15')
        modified.close()
        file = '/home/afsari/SNEC-1.01/s18.8_ni56_7_efin_1.00E+51/tables/GridPattern.dat'
        dat = np.loadtxt(file)
        dat_csm=dat[dat>prog_fac]
        print dat_csm
        dat=prog_fac*dat
        print dat
        dat=np.concatenate([dat,dat_csm])
        np.savetxt('GridPattern.dat',dat)




