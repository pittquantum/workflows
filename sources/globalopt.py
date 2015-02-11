#!/usr/bin/env python

import sys
import os
from distutils.dir_util import mkpath

import pybel
import openbabel as ob

def globalopt(mol, debug=False, fast=False):
        pybel._builder.Build(mol.OBMol)
        mol.addh()

        # if fast, skip the forcefield cleanup
        if not fast:
                ff = pybel._forcefields["mmff94"]
                success = ff.Setup(mol.OBMol)
                if not success:
                        ff = pybel._forcefields["uff"]
                        success = ff.Setup(mol.OBMol)
                if not success:
                        sys.exit("Cannot set up forcefield")

                ff.ConjugateGradients(250, 1.0e-3)
                ff.WeightedRotorSearch(250, 10)
                ff.WeightedRotorSearch(250, 10)
                ff.ConjugateGradients(100, 1.0e-5)
                ff.GetCoordinates(mol.OBMol)

if __name__ == "__main__":
    # iterate through all the files, all the molecules in the files and optimize
        for argument in sys.argv[1:]:
            with open(argument) as f:
                for line in f:
                    ikey, smi = line.split()

                    try:
                        mol = pybel.readstring("smi", smi)
                    except IOError:
                        continue

                    globalopt(mol)

                    filename = "library/%s/%s/%s" % (ikey[0], ikey[1], ikey)
                    mkpath('library/%s/%s' % (ikey[0], ikey[1]))
                    if not os.path.isfile(filename):
                        out = pybel.Outputfile("sdf", "%s.sdf" % filename, True)
                        out.write(mol)
                        out.close()
