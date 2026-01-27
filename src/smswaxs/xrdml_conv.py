# -*- coding: utf-8 -*-
"""
Convert xrdml files to xy format for use in TOPAS. Extract metadata, but drop units from pint quantities.
@author: u0092172
"""
from pathlib import Path
import json
import argparse as ap
import numpy as np
from fairmat_readers_xrd import read_file


def _to_magnitude(obj):
    """Recursively convert pint quantities to their magnitudes."""
    if hasattr(obj, 'magnitude'):
        return obj.magnitude
    if isinstance(obj, dict):
        return {k: _to_magnitude(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        converted = [_to_magnitude(v) for v in obj]
        return tuple(converted) if isinstance(obj, tuple) else converted
    return obj

def cli():
    """Convert xrdml files to xy format for use in TOPAS"""
    parser = ap.ArgumentParser(description='Sort out xrdml files')
    parser.add_argument("input", help="xrdml file")
    args = parser.parse_args()  # map arguments to args



    data = read_file(args.input)
    two_theta = data['2Theta'].magnitude
    intensity = data['intensity'].magnitude

    metadata = _to_magnitude(data['metadata'])

    outfile = Path(args.input).with_suffix('.xy')

    np.savetxt(outfile, np.column_stack((two_theta, intensity)), fmt='%1.6f', delimiter='\t')

    meta_outfile = Path(args.input).with_suffix('.json')
    with open(meta_outfile, 'w') as f:
        json.dump(metadata, f, indent=4)


if __name__ == '__main__':
    cli()
