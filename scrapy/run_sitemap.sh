#!/bin/bash

. ~/.bash_profile

cd /home/opc/scrapy/
source .venv/bin/activate
scrapy crawl emag_sitemap
