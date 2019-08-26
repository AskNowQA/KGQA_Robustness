"""
    This script will use the robustness repo (https://github.com/geraltofrivia/robustness) to inflect questions
        from existing datasets and store them in ./data/auto/<datasetname>
"""
import sys
import json
import spacy
import traceback
from tqdm import tqdm
sys.path.append('./auto')

# Local/Custom imports
from utilities import load_lcquad, InflectionError, save_auto
from auto import rules

# Important globals
nlp = spacy.load("en_core_web_sm")
RULES_PROFILE = 'all'

with open("./info.json", 'r') as config_file:
    config = json.load(config_file)

# Load raw datasets
lcquad = load_lcquad()
simplequestions = None # @TODO

# Get all relevant rules and their distribution
with open("./rules_dist.json", "r") as rules_file:
    rules_dists = json.load(rules_file)

# Use "all" rules for now
rules_dist = [x for x in rules_dists if x['_profile'] == RULES_PROFILE][0]

# Initialize the rule classes and put it in the dictionary as well.
for rule_name, rule_prob in rules_dist['distribution'].items():
    # Pull out the rule implementation
    rule_obj = getattr(rules, rule_name)(nlp)
    rules_dist['distribution'][rule_name] = (rule_prob, rule_obj)

# Add configuration and other metadata to file
lcquad['_config'] = config
lcquad['_rule_application_distribution'] = [x for x in rules_dists if x['_profile'] == RULES_PROFILE][0]

'''
    Now loop over the dataset(s) and inflect it.
'''
# LC-QuAD inflections
for i, datum in tqdm(enumerate(lcquad['raw']['train']), total=len(lcquad['raw']['train'])):
    raw, inflected = datum['corrected_question'], []
    for rule_name, (rule_prob, rule_obj) in rules_dist['distribution'].items():
        # Make a doc of input
        raw_spacied = nlp(raw)
        try:
            inflected.append([rule_name, rule_obj.apply(raw_spacied, rule_prob)])
        except TypeError:
            traceback.print_exc()
            print(raw)
            raise InflectionError

    lcquad['auto'].setdefault('train', []).append(inflected)

# LC-QuAD inflections
for i, datum in tqdm(enumerate(lcquad['raw']['test']), total=len(lcquad['raw']['test'])):
    raw, inflected = datum['corrected_question'], []
    for rule_name, (rule_prob, rule_obj) in rules_dist['distribution'].items():
        # Make a doc of input
        raw_spacied = nlp(raw)
        try:
            inflected.append([rule_name, rule_obj.apply(raw_spacied, rule_prob)])
        except TypeError:
            traceback.print_exc()
            print(raw)
            raise InflectionError

    lcquad['auto'].setdefault('test', []).append(inflected)

# Dump this in the `data/auto` dir
save_auto('lcquad', lcquad)

print(lcquad.keys())








