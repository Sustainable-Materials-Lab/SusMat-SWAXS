# SWAXS tools

## Description
This is a collection of scripts to perform data conversion on X-ray scattering data.

dat_conv - Converts Xenocs format 1D data (.dat) to TOPAS compatible .xye
sph_harm - Plot the spherical harmonics function using coefficients from TOPAS input file
saxs_integration - Integrate SAXS data from different sources
sph_harm - calculate the visual representation of a spherical harmonics function in real space.
topas_init - Automate creation of topas input files
xeuss_ - scripts designed for data conversion for files from Xenocs Xeuss instrumentation

## Installation
Install in a virtual environment to avoid clashes.


## Usage
All scripts are designed to be run from the command line with arguments. Command line interface is not always annotated.

### dat_conv

#### Input
.dat file consisting of tab separated columns for q, I(q) (and sigma q).

```shell
python dat_conv.py <filename_without_extension>
```
To automate for an entire folder in windows, you could use PowerShell:

```powershell
Get-ChildItem -Filter *.dat | ForEach-Object -Process {python.exe dat_conv.py $_.BaseName}
```

#### Output
.xy(e) file consisting of tab separated columns for 2theta, I and error if present in the input.

### sph_harm

#### Input
Coefficients of spherical harmonics function from the TOPAS academic output file (.out)

`python sph_harm.py <c00> <c20>...`

e.g.
```shell
python sph_harm.py 1 -.54889 0.48504 0.74711 0.79916 -0.33178 0.16323 0.45369 -.29782 -.29214 -.43949\
 .01524 .09042 .85340 .40316 -.01881 1.47673 -.55751 -.68970 .02621 -.06565 -.56472 1.00981 -.12339 -.25831
```

#### Output
Image containing a graphical representation of the function.

## Support
Contact Sam (@u0092172)

## Contributing
Contact Sam (@u0092172) if you are interested in contributing.

## Authors and acknowledgment
Originally authored by Sam Eyley (@u0092172)

## License
MIT License
