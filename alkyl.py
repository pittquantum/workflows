#!/usr/bin/env python

# Generate a bunch of alkyl SMILES

def straightchain(max):
    list = []
    for carbon in range(1, max):
        smiles = "C" * carbon
        list.append(smiles)
    return list

def cyclic(max):
    list = []
    # start at atom 2, since first atom is always the ring initiator
    for carbon in range(2, max):
        smiles = "C1" + "C"*carbon + "1"
        list.append(smiles)
    return list

def addbranches(list):
    branched = []
    for alkyl in list:
        for i in range(1, len(alkyl)):
            if alkyl[i] == 'C':
                branched.append(str(alkyl[0:i-1]) + '[C@C]' + str(alkyl[i+1:]))
                branched.append(str(alkyl[0:i-1]) + '[C@@C]' + str(alkyl[i+1:]))
                branched.append(str(alkyl[0:i]) + '(C)(C)' + str(alkyl[i+1:]))
    return branched

commonbranches = ['C(C)(C)', #isopropyl
                  'C(C)(C)C', #isobutyl
                  'C(C)(CC)', #sec-butyl
                  'CC(C)(C)', #t-butyl
                  'C(C)(C)CC', #isopentyl
                  'C(C)(CCC)', #sec-pentyl
                  ]

# TODO: add parameters
def alkyls():
    # straight chain alklyls
    list = straightchain(12)

    # cyclic
    for item in cyclic(10):
        list.append(item)

    # branching alkyls
    for branching in range(3):
        print "branching level: " + str(branching) + " size: " + str(len(list))
        for item in addbranches(list):
            # remove strings larger than N carbons
            if item.count('C') <= 8:
                list.append(item)

    # add common branches
    for item in commonbranches:
        list.append(item)
    return list
