import os
from json_parser.main_parser import EncodeParser
import pandas as pd
import random
import json

# the parser automatically downloads large JSON files for the experiments
# here you can specify where those files are stored
# this folder is checked automatically, so JSONs are downloaded again and again
parser = EncodeParser('../../encode_jsons/genmod_test/',force_json_update=True)

accessions = ['ENCSR000EHA', 'ENCSR140GLO', 'ENCSR668LDD']
for accession in accessions:
    print('Parsing the dataset', accession)
    genmod_info = parser.get_antibody_for_ChIP(accession)
    
    print(genmod_info)

    print('\n%s\n'%(80*'#'))












