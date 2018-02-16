import scipy.integrate as s
import numpy as np 

def integrate2(x,y):
 ''' integrate2 is cumulative integral y dx, [0, cumtrapz(y,x)] via cumulative trapezoid, formatted (first component 0).''' 
 return np.hstack([0,s.cumtrapz(y,x)])
 #return s.cumtrapz(y,x)

def integral2(x,y):
 ''' integral2 is total integral trapz(y,x).  Consider using simps instead. ''' 
 return s.trapz(y,x) 

def mydiff(x,y):
 ''' mydiff(x,y) returns second-order difference dy/dx except at ends (1st-order) ''' 
 z = y*0.
 z[0] = (y[1]-y[0])/(x[1]-x[0])
 z[-1] = (y[-1]-y[-2])/(x[-1]-x[-2])
 w = np.arange(1,len(z)-1)
 z[w] = (y[w+1]-y[w-1])/(x[w+1]-x[w-1])
 return z

def myrange(x):
    ''' myrange x is just (min, max) ''' 
    return (np.min(x), np.max(x))

def statreport(x):
    ''' print statistics of array ''' 
    print 'min ', np.min(x), '.  median ', np.median(x), '.  mean ', np.mean(x), '.  std ', np.std(x), '. log-mean ', 10.**np.mean(np.log10(x[x>0])), '.  log10-std ', np.std(np.log10(x[x>0])), '= factor of ', 10.**np.std(np.log10(x[x>0])), '. max ', np.max(x), '. ', x.size, ' elements.' 
    return ( np.min(x), np.median(x),  np.mean(x),   np.std(x), 10.**np.mean(np.log10(x[x>0])), np.std(np.log10(x[x>0])), np.max(x)) 

def interploglog(x,y,xnew,order=3, slop = 0.):
    ''' xnew = interploglog(x,y,xnew,order=3, slop = 0.): attempts log-log interpolation to xnew from points where both x,y are >0 ''' 
    from scipy.interpolate import UnivariateSpline as us ## NOTE: YoU NEED INCREASING REAL VALUES OR THIS BREAKS BADLY. 
    w = (x>0)&(y>0)
    return np.exp( us(np.log(x[w]), np.log(y[w]), k = order, s=slop)(np.log(xnew)) )

def flip(x):
 return x[::-1]

def mygradient(x,y,z):
    dxa,dxb = np.gradient(x)
    dya, dyb = np.gradient(y)
    return np.gradient(z,dxa, dyb) # assumes you have the order correct. 

def datathief(filename):
    ''' x,y = datathief(filename) is port of the matlabscripts version.
        ... unfortunately the interactive figure is not really up to snuff.
        You can deterine Left,Right,Low,Up and LeftLim, RightLim,LowLim,UpLim
        yourself and then just copy and paste the rest of the thing.   '''
    import Image 
    import scipy.interpolate as interp
    import matplotlib.pyplot as plt
    #plt.ion()
    f = Image.open(filename)
    plt.clf
    plt.imshow(f)
    plt.show()
    #print 'Click on four points to define a data rectangle... '
    #print 'If this does not work, try the matplotlib magic within IPython. '     
    ## xcoords, ycoords = np.array(plt.ginput(4)).T
    ## plt.plot(xcoords,ycoords,'o')
    ## xsort = np.sort(x)
    ## ysort = np.sort(y)
    Left = input('X pixel-val of left of plot? (Use cursor to find this out) ')*1.0  # np.mean(xsort[:2])  # this means 0 and 1 (NOT including 2) 
    Right = input('X pixel-val of right of plot? (Use cursor to find this out) ')*1.0  #np.mean(xsort[2:])  # this means 2 and on 
    Low = input('Y pixel-val of bottom of plot? (Use cursor to find this out) ')*1.0 #np.mean(ysort[:2])
    Up = input('Y pixel-val of top of plot? (Use cursor to find this out) ')*1.0 #np.mean(ysort[2:])
    LeftLim  = input('x-min (left of graph?) ')*1.0
    RightLim = input('x-max (right of graph?) ')*1.0 
    LowLim   = input('y-min (bottom of graph?) ')*1.0 
    UpLim    = input('y-max (top of graph?) ')*1.0

    print 'click on points to be stolen.  Delete to remove a point.  Return when done.  Other keys act like click ' 
    X,Y = np.array( plt.ginput(n=0, timeout = 100, show_clicks = True) ).T
    x = (X-Left)*(RightLim-LeftLim)/(Right-Left) + LeftLim; 
    y = (Y-Low) *(UpLim-LowLim)    /(Up-Low)     + LowLim;
    return (x,y) 


# values: referenced as U.Year etc
Angstrom = 1.e-8
pi = np.pi
Kps= 1e5
Clight= 2.99792458e10
Ggrav= 6.6726e-8
Hplanck= 6.6260755e-27
Echarge= 4.8032068e-10
Me= 9.1093898e-28
Mp= 1.6726231e-24
Mn= 1.6749286e-24
Kb= 1.380658e-16
Nav= 6.0221367e23
SigmaBlack= 5.67051e-5
Sigmablack= 5.67051e-5
SigmaT= 8*pi/3 *(4.8032068e-10**2/(9.1093898e-28* 2.99792458e10**2))**2 
Ablack= 7.56591e-15
EV= 1.60217733e-12
Lsun= 3.847e33
Msun= 1.9891e33
Rsun= 6.96e10
Teffsun= 5780
Year= 365.25*24*3600
Pc= 3.086e18
Au= 1.495979e13
Amu= 1.66057e-24
Hbar= 6.6260755e-27/(2*pi)
Arcsec= 1.495979e13/3.086e18
Mas= 1.495979e13/3.086e18
Degree= 2*pi/360 
Arcmin= 60*1.495979e13/3.086e18 
Myr= 1e6*365.25*24*3600

def zams(M, logZonZsun=0):
 ''' function L,R,Teff,tyrSN = zamsB.zams(M,logZonZsun=0)
     to get just L, try L, _ = zamsB.zams(m)  ''' 
# function [L,R,Teff,tyrSN] = zams(M,logZonZsun,[ToutTable])
# determines ZAMS using formulae from Tout et al. 96
# Valid range: M: 0.1->100, Z:1e-4 ->0.03
#  Note, if Tout's tables aren't loaded, it loads them. 
#  Supernova times are from a 7th-order polyfit to SB99 results
#    [over the range 8-120 Msun; extrapolation is unwise]
 result = []
 t = np.loadtxt('ToutEqns3and4.txt')
 tEq3 = t[0:7,:].transpose()
 tEq4 = t[7:,:].transpose()
 lz = logZonZsun
 z = np.zeros(np.size(lz)); 
 a,b,c,d,e = tEq3  
 ap,bp,cp,dp,ep = tEq4 
 greekEq3 = a + b*lz + c*lz**2 + d*lz**3 + e*lz**4 #tout eq 3
 greekEq4 = ap + bp*lz + cp*lz**2 + dp*lz**3 + ep*lz**4 #tout eq 4
 alpha, beta, gamma, delta, epsilon, zeta, eta = greekEq3
 theta, iota, kappa, llambda, mu, nu, xi, omicron, pi = greekEq4
 # equation 1 of Tout et al
 L=(alpha*M**5.5+beta*M**11.)/(gamma+M**3.+delta*M**5.+epsilon*M**7.+zeta*M**8.+eta*M**9.5); 
 # eq. 2 
 R=(theta*M**2.5+iota*M**6.5+kappa*M**11.+llambda*M**19.+mu*M**19.5)/(nu + xi*M**2. + omicron*M**8.5 + M**18.5 + pi*M**19.5);

 Teff = 5780*L**0.25/R**0.5; 

 # hmm, this version of tyrSN doesn't seem to work so well. 
 tf = np.array([-3.6512, 39.3154, -178.2995, 441.1129, -642.9829, 553.6047, -263.4056, 61.7241])
 lm = np.log10(M); lt = 0.; 
 for i in np.r_[1:(len(tf)+1)]: lt=lt+lm**(i-1)*tf[-i+1];
 tyrSN = 10**lt;

 result.append([L,R,Teff,tyrSN])
 return(result[0])

def blackbody(nu,T):
    ''' blackbody(nu,T) takes nu array and T and returns Bnu(T). '''
    lamb = Clight/nu 
    return 2*Hplanck*nu/lamb**2/(np.exp(Hplanck*nu/(Kb*T))-1)

def blackfraction(hnuonKT):
    ''' fraction of luminosity in freq > nu in blackbody, based on h nu/kT.  Can take array input '''
    from scipy.integrate import quad
    if hnuonKT.shape[0]==1:
        hnuonKT = np.array([hnuonKT])  # allows us to treat single numbers as well as arrays; otherwise can't use copy(). 
    ion = hnuonKT.copy()*0.
    tot = hnuonKT.copy()*0.
    for i in np.arange(0, hnuonKT.ravel().shape[0] ):
        nu = hnuonKT.ravel()[i]
        ion.ravel()[i], ionerr = quad(lambda nu: nu**3/(np.exp(nu)-1), nu,np.inf)
        tot.ravel()[i], toterr = quad(lambda nu: nu**3/(np.exp(nu)-1), 0,np.inf)
    return ion/tot



