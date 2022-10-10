# SWAXS 1D data conversion

## Description
This is a script to convert 1D data from data reduction of SWAXS images given as q,I (.dat) to xy(e) format suitable for use in TOPAS academic (2theta,I).

## Installation
Requires python3, numpy and argparse. Works "out of the box" with anaconda python 3 distribution.
## Usage

`python dat_conv.py <filename_without_extension>`

To automate for an entire folder in windows, you could use PowerShell:

`Get-ChildItem -Filter *.dat | ForEach-Object -Process {python.exe dat_conv.py $_.BaseName}`

## Support
Contact Sam (@u0092172)

## Contributing
Contact Sam (@u0092172) if you are interested in contributing.

## Authors and acknowledgment
Originally authored by Sam Eyley (@u0092172)

## License
CC-BY-SA 4.0