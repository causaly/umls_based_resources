#!/usr/bin/python
# -*- coding: utf-8 -*-

import pickle

# GENERATE CONCEPTS PREFERRED PICKLE FILE
# GET RANKS ##############
filename = '/data-processing/2022_umls_download/2022AA/META/MRRANK.RRF'

file = open(filename, 'r').read().split('\n')
print len(file)

mrranks = {}

for line in file:

    rel_list = line.split('|')

    if len(rel_list) != 5:
        print 'LENGTH ISSUE', rel_list
        continue

    pair = rel_list[1]+'-'+rel_list[2]
    if pair not in mrranks:
        mrranks[pair] = int(rel_list[0])

    else:
        print 'SMTHS WRONG', rel_list

print 'MRRANKS: ', len(mrranks)

# PROCESS DATA ############

filename = '/data-processing/2022_umls_download/2022AA/META/MRCONSO.RRF'

file = open(filename, 'r').read().split('\n')
print len(file)

mrconso_concepts = {}
counter = 0

for line in file:
    counter += 1

    rel_list = line.split('|')

    if len(rel_list) != 19:
        print 'LENGTH ISSUE', rel_list
        continue

    if rel_list[1] != 'ENG' or rel_list[6] != 'Y':
        continue

    cui = rel_list[0]
    name = rel_list[14]

    pair = rel_list[11]+'-'+rel_list[12]
    pair_rank = 0
    if pair in mrranks:
        pair_rank = mrranks[pair]
    else:
        print 'ERROR: ', rel_list

    if cui not in mrconso_concepts:
        mrconso_concepts[cui] = [pair_rank, name]
    else:
        if int(pair_rank) > int(mrconso_concepts[cui][0]):
            mrconso_concepts[cui] = [pair_rank, name]

    if not counter % 250000:
        print counter

print len(mrconso_concepts)
with open('concepts_preferred_2022AA.pickle', 'wb') as handle:
    pickle.dump(mrconso_concepts, handle, protocol=pickle.HIGHEST_PROTOCOL)
