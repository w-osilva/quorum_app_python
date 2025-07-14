#!/usr/bin/env bash

# Create and activate a Python virtual environment
python -m venv .venv
source .venv/bin/activate

# Install required packages
make install 

# Create the database and import initial data
make db-create 
make db-import
