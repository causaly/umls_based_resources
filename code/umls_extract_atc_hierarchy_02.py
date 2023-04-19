#!/usr/bin/python
# -*- coding: utf-8 -*-

import pickle
import csv
import copy

from config import concepts_preferred, concepts_categories_map,atc_02_output, umls_mrrel

'''
    BLOCK 2 - Get all ATC relationships from MRREL.RRF - generates the csv, which then should be loaded into Neo4j
'''

with open(concepts_preferred, 'rb') as handle:
    mrconso_concepts = pickle.load(handle)

with open(concepts_categories_map, 'rb') as handle:
    conc_cat_map = pickle.load(handle)

print '# of Concepts in the map: ', len(mrconso_concepts)

output_pmid = atc_02_output
outcsv_pmid = open(output_pmid, "wb")
writer_pmid = csv.writer(outcsv_pmid, delimiter='\t', quoting = csv.QUOTE_NONE, quotechar='')

row = ['child_concept_cui', 'child_concept_name', 'child_category', 'parent_concept_cui', 'parent_concept_name', 'parent_category', 'src', 'rel']
writer_pmid.writerow([unicode(s).encode("utf-8") for s in row])

filename = umls_mrrel

relevant_sources = ['ATC']

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
    if rel_list[10] not in relevant_sources:
        continue

    child_concept = '0'
    rel_type = rel_list[3]

    # REL TYPE
    if rel_list[3].lower() == 'chd':

        child_concept = rel_list[4]
        if child_concept in mrconso_concepts:
            child_concept_name = mrconso_concepts[child_concept][1]
        else:
            #child_concept_name = '0'
            print 'Need input for CONCEPT NAME: ', child_concept
            user_cname = input("CONCEPT NAME: ")
            user_cname = str(user_cname)
            mrconso_concepts[child_concept] = [0, user_cname]
            child_concept_name = user_cname

        parent_concept = rel_list[0]
        if parent_concept in mrconso_concepts:
            parent_concept_name = mrconso_concepts[parent_concept][1]
        else:
            #parent_concept_name = '0'
            print 'Need input for CONCEPT NAME: ', parent_concept
            user_cname = input("CONCEPT NAME: ")
            user_cname = str(user_cname)
            mrconso_concepts[parent_concept] = [0, user_cname]
            parent_concept_name = user_cname

    if child_concept != '0':

        # REMOVE SELF REFs
        if child_concept == parent_concept:
           continue

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

        row = [child_concept, child_concept_name.replace('&#x7C;', '|').replace('&#124;', '|'), child_category, parent_concept, parent_concept_name.replace('&#x7C;', '|').replace('&#124;', '|'), parent_category, rel_list[10], rel_type]

        for ind, item in enumerate(row):
            if '"' in row[ind]:
                row[ind] = row[ind].replace('"', '\'')
                print counter

        try:
            writer_pmid.writerow([unicode(s).encode("utf-8") for s in row])
        except Exception, e:
            print row