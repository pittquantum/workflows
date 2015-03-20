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

def spiro(max):
    list = []
    # start at bridge spiro
    for l1 in range (2, max):
        for l2 in range (2, max):
            smiles = "C12(%s1)(%s2)" % ("C"*l1, "C"*l2)
            list.append(smiles)
    return list

def bicyclo(max):
    list = []
    # bridgeheads
    for l1 in range(0, max):
        for l2 in range(0, max):
            for l3 in range(0, max):
                if (l1 + l2 + l3) < 3:
                    continue
                smiles = "C(%s1)(%s2)%sC12" % ("C"*l1, "C"*l2, "C"*l3)
                list.append(smiles)
    return list

def addbranches(list):
    branched = []
    for alkyl in list:
        for i in range(1, len(alkyl)):
            if alkyl[i] == 'C':
                branched.append(str(alkyl[0:i-1]) + '(C)' + str(alkyl[i+1:]))
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
    list = straightchain(6)

    # cyclic
    for item in cyclic(6):
        list.append(item)

    # branching alkyls
    for branching in range(1):
        print "branching level: " + str(branching) + " size: " + str(len(list))
        for item in addbranches(list):
            # remove strings larger than N carbons
            if item.count('C') <= 6:
                list.append(item)

    # add common branches
    for item in commonbranches:
        list.append(item)
    return list
