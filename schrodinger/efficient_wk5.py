# Basically, I copied the sympy-less answer from Tutor. Only wrote the
# hydrogen_wave_func myself. My versions are way too slow to run on tutor,
# though I think there's a way to get sympy to calculate the functions
# necessary once and then just cache efficient versions of them (lambdaify
# or something). Worth looking into.

import numpy as np
import scipy.constants as c
from math import cos, e, pi, isnan

a = c.physical_constants['Bohr radius'][0]

def spherical_to_cartesian(r,theta,phi):
    x=r*np.sin(theta)*np.cos(phi)
    y=r*np.sin(theta)*np.sin(phi)
    z=r*np.cos(theta)
    return round(x,5),round(y,5),round(z,5)

def cartesian_to_spherical(x, y, z):
    x=float(x)
    y=float(y)
    z=float(z)
    r=np.sqrt(x**2+y**2+z**2)
    rxy=np.sqrt(x**2+y**2)
    if x!=0:
        phi=np.arctan(y/x)
    else:
        eps=1e-10
        phi=np.arctan(y/eps)
    theta=np.arccos(z/r)
    return round(r,5), round(theta,5), round(phi,5)


def l00(x):
    return 1

def l01(x):
    return -x+1

def l02(x):
    return x*x-4*x+2

def l03(x):
    return -x*x*x+9*x*x-18*x+6

def l04(x):
    return x ** 4 - 16 * x ** 3 + 72 * x ** 2 - 96 * x +24

def l10(x):
    return 1

def l11(x):
    return -2*x+4

def l12(x):
    return 3*x*x-18*x+18

def l13(x):
    return -4*x*x*x+48*x*x-144*x+96

def l14(x):
    return 5 * x ** 4 - 100 * x ** 3 + 600 * x ** 2 - 1200 * x + 600

def l15(x):
    return -720 * (x - 6)

def l20(x):
    return 2

def l21(x):
    return -6*x+18

def l22(x):
    return 12*x*x-96*x+144

def l23(x):
    return -20*x*x*x+300*x*x-1200*x+1200

def l24(x):
    return 30 * x ** 4 - 720 * x ** 3 + 5400 * x ** 2 - 14400 * x + 10800

def l30(x):
    return 6

def l31(x):
    return -24*x+96

def l32(x):
    return 60*x*x-600*x+1200

def l33(x):
    return -120 * x ** 3 + 2160 * x ** 2 - 10800 * x + 14400

def l34(x):
    return -210 * x ** 4 + 5880 * x ** 3 - 52920 * x ** 2 + 176400 * x - 176400

def l44(x):
    return 1680 * x ** 4 - 53760 * x ** 3 + 564480 * x ** 2 - 2257920 * x + 2822400

def l50(x):
    return 120

def l51(x):
    return -720 * (x - 6)

def l70(x):
    return 5040

def assoc_laguerre(p,qmp):
    if p==0 and qmp==0:
        return l00
    elif p==0 and qmp==1:
        return l01
    elif p==0 and qmp==2:
        return l02
    elif p==0 and qmp==3:
        return l03
    elif p==0 and qmp==4:
        return l04
    elif p==1 and qmp==0:
        return l10
    elif p==1 and qmp==1:
        return l11
    elif p==1 and qmp==2:
        return l12
    elif p==1 and qmp==3:
        return l13
    elif p==1 and qmp==4:
        return l14
    elif p==1 and qmp==5:
        return l15
    elif p==2 and qmp==0:
        return l20
    elif p==2 and qmp==1:
        return l21
    elif p==2 and qmp==2:
        return l22
    elif p==2 and qmp==3:
        return l23
    elif p==2 and qmp==4:
        return l24
    elif p==3 and qmp==0:
        return l30
    elif p==3 and qmp==1:
        return l31
    elif p==3 and qmp==2:
        return l32
    elif p==3 and qmp==3:
        return l33
    elif p==3 and qmp==4:
        return l34
    elif p==4 and qmp==4:
        return l44
    elif p==5 and qmp==0:
        return l50
    elif p==5 and qmp==1:
        return l51
    elif p==7 and qmp==0:
        return l70
    else:
        return None

def fact(n):
    result=1
    while n>1:
        result*=n
        n-=1
    return result

def radial_wave_func(n,l,r):
    a=c.physical_constants['Bohr radius'][0]
    y1=(2.0/(n*a))**3
    y2=fact(n-l-1)/float(2*n*fact(n+l)**3)
    ya=np.sqrt(y1*y2)*np.exp(-r/(n*a))
    yb=(2*r/(n*a))**l
    lfunc=assoc_laguerre(2*l+1,n-l-1)
    yc=lfunc(2*r/(n*a))
    #print ya, yb, yc
    return np.round((ya*yb*yc)/(a**(-1.5)),5)

def p00(theta):
    return 1

def p01(theta):
    return np.cos(theta)

def p02(theta):
    return 0.5*(3*np.cos(theta)**2-1)

def p03(theta):
    return 0.5*(5*np.cos(theta)**3-3*np.cos(theta))

def p04(theta):
    return 0.125 * (35 * np.cos(theta) ** 4 - 30 * np.cos(theta) ** 2 + 3)

def p11(theta):
    return np.sin(theta)

def p12(theta):
    return 3*np.sin(theta)*np.cos(theta)

def p13(theta):
    return 1.5*np.sin(theta)*(5*np.cos(theta)**2-1)

def p14(theta):
    return 2.5 * (7 * np.cos(theta) ** 3 - 3 * np.cos(theta)) * np.sin(theta)

def p20(theta):
    return 0.5 * (3 * (np.cos(theta) ** 2) - 1)

def p22(theta):
    return 3*np.sin(theta)**2

def p23(theta):
    return 15*np.sin(theta)**2*np.cos(theta)


def p24(theta):
    return 7.5 * (7 * np.cos(theta) ** 2 - 1) * np.sin(theta) ** 2

def p33(theta):
    return 15*np.sin(theta)*(1-np.cos(theta)**2)

def p34(theta):
    return 105 * np.cos(theta) * np.sin(theta) ** 3

def p43(theta):
    return 105 * np.cos(theta) * np.sin(theta) ** 3

def p44(theta):
    return 105 * np.sin(theta) ** 4

def assoc_legendre(m,l):
    m=abs(m)
    if m==0 and l==0:
        return p00
    elif m==0 and l==1:
        return p01
    elif m==0 and l==2:
        return p02
    elif m==0 and l==3:
        return p03
    elif m==0 and l==4:
        return p04
    elif m==1 and l==1:
        return p11
    elif m==1 and l==2:
        return p12
    elif m==1 and l==3:
        return p13
    elif m==1 and l==4:
        return p14
    elif m==2 and l==0:
        return p20
    elif m==2 and l==2:
        return p22
    elif m==2 and l==3:
        return p23
    elif m==2 and l==4:
        return p24
    elif m==3 and l==3:
        return p33
    elif m==3 and l==4:
        return p34
    elif m==4 and l==3:
        return p43
    elif m==4 and l==4:
        return p44
    else:
        return None

def azimuth(m,theta):

    return np.exp(1j* m * theta)

def angular_wave_func(m,l,theta,phi):
    if m>=0:
        eps=(-1)**m
    else:
        eps=1

    y1=(2*l+1)/(4.0*c.pi)
    y2=float(fact(l-abs(m)))/fact(l+abs(m))
    ymid=np.sqrt(y1*y2)
    pfunc=assoc_legendre(m,l)
    x=azimuth(m,phi)
    #print ymid,x, pfunc(theta)
    result=eps*ymid*x*pfunc(theta)
    #newresult=round(result.real,5)+1j*round(result.imag,5)
    return np.round(result,5)

def hydrogen_wave_func(n, l, m, r_max, *n_xyz):
    x, y, z = [np.linspace(-r_max, r_max, n_dim) for n_dim in n_xyz]
    cartesian_mesh   = np.meshgrid(x, y, z)

    r3, theta3, phi3 = np.vectorize(cartesian_to_spherical)(*cartesian_mesh)
    r3              *= a

    ang_func, rad_func = map(np.vectorize, [angular_wave_func, radial_wave_func])
    ang_mag,  rad_mag  = ang_func(m,l,theta3,phi3), rad_func(n,l,r3)

    density = np.absolute(ang_mag*rad_mag)**2
    density = np.round(density, 5)

    x3, y3, z3 = np.round(cartesian_mesh, 5)

    return x3, y3, z3, density
