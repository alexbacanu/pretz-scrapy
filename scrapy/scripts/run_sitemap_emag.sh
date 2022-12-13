#!/bin/bash

. ~/.bash_profile

# Run Scrapy->emag_sitemap
cd ~/scrapy/
source .venv/bin/activate
scrapy crawl emag_sitemap
