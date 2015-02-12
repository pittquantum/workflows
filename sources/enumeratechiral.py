#!/usr/bin/env python

import pybel
import openbabel as ob
import itertools

def enumerateChiral(mol):
        """ enumerate tetrahedral stereocenters
            in the molecule
        """
        if not mol.IsChiral():
            yield mol # we know the molecule is not chiral
        else:
            chiral = []
            chiralSet = []
            facade = ob.OBStereoFacade(mol)
            for a in ob.OBMolAtomIter(mol):
                idx = a.GetIdx()
                if a.IsChiral():
                    chiral.append(idx)
            if len(chiral) == 0:
                yield mol # no chiral centers
            else:
                atomList = chiral
                step = len(atomList)

                for winding in itertools.product([1,2], repeat=step):
                    for idx, aIdx in enumerate(atomList):
                        ts = facade.GetTetrahedralStereo(aIdx-1)
                        config = ts.GetConfig()
                        config.winding = winding[idx]
                        config.specified = True
                        ts.SetConfig(config)
                    yield mol
