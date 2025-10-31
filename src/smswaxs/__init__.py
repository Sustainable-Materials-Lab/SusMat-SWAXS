"""
SusMat-SWAXS: A collection of python scripts for SWAXS data processing and conversion.

This package provides tools for:
- SAXS/WAXS data integration from Xenocs Xeuss instruments
- Data format conversions (EDF to HDF5, TIFF, etc.)
- Background subtraction and absorption corrections
- Data visualization and analysis
"""

__version__ = "1.1.0"
__author__ = "Samuel Eyley"
__email__ = "samuel.eyley@kuleuven.be"

# Import CLI functions for programmatic access
from .dat_conv import cli as dat_conv_cli
from .xeuss_edf_h5_multi import add_edfs_to_hdf5
from .saxs_integration_xeuss import cli as saxs_integration_cli
from .waxs_integration_xeuss import cli as waxs_integration_cli
from .sph_harm import cli as sph_harm_cli

# Make CLI functions available at package level
__all__ = [
    "__version__",
    "__author__", 
    "__email__",
    "dat_conv_cli",
    "add_edfs_to_hdf5", 
    "saxs_integration_cli",
    "waxs_integration_cli",
    "sph_harm_cli"
]