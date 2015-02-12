#!/usr/bin/env python

import sys
import os

import pybel
import openbabel as ob

import alkyl
from enumeratechiral import enumerateChiral

# get a list of fragments
chains = alkyl.alkyls()

# OK, remove chemical duplicates
inchis = []
unique = []

for smi in chains:
    smi = smi + "F" # use fluoride for now
    try:
        mol = pybel.readstring("smi", smi)
    except IOError:
        continue
    inchi = mol.write(format='inchikey').rstrip()
    if inchi not in inchis:
        inchis.append(inchi)
        unique.append(smi[:-1]) # strip the "F" off

print "unique smiles: ", len(unique)

smiles = []
for alkylA in unique:
    a = str(alkylA)
    # alcohols
    smiles.append(a + "O")
    # aldehydes
    smiles.append(a + "C(=O)")
    # acids
    smiles.append(a + "C(=O)O")
    # acid halides
    smiles.append(a + "C(=O)[Cl]")
    smiles.append(a + "C(=O)[Br]")
    # primary amines
    smiles.append(a + "N")
    # phospines
    smiles.append(a + "P")
    # primary amides
    smiles.append(a + "C(=O)N")
    # nitriles
    smiles.append(a + "C#N")
    # thiols
    smiles.append(a + "S")
    # terminal alkyne
    smiles.append(a + "C#C")
    # terminal alkene
    smiles.append(a + "C=C")
    # terminal fluoride
    smiles.append(a + "F")
    # terminal chloride
    smiles.append(a + "[Cl]")
    # terminal bromide
    smiles.append(a + "[Br]")
    # terminal iodide
    smiles.append(a + "I")
    # terminal nitro
    smiles.append(a + "N(=O)=O")
    # enamine
    smiles.append(a + "C(=C)N")
    # isocyanate
    smiles.append(a + "N=C=O")
    # isocyanate
    smiles.append(a + "N=C=S")
    # ketene
    smiles.append(a + "C=C=O")

    # two components
    for alkylB in unique:
        b = str(alkylB)
        # secondary amines
        smiles.append(a + "N" + b)
        # phosphines
        smiles.append(a + "P" + b)
        # secondary amides
        smiles.append(a + "C(=O)N" + b)
        # ethers
        smiles.append(a + "O" + b)
        # epoxides
        smiles.append(a + "C(O2)C2" + b)
        # esters
        smiles.append(a + "C(=O)O" + b)
        # anhydride
        smiles.append(a + "C(=O)OC(=O)C" + b)
        # ketones
        smiles.append(a + "C(=O)" + b)
        # thione
        smiles.append(a + "C(=S)" + b)
        # sulfoxide
        smiles.append(a + "S(=O)" + b)
        # thioether
        smiles.append(a + "S" + b)
        # thio-esters
        smiles.append(a + "C(=O)S" + b)
        # internal alkenes
        smiles.append(a + '\\C=C\\' + b)
        smiles.append(a + '/C=C\\' + b)
        # internal azo
        smiles.append(a + '\\N=N\\' + b)
        # internal alkynes
        smiles.append(a + "#" + b)
        # hydroxyl amine
        smiles.append(a + "N(O)" + b)

print "SMILES: ", len(smiles)

inchis = dict()
obConversion = ob.OBConversion()
obConversion.SetInAndOutFormats("smi", "smi")

# eliminate redundant (e.g., symmetric)
for smi in smiles:
    try:
        mol = pybel.readstring("smi", smi)
    except IOError:
        continue
    ikey = mol.write(format='inchikey').rstrip()
    if ikey not in inchis:
        # save the smiles string for now
        inchis[ikey] = smi
        # generate all stereoisomers
        mol.addh()
        for stereoMol in enumerateChiral(mol.OBMol):
            smi = obConversion.WriteString(stereoMol)
            smi = smi.rstrip()
            print smi
