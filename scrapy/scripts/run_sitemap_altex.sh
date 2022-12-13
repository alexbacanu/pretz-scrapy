#!/bin/bash

. ~/.bash_profile

# Run Scrapy->altex_sitemap
cd ~/scrapy/
source .venv/bin/activate
scrapy crawl altex_sitemap
