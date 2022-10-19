#!/bin/bash

# Load variables from .env file.
source .env

pip install -r requirements.txt
python3 mailbox_check.py
