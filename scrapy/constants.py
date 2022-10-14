# Dev tag
STORE_NAME = "emag"
DEV_TAG = ""

# Scrapy
SPIDER_SITEMAP = f"{STORE_NAME}_sitemap"
SPIDER_DOMAINS = f"{STORE_NAME}.ro"
SPIDER_START_URLS = "https://www.emag.ro/sitemaps/category-filters-index.xml"

SPIDER_PRODUCTS = f"{STORE_NAME}_products"

# Redis
REDIS_URL_KEY = f"{STORE_NAME}_sitemap{DEV_TAG}:start_urls"

# MongoDB
MONGODB_DB = f"pretz{DEV_TAG}"
MONGODB_COLL = f"{STORE_NAME}{DEV_TAG}"
