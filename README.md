# SWAXS tools

## Description
This is a collection of scripts to perform data conversion and integration on X-ray scattering data, specifically for data collected on the Xenocs Xeuss SWAXS instrument.

**Available tools:**
- `sm-datconv` - Converts Xenocs format 1D data (.dat) to TOPAS compatible .xye format
- `sm-edfh5` - Convert EDF files to HDF5 format with metadata preservation
- `sm-saxsint` - Integrate 2D SAXS data from Xenocs Xeuss instruments with background subtraction
- `sm-waxsint` - Integrate 2D WAXS data from Xenocs Xeuss instruments with absorption correction
- `sm-spharm` - Visualize spherical harmonics functions from TOPAS coefficients

## Installation
Install in a virtual environment to avoid dependency conflicts:

```bash
pip install SusMat-SWAXS
```

Or install from source:

```bash
git clone https://gitlab.kuleuven.be/susmat/general/swaxs-1d-data-conversion.git
cd swaxs-1d-data-conversion
pip install -e .
```


## Usage
All scripts are available as command-line tools after installation. Use the `--help` flag with any command to see detailed usage information.

### sm-datconv
Converts Xenocs format 1D data (.dat) to TOPAS compatible .xye format.

**Input:** `.dat` file with tab-separated columns for q, I(q) (and optionally sigma).

**Usage:**
```bash
sm-datconv <filename_without_extension>
```

**Output:** `.xye` file with tab-separated columns for 2θ, I, and error (if present in input).

**Batch processing example (PowerShell):**
```powershell
Get-ChildItem -Filter *.dat | ForEach-Object -Process {sm-datconv $_.BaseName}
```

### sm-edfh5
Convert multiple EDF files to a single HDF5 file with metadata preservation.

**Usage:**
```bash
sm-edfh5 <path to directory containing edf files>
```

This tool provides an interactive interface for selecting and converting EDF files.

### sm-saxsint
Integrate 2D SAXS data from Xenocs Xeuss instruments with background subtraction and absorption correction.

**Usage:**
```bash
sm-saxsint <sample.edf> <mask.edf> [OPTIONS]
```

**Key options:**
- `--poni <file.poni>` - PONI calibration file
- `--background <bkg.edf>` - Background file for subtraction
- `--bkg_factor <float>` - Background scaling factor (default: 1.0)
- `--unit <q|2th>` - Radial unit for integration (default: q)
- `--xmin <float>` - Minimum q value (default: 0.004)
- `--xmax <float>` - Maximum q value (default: 0.7)
- `--opencl` - Use OpenCL acceleration (requires pyopencl)
- `--raw2D` - Display 2D image in lab frame

**Output:** 
- `*_1D.dat` - Integrated 1D data
- `*_subtracted.dat` - Background-subtracted data
- `*.svg` - Visualization plot

### sm-waxsint
Integrate 2D WAXS data from Xenocs Xeuss instruments with absorption correction.

**Usage:**
```bash
sm-waxsint <sample.edf> <mask.edf> [OPTIONS]
```

**Key options:**
- `--poni <file.poni>` - PONI calibration file
- `--background <bkg.edf>` - Background file for subtraction
- `--bkg_factor <float>` - Background scaling factor (default: 1.0)
- `--unit <q|2th>` - Radial unit for integration (default: q)
- `--xmin <float>` - Minimum q value (default: 0.36)
- `--xmax <float>` - Maximum q value (default: 3.8)
- `--lac <float>` - Linear absorption coefficient in cm⁻¹ for thickness correction
- `--thickness <float>` - Sample thickness in cm for transmission correction
- `--noabs` - Disable absorption correction
- `--opencl` - Use OpenCL acceleration (requires pyopencl)
- `--raw2D` - Display 2D image in lab frame

**Output:**
- `*_1D.dat` - Integrated 1D data
- `*_subtracted.dat` - Background-subtracted, absorption-corrected data
- `*.svg` - Visualization plot

### sm-spharm
Visualize spherical harmonics functions using coefficients from TOPAS academic output files.

**Usage:**
```bash
sm-spharm C00 C20 C22P C22M C40 C42P C42M C44P C44M C60 C62P C62M C64P C64M C66P C66M C80 C82P C82M C84P C84M C86P C86M C88P C88M [OPTIONS]
```

**Arguments:** 25 spherical harmonics coefficients (c00 through c88m) from TOPAS output file

**Options:**
- `--output <filename>` / `-o <filename>` - Output filename for the plot (default: sph_harm.svg)
- `--resolution <int>` / `-r <int>` - Angular resolution for the plot (default: 200)

**Example:**
```bash
sm-spharm 1 -0.54889 0.48504 0.74711 0.79916 -0.33178 0.16323 0.45369 \
          -0.29782 -0.29214 -0.43949 0.01524 0.09042 0.85340 0.40316 \
          -0.01881 1.47673 -0.55751 -0.68970 0.02621 -0.06565 -0.56472 \
          1.00981 -0.12339 -0.25831 --output my_spherical_harmonics.svg
```

**Output:** 3D visualization plot showing the spherical harmonics function in real space

### Programmatic Usage

The CLI functions can also be imported and used in Python scripts:

```python
import smswaxs

# Access CLI functions programmatically
smswaxs.dat_conv_cli()
smswaxs.add_edfs_to_hdf5()
smswaxs.saxs_integration_cli()
smswaxs.waxs_integration_cli()
smswaxs.sph_harm_cli()

# Check package version
print(smswaxs.__version__)
```

## Support
Contact Sam (@u0092172)

## Contributing
Contact Sam (@u0092172) if you are interested in contributing.

## Authors and acknowledgment
Originally authored by Sam Eyley (@u0092172). 

Significant portions of code were developed with the help of Github Copilot (2025).

## License
MIT License
