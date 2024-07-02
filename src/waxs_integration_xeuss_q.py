# -*- coding: utf-8 -*-
"""
Absorption correction not implemented correctly
"""

import pyFAI
from pyFAI.azimuthalIntegrator import AzimuthalIntegrator
import fabio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.ticker as ticker
import argparse as ap



parser = ap.ArgumentParser(description=
                           "Perform data reduction on data from Xeuss 2.0C")

parser.add_argument("sample", help="sample file (.edf)")

parser.add_argument("mask", help="mask file (.edf)")
#parser.add_argument("poni", help="PONI configuration file (.poni)")
parser.add_argument("--empty", help="empty file (.edf)")
parser.add_argument("--background", help="background file (.edf)")
parser.add_argument("--opencl", help="Use OpenCL (requires pyopencl)",action="store_true")
parser.add_argument("--bkg_factor", help="background correction factor",type=float,default=float(1))
parser.add_argument("--noabs", help="No absorption correction",action="store_true")
parser.add_argument("--autobkg", help="Automatic background scaling",action="store_true")
parser.add_argument("--xmin",help="Minimum value of radial unit (q)",type=float,default=float(0.36))
parser.add_argument("--xmax",help="Max value of radial unit (q)",type=float,default=float(3.8))
parser.add_argument("--raw2D",help="Display the 2D image in the lab frame",action="store_true")
args = parser.parse_args()


file = fabio.open(args.sample)
mask = fabio.open(args.mask)

args.noabs = True

if args.noabs == False:
    def abscor (tth,intensity,trans):
        fabs = (np.log(trans)*((1/np.cos(np.radians(tth)))-1))/(np.exp(np.log(trans)*((1/np.cos(np.radians(tth)))-1))-1)
        cor_int = intensity/fabs
        return cor_int
else:
    def abscor (tth,intensity,trans):
        return intensity

if args.opencl==True:
    intmeth='opencl'
else:
    intmeth='csr'



geo = {               
      "detector": pyFAI.detectors.Detector(float(file.header['PSize_2']),float(file.header['PSize_1'])),
      "dist": float(file.header['SampleDistance']),
      "poni1": float(file.header['PSize_2'])*float(file.header['Center_2']),
      "poni2": float(file.header['PSize_1'])*float(file.header['Center_1']),
      "rot1": 0,
      "rot2": 0,
      "rot3": 0,
      "wavelength": float(file.header['WaveLength'])
}

poni = AzimuthalIntegrator(**geo)
try:
    transmission_sample = float(file.header['Transmission'])
except KeyError:
    transmission_sample = 1
print("Sample transmission:"+str(round(transmission_sample,4)))

#norm_sample = float(file.header['Intensity1'])
norm_sample = 1


data_1D = poni.integrate1d(file.data,
                           1000, correctSolidAngle=True,
                                  method=intmeth, radial_range=(args.xmin,args.xmax), azimuth_range=(None),
                                  unit="q_A^-1", mask=mask.data, normalization_factor=norm_sample,
                                  metadata=None,error_model="poisson") 

data_1D = [data_1D[0],data_1D[1],data_1D[2]]
data_1D[1] = abscor(data_1D[0],data_1D[1],transmission_sample)

data_2D = file.data/transmission_sample

if args.background != None:
    bkg = fabio.open(args.background)
    if np.allclose(float(bkg.header['Transmission']),1,atol=5e-3) == True:
        transmission_bkg = 1
    else:
        transmission_bkg = float(bkg.header['Transmission'])

    print("Background transmission:"+str(round(transmission_bkg,4)))

    #norm_bkg = float(bkg.header['Intensity1'])
    norm_bkg = 1
    bkg_1D = poni.integrate1d(bkg.data,
                              1000, correctSolidAngle=True,
                                  method=intmeth, radial_range=(args.xmin,args.xmax), azimuth_range=(None),
                                  unit="q_A^-1", mask=mask.data, normalization_factor=norm_bkg,
                                  metadata=None,error_model="poisson")
    bkg_1D = [bkg_1D[0],bkg_1D[1],bkg_1D[2]]
    bkg_1D[1] = abscor(bkg_1D[0],bkg_1D[1],transmission_bkg)
    
    bkg_2D = bkg.data/transmission_bkg
    
    if args.autobkg == True:
        print("Use automated background scaling with caution!")
        if max(bkg_1D[1][:np.where(bkg_1D[0]>0.02)[0][0]]) > max(data_1D[1][:np.where(data_1D[0]>0.02)[0][0]]):
            bkg_1D = [bkg_1D[0],bkg_1D[1],bkg_1D[2]]
            bkg_1D[1] -=  max(bkg_1D[1][:np.where(bkg_1D[0]>0.02)[0][0]]) - max(data_1D[1][:np.where(data_1D[0]>0.02)[0][0]])
else:
    data_I = data_1D[1]
    data_sig = abs(data_1D[2])
    bkg_2D = 0
if args.empty != None:
    empty = fabio.open(args.empty)
    if np.allclose(float(empty.header['Transmission']),1,atol=5e-3) == True:
        transmission_empty = 1
    else:
        transmission_empty = float(empty.header['Transmission'])
    norm_empty = float(empty.header['Intensity1'])
    norm_empty = 1
    empty_1D = poni.integrate1d(empty.data,
                              1000, correctSolidAngle=True,
                                  method=intmeth, radial_range=(args.xmin,args.xmax), azimuth_range=(None),
                                  unit="q_A^-1", mask=mask.data, normalization_factor=norm_empty,
                                  metadata=None,error_model="poisson")
    empty_1D = [empty_1D[0],empty_1D[1],empty_1D[2]]
    empty_1D[1] = abscor(empty_1D[0],empty_1D[1],transmission_empty)
    
    empty_2D = empty.data/transmission_empty
    
    if args.autobkg == True:
        if max(empty_1D[1][:np.where(empty_1D[0]>0.02)[0][0]]) > max(data_1D[1][:np.where(data_1D[0]>0.02)[0][0]]):
            empty_1D[1] -= max(empty_1D[1][:np.where(empty_1D[0]>0.02)[0][0]]) - max(data_1D[1][:np.where(data_1D[0]>0.02)[0][0]])
    if args.background != None:
        data_I = (data_1D[1]-empty_1D[1])-(bkg_1D[1]-empty_1D[1])
        data_2I = (data_2D-empty_2D)-(bkg_2D-empty_2D)
        data_sig = abs(data_1D[2])+abs(empty_1D[2])+abs(bkg_1D[2])+abs(empty_1D[2])
    else:
        data_I = data_1D[1]-empty_1D[1]
        data_2I = data_2D-empty_2D
        data_sig = abs(data_1D[2])+abs(empty_1D[2])
else:
    if args.background == None:
        data_I = data_1D[1]
        data_2I = data_2D
        data_sig = abs(data_1D[2])
    else:
        data_I = data_1D[1]-bkg_1D[1]
        data_2I = data_2D - bkg_2D
        data_sig = abs(data_1D[2])+abs(bkg_1D[2])
if args.raw2D == False:
    data_2I2 = poni.integrate2d(data_2I,3000,3600,unit="q_A^-1")

    I2,q2,chi2 = data_2I2

    if np.min(I2) < 0:
        I2min = 1e-1
    else:
        I2min = np.min(I2)
    I2max = np.max(I2)
else:
    if np.min(data_2I) < 0:
        I2min = 1e-1
    else:
        I2min = np.min(data_2I)
    I2max = np.max(data_2I)

fig, axs = plt.subplot_mosaic([['(a)','(b)']],figsize=(6.5,3.5),constrained_layout=True)
if args.raw2D == False:
    fig1 = axs['(a)'].imshow(I2,origin="lower",extent=[q2.min(),q2.max(),chi2.min(),chi2.max()],
                             norm=LogNorm(vmin=I2min, vmax=I2max),cmap=plt.get_cmap('inferno'),aspect="auto")
    axs['(a)'].set_xlabel(r'q /$\AA^{-1}$',fontsize=8)
    axs['(a)'].set_ylabel(r'$\phi$ /$^{\circ}$',fontsize=8)
else:
    fig1 = axs['(a)'].imshow(data_2I,norm=LogNorm(vmin=I2min, vmax=I2max),cmap=plt.get_cmap('inferno'),aspect="auto")
    axs['(a)'].set_xlabel('X /px',fontsize=8)
    axs['(a)'].set_ylabel('Z /px',fontsize=8)   
divider = make_axes_locatable(axs['(a)'])
cax = divider.append_axes("top", size="5%", pad=0.05)

cbar = plt.colorbar(fig1, cax=cax,orientation="horizontal")
cbar.ax.tick_params(labelsize=8)
cax.xaxis.set_ticks_position("top")

axs['(a)'].tick_params(labelsize=8)

fig2 = axs['(b)'].errorbar(data_1D[0],data_I,yerr=data_sig,linestyle='',)

#axs['(b)'].set_xscale('log')
#axs['(b)'].set_yscale('log')
axs['(b)'].set_xlabel(r'q /$\AA^{-1}$',fontsize=8)
axs['(b)'].set_ylabel('I /Arb.',fontsize=8)
#axs['(b)'].get_xaxis().set_major_formatter(ticker.ScalarFormatter())
#axs['(b)'].get_yaxis().set_major_formatter(ticker.ScalarFormatter())
#axs['(b)'].ticklabel_format(style='sci', axis='both', scilimits=(0,0))
axs['(b)'].yaxis.major.formatter._useMathText = True
axs['(b)'].xaxis.major.formatter._useMathText = True
#axs['(b)'].set_xticks([0.01,0.1,1])
#axs['(b)'].get_xaxis().set_major_formatter(ticker.ScalarFormatter())
axs['(b)'].tick_params(labelsize=8)
#plt.show()
plt.savefig(args.sample[:-4]+".svg", bbox_inches="tight")

#data_out = np.column_stack((data_1D[0],data_I,data_sig))
#np.savetxt(args.sample[:-4]+"_subtracted.dat",data_out,delimiter='\t',fmt='%s')
