#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Code for generating a parent - child dictionaries for each concept found in Causaly KG.
Latest run is for PG5 KG.

Change log:
10.02.2020 - Added PAR CHD extraction of:
- HPO
- SNOMEDCT_VET
- AOD

For synonyms:
- MEDLINEPLUS (RQ/mapped_to)
- MEDCIN (SY/same_as)

'''

import pickle

# with open('/Users/asaudabayev/corpus/03_umls/atoms_entry_UMLS_2019AA.pickle', 'rb') as handle:
#     mrconso_concepts = pickle.load(handle)

with open('concepts_preferred_2022AA.pickle', 'rb') as handle:
    concepts_preferred = pickle.load(handle)

filename = '/data-processing/2022_umls_download/2022AA/META/MRREL.RRF'

relevant_sources = ['MSH', 'SNOMEDCT_US', 'RXNORM', 'NDFRT', 'MED-RT', 'NCI', 'GO', 'LNC', 'MDR', 'NCBI', 'FMA',
                    'ATC', 'MTH', 'UMD', 'CSP',
                    'HPO', 'SNOMEDCT_VET', 'AOD',
                    'MEDLINEPLUS', 'MEDCIN']

counter = 0

seen_rels = {}

parents = {}
children = {}

synonyms = {}
synonym_count_csp = 0
synonym_count_medcin = 0
synonym_count_mdr = 0
synonym_count_medlineplus = 0

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
    if rel_list[3].lower() == 'chd' or rel_list[3].lower() == 'rn':

        child_concept = rel_list[4]
        parent_concept = rel_list[0]

    elif rel_list[3].lower() == 'ro' and rel_list[7].lower() == 'is_related_to_endogenous_product':

        child_concept = rel_list[4]
        parent_concept = rel_list[0]

        rel_type = rel_list[3]+'is_related_to_endogenous_product'

    elif rel_list[10] == 'MDR' and rel_list[3].lower() == 'rq' and rel_list[7].lower() in ['classified_as', 'classifies']:

        synonym_count_mdr += 1

        if rel_list[0] not in synonyms:
            synonyms[rel_list[0]] = [rel_list[4]]
        else:
            synonyms[rel_list[0]].append(rel_list[4])

        if rel_list[4] not in synonyms:
            synonyms[rel_list[4]] = [rel_list[0]]
        else:
            synonyms[rel_list[4]].append(rel_list[0])

        continue

    elif rel_list[10] == 'CSP' and rel_list[3].lower() == 'rq' and rel_list[7].lower() in ['used', 'used_for']:

        synonym_count_csp += 1

        if rel_list[0] not in synonyms:
            synonyms[rel_list[0]] = [rel_list[4]]
        else:
            synonyms[rel_list[0]].append(rel_list[4])

        if rel_list[4] not in synonyms:
            synonyms[rel_list[4]] = [rel_list[0]]
        else:
            synonyms[rel_list[4]].append(rel_list[0])

        continue

    elif rel_list[10] == 'MEDCIN' and rel_list[3].lower() == 'sy' and rel_list[7].lower() in ['same_as']:

        synonym_count_medcin += 1

        if rel_list[0] not in synonyms:
            synonyms[rel_list[0]] = [rel_list[4]]
        else:
            synonyms[rel_list[0]].append(rel_list[4])

        if rel_list[4] not in synonyms:
            synonyms[rel_list[4]] = [rel_list[0]]
        else:
            synonyms[rel_list[4]].append(rel_list[0])

        continue

    elif rel_list[10] == 'MEDLINEPLUS' and rel_list[3].lower() == 'rq' and rel_list[7].lower() in ['mapped_to']:

        synonym_count_medlineplus += 1

        if rel_list[0] not in synonyms:
            synonyms[rel_list[0]] = [rel_list[4]]
        else:
            synonyms[rel_list[0]].append(rel_list[4])

        if rel_list[4] not in synonyms:
            synonyms[rel_list[4]] = [rel_list[0]]
        else:
            synonyms[rel_list[4]].append(rel_list[0])

        continue


    if child_concept != '0' and rel_list[10] not in ['CSP', 'MEDLINEPLUS', 'MEDCIN']:

        # REMOVE SELF REFs
        if child_concept == parent_concept:
            continue

        # Deduplicate
        curr_rel = child_concept+'-'+parent_concept+'-'+rel_type
        if curr_rel in seen_rels:
            continue
        else:
            seen_rels[curr_rel] = 1

        if parent_concept not in children:
            children[parent_concept] = [child_concept+'%'+rel_list[10]]
        else:
            if child_concept+'%'+rel_list[10] not in children[parent_concept]:
                children[parent_concept].append(child_concept+'%'+rel_list[10])

        if child_concept not in parents:
            parents[child_concept] = [parent_concept+'%'+rel_list[10]]
        else:
            if parent_concept+'%'+rel_list[10] not in parents[child_concept]:
                parents[child_concept].append(parent_concept+'%'+rel_list[10])


print len(parents), len(children), len(synonyms)
print 'CSP Synonyms: ', synonym_count_csp
print 'MEDCIN Synonyms: ', synonym_count_medcin
print 'MDR Synonyms: ', synonym_count_mdr
print 'MEDLINEPLUS Synonyms: ', synonym_count_medlineplus

syn_counter = 0

for item in synonyms:

    if item not in parents:
        for syn in synonyms[item]:
            if syn in parents:
                parents[item] = parents[syn]

                if item in concepts_preferred and syn in concepts_preferred and not syn_counter % 50:
                    print concepts_preferred[item][1]+':'+item
                    print concepts_preferred[syn][1]+':'+syn
                    print parents[syn]

                syn_counter += 1
                break


with open('parents_2022AA.pickle', 'wb') as handle:
    pickle.dump(parents, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open('children_2022AA.pickle', 'wb') as handle:
    pickle.dump(children, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open('synonyms_2022AA.pickle', 'wb') as handle:
    pickle.dump(synonyms, handle, protocol=pickle.HIGHEST_PROTOCOL)

print parents['C2239176']
print children['C2239176']
print syn_counter

