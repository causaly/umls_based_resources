#!/usr/bin/python
# -*- coding: utf-8 -*-

import pickle
import csv
import copy

from config import umls_mrsat, atc_01_output

'''
    BLOCK 1 - Get all concept and their level in ATC ONTOLOGY
    Comment/Uncomment the blocks for specific function
'''

counter = 0
filename = umls_mrsat

atc_level_map = {}

file = open(filename, 'r').read().split('\n')
print len(file)
for line in file:

    counter += 1

    if not counter % 1000000:
        print counter

    rel_list = line.split('|')

    if len(rel_list) != 14:
        print 'ROW LEGNTH ERROR: ', rel_list
        continue

    if rel_list[0] in ['C0244672', 'C2369192']:
        print rel_list

    if rel_list[9] == 'ATC' and rel_list[8] == 'ATC_LEVEL':
        if rel_list[0] not in atc_level_map:
            atc_level_map[rel_list[0]] = rel_list[10]

with open(atc_01_output, 'wb') as handle:
    pickle.dump(atc_level_map, handle, protocol=pickle.HIGHEST_PROTOCOL)

print 'DONE ', len(atc_level_map)
print atc_level_map['C3542961']
