# hp_emag/crawl.py
# See: https://blog.vikfand.com/posts/scrapy-fargate-sls-guide/
import sys
import imp
import os

from scrapy.spiderloader import SpiderLoader
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# Need to "mock" sqlite for the process to not crash in AWS Lambda / Amazon Linux
sys.modules["sqlite"] = imp.new_module("sqlite")
sys.modules["sqlite3.dbapi2"] = imp.new_module("sqlite.dbapi2")


def is_in_aws():
    return os.getenv("AWS_EXECUTION_ENV") is not None


def crawl(settings={}, spider_name="emag_products", spider_kwargs={}):
    project_settings = get_project_settings()
    spider_loader = SpiderLoader(project_settings)

    spider_cls = spider_loader.load(spider_name)

    if is_in_aws():
        # Lambda can only write to the /tmp folder.
        settings["HTTPCACHE_DIR"] = "/tmp"

    process = CrawlerProcess({**project_settings, **settings})

    process.crawl(spider_cls, **spider_kwargs)
    process.start()
