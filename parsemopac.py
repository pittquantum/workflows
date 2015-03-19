#!/usr/bin/env python

import sys, os, json, glob

from pqrJson import *

# read through multiple files on command-line
for argument in glob.iglob('pm7/*/*/*.out'):
    fileName, fileExt = os.path.splitext(argument)
    ikey = fileName.split('/')[-1]

    print ikey
    item = getJSON(ikey)

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
        item['heatOfForm'] = hf
        item['volume'] = volume
        item['surfaceArea'] = area
        item['homo'] = homo
        item['lumo'] = lumo
        item['dipole'] = dipole
        item['dipoleMoment'] = moment

        # save JSON
        saveJSON(ikey, item)
