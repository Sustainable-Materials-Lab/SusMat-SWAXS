# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 11:38:05 2023

@author: u0092172
"""

import sys
def cli():
    if len(sys.argv) != 2:
        print("Usage: python topas_init.py <input_file>")
        sys.exit(1)
    with open(sys.argv[1],'r',encoding="utf-8") as inputfile:
        data = inputfile.readlines()

    for i, line in enumerate(data):
        if 'xdd' in line:
            data[i] = 'xdd '+sys.argv[1][:-3]+'xye\n'

    with open(sys.argv[1], 'w',encoding="utf-8") as outfile:
        outfile.writelines(data)

if __name__ == "__main__":
    cli()