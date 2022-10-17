import logging

from scrapy.crawler import CrawlerProcess
from scrapy.spiderloader import SpiderLoader
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings


def crawl(spider_name):
    # Enable scrapy logs
    configure_logging({"LOG_FORMAT": "%(levelname)s: %(message)s"})

    # Log start of script
    logging.info(f"[Main] Started crawl {spider_name}")

    # Get project settings
    project_settings = get_project_settings()

    # Load spiders
    spider_loader = SpiderLoader(project_settings)
    spider_run = spider_loader.load(spider_name)

    process = CrawlerProcess(project_settings)
    process.crawl(spider_run)

    process.start()
