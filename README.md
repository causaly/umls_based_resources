# UMLS based resources

Warning: this code is written in Python 2. It will be refactored to Python 3 soon. 

## Resources Locations 
For this project to work, you need access to two sets of data, which can be found on the `aws_dev_pipeline_01` server.
These resources are used in the config file, and both have to do with the UMLS version we are currently using:
1. The first resource is the *2022AA release of UMLS* (version subject to change when newer version is released). This can be found in the following folder of the server: `/data-processing/2022_umls_download/2022AA/`. Please change the config paths of the following variables to match the path in your environment: `umls_mrsat`, `umls_mrrel`, `umls_mrconso`. For more information on these three files and their schema, check the [UMLS documentation](https://www.ncbi.nlm.nih.gov/books/NBK9685/) and check out our own [documentation](https://causaly.atlassian.net/wiki/spaces/KE/pages/519962821/UMLS+Knowledge+Resources) to see how and where we use them.
2. The second resource is the *resources_2022AA* folder found in the server at `/home/y.svetashova/umls/resources_2022AA/`. After you get the files locally, please make sure that the following variables in `config.py` point to the correct path: `atc_01_output`, `concepts_preferred`, `concepts_categories_map`, `atc_02_output`, `atc_03_output`, `MEDDRA_cui_to_atom`, `MEDDRA_atom_to_cui`, `meddra_01_output`, `meddra_02_output`, `OUT_STAGE_ONE`, `IN_STAGE_ONE`, `umls_parents`, `OUT_STAGE_TWO`
3. The third source is the data we get from our current monthly batch. Create a folder in `data/` with the name of the current batch, get the batch data an add them to this folder. This will allow the monthly run for hierarchy generation to run.

## Running the Scripts in this project
There are multiple scripts in the `code/` folder. These all have to do with UMLS, but they can be divided into 3 separate jobs, with the following scripts ran (for more information on how all these scripts work, please see our [Confluence](https://causaly.atlassian.net/wiki/spaces/KE/pages/519962821/UMLS+Knowledge+Resources) page):

1. Hierarchy Generation - run monthly during Neo4j loading
    a. `02_parent_child_hierarchy_generation_01.py`
    b. `02_parent_child_hierarchy_generation_02.py`

2. Dictionaries Generation - run every time there's a new UMLS update
    a. `categories_map.pickle`
    b. `atoms_entry.py`
    c. `conc_cat_map.py`
    d. `concepts_preferred.py`
    e. `parents_children.py`

3. ATC Hierarchy Generation -  run every time there's a new UMLS update (?)
    a. `umls_extract_atc_hierarchy_01.py`
    b. `umls_extract_atc_hierarchy_02.py`
    c. `umls_extract_atc_hierarchy_03.py`

3. MedDRA Hierarchy Generation -  run every time there's a new UMLS update (?)
    a. `umls_extract_meddra_hierarchy_01.py`
    b. `umls_extract_meddra_hierarchy_02.py`
    c. `umls_extract_meddra_hierarchy_03.py`


Further documentation can be found in [Confluence](https://causaly.atlassian.net/wiki/spaces/KE/pages/519962821/UMLS+Knowledge+Resources).