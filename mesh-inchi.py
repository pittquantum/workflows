#!/usr/bin/python

import sys
import os
import json
from distutils.dir_util import mkpath

import openbabel as ob
import pybel

# NIH resolver interface
import cirpy
# PubChem interface
import pubchempy as pcp

cidNames = {}
cidKeys = {}
for line in open ('CID-MeSH'):
    tokens = line.split('\t')
    if len(tokens) < 2:
        continue

    cid = int(tokens[0])
    name = " ".join(tokens[1:]).strip().lower()
    cidNames[cid] = name

    mol = pcp.Compound.from_cid(cid)
    ikey = mol.inchikey
    cidKeys[cid] = ikey

    fileName = 'pm7/%s/%s/%s.mop' % (ikey[0], ikey[1], ikey)
    if not os.path.isfile(fileName):
        print cid, ikey, name
