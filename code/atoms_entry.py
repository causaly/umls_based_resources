# GET ALL ATOMS

#!/usr/bin/python
# -*- coding: utf-8 -*-

import pickle

filename = '/data-processing/2022_umls_download/2022AA/META/MRCONSO.RRF'
f_handle = open(filename, 'r')

all_concepts = {}

counter = 0

for line in f_handle.readlines():
    counter += 1
    if not counter % 100000:
        print counter

    tokens = line.split('|')
    cui = tokens[0]
    name = tokens[14]

    vocab = tokens[11]
    if 'CZE' in vocab or 'FIN' in vocab or 'GER' in vocab or 'DUT' in vocab or 'ITA' in vocab or 'JPN' in vocab \
            or 'NOR' in vocab or 'POL' in vocab or 'RUS' in vocab or 'POR' in vocab or 'SCR' in vocab \
            or 'SPA' in vocab or 'SWE' in vocab or 'FRE' in vocab or 'HUN' in vocab or 'BPO' in vocab or 'KOR' in vocab:
        continue

    # don't allow abbreviations
    if len(name) < 3:
        continue

    if cui not in all_concepts:
        all_concepts[cui] = [name]
    else:
        if name not in all_concepts[cui]:
            all_concepts[cui].append(name)

for item in all_concepts['C0027051']:
    print item

print len(all_concepts)

with open('atoms_entry_2022AA.pickle', 'wb') as handle:
    pickle.dump(all_concepts, handle, protocol=pickle.HIGHEST_PROTOCOL)
