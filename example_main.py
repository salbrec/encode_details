import os
from json_parser.main_parser import EncodeParser
import pandas as pd
import random
import json

print('Read in some ChIP-seq meta data...')
general_meta = pd.read_csv('./encode_tsvs/ChIP-seq_SIMPA_allOrgas_withGenMod.tsv', sep='\t')
accessions = list(general_meta['Accession'])
print('Got %d accessions\n\n'%(len(accessions)))

# just to get some random order in the hope to simply see some different organisms
random.shuffle(accessions)

# the parser automatically downloads large JSON files for the experiments
# here you can specify where those files are stored
# this folder is checked automatically, so JSONs are downloaded again and again
parser = EncodeParser('../../encode_jsons/',force_json_update=True)

for accession in accessions:
    print('Parsing the dataset', accession)
    biosample_info = parser.get_biosample_for_dataset(accession)
    if biosample_info['uniq_biosample'] != None:
        the_biosample = biosample_info['uniq_biosample']
        print('The Biosample accession:', the_biosample['accession'],
        '(and the id: %s, uuid: %s)'%(the_biosample['@id'], the_biosample['uuid']))
        print('Age:\t', the_biosample.get('age', None), the_biosample.get('age_units',None))
        print('Sex:\t', the_biosample.get('sex', None))
        print('Stage:\t', the_biosample.get('life_stage',None))
    else:
        print('There was no uniq biosample...')
        if biosample_info['avail']:
            print('But there seems to be something...')
    print('\n%s\n'%(80*'#'))












