#!/usr/bin/env python

from distutils.dir_util import mkpath
import sys
import json
from types import *

# NIH resolver interface
import cirpy
# PubChem interface
import pubchempy as pcp

# json array
items = {}
try:
    with open('index.json') as index:
        items = json.load(index)
except ValueError:
    print "No JSON yet"

# read through multiple files on command-line
for argument in sys.argv[1:]:
    with open(argument) as f:
        for line in f:
            line = line.rstrip()
            # skip blank lines and comments
            if not line or line[0] == '#':
                continue

            line_list = line.split()
            ikey = line_list[0]
            if "cid=" in line:
                # ok, there's already a PubChem CID
                cidstr = line_list[-1]
                cid = cidstr[4:]
            else:
                # try to get the PubChem cid
                results = pcp.get_compounds(ikey, 'inchikey')
                results.sort()
                compound = results[0]
                cid = compound.cid

            line_list = line.split('"') # get the name
            name = "none"
            if len(line_list) > 2):
                name = line_list[1]

            # add to json
            items[ikey] = {
                'inchikey': ikey,
                'name': name.lower(),
                'cid': compound.cid,
                'cas': mol.cas,
                'formula': mol.formula,
                'molwt': mol.mw
            }


with open('index.json', 'w') as index:
    json.dump(items, index, indent=4)
