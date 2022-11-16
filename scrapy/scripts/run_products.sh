#!/bin/bash

. ~/.bash_profile

# Run Scrapy->emag_products
cd /home/opc/scrapy/
source .venv/bin/activate
scrapy crawl emag_products
