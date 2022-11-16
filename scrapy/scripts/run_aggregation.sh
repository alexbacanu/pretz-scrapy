#!/bin/bash

. ~/.bash_profile

# Run MongoDB Aggregation
cd /home/opc/scrapy/
source .venv/bin/activate
python aggregate.py
