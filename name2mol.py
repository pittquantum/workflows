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

            mol = cirpy.Molecule(line, ['name'])
            ikey = mol.stdinchikey
            if ikey is None:
                continue

            if ikey.startswith('InChIKey='):
                ikey = ikey[9:]

            # try to get the PubChem cid
            results = pcp.get_compounds(ikey, 'inchikey')
            results.sort()
            compound = results[0]

            name = mol.iupac_name
            if name is None:
                name = compound.iupac_name
            if type(name) is ListType:
                name = name[0]
            if name is None:
                name = line

            # get properties
            # add to json
            items[ikey] = {
                'inchikey': ikey,
                'name': name.lower(),
                'cid': compound.cid,
                'cas': mol.cas,
                'formula': mol.formula,
                'molwt': mol.mw
            }

            print line, ikey

            filename = "library/%s/%s/%s.mol2" % (ikey[0], ikey[1], ikey)
            mkpath('library/%s/%s' % (ikey[0], ikey[1]))

            mol.download(filename, 'mol2', True)

print items
with open('index.json', 'w') as index:
    json.dump(items, index, indent=4)
