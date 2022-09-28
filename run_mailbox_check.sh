#!/bin/bash

# Load variables from .env file.
source .env

pip install -r requirements.txt
cd apis
python3 rock_block_api.py

