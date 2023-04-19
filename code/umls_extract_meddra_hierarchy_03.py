#!/usr/bin/python
# -*- coding: utf-8 -*-

import pickle
import csv
import copy
import sys

from config import meddra_01_output, meddra_02_output, MEDDRA_cui_to_atom, concepts_preferred, concepts_categories_map

reload(sys)

sys.setdefaultencoding('utf-8')

'''
    Block 3 - Go through the previously created file, and extract all child-parent relationships maps
    The maps will then be used to map all non-SOC concepts to their SOC parents
'''

output_csv = meddra_02_output
outcsv_csv = open(output_csv, "wb")
writer_csv = csv.writer(outcsv_csv, delimiter='\t', quoting = csv.QUOTE_NONE, quotechar='')


input_filename = meddra_01_output

parents = {}
smq_lvl = {}

with open(input_filename, 'r') as my_file:
    reader = csv.reader(my_file, delimiter='\t', quoting = csv.QUOTE_NONE, quotechar='')

    for idx, row in enumerate(reader):

        if idx == 0:
            row = ['child_concept_cui', 'child_concept_name', 'child_category', 'child_meddra_type', 'child_smq_level',
                   'parent_concept_cui', 'parent_concept_name', 'parent_category', 'parent_meddra_type', 'parent_smq_level']
            writer_csv.writerow(row)
            continue

        child_concept_smqlvl = int(row[4])
        parent_concept_smqlvl = int(row[11])

        if parent_concept_smqlvl <= child_concept_smqlvl:
            continue

        child_concept = row[0]
        parent_concept = row[5]

        if child_concept not in parents:
            parents[child_concept] = [parent_concept]
        else:
            parents[child_concept].append(parent_concept)

        if child_concept not in smq_lvl:
            smq_lvl[child_concept] = str(child_concept_smqlvl)
        if parent_concept not in smq_lvl:
            smq_lvl[parent_concept] = str(parent_concept_smqlvl)

print 'All rows read, now iterating the dictionary until no change detected'

still_changing = 1
while still_changing:
    still_changing = 0
    for concept in parents:
        # if no lists grow - time to end the while loop
        original_parent_list_len = len(parents[concept])

        new_parents = copy.deepcopy(parents[concept])
        for concept_parents in parents[concept]:
            if concept_parents in parents:

                for parent_parent_concept in parents[concept_parents]:
                    if parent_parent_concept not in new_parents:
                        new_parents.append(parent_parent_concept)

        parents[concept] = copy.deepcopy(new_parents)
        new_parent_list_len = len(parents[concept])
        if original_parent_list_len != new_parent_list_len:
            still_changing = 1


    print 'Still changing..'

print 'Done retrieveing, loading ATC Level Map, Preferred Concept and Category maps now and proceeding with CSV generation..'


with open(concepts_preferred, 'rb') as handle:
    mrconso_concepts = pickle.load(handle)

with open(concepts_categories_map, 'rb') as handle:
    conc_cat_map = pickle.load(handle)

with open(MEDDRA_cui_to_atom, 'rb') as handle:
    cui_to_atom_meddra = pickle.load(handle)

reverse_map = {
    '5': 'OS',
    '4': 'HG',
    '3': 'HT',
    '2': 'PT',
    '1': 'LLT'
}

for concept in parents:

    child_concept = concept
    if smq_lvl[child_concept] != '5' and smq_lvl[child_concept] != '6':
        for parent_concept in parents[child_concept]:

            if smq_lvl[parent_concept] == '5':

                # WRITE DOWN THE FINAL CSV
                # GET CONCEPT CATEGORIES
                if child_concept in conc_cat_map:
                    child_category = '%'.join(conc_cat_map[child_concept])
                else:
                    print 'Need input for CONCEPT CATEGORY: ', child_concept
                    user_cat = input("Cat: ")
                    user_cat = str(user_cat)
                    child_category = user_cat
                    conc_cat_map[child_category] = user_cat.split('%')

                if parent_concept in conc_cat_map:
                    parent_category = '%'.join(conc_cat_map[parent_concept])
                else:
                    print 'Need input for CONCEPT CATEGORY: ', parent_concept
                    user_cat = input("Cat: ")
                    user_cat = str(user_cat)
                    parent_category = user_cat
                    conc_cat_map[parent_concept] = user_cat.split('%')

                if child_concept in mrconso_concepts:
                    child_concept_name = mrconso_concepts[child_concept][1]
                else:
                    #child_concept_name = '0'
                    print 'Need input for CONCEPT NAME: ', child_concept
                    user_cname = input("CONCEPT NAME: ")
                    user_cname = str(user_cname)
                    mrconso_concepts[child_concept] = [0, user_cname]
                    child_concept_name = user_cname

                if parent_concept in cui_to_atom_meddra:
                    parent_concept_name = cui_to_atom_meddra[parent_concept][3]
                else:
                    #child_concept_name = '0'
                    print 'Need input for CONCEPT NAME: ', parent_concept
                    user_cname = input("CONCEPT NAME: ")
                    user_cname = str(user_cname)
                    parent_concept_name = user_cname


                child_meddra_type = reverse_map[smq_lvl[child_concept]]
                parent_meddra_type = reverse_map[smq_lvl[parent_concept]]

                row = [child_concept, child_concept_name, child_category, child_meddra_type, smq_lvl[child_concept],
                       parent_concept, parent_concept_name, parent_category, parent_meddra_type, smq_lvl[parent_concept]]
                writer_csv.writerow(row)

print 'Mission complete.'