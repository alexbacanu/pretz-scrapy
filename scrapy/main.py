import logging

import scrapydo

from scrapy.exceptions import CloseSpider
from scrapy.spiderloader import SpiderLoader
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings


def crawl(spider_name):
    # Enable scrapy logs
    configure_logging({"LOG_FORMAT": "%(levelname)s: %(message)s"})

    # Log start of script
    logging.info(f"Starting crawl {spider_name}")

    # Initialize Scrapydo
    scrapydo.setup()

    # Get project settings
    project_settings = get_project_settings()

    # Load spiders
    spider_loader = SpiderLoader(project_settings)
    spider_run = spider_loader.load(spider_name)

    # Run spiders with scrapydo
    results = scrapydo.run_spider(
        spider_run,
        settings=project_settings,
        return_crawler=True,
    )

    # Get number of items scraped
    results_count = len(results.items)

    # Log number of items scraped
    # This check keeps running the whole duration for bot
    if results_count > 0:
        return results
    else:
        raise CloseSpider("No results")
