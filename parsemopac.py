#!/usr/bin/env python

import sys, os, json, glob
from distutils.dir_util import mkpath

from pqrJson import *
import pybel

# read through multiple files on command-line
for argument in glob.iglob('pm7/*/*.out'):
    fileName, fileExt = os.path.splitext(argument)
    ikey = fileName.split('/')[-1]

    print ikey
    item = getJSON(ikey)

    # hand-parse the MOPAC output
    with open(argument) as f:

        pointGroup = "C1"
        hf = 0.0
        volume = 0.0
        area = 0.0
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
            if 'COSMO AREA' in line:
                area = float(line.split()[3])
            if 'HOMO LUMO ENERGIES' in line:
                homo = float(line.split()[5])
                lumo = float(line.split()[6])
            if 'SUM' in line:
                dipole = line.split()[1:4]
                moment = float(line.split()[4])

        # finished parsing
        item['pointGroup'] = pointGroup
        pm7 = {
                'heatOfFormation': hf,
                'volume': volume,
                'surfaceArea': area,
                'homo': homo,
                'lumo': lumo,
                'dipole': dipole,
                'dipoleMoment': moment
        }
        item['pm7']  = pm7

        # save JSON
        saveJSON(ikey, item)

    # now read as a Pybel file and update the mol2 geometry
    try:
        mol = pybel.readfile("mopout", argument).next()
        mol2name = 'mol2/%s/%s.mol2' % (ikey[0:2], ikey)
        if os.path.isfile(mol2name):
            mol2 = pybel.readfile("mol2", mol2name).next()
            numAtoms = mol2.OBMol.NumAtoms()
            for i in range(numAtoms):
                oldAtom = mol2.atoms[i]
                nuAtom = mol.atoms[i]
                oldAtom.OBAtom.SetVector(nuAtom.vector)
                oldAtom.OBAtom.SetPartialCharge(nuAtom.partialcharge)
        else:
            mol2 = mol
            mkpath("mol2/%s" % ikey[0:2])

        mol2.title = str(item['name'])
        mol2.OBMol.SetEnergy(float(item['pm7']['heatOfFormation']))
        mol2.write('mol2', mol2name, overwrite=True)
    except Exception:
        print "Error: ", argument
