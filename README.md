# Camphor_Tree
Pair of flask servers to communicate between RockBLOCK+ and an email server

## Pair of Sister Servers
`Satsuki` runs in cloud and handles GMail and CloudLoop API

`Mei` runs locally and handles RockBLOCK and AT commands

## Install
```commandline
git clone git@github.com:lzbrooks/Camphor_Tree.git
```

### Dependencies
- Python 3.8
- Package Requirements listed in `requirements.txt`
    - Development
        - pytest
        - pytest-mock
    - Both sisters
        - Flask
        - Werkzeug
        - WTForms
        - dnspython
        - email-validator
        - idna
        - requests
        - gunicorn
    - Mei specific
        - adafruit-python-shell
        - Adafruit-Blinka
        - adafruit-circuitpython-rockblock
        - pyserial
        - pyopenssl

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
export GOOGLE_APPLICATION_CREDENTIALS='...' # file path to credentials.json
export CAMPHOR_TREE_ACCESS_TOKEN_FILE='...' # file path to token.json
export CAMPHOR_TREE_AUTH_TOKEN='...'
export CAMPHOR_TREE_EMAIL='...'
export CAMPHOR_TREE_HARDWARE_ID='...'
export CAMPHOR_TREE_ID='...'
export CAMPHOR_TREE_IMEI='...'
export CAMPHOR_TREE_MAX_SIZE='...'
export CAMPHOR_TREE_PASS='...'
export CAMPHOR_TREE_REFRESH_TOKEN='...'
export CAMPHOR_TREE_RELAY='...'
export CAMPHOR_TREE_SECRET='...'
export CAMPHOR_TREE_SIS='...'
export CAMPHOR_TREE_SUB='...'
export CAMPHOR_TREE_TOPIC='...'
export CAMPHOR_TREE_WHITELIST='...'
```
All environment variables' values should be wrapped in single quotes `'`

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

## WSGI Config for Satsuki

Example WSGI config file:
```python
import os
import shlex
import subprocess
import sys

command = shlex.split("env -i bash -c 'source /home/project_name/Camphor_Tree/.env && env'")
proc = subprocess.Popen(command, stdout = subprocess.PIPE)
for line in proc.stdout:
    line = line.decode().strip()
    (key, _, value) = line.partition("=")
    os.environ[key] = value
proc.communicate()

path = '/home/project_name/Camphor_Tree'

if path not in sys.path:
    sys.path.append(path)

from app import app as application  # noqa
```
