from pathlib import Path
import json

DATA_DIR = Path('./data')
AUTO_DIR = DATA_DIR / 'auto'
DATASETS = list(json.load(open('info.json'))['datasets'].keys())


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


def save_auto(dataset: str, data: dict) -> None:
    """ Dumping inflected data """

    assert dataset in DATASETS, f"Unknown Dataset"
    dump_dir = AUTO_DIR / dataset
    with open(dump_dir / 'dump.json') as f:
        json.dump(data, f)


def load_simplequestions():
    # @TODO: this
    raise NotImplementedError


if __name__ == '__main__':
    load_lcquad()
