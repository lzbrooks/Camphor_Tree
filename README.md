# Camphor_Tree
Pair of flask servers to communicate between RockBLOCK+ and an email server

## Pair of Sister Servers
`Satsuki` runs in cloud and handles GMail and CloudLoop API

`Mei` runs locally and handles RockBLOCK and AT commands

## Install
```commandline
git clone git@github.com:lzbrooks/Camphor_Tree.git
```

## Register RockBLOCK
- Need to own and register a RockBLOCK Iridium Modem of some kind
- Codebase currently tested with a RockBLOCK+

## Set up Google Pub/Sub Topic
- Set up a free [Google Cloud](https://console.cloud.google.com/) account
- GMail publisher to Topic
- Push HTTP POST subscribe Satsuki server url to Topic

## Set up ENV VARs
Make `.env` file up one folder from `Camphor_Tree` folder
```commandline
nano .env
```
e.g.
```commandline
CAMPHOR_TREE_AUTH_TOKEN=...
CAMPHOR_TREE_EMAIL=...
CAMPHOR_TREE_HARDWARE_ID=...
CAMPHOR_TREE_ID=...
CAMPHOR_TREE_IMEI=...
CAMPHOR_TREE_MAX_SIZE=...
CAMPHOR_TREE_PASS=...
CAMPHOR_TREE_REFRESH_TOKEN=...
CAMPHOR_TREE_RELAY=...
CAMPHOR_TREE_SECRET=...
CAMPHOR_TREE_SIS=...
CAMPHOR_TREE_SUB=...
CAMPHOR_TREE_TOPIC=...
CAMPHOR_TREE_WHITELIST=...
```

## Run dev server on LAN
Run bash script up one folder from `Camphor_Tree` folder

Bash script:
```commandline
#!/usr/bin/env sh

# Load variables from .env file.
export $(cat ./.env | grep -v ^# | xargs) >/dev/null

cd Camphor_Tree
pip install -r requirements.txt
flask run --host=0.0.0.0
```

## Check RockBLOCK+ Buffer
Make `Inbox` folder in `Camphor_Tree` folder

Run bash script up one folder from `Camphor_Tree` folder

Bash script:
```commandline
#!/usr/bin/env sh

# Load variables from .env file.
export $(cat ./.env | grep -v ^# | xargs) >/dev/null

cd Camphor_Tree
pip install -r requirements.txt
python3 rock_block_api.py
```
