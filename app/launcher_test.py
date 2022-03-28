# launcher.py
# See: https://blog.vikfand.com/posts/scrapy-fargate-sls-guide/
import json
import sys

from hp_emag.crawl import crawl


def scrape(event={}, context={}):
    spider_name = "test_response"
    crawl(spider_name)


if __name__ == "__main__":
    try:
        event = json.loads(sys.argv[1])
    except IndexError:
        event = {}
    scrape(event)
