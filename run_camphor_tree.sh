#!/bin/bash

# Load variables from .env file
source .env

pip install -r requirements.txt
flask run --host=0.0.0.0

