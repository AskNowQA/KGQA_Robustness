from pathlib import Path
import pandas as pd
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


def load_simplequestions():
    """ Assume we only have train data """
    simplequestions = {
        "rawdir": DATA_DIR / "raw" / "simplequestions",
        "autodir": DATA_DIR / "auto" / "simplequestions",
        "golddir": DATA_DIR / "gold" / "simplequestions",
        "raw": {},
        "auto": {}
    }

    data = pd.read_csv(simplequestions['rawdir'] / 'amt.csv').values.tolist()

    real_data = []
    for datum in data:
        assert len(datum) is 4
        _datum = [{
            'uid': datum[0],
            'question': datum[1]
        }, {
            'uid': datum[2],
            'question': datum[3]
        }]
        real_data += _datum

    # Assume its all train data
    simplequestions['raw']['train'] = real_data
    return simplequestions


def save_auto(dataset: str, data: dict) -> None:
    """ Dumping inflected data """

    assert dataset in DATASETS, f"Unknown Dataset"
    dump_dir = data['autodir']

    # Convert all paths to str
    for k, v in data.items():
        if type(v) is type(Path()):
            data[k] = str(v)

    # Dump eeet
    with open(dump_dir / 'dump.json', 'w+') as f:
        json.dump(data, f)


if __name__ == '__main__':
    load_lcquad()
