# Camphor_Tree
A pair of flask servers to communicate between RockBLOCK+ and an email server

The goal of this project is to receive and send emails while underway across the Pacific out of cellphone signal distance on my sailboat without paying for an InReach.  The system works using an inexpensive company-facing Iridium satellite modem (RockBLOCK+) which was IPV8, extremely low power and low latency.  Because the RockBLOCK+ provided Short Burst Data intended for IoT relay, any data I wanted to transmit needed to processed.

To accomplish this the RockBLOCK+ needed to be controlled by the vessel's RaspberryPi single board computer.  I wrote server software that relayed base64 bit encoded emails from the vessel's Pi (Mei) to and from a cloud-based instance (Satsuki).  When I want to retrieve messages I use Mei's LAN website interface, which I made accessible from any browser, like, say, from my phone.  Mei, through the RockBLOCK+, requests all messages from the satellite and unencodes and decompresses all incoming messages. 

- Mei encodes plaintext emails into base64 chunks sized to send from the RockBLOCK+ to the Iridium Satellite Low Orbit Dishes above the Pacific down to a little email server in the UK run by CloudLoop (the company I buy satellite bandwidth from by the kilobyte).  Because satellite bandwidth is expensive, I also compressed each email using a shorthand shared by both onboard and onshore servers before encoding for transmit.

- At the CloudLoop email server I have all arriving messages forwarded to Satsuki.  Once Satsuki gets all the encoded and compressed email chunks, it first strings the chunks back together then unencodes and decompresses the completed emails, and sends them on to the indicated recipients using an email address Satsuki is authorized to use and monitor.  Any emails sent to the email address Satuki monitors are downloaded, chunked, compressed, encoded, and relayed to the CloudLoop email server by Satuki to wait for Mei to request any waiting messages.

Future Work: reconstituting emails from chunks automatically, parsing sent emails of arbitrary length from the RockBLOCK+, and GRIB requests through SailDocs

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
