#!/bin/bash

# Install Python's selenium and requests libraries
pip install selenium requests

# Download the latest version of geckodriver
wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz

# Unpackage geckodriver
tar -xvf geckodriver-v0.24.0-linux64.tar.gz

# Add geckodriver to the system's PATH
export PATH=$PATH:$(pwd)