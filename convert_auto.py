"""
    This script will use the robustness repo (https://github.com/geraltofrivia/robustness) to inflect questions
        from existing datasets and store them in ./data/auto/<datasetname>
"""

import json


config = json.load('./info.json')

# Load dataset