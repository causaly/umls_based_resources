#!/usr/bin/python
# -*- coding: utf-8 -*-

import pickle
import csv
import copy

from config import atc_01_output, atc_02_output, atc_03_output, concepts_preferred, concepts_categories_map

'''
    BLOCK 3 - go through findings and create a csv where only level 5 parents are present
    Iteratively grow list of parents-of parents-of parents until reach the top
    Then write a csv, allowing only Level 5 concepts as parents
'''

output_csv = atc_03_output
outcsv_csv = open(output_csv, "wb")
writer_csv = csv.writer(outcsv_csv, delimiter='\t', quoting = csv.QUOTE_NONE, quotechar='')


input_filename = atc_02_output

parents = {}

with open(input_filename, 'r') as my_file:
    reader = csv.reader(my_file, delimiter='\t', quoting = csv.QUOTE_NONE, quotechar='')

    for idx, row in enumerate(reader):

        if idx == 0:
            writer_csv.writerow(row)
            continue

        child_concept = row[0]
        parent_concept = row[3]

        if child_concept not in parents:
            parents[child_concept] = [parent_concept]
        else:
            parents[child_concept].append(parent_concept)

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


with open(atc_01_output, 'rb') as handle:
    atc_level_map = pickle.load(handle)
    atc_level_map['C4722517'] = '0'   # LEVEL 0 WHOLE-ATC parent class

with open(concepts_preferred, 'rb') as handle:
    mrconso_concepts = pickle.load(handle)

with open(concepts_categories_map, 'rb') as handle:
    conc_cat_map = pickle.load(handle)

for concept in parents:

    child_concept = concept
    if atc_level_map[child_concept] != '1':
        for parent_concept in parents[child_concept]:

            if atc_level_map[parent_concept] == '1':

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

                if parent_concept in mrconso_concepts:
                    parent_concept_name = mrconso_concepts[parent_concept][1]
                else:
                    #child_concept_name = '0'
                    print 'Need input for CONCEPT NAME: ', parent_concept
                    user_cname = input("CONCEPT NAME: ")
                    user_cname = str(user_cname)
                    mrconso_concepts[parent_concept] = [0, user_cname]
                    parent_concept_name = user_cname

                row = [child_concept, child_concept_name.replace('&#x7C;', '|').replace('&#124;', '|'), child_category, parent_concept, parent_concept_name.replace('&#x7C;', '|').replace('&#124;', '|'), parent_category, 'ATC', 'CHD']
                writer_csv.writerow(row)

print 'Mission complete.'
