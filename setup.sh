# Setting up folders
mkdir data
mkdir data/raw
mkdir data/gold
mkdir data/auto
mkdir data/raw/lcquad
mkdir data/raw/simplequestions
mkdir data/gold/lcquad
mkdir data/gold/simplequesitons
mkdir data/auto/lcquad
mkdir data/auto/simplequestions

echo "Set up data directory. Pulling data now."
cd data/raw/lcquad
wget https://raw.githubusercontent.com/AskNowQA/LC-QuAD/data/test-data.json
wget https://raw.githubusercontent.com/AskNowQA/LC-QuAD/data/train-data.json
cd ../../..
# TODO: pull raw simplequestions, other things


# Init needed repos
cd auto
./setup.sh
cd ..

# Get KGQA systems
mkdir kgqa/krantikari

# @TODO: @Gaurav add the link here
# git clone <buboqa fork link> kgqa/buboqa