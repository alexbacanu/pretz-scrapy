#!/bin/bash

. ~/.bash_profile

# Move failed url to start_urls
redis-cli -u $REDIS_URI SREM emag_products:failed_urls "https://www.emag.ro/robots.txt"
redis-cli -u $REDIS_URI SUNIONSTORE emag_sitemap:start_urls emag_products:failed_urls emag_sitemap:start_urls
redis-cli -u $REDIS_URI DEL emag_products:failed_urls

redis-cli -u $REDIS_URI SUNIONSTORE altex_sitemap:start_urls altex_products:failed_urls altex_sitemap:start_urls
redis-cli -u $REDIS_URI DEL altex_products:failed_urls

# Clear temp files
rm -r /tmp/emag_*
rm -r /tmp/altex_*