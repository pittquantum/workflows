Workflows
=========

Backend workflow scripts for the Pitt Quantum Repository
(http://pqr.pitt.edu/)

First off, get yourself some molecules:
* cd pubchem/; sh get-mesh # wait while ~90,000 entries are downloaded
* cd sources/; sh get-sources # wait

These scripts will download a set of source molecules:
* The subset of PubChem compounds with MeSH terms
* The PDB ligand database
* The MMFF94 validation set
* The Blue Obelisk "chemical structure" set (~550 molecules in v2.2)

The scripts are mainly in Python (with some shell script).

pip install chemspipy
pip install pubchempy

