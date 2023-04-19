#!/usr/bin/python
# -*- coding: utf-8 -*-

import pickle

# Categories map is a dictionary which translates cat code to full category description
# T041 - DISO|BLABLA|BLABLA|Disease or Syndrome
with open('categories_map.pickle', 'rb') as handle:
    cat_map = pickle.load(handle)

concept_cat_map = {}

filename = '/data-processing/2022_umls_download/2022AA/META/MRSTY.RRF'

file = open(filename, 'r').read().split('\n')
print len(file)

for line in file:

    rel_list = line.split('|')

    if len(rel_list) != 7:
        print 'LENGTH: ', rel_list
        continue

    cui = rel_list[0]
    cat_code = rel_list[1]

    if cui not in concept_cat_map:
        concept_cat_map[cui] = [cat_map[cat_code]]
    else:
        if cat_map[cat_code] not in concept_cat_map[cui]:
            concept_cat_map[cui].append(cat_map[cat_code])

count = 0
for item in concept_cat_map:
    if item == 'C1451207' or item == 'C0072054':
        print item
        print concept_cat_map[item]

with open('conc_cat_map_2022AA.pickle', 'wb') as handle:
    pickle.dump(concept_cat_map, handle, protocol=pickle.HIGHEST_PROTOCOL)
