# SWAXS 1D tools

## Description
This is a collection of  scripts to perform data manipulation on 1D data.

dat_conv - Converts Xenocs format 1D data (.dat) to TOPAS compatible .xye
sph_harm - Plot the spherical harmonics function using coefficients from TOPAS input file

## Installation
Requires python3, numpy and argparse. Works "out of the box" with anaconda python 3 distribution.
## Usage

### dat_conv
`python dat_conv.py <filename_without_extension>`

To automate for an entire folder in windows, you could use PowerShell:

`Get-ChildItem -Filter *.dat | ForEach-Object -Process {python.exe dat_conv.py $_.BaseName}`

### sph_harm
`python sph_harm.py <c00> <c20>...`

e.g.
```
python sph_harm.py 1 -.54889 0.48504 0.74711 0.79916 -0.33178 0.16323 0.45369 -.29782 -.29214 -.43949\
 .01524 .09042 .85340 .40316 -.01881 1.47673 -.55751 -.68970 .02621 -.06565 -.56472 1.00981 -.12339 -.25831
```

## Support
Contact Sam (@u0092172)

## Contributing
Contact Sam (@u0092172) if you are interested in contributing.

## Authors and acknowledgment
Originally authored by Sam Eyley (@u0092172)

## License
CC-BY-SA 4.0