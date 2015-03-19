# Base Python libraries
import sys, os, json
from types import *
from distutils.dir_util import mkpath

# NIH resolver interface
import cirpy
# PubChem interface
import pubchempy as pcp

# ChemSpider
CST = os.environ['CHEMSPIDER_SECURITY_TOKEN']
from chemspipy import ChemSpider
cs = ChemSpider(security_token=CST)

def getJSON(inchikey):
    items = {}
    filename = 'json/%s/%s.json' % (inchikey[0:2], inchikey)
    try:
        with open(filename) as file:
            items = json.load(file)
    except IOError, ValueError:
        items["inchikey"] = inchikey

    # check if we need to get various keys

    # PubChem CID
    if not "pubchem_cid" in items:
        results = pcp.get_compounds(inchikey, 'inchikey')
        results.sort()
        pcpCmpd = results[0]
        cid = pcpCmpd.cid
        items["pubchem_cid"] = cid
    else:
        cid = items["pubchem_cid"]
        pcpCmpd = pcp.Compound.from_cid(cid)
    # ChemSpider
    if not "chemspider_id" in items:
        results = cs.simple_search(inchikey)
        results.sort()
        csCmpd = results[0]
        csid = csCmpd.csid
        items["chemspider_id"] = csid
        items["name"] = csCmpd.common_name.lower()
    else:
        csid = items["chemspider_id"]
        csCmpd = cs.get_compound(csid)

    # NIH resolver
    nihCmpd = cirpy.Molecule(inchikey, ['stdinchikey'])
    if not "iupac_name" in items:
        name = nihCmpd.iupac_name # try NIH resolver
        if name is None: # try PubChem
            name = pcpCmpd.iupac_name
        if type(name) is ListType:
            name = name[0]
        if name is None:
            name = items["name"] # chemspider common name
        items["iupac_name"] = name.lower()

    if not "molwt" in items:
        items["molwt"] = pcpCmpd.molecular_weight
    if not "cas" in items:
        items["cas"] = nihCmpd.cas
    if not "formula" in items:
        items["formula"] = pcpCmpd.molecular_formula

    if not "synonyms" in items:
        synonyms = []
        for name in nihCmpd.names:
            synonyms.append(name.lower())

        # give me a sorted list with no duplicates
        synonyms = sorted(list(set(synonyms)))
        items["synonyms"] = synonyms

    return items


def saveJSON(inchikey, items):
    filename = 'json/%s/%s.json' % (inchikey[0:2], inchikey)
    mkpath('json/%s' % (inchikey[0:2]))
    with open(filename, 'w') as file:
        json.dump(items, file, indent=2)
