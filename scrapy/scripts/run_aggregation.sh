#!/bin/bash

. ~/.bash_profile

cd /home/opc/scrapy/
source .venv/bin/activate
python aggregate.py
