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
Make `.env` file in `Camphor_Tree` folder
```commandline
nano .env
```
e.g.
```commandline
export CAMPHOR_TREE_AUTH_TOKEN=...
export CAMPHOR_TREE_EMAIL=...
export CAMPHOR_TREE_HARDWARE_ID=...
export CAMPHOR_TREE_ID=...
export CAMPHOR_TREE_IMEI=...
export CAMPHOR_TREE_MAX_SIZE=...
export CAMPHOR_TREE_PASS=...
export CAMPHOR_TREE_REFRESH_TOKEN=...
export CAMPHOR_TREE_RELAY=...
export CAMPHOR_TREE_SECRET=...
export CAMPHOR_TREE_SIS=...
export CAMPHOR_TREE_SUB=...
export CAMPHOR_TREE_TOPIC=...
export CAMPHOR_TREE_WHITELIST=...
```

## Run dev server on LAN
Run bash script in `Camphor_Tree` folder

Bash script:
```commandline
#!/bin/bash

# Load variables from .env file
source .env

pip install -r requirements.txt
flask run --host=0.0.0.0
```

## Check RockBLOCK+ Buffer
Make `Inbox` folder in `Camphor_Tree` folder

Run bash script in `Camphor_Tree` folder

Bash script:
```commandline
#!/bin/bash

# Load variables from .env file
source .env

pip install -r requirements.txt
cd apis
python3 rock_block_api.py
```
