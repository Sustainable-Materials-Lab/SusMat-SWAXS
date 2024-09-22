"""This script converts Xeuss edf files to TIFF format + JSON for archival storage"""
import sys
from pathlib import Path
import json
import numpy as np
import fabio


file_path = Path(sys.argv[1])

infile = fabio.open(file_path)

output_path = file_path.with_suffix(".csv")
json_output = file_path.with_suffix(".json")

np.savetxt(output_path,infile.data,delimiter=',')

with open(json_output, 'w',encoding="utf-8") as json_f:
    json.dump(infile.header, json_f, indent=4)