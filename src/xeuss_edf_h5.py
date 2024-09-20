"""This script converts Xeuss edf files to HDF5 format for archival storage"""
import sys
from pathlib import Path
import fabio
import h5py

file_path = Path(sys.argv[1])

infile = fabio.open(file_path)

output_path = file_path.with_suffix(".h5")

with h5py.File(output_path, 'w') as hdf:
    dset = hdf.create_dataset(
        infile.header['EDF_DataBlockID'], data=infile.data, compression='gzip')
    for attr_name, attr_value in infile.header.items():
        dset.attrs[attr_name] = attr_value
