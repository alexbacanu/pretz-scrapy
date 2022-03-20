# launcher.py
# See: https://blog.vikfand.com/posts/scrapy-fargate-sls-guide/
import sys
import json
from hp_emag.crawl import crawl


def scrape(event={}, context={}):
    crawl(**event)


if __name__ == "__main__":
    try:
        event = json.loads(sys.argv[1])
    except IndexError:
        event = {}
    scrape(event)
