"""
    This script will use the robustness repo (https://github.com/geraltofrivia/robustness) to inflect questions
        from existing datasets and store them in ./data/auto/<datasetname>
"""
import sys
import json
import spacy
import pickle
import traceback
from tqdm import tqdm
sys.path.append('./auto')

# Local/Custom imports
from utilities import load_lcquad, InflectionError, save_auto, load_simplequestions
from auto import rules


RULES_PROFILE = 'all'


def init(nlp: spacy, rules_dist: dict) -> dict:

    # Initialize the rule classes and put it in the dictionary as well.
    for rule_name, rule_prob in rules_dist['distribution'].items():
        # Pull out the rule implementation
        rule_obj = getattr(rules, rule_name)(nlp)
        rules_dist['distribution'][rule_name] = (rule_prob, rule_obj)

    return rules_dist


def inflect_lcquad(data: dict, rules_dist: dict) -> dict:
    """Simply loop over the raw, and inflect it."""

    # LC-QuAD inflections
    for i, datum in tqdm(enumerate(data['raw']['train']), total=len(data['raw']['train'])):
        raw, inflected = datum['corrected_question'], []
        for rule_name, (rule_prob, rule_obj) in rules_dist['distribution'].items():
            # Make a doc of input
            raw_spacied = nlp(raw)
            try:
                flag, res = rule_obj.apply(raw_spacied, rule_prob)
                res = str(res)
                inflected.append([rule_name, (flag, res)])
            except TypeError:
                traceback.print_exc()
                print(raw)
                raise InflectionError

        data['auto'].setdefault('train', []).append(inflected)

    # LC-QuAD inflections
    for i, datum in tqdm(enumerate(data['raw']['test']), total=len(data['raw']['test'])):
        raw, inflected = datum['corrected_question'], []
        for rule_name, (rule_prob, rule_obj) in rules_dist['distribution'].items():
            # Make a doc of input
            raw_spacied = nlp(raw)
            try:
                flag, res = rule_obj.apply(raw_spacied, rule_prob)
                res = str(res)
                inflected.append([rule_name, (flag, res)])
            except TypeError:
                traceback.print_exc()
                print(raw)
                raise InflectionError

        data['auto'].setdefault('test', []).append(inflected)

    return data


def inflect_simplequestions(data: dict, rules_dist: dict) -> dict:
    """ Similar logic as above """

    for i, datum in tqdm(enumerate(data['raw']['train']), total=len(data['raw']['train'])):
        uid, raw = datum.values()
        inflected = []

        for rule_name, (rule_prob, rule_obj) in rules_dist['distribution'].items():
            raw_spacied = nlp(raw)
            try:
                flag, res = rule_obj.apply(raw_spacied, rule_prob)
                res = str(res)
                inflected.append([uid, rule_name, (flag, res)])
            except TypeError:
                traceback.print_exc()
                print(raw)
                raise InflectionError

        data['auto'].setdefault('train', []).append(inflected)

    return data


def inflect_again(data: dict) -> dict:
    raise NotImplementedError


if __name__ == '__main__':

    toinflect = ['simplequestions']

    # Important globals
    nlp = spacy.load("en_core_web_sm")

    with open("./info.json", 'r') as config_file:
        config = json.load(config_file)

    # Load raw datasets
    lcquad = load_lcquad()
    simplequestions = load_simplequestions()

    # Get all relevant rules and their distribution
    with open("./rules_dist.json", "r") as rules_file:
        rules_dists = json.load(rules_file)

    # Add configuration and other metadata to file
    lcquad['_config'] = config
    lcquad['_rule_application_distribution'] = RULES_PROFILE
    simplequestions['_rule_application_distribution'] = RULES_PROFILE

    # Use "all" rules for now
    rules_dist = [x for x in rules_dists if x['_profile'] == RULES_PROFILE][0]
    rules_dist = init(nlp, rules_dist)

    if 'lcquad' in toinflect:
        # Get inflections
        lcquad = inflect_lcquad(lcquad, rules_dist)

        # TO DELETE
        with open('tmp.pkl', 'wb+') as f:
            pickle.dump(lcquad, f)

        save_auto('lcquad', lcquad)

    if 'simplequestions' in toinflect:
        # Get inflections
        simplequestions = inflect_simplequestions(simplequestions, rules_dist)

        # TO DELETE
        with open('tmp_sq.pkl', 'wb+') as f:
            pickle.dump(simplequestions, f)

        save_auto('simplequestions', simplequestions)

    print("Done")





