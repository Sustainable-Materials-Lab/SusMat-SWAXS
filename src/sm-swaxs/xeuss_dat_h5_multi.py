"""This script converts XSACT or Foxtrot dat files to HDF5 format for archival storage"""
import sys
import re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import h5py
import numpy as np


def get_line_number(phrase: str, file_name: str):
    """Determine the line in the text file containing the specified str"""
    with open(file_name, encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            p = re.compile(phrase)
            if p.match(line) is not None:
                return i


def process_dat_file(file_path: str, hdf):
    """determine the header and data block in the dat file and create an
    hdf5 dataset"""
    dataset_name = file_path.stem
    with open(file_path, encoding="utf-8") as infile:
        lines = infile.read().splitlines()
        lines = [line.replace('##', ' ') for line in lines]
        meta = {s.split("   ")[0].replace("# ", "").strip(): s.split(
            "   ")[-1].strip() for s in lines if '#' in s}
        meta = {key.replace("#", ""): value.replace("#", "")
                for key, value in meta.items()}
        meta = {key: value for key, value in meta.items() if key}
        head = get_line_number('.*q\\([AÅ].*', file_path)
        meta["columns"] = lines[head-1].split()
        data = np.genfromtxt(file_path, skip_header=head,
                             usecols=(0, 1, 2), encoding="utf-8")

    dset = hdf.create_dataset(
        dataset_name, data=data, compression='gzip')

    for attr_name, attr_value in meta.items():
        dset.attrs[attr_name] = attr_value


def add_dats_to_hdf5(directory: str, hdf5_filename: str):
    """find all dat files in the current folder and subfolders, then 
    add them to a single hdf5 file"""
    files = list(Path(directory).glob('**/*.dat'))
    hdf = h5py.File(hdf5_filename, 'w')
    with ThreadPoolExecutor() as executor:
        executor.map(lambda file: process_dat_file(file, hdf), files)
    hdf.close()


if __name__ == '__main__':
    add_dats_to_hdf5(sys.argv[1], sys.argv[2])
