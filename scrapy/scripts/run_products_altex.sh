#!/bin/bash

. ~/.bash_profile

# Run Scrapy->altex_products
cd ~/scrapy/
source .venv/bin/activate
scrapy crawl altex_products
