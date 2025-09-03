"""This script converts Xeuss edf files to HDF5 format for archival storage"""
import argparse as ap
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import fabio
import h5py



def process_edf_file(file_path: Path, hdf):
    """Create hdf5 dataset from edf file"""
    infile = fabio.open(file_path)
    dataset_name = file_path.stem
    
    dset = hdf.create_dataset(
        dataset_name, data=infile.data, compression='gzip')
    
    for attr_name, attr_value in infile.header.items():
        dset.attrs[attr_name] = attr_value

def add_edfs_to_hdf5():
    """Find all edf files in all subdirectories of the specified
    path and add them to the hdf5"""
    parser = ap.ArgumentParser(description="Convert Xeuss edf files to HDF5 format")
    parser.add_argument("directory", help="Directory containing edf files")
    args = parser.parse_args()
    if ".edf" in args.directory:
        files = [Path(args.directory)]
        args.hdf5_filename = files[0].with_suffix('.h5').name
    else:
        files = list(Path(args.directory).glob('**/*.edf'))
        args.hdf5_filename = Path(args.directory).name + '.h5'
    hdf = h5py.File(args.hdf5_filename,'w')
    with ThreadPoolExecutor() as executor:
        executor.map(lambda file: process_edf_file(file, hdf), files)
    hdf.close()

if __name__ == '__main__':
    add_edfs_to_hdf5()