# launcher.py
# See: https://blog.vikfand.com/posts/scrapy-fargate-sls-guide/
import json
import sys

from hp_emag.crawl import crawl


def lambdaScrapeProducts(event={}, context={}):
    spider_name = "emag_products"
    crawl(spider_name)


def lambdaScrapeFailed(event={}, context={}):
    spider_name = "emag_failed_products"
    crawl(spider_name)


def lambdaScrapeSitemap(event={}, context={}):
    spider_name = "emag_sitemap"
    crawl(spider_name)


def lambdaScrapeTest(event={}, context={}):
    spider_name = "test_response"
    crawl(spider_name)


if __name__ == "__main__":
    try:
        event = json.loads(sys.argv[1])
    except IndexError:
        event = {}
    scrape(event)
