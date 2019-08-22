from pathlib import Path
import json

DATA_DIR = Path('./data')


class InflectionError(Exception): pass


def load_lcquad():
    lcquad = {
        "rawdir": DATA_DIR/"raw"/"lcquad",
        "autodir": DATA_DIR/"auto"/"lcquad",
        "golddir": DATA_DIR/"gold"/"lcquad",
        "raw": {},
        "auto": {}
    }

    with open(DATA_DIR/"raw"/"lcquad"/"test-data.json", 'r') as file:
        test = json.load(file)

    with open(DATA_DIR/"raw"/"lcquad"/"train-data.json", 'r') as file:
        train = json.load(file)

    lcquad['raw']['train'] = train
    lcquad['raw']['test'] = test

    return lcquad


def load_simplequestions():
    # @TODO: this
    raise NotImplementedError


if __name__ == '__main__':
    load_lcquad()
