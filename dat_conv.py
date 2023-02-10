# -*- coding: utf-8 -*-
"""
Created on Thu May  7 11:44:10 2015

@author: u0092172
"""
import os
import numpy as np
import argparse as ap
import re


parser = ap.ArgumentParser(description='Sort out stupid Xenocs edf files')
parser.add_argument("input", help="Filename of the .dat (excl. ext.)")
parser.add_argument("--wavelength", help="Wavelength in Angstroms",default=float(1.54189))
parser.add_argument("--highscore",help="Output for highscore plus", action="store_true")
parser.add_argument("--exposure",help="Counting time (convert to counts from CPS)",type=float,default=1)
#parser.add_argument("--dat", help="convert from dat file", action="store_true")
parser.add_argument("--SAXS", help="output SAXS data (q and don't cut low angle)", action="store_true")
parser.add_argument("--renormalize", help="boost counts", action="store_true")
parser.add_argument("--clip", help="clip range", action="store_true")
parser.add_argument("--fullprof",help="general fullprof input", action="store_true")
parser.add_argument("--kratky",help="Generate Kratky plot columns", action="store_true")
parser.add_argument("--pyfai",help="pyfai input", action="store_true")
parser.add_argument("--zero",help="set minimum to zero", action="store_true")
args = parser.parse_args() #map arguments to args

fname=args.input
if args.highscore == True:
    ext = ".asc"
elif args.fullprof == True:
    ext = "_FP.dat"
elif args.kratky == True:
    ext = "_kratky.dat"
else:
    ext = ".xye"



"""Import the data"""
def get_line_number(phrase, file_name):
        with open(file_name, encoding="utf-8") as f:
            for i, line in enumerate(f, 1):
                p = re.compile(phrase)
                if p.match(line) != None:
                    return i
def get_number_lines(file_name):
    with open(file_name, encoding="utf-8") as f:
       for i, line in enumerate(f, 1):
           pass
    return i

if args.kratky == True:
    args.SAXS = True

if args.pyfai == True:
    data = np.genfromtxt(fname,comments='#',usecols=(0,1,2),encoding="utf-8")
else:
    head = get_line_number('.*q\\([AÅ].*',fname)
    data = np.genfromtxt(fname,skip_header=head,usecols=(0,1,2),encoding="utf-8")


data = data[~np.isnan(data).any(axis=1)]

q = data[:,0]
i = data[:,1]
e = data[:,2]

if args.pyfai == True:
    ttheta = q
    if args.clip == True: 
        start = np.where(ttheta>5)[0][0]
        ttheta = ttheta[start:]
        i = i[start:]
        e = e[start:]
elif args.SAXS == False:
    """Calc 2theta"""

    ttheta = 2*np.degrees(np.arcsin((q*args.wavelength)/(4*np.pi)))
    
    """Clip the data to start at 5 degrees to remove excessive intensity"""
    if args.clip == True: 
        start = np.where(ttheta>5)[0][0]
        ttheta = ttheta[start:]
        i = i[start:]
        e = e[start:]
    
    """Convert i to counts"""
if args.renormalize == True:
     i = i*args.exposure*1e11
else:
     i=i*args.exposure
	 
if min(i) < 0:
	i -= min(i)
    
if args.zero == True:
    i -= min(i)

if args.highscore == True:
    out = np.column_stack((ttheta.flatten(),i.flatten()))
else:
    if args.SAXS == False:
        out = np.column_stack((ttheta.flatten(),i.flatten(),e.flatten()))
    elif args.kratky == False:
        out = np.column_stack((q.flatten(),i.flatten(),e.flatten()))
    else:
        q2i = (q**2)*i
        q2sig = (q**2)*e
        out = np.column_stack((q.flatten(),i.flatten(),q2i.flatten(),e.flatten(),q2sig.flatten()))

if args.fullprof == True:
    head2 = 'XYDATA' + '\n' + 'INTER 0 0 2' + 4*'\n'
elif args.kratky == True:
    head2 = "q I(q) q2I(q) sig(q) q2sig(q)"
else:
    head2 = ''

np.savetxt(fname[:-4]+ext,out,delimiter=' ',fmt='%.10f',header=head2,comments='',newline='\n')
