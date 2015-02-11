#!/usr/bin/env python

# Generate a helicene SMILES
# n=4  C1(C(C(C=CC=C2)=C2C=C3)=C3C=C4)=C4C=CC=C1
# n=5  C1(C(C(C(C=CC=C2)=C2C=C3)=C3C=C4)=C4C=C5)=C5C=CC=C1
# n=6  C1(C(C(C(C(C=CC=C2)=C2C=C3)=C3C=C4)=C4C=C5)=C5C=C6)=C6C=CC=C1

def helicene(number):
    smiles = "c1" + "(c"*(number-1)
    smiles = smiles + "ccc2)"
    for link in range(2,number):
        smiles = smiles + "c%dcc%d)" % (link, link+1)
    smiles = smiles + "c%dcccc1" % (number)
    return smiles

# size 3 = phenanthrene
for size in range(4,12):
    print helicene(size)
