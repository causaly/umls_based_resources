batch = '20230224'

umls_mrsat = '/data-processing/2022_umls_download/2022AA/META/MRSAT.RRF'# input to 01_atc
atc_01_output = '/home/y.svetashova/umls/resources_2022AA/atc_level_map.pickle'

concepts_preferred = '/home/y.svetashova/umls/resources_2022AA/concepts_preferred_2022AA.pickle'
concepts_categories_map = '/home/y.svetashova/umls/resources_2022AA/conc_cat_map_2022AA.pickle'
atc_02_output = '/home/y.svetashova/umls/resources_2022AA/pg6_atc_hierarchy_metathesaurus.csv' # input to 03_atc
umls_mrrel = '/data-processing/2022_umls_download/2022AA/META/MRREL.RRF' # input to 02_atc

atc_03_output = '/home/y.svetashova/umls/resources_2022AA/to_load_pg6_atc_hierarchy_metathesaurus.csv'

umls_mrconso = '/data-processing/2022_umls_download/2022AA/META/MRCONSO.RRF'
MEDDRA_cui_to_atom = '/home/y.svetashova/umls/resources_2022AA/MEDDRA_cui_to_atom.pickle'
MEDDRA_atom_to_cui = '/home/y.svetashova/umls/resources_2022AA/MEDDRA_atom_to_cui.pickle'
meddra_01_output = '/home/y.svetashova/umls/resources_2022AA/mdr_hierarchy_metathesaurus.csv'

meddra_02_output = '/home/y.svetashova/umls/resources_2022AA/to_load_pg6_mdr_hierarchy_metathesaurus.csv'

OUT_STAGE_ONE = "/home/y.svetashova/umls/data/{}/pg6_{}_par_chd_stage1_agg.csv".format(batch, batch)

IN_STAGE_ONE  = "/home/y.svetashova/umls/data/{}/all_cuis_pg6_{}.txt".format(batch, batch)

umls_parents = '/home/y.svetashova/umls/resources_2022AA/parents_2022AA.pickle'

OUT_STAGE_TWO = '/home/y.svetashova/umls/data/{}/pg6_{}_par_chd_stage2_agg.csv'.format(batch, batch)
