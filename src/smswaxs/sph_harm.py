# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 11:00:51 2022

@author: u0092172
"""

import matplotlib.pyplot as plt
import scipy.special as sp
from scipy.special import factorial
from sympy.functions.special.polynomials import assoc_legendre
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm,colors
import argparse as ap

parser = ap.ArgumentParser(description='Plot spherical harmonics functions given by TOPAS')
parser.add_argument("c00", help="Coefficient 00",type=float)
parser.add_argument("c20", help="Coefficient 20",type=float)
parser.add_argument("c22p", help="Coefficient 22p",type=float)
parser.add_argument("c22m", help="Coefficient 22m",type=float)
parser.add_argument("c40", help="Coefficient 40",type=float)
parser.add_argument("c42p", help="Coefficient 42p",type=float)
parser.add_argument("c42m", help="Coefficient 42m",type=float)
parser.add_argument("c44p", help="Coefficient 44p",type=float)
parser.add_argument("c44m", help="Coefficient 44m",type=float)
parser.add_argument("c60", help="Coefficient 60",type=float)
parser.add_argument("c62p", help="Coefficient 62p",type=float)
parser.add_argument("c62m", help="Coefficient 62m",type=float)
parser.add_argument("c64p", help="Coefficient 64p",type=float)
parser.add_argument("c64m", help="Coefficient 64m",type=float)
parser.add_argument("c66p", help="Coefficient 66p",type=float)
parser.add_argument("c66m", help="Coefficient 66m",type=float)
parser.add_argument("c80", help="Coefficient 80",type=float)
parser.add_argument("c82p", help="Coefficient 82p",type=float)
parser.add_argument("c82m", help="Coefficient 82m",type=float)
parser.add_argument("c84p", help="Coefficient 84p",type=float)
parser.add_argument("c84m", help="Coefficient 84m",type=float)
parser.add_argument("c86p", help="Coefficient 86p",type=float)
parser.add_argument("c86m", help="Coefficient 86m",type=float)
parser.add_argument("c88p", help="Coefficient 88p",type=float)
parser.add_argument("c88m", help="Coefficient 88m",type=float)

args = parser.parse_args()

phi, theta = np.mgrid[0:2*np.pi:200j,0:np.pi:100j]

def Nlm (l,m):
    N = np.sqrt(((2*l+1)/(4*np.pi))*(factorial((l-m))/factorial((l+m))))
    return N

def y20 (theta):
    y = Nlm(2,0)*(assoc_legendre(2,0,np.cos(theta)))
    return y

def y40 (theta):
    y = Nlm(4,0)*(assoc_legendre(4,0,np.cos(theta)))
    return y

def y60 (theta):
    y = Nlm(6,0)*(assoc_legendre(6,0,np.cos(theta)))
    return y

def y80 (theta):
    y = Nlm(8,0)*(assoc_legendre(8,0,np.cos(theta)))
    return y

def y22p (theta,phi):
    y = np.sqrt(2)*Nlm(2,2)*np.cos(2*phi)*(assoc_legendre(2,2,np.cos(theta)))
    return y

def y22m (theta,phi):
    y = np.sqrt(2)*Nlm(2,2)*np.sin(2*phi)*(assoc_legendre(2,2,np.cos(theta)))
    return y

def y42p (theta,phi):
    y = np.sqrt(2)*Nlm(4,2)*np.cos(2*phi)*(assoc_legendre(4,2,np.cos(theta)))
    return y

def y42m (theta,phi):
    y = np.sqrt(2)*Nlm(4,2)*np.sin(2*phi)*(assoc_legendre(4,2,np.cos(theta)))
    return y

def y62p (theta,phi):
    y = np.sqrt(2)*Nlm(6,2)*np.cos(2*phi)*(assoc_legendre(6,2,np.cos(theta)))
    return y

def y62m (theta,phi):
    y = np.sqrt(2)*Nlm(6,2)*np.sin(2*phi)*(assoc_legendre(6,2,np.cos(theta)))
    return y

def y82p (theta,phi):
    y = np.sqrt(2)*Nlm(8,2)*np.cos(2*phi)*(assoc_legendre(8,2,np.cos(theta)))
    return y

def y82m (theta,phi):
    y = np.sqrt(2)*Nlm(8,2)*np.sin(2*phi)*(assoc_legendre(8,2,np.cos(theta)))
    return y

def y44p (theta,phi):
    y = np.sqrt(2)*Nlm(4,4)*np.cos(4*phi)*(assoc_legendre(4,4,np.cos(theta)))
    return y

def y44m (theta,phi):
    y = np.sqrt(2)*Nlm(4,4)*np.sin(4*phi)*(assoc_legendre(4,4,np.cos(theta)))
    return y

def y64p (theta,phi):
    y = np.sqrt(2)*Nlm(6,4)*np.cos(4*phi)*(assoc_legendre(6,4,np.cos(theta)))
    return y

def y64m (theta,phi):
    y = np.sqrt(2)*Nlm(6,4)*np.sin(4*phi)*(assoc_legendre(6,4,np.cos(theta)))
    return y

def y84p (theta,phi):
    y = np.sqrt(2)*Nlm(8,4)*np.cos(4*phi)*(assoc_legendre(8,4,np.cos(theta)))
    return y

def y84m (theta,phi):
    y = np.sqrt(2)*Nlm(8,4)*np.sin(4*phi)*(assoc_legendre(8,4,np.cos(theta)))
    return y

def y66p (theta,phi):
    y = np.sqrt(2)*Nlm(6,6)*np.cos(6*phi)*(assoc_legendre(6,6,np.cos(theta)))
    return y

def y66m (theta,phi):
    y = np.sqrt(2)*Nlm(6,6)*np.sin(6*phi)*(assoc_legendre(6,6,np.cos(theta)))
    return y

def y86p (theta,phi):
    y = np.sqrt(2)*Nlm(8,6)*np.cos(6*phi)*(assoc_legendre(8,6,np.cos(theta)))
    return y

def y86m (theta,phi):
    y = np.sqrt(2)*Nlm(8,6)*np.sin(6*phi)*(assoc_legendre(8,6,np.cos(theta)))
    return y

def y88p (theta,phi):
    y = np.sqrt(2)*Nlm(8,8)*np.cos(8*phi)*(assoc_legendre(8,8,np.cos(theta)))
    return y

def y88m (theta,phi):
    y = np.sqrt(2)*Nlm(8,8)*np.sin(8*phi)*(assoc_legendre(8,8,np.cos(theta)))
    return y

y20n = np.frompyfunc(y20,1,1)
y40n = np.frompyfunc(y40,1,1)
y60n = np.frompyfunc(y60,1,1)
y80n = np.frompyfunc(y80,1,1)

y22pn = np.frompyfunc(y22p,2,1)
y22mn = np.frompyfunc(y22m,2,1)
y42pn = np.frompyfunc(y42p,2,1)
y42mn = np.frompyfunc(y42m,2,1)
y44pn = np.frompyfunc(y44p,2,1)
y44mn = np.frompyfunc(y44m,2,1)
y62pn = np.frompyfunc(y62p,2,1)
y62mn = np.frompyfunc(y62m,2,1)
y64pn = np.frompyfunc(y64p,2,1)
y64mn = np.frompyfunc(y64m,2,1)
y66pn = np.frompyfunc(y66p,2,1)
y66mn = np.frompyfunc(y66m,2,1)
y82pn = np.frompyfunc(y82p,2,1)
y82mn = np.frompyfunc(y82m,2,1)
y84pn = np.frompyfunc(y84p,2,1)
y84mn = np.frompyfunc(y84m,2,1)
y86pn = np.frompyfunc(y86p,2,1)
y86mn = np.frompyfunc(y86m,2,1)
y88pn = np.frompyfunc(y88p,2,1)
y88mn = np.frompyfunc(y88m,2,1)

y00 = 1
y20r = y20n(theta).astype(float)
y40r = y40n(theta).astype(float)
y60r = y60n(theta).astype(float)
y80r = y80n(theta).astype(float)

y22pr = y22pn(theta,phi).astype(float)
y22mr = y22mn(theta,phi).astype(float)
y42pr = y42pn(theta,phi).astype(float)
y42mr = y42mn(theta,phi).astype(float)
y44pr = y44pn(theta,phi).astype(float)
y44mr = y44mn(theta,phi).astype(float)
y62pr = y62pn(theta,phi).astype(float)
y62mr = y62mn(theta,phi).astype(float)
y64pr = y64pn(theta,phi).astype(float)
y64mr = y64mn(theta,phi).astype(float)
y66pr = y66pn(theta,phi).astype(float)
y66mr = y66mn(theta,phi).astype(float)
y82pr = y82pn(theta,phi).astype(float)
y82mr = y82mn(theta,phi).astype(float)
y84pr = y84pn(theta,phi).astype(float)
y84mr = y84mn(theta,phi).astype(float)
y86pr = y86pn(theta,phi).astype(float)
y86mr = y86mn(theta,phi).astype(float)
y88pr = y88pn(theta,phi).astype(float)
y88mr = y88mn(theta,phi).astype(float)

R = y00*args.c00 + y20r*args.c20 + y22pr*args.c22p + y22mr*args.c22m\
    + y40r*args.c40 + y42pr*args.c42p + y42mr*args.c42m + y44pr*args.c44p\
    + y44mr*args.c44m + y60r*args.c60 + y62pr*args.c62p + y62mr*args.c62m\
    + y64pr*args.c64p + y64mr*args.c64m + y66pr*args.c66p + y66mr*args.c66m \
    + y80r*args.c80 + y82pr*args.c82p + y82mr*args.c82m + y84pr*args.c84p\
    + y84mr*args.c84m + y86pr*args.c86p + y86mr*args.c86m\
    + y88pr*args.c88p + y88mr*args.c88m

x = R*np.sin(theta)*np.cos(phi)
y = R*np.sin(theta)*np.sin(phi)
z = R*np.cos(theta)

fig, ax = plt.subplots(subplot_kw=dict(projection='3d'), figsize=(14,10))
m = cm.ScalarMappable(cmap=cm.jet)
norm = colors.Normalize()
ax.plot_surface(x, y, z, rstride=1, cstride=1, facecolors=cm.jet(norm(R)))

plt.savefig('sph_harm.svg', bbox_inches='tight')