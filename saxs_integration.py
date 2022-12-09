# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import h5py
import hdf5plugin
import pyFAI
import fabio
import numpy as np
import os
import glob
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.ticker as ticker
import argparse as ap

parser = ap.ArgumentParser(description=
                           "Perform data reduction on hdf5 data from DESY")

parser.add_argument("sample", help="sample file (.nxs)")
#parser.add_argument("background", help="background file (.nxs)")
parser.add_argument("mask", help="mask file (.edf)")
parser.add_argument("poni", help="PONI configuration file (.poni)")

args = parser.parse_args()

#path = "/home/u0092172/Documents/"
#folder = "DESY/"
#sample = "GA5/GA5_2.nxs"
#background = "water/water_2.nxs"
mask = fabio.open(args.mask)
poni = pyFAI.load(args.poni)#"config_saxs_sdetx_1500_12keV.poni")
file = h5py.File(args.sample,'r')
#bkg = h5py.File(args.background,'r')


#transmission_bkg = bkg['scan']['data']['beamstop_2'][()]/bkg['scan']['data']['ic1'][()]
#print("Background transmission:"+str(transmission_bkg))

transmission_sample = file['scan']['data']['beamstop_2'][()]/file['scan']['data']['ic1'][()]
print("Sample transmission:"+str(transmission_sample))

temperature = str(round(file['scan']['data']['p62']['t95tempproglinkam']['eh.01']['temperature'][()],2))

#data_cor = file['scan']['data']['saxs_raw'][()][0]/transmission_sample - bkg['scan']['data']['saxs_raw'][()][0]/transmission_bkg

data_cor = file['scan']['data']['saxs_raw'][()][0]
#data_cor = bkg['scan']['data']['saxs_raw'][()][0]

data_1D = poni.integrate1d(data_cor, 1000, filename=args.sample+"_"+temperature+'_1D.dat', correctSolidAngle=True,
                                  method='csr', radial_range=(None), azimuth_range=(None),
                                  unit="q_A^-1", mask=mask.data, normalization_factor=1.0,
                                  metadata=None) 

fig, ax = plt.subplots(1,2,figsize=(25,10),constrained_layout=True)
fig1 = ax[0].imshow(data_cor,norm=LogNorm(vmin=1e-1, vmax=10**3),cmap=plt.get_cmap('plasma'))
# fig1 = ax[0].imshow(data_cor,norm=LogNorm(vmin=300, vmax=10**5),cmap=plt.get_cmap('plasma'))
# create an axes on the right side of ax. The width of cax will be 5%
# of ax and the padding between cax and ax will be fixed at 0.05 inch.
divider = make_axes_locatable(ax[0])
cax = divider.append_axes("right", size="5%", pad=0.05)

cbar = plt.colorbar(fig1, cax=cax)
cbar.ax.tick_params(labelsize=25)

ax[0].set_xlabel('pixel',fontsize=25)
ax[0].set_ylabel('pixel',fontsize=25)
ax[0].tick_params(labelsize=25)

# fig2 = ax[1].plot(q, Intensity)
fig2 = ax[1].plot(data_1D[0],data_1D[1])
ax[1].set_xscale('log')
ax[1].set_yscale('log')
ax[1].set_xlabel(r'$Q\/[\AA^{-1}]$',fontsize=25)
ax[1].set_ylabel('intensity [a.u.]',fontsize=25)
# ax[1].set_xticks([0.01,0.1,0.4,0.6])
ax[1].get_xaxis().set_major_formatter(ticker.ScalarFormatter())
ax[1].tick_params(labelsize=25)
plt.savefig(args.sample+"_"+temperature+".png", bbox_inches="tight", dpi=600)