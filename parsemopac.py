#!/usr/bin/env python

from distutils.dir_util import mkpath
import sys, os
import json
from types import *

# NIH resolver interface
import cirpy
# PubChem interface
import pubchempy as pcp


# json array
items = {}
try:
    with open('properties.json') as index:
        items = json.load(index)
except ValueError:
    print "No JSON yet"

# read through multiple files on command-line
for argument in sys.argv[1:]:
    fileName, fileExt = os.path.splitext(argument)
    ikey = fileName.split('/')[-1]

    print ikey

    # try to get the PubChem cid
    results = pcp.get_compounds(ikey, 'inchikey')
    results.sort()
    compound = results[0]

    name = compound.iupac_name
    if type(name) is ListType:
        name = name[0]

    mol = cirpy.Molecule(ikey)

    with open(argument) as f:

        pointGroup = "C1"
        hf = 0.0
        volume = 0.0
        homo = 0.0
        lumo = 0.0
        dipole = []
        moment = 0.0

        for line in f:

            if 'MOLECULAR POINT GROUP' in line:
                pointGroup = line.split()[4]
            if 'FINAL HEAT OF FORMATION' in line:
                hf = float(line.split()[8]) #kJ/mol
            if 'COSMO VOLUME' in line:
                volume = float(line.split()[3])
            if 'HOMO LUMO ENERGIES' in line:
                homo = float(line.split()[5])
                lumo = float(line.split()[6])
            if 'SUM' in line:
                dipole = line.split()[1:4]
                moment = float(line.split()[4])


            # get properties
            # add to json
            items[ikey] = {
                'inchikey': ikey,
                'name': name.lower(),
                'cid': compound.cid,
                'cas': mol.cas,
                'formula': mol.formula,
                'molwt': mol.mw,
                'pointGroup': pointGroup,
                'heatOfForm': hf,
                'volume': volume,
                'homo': homo,
                'lumo': lumo,
                'dipole': dipole,
                'moment': moment
            }

with open('properties.json', 'w') as index:
    json.dump(items, index, indent=4)
