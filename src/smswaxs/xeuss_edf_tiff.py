"""This script converts Xeuss edf files to TIFF format + JSON for archival storage"""
import sys
from pathlib import Path
import json
import fabio
from PIL import Image

file_path = Path(sys.argv[1])

infile = fabio.open(file_path)

output_path = file_path.with_suffix(".tif")
json_output = file_path.with_suffix(".json")

"""The original edf files contain 32-bit floats, so the F mode is used to
retain precision, however, mask files are only 8-bit and will throw an error,
in this case we fall back to auto detection"""
try:
    image = Image.fromarray(infile.data,mode='F')
except ValueError:
    image = Image.fromarray(infile.data)

image.save(output_path,format='TIFF',compression='tiff_deflate')

with open(json_output, 'w',encoding="utf-8") as json_f:
    json.dump(infile.header, json_f, indent=4)
