# launcher.py
# See: https://blog.vikfand.com/posts/scrapy-fargate-sls-guide/
import json
import sys

from hp_emag.crawl import crawl


def scrape(spider_name):
    crawl(spider_name)


if __name__ == "__main__":
    try:
        spider_name = json.loads(sys.argv[1])
    except IndexError:
        spider_name = {}
    scrape(spider_name)
