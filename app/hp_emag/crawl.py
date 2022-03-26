# hp_emag/crawl.py
# See: https://blog.vikfand.com/posts/scrapy-fargate-sls-guide/

import os
import sys
import types

# Avoid ReactorNotRestartable using scrapydo
import scrapydo
from scrapy.spiderloader import SpiderLoader
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

scrapydo.setup()
# Need to 'mock' sqlite for the process to not crash in AWS Lambda, Amazon Linux
sys.modules["sqlite"] = types.ModuleType("sqlite")
sys.modules["sqlite3.dbapi2"] = types.ModuleType("sqlite.dbapi2")


def is_in_aws():
    return os.getenv("AWS_EXECUTION_ENV") is not None


def crawl(spider_name):
    # See logs in serverless invoke command
    configure_logging({"LOG_FORMAT": "%(levelname)s: %(message)s"})

    project_settings = get_project_settings()
    spider_loader = SpiderLoader(project_settings)
    spider_cls = spider_loader.load(spider_name)

    if is_in_aws():
        # Lambda can only write to the /tmp folder.
        project_settings["HTTPCACHE_DIR"] = "/tmp"

    scrapydo.run_spider(spider_cls, settings=project_settings)
