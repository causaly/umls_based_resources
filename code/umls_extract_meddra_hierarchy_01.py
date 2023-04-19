#!/usr/bin/python
# -*- coding: utf-8 -*-

import pickle
import csv
import copy
import sys

from config import umls_mrconso, MEDDRA_cui_to_atom, MEDDRA_atom_to_cui

reload(sys)
sys.setdefaultencoding('utf-8')

'''
    Block 1 - Extract meddra concepts with their metadata
    Output pickle file dictionaries
'''

map = {
    'OS': 5,
    'HG': 4,
    'HT': 3,
    'PT': 2,
    'LLT': 1
}

filename = umls_mrconso

file = open(filename, 'r').read().split('\n')
print len(file)

cui_to_atom_meddra = {}

# CREATE LIST OF VALID CUIS (WHICH ARE PAs) FOR FURTHER EXTRACTION FROM MRREL
for line in file:

    rel_list = line.split('|')

    if len(rel_list) != 19:
        print 'LENGTH WRONG: ', rel_list
        continue

    if rel_list[1] != 'ENG':
        continue

    if rel_list[11] != 'MDR':
        continue

    if rel_list[12] in map:
        atom_type = rel_list[12]
        priority = map[atom_type]

        cui = rel_list[0]
        atom = rel_list[7]
        concept_name = rel_list[14]

        if cui in cui_to_atom_meddra:

            if map[atom_type] > cui_to_atom_meddra[cui][2]:
                cui_to_atom_meddra[cui] = [atom, atom_type, priority, concept_name]

        else:

            cui_to_atom_meddra[cui] = [atom, atom_type, priority, concept_name]


cui_to_atom_meddra['C1140263'] = ['A1605890', 'MTH_OS', 6, 'MedDRA']

print cui_to_atom_meddra['C0014130']
print cui_to_atom_meddra['C1140263']

atom_to_cui_meddra = {}

for item in cui_to_atom_meddra:
    triplet = cui_to_atom_meddra[item]

    if triplet[0] not in atom_to_cui_meddra:
        atom_to_cui_meddra[triplet[0]] = [item, triplet[3]]


print atom_to_cui_meddra['A1595701']
print
print len(cui_to_atom_meddra)
print len(atom_to_cui_meddra)

with open(MEDDRA_cui_to_atom, 'wb') as handle:
    pickle.dump(cui_to_atom_meddra, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open(MEDDRA_atom_to_cui, 'wb') as handle:
    pickle.dump(atom_to_cui_meddra, handle, protocol=pickle.HIGHEST_PROTOCOL)
