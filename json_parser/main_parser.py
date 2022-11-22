import requests
import json
import os

class EncodeParser:
    def __init__(self):
        self.json_dir = None
        self.force_json_update = True

    def __init__(self, json_dir, force_json_update=False, use_custom_id=True):
        self.json_dir = json_dir
        self.force_json_update = force_json_update

    def get_biosample_for_dataset(self, exp_accession):
        headers = {'accept': 'application/json'}
        biosample_info = {'avail':False, 'n_replicates':0, 'biosample_jsons':[],
            'biosample_IDs':[], 'biosample_uuids':[], 'uniq_biosample':None,
            'custom_IDs':[], 'donor_IDs':[]}

        exp = None
        json_fp = '%s%s.json'%(self.json_dir, exp_accession)
        if self.json_dir != None and os.path.exists(json_fp) and not self.force_json_update:
            exp = json.load(open(json_fp,'r'))
        else:
            url = 'https://www.encodeproject.org/experiments/%s/?frame=object&frame=embedded'%(exp_accession)
            exp = requests.get(url, headers={'accept': 'application/json'}).json()
            if self.json_dir != None:
                open(json_fp,'w').write(json.dumps(exp, indent=4))

        replicates = exp.get('replicates',None)
        if replicates == None:
            print('Dataset %s has no replicates.'%(exp_accession))
            return biosample_info
        biosample_info['n_replicates'] = len(replicates)
        for repl_i, repl in enumerate(replicates):
            library = repl.get('library',None)
            if library == None:
                print('Replicate %d of dataset %s has no library.'%(repl_i, exp_accession))
                return biosample_info
            biosample = library.get('biosample',None)
            if biosample == None:
                print('Replicate %d of dataset %s has no biosample in library.'%(repl_i, exp_accession))
                return biosample_info

            biosample_info['avail'] = True
            biosample_info['biosample_IDs'].append(biosample['@id'])
            biosample_info['biosample_uuids'].append(biosample['uuid'])
            biosample_info['biosample_jsons'].append(biosample)
            custom_id = ''

            donor_id = 'NA'
            if 'donor' in biosample:
                donor_id = biosample['donor']['@id']
            biosample_info['donor_IDs'].append(donor_id)

        if len(set(biosample_info['biosample_IDs'])) == 1:
            biosample_info['uniq_biosample'] = biosample_info['biosample_jsons'][0]
        if len(set(biosample_info['donor_IDs'])) == 1:
            biosample_info['uniq_biosample'] = biosample_info['biosample_jsons'][0]

        return biosample_info

    def get_genetic_mods_for_dataset(self, exp_accession):
        headers = {'accept': 'application/json'}
        genmod_info = {'modified':False, 'genmod_IDs':[], 'short_descr':[],
            'n_replicates':0}

        exp = None
        json_fp = '%s%s.json'%(self.json_dir, exp_accession)
        if self.json_dir != None and os.path.exists(json_fp) and not self.force_json_update:
            exp = json.load(open(json_fp,'r'))
        else:
            url = 'https://www.encodeproject.org/experiments/%s/?frame=object&frame=embedded'%(exp_accession)
            exp = requests.get(url, headers={'accept': 'application/json'}).json()
            if self.json_dir != None:
                open(json_fp,'w').write(json.dumps(exp, indent=4))

        replicates = exp.get('replicates',None)
        if replicates == None:
            print('Dataset %s has no replicates.'%(exp_accession))
            return genmod_info
        genmod_info['n_replicates'] = len(replicates)
        for repl_i, repl in enumerate(replicates):
            library = repl.get('library',None)
            if library == None:
                print('Replicate %d of dataset %s has no library.'%(repl_i, exp_accession))
                return genmod_info
            biosample = library.get('biosample',None)
            if biosample == None:
                print('Replicate %d of dataset %s has no biosample in library.'%(repl_i, exp_accession))
                return genmod_info

            genmods = biosample.get('genetic_modifications',[])
            genmod_info['genmod_IDs'] += genmods
            if len(genmods) > 0:
                genmod_info['modified'] = True
                if 'applied_modifications' in biosample:
                    for modi in biosample['applied_modifications']:
                        short = '%d_%s_%s_%s'%(repl_i, modi.get('category','NA'),
                            modi.get('purpose','NA'), modi.get('method','NA'))
                        genmod_info['short_descr'].append(short)

        return genmod_info

    def get_antibody_for_ChIP(self, exp_accession):
        headers = {'accept': 'application/json'}
        antibody_info = {'n_replicates':0, 'antibody_IDs':[], 'antibodies':[]}

        exp = None
        json_fp = '%s%s.json'%(self.json_dir, exp_accession)
        if self.json_dir != None and os.path.exists(json_fp) and not self.force_json_update:
            exp = json.load(open(json_fp,'r'))
        else:
            url = 'https://www.encodeproject.org/experiments/%s/?frame=object&frame=embedded'%(exp_accession)
            exp = requests.get(url, headers={'accept': 'application/json'}).json()
            if self.json_dir != None:
                open(json_fp,'w').write(json.dumps(exp, indent=4))

        replicates = exp.get('replicates',None)
        if replicates == None:
            print('Dataset %s has no replicates.'%(exp_accession))
            return antibody_info
        antibody_info['n_replicates'] = len(replicates)
        for repl_i, repl in enumerate(replicates):
            antibody = repl.get('antibody',None)
            if antibody == None:
                print('Replicate %d of dataset %s has no antibody.'%(repl_i, exp_accession))
                return antibody_info
            antibody_info['antibody_IDs'].append(antibody['@id'])
            antibody_info['antibodies'].append(antibody)

        return antibody_info

