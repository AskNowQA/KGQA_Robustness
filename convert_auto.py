"""
    This script will use the robustness repo (https://github.com/geraltofrivia/robustness) to inflect questions
        from existing datasets and store them in ./data/auto/<datasetname>
"""
import sys
import json
sys.path.append('./auto')

# Local/Custom imports
from utils import *
from auto import rules

with open("./info.json", 'r') as config_file:
    config = json.load(config_file)

# Load raw datasets
lcquad = load_lcquad()
simplequestions = None # @TODO

# Get all relevant rules and their distribution
with open("./rules_dist","r") as rules_file:
    rules_dists = json.load(rules_file)

# Use "all" rules for now
rules_dist = [x for x in rules_dists if x['_profile'] == "all"][0]

for rule_name in rules_dist['distribution'].keys():
    # Pull out the rule implementation







