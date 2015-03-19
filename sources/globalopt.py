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
                ff.WeightedRotorSearch(250, 5)
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

                    mol = cirpy.Molecule(ikey, ['inchikey'])

                    filename = "library/%s/%s/%s.mol2" % (ikey[0], ikey[1], ikey)
                    if not os.path.isfile(filename):
                        if mol.twirl_url is not None:
                            mol.download(filename, 'mol2', True)
                        else:
                            globalopt(mol)
                            mkpath('library/%s/%s' % (ikey[0], ikey[1]))
                            mol.write("mol2", filename)
