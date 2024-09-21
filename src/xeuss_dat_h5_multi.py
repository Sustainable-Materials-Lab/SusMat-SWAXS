"""This script converts Xeuss edf files to HDF5 format for archival storage"""
import sys
import re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import h5py
import numpy as np

def get_line_number(phrase, file_name):
    with open(file_name, encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            p = re.compile(phrase)
            if p.match(line) != None:
                return i

def process_edf_file(file_path, hdf):
    # Read the TIFF file
    dataset_name = file_path.stem

    with open(file_path, encoding="utf-8") as infile:
        lines = infile.read().splitlines()
        lines = [line.replace('##', ' ') for line in lines]
        meta = {s.split("   ")[0].replace("# ", "").strip(): s.split(
            "   ")[-1].strip() for s in lines if '#' in s}
        head = get_line_number('.*q\\([AÅ].*',file_path)
        meta["columns"] = lines[head-1].split()
        data = np.genfromtxt(file_path,skip_header=head,usecols=(0,1,2),encoding="utf-8")
    # Open the HDF5 file and add the image data as a dataset
    dset = hdf.create_dataset(
        dataset_name, data=data, compression='gzip')
    for attr_name, attr_value in meta.items():
        dset.attrs[attr_name] = attr_value

def add_edfs_to_hdf5(directory, hdf5_filename):
    files = list(Path(directory).glob('**/*.dat'))
    hdf = h5py.File(hdf5_filename,'w')
    with ThreadPoolExecutor() as executor:
        executor.map(lambda file: process_edf_file(file, hdf), files)
    hdf.close()

if __name__ == '__main__':
    add_edfs_to_hdf5(sys.argv[1],sys.argv[2])
