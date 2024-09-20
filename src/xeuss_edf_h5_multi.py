"""This script converts Xeuss edf files to HDF5 format for archival storage"""
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import fabio
import h5py



def process_edf_file(file_path, hdf):
    # Read the TIFF file
    infile = fabio.open(file_path)
    
    # Get the dataset name from the file name
    dataset_name = file_path.stem
    
    # Open the HDF5 file and add the image data as a dataset
    dset = hdf.create_dataset(
        dataset_name, data=infile.data, compression='gzip')
    for attr_name, attr_value in infile.header.items():
        dset.attrs[attr_name] = attr_value

def add_edfs_to_hdf5(directory, hdf5_filename):
    files = list(Path(directory).glob('**/*.edf'))
    hdf = h5py.File(hdf5_filename,'w')
    with ThreadPoolExecutor() as executor:
        executor.map(lambda file: process_edf_file(file, hdf), files)
    hdf.close()

if __name__ == '__main__':
    add_edfs_to_hdf5(sys.argv[1],sys.argv[2])