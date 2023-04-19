#!/usr/bin/python
# -*- coding: utf-8 -*-

import pickle
import csv
import copy
import sys

from config import umls_mrrel, MEDDRA_cui_to_atom, meddra_01_output, concepts_preferred, concepts_categories_map

reload(sys)
sys.setdefaultencoding('utf-8')
'''
    Block 2 - Create the csv with MDR parents
    Output - csv for loading into Neo4j
'''

with open(MEDDRA_cui_to_atom, 'rb') as handle:
    cui_to_atom_meddra = pickle.load(handle)

with open(concepts_preferred, 'rb') as handle:
    mrconso_concepts = pickle.load(handle)

with open(concepts_categories_map, 'rb') as handle:
    conc_cat_map = pickle.load(handle)


print '# of Concepts in the map MRCONSO_MAP: ', len(mrconso_concepts)

output = meddra_01_output
outcsv = open(output, "wb")
writer = csv.writer(outcsv, delimiter='\t', quoting = csv.QUOTE_NONE, quotechar='')

row = ['child_concept_cui', 'child_concept_name', 'child_category', 'child_meddra_type', 'child_smq_level', 'parent_concept_cui', 'parent_concept_name', 'parent_category', 'parent_meddra_type', 'src', 'rel', 'parent_smq_level']
writer.writerow([unicode(s).encode("utf-8") for s in row])

filename = umls_mrrel

relevant_sources = ['MDR']

counter = 0

seen_rels = {}

file = open(filename, 'r').read().split('\n')
print len(file)
for line in file:

    counter += 1

    if not counter % 1000000:
        print counter

    rel_list = line.split('|')

    if len(rel_list) != 17:
        print 'WRONG LEN: ', len(rel_list)
        print rel_list
        continue

    # IF SOURCE IS NOT IN WHITELIST - SKIP
    if rel_list[10] not in relevant_sources and rel_list[11] not in relevant_sources:
        continue

    child_concept = '0'
    rel_type = rel_list[3]

    # REL TYPE
    if (rel_list[3].lower() == 'par' and rel_list[0] in cui_to_atom_meddra and rel_list[4] in cui_to_atom_meddra) \
            or (rel_list[3].lower() == 'rq' and rel_list[7].lower() == 'classifies' \
            and rel_list[0] in cui_to_atom_meddra and rel_list[4] in cui_to_atom_meddra):

        child_concept = rel_list[0]
        if child_concept in mrconso_concepts:
            #child_concept_name = atom_to_cui_meddra[rel_list[1]][1]
            child_concept_name = mrconso_concepts[child_concept][1]
        else:
            #child_concept_name = '0'
            print 'Need input for CONCEPT NAME: ', child_concept
            user_cname = input("CONCEPT NAME: ")
            user_cname = str(user_cname)
            mrconso_concepts[child_concept] = [0, user_cname]
            child_concept_name = user_cname

        parent_concept = rel_list[4]
        if parent_concept in mrconso_concepts:
            #parent_concept_name = atom_to_cui_meddra[rel_list[5]][1]
            parent_concept_name = mrconso_concepts[parent_concept][1]
        else:
            #parent_concept_name = '0'
            print 'Need input for CONCEPT NAME: ', parent_concept
            user_cname = input("CONCEPT NAME: ")
            user_cname = str(user_cname)
            mrconso_concepts[parent_concept] = [0, user_cname]
            parent_concept_name = user_cname

    if child_concept != '0':

        # Deduplicate
        curr_rel = child_concept+'-'+parent_concept+'-'+rel_type
        if curr_rel in seen_rels:
            continue
        else:
            seen_rels[curr_rel] = 1

        if child_concept in conc_cat_map:
            child_category = '%'.join(conc_cat_map[child_concept])
        else:
            print 'Need input for CONCEPT CATEGORY: ', child_concept
            user_cat = input("Cat: ")
            user_cat = str(user_cat)
            child_category = user_cat
            conc_cat_map[child_concept] = user_cat.split('%')

        if parent_concept in conc_cat_map:
            parent_category = '%'.join(conc_cat_map[parent_concept])
        else:
            print 'Need input for CONCEPT CATEGORY: ', parent_concept
            user_cat = input("Cat: ")
            user_cat = str(user_cat)
            parent_category = user_cat
            conc_cat_map[parent_concept] = user_cat.split('%')

        child_smq_level = 'NaN'
        parent_smq_level = 'NaN'

        if child_concept in cui_to_atom_meddra:
            child_smq_level = str(cui_to_atom_meddra[child_concept][2])

        if parent_concept in cui_to_atom_meddra:
            parent_smq_level = str(cui_to_atom_meddra[parent_concept][2])

        child_meddra_type = cui_to_atom_meddra[child_concept][1]
        parent_meddra_type = cui_to_atom_meddra[parent_concept][1]

        row = [child_concept, child_concept_name, child_category, child_meddra_type, child_smq_level,  parent_concept, parent_concept_name, parent_category, parent_meddra_type, rel_list[10], rel_type, parent_smq_level]

        for ind, item in enumerate(row):
            if '"' in row[ind]:
                row[ind] = row[ind].replace('"', '\'')
                print counter


        writer.writerow([unicode(s).encode("utf-8") for s in row])
