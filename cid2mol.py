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

            list = line.split()
            cid = list[0]
            ikey = list[1]
            name = list[2:]

            mol = cirpy.Molecule(ikey, ['stdinchikey'])

            filename = "test-lib/%s/%s/%s.mol2" % (ikey[0], ikey[1], ikey)
            mkpath('test-lib/%s/%s' % (ikey[0], ikey[1]))

            mol.download(filename, 'mol2', True)

print items
with open('index.json', 'w') as index:
    json.dump(items, index, indent=4)
