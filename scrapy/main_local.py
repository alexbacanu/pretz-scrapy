import logging

import scrapydo

from scrapy.exceptions import CloseSpider
from scrapy.spiderloader import SpiderLoader
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings


def crawl(spider_name):
    try:
        # Enable scrapy logs
        configure_logging({"LOG_FORMAT": "%(levelname)s: %(message)s"})

        # Log start of script
        logging.info(f"Crawling {spider_name}")

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
            # start_url=url,
            return_crawler=True,
        )

        # Get number of items scraped
        results_count = len(results.items)

        # Log number of items scraped
        # This check keeps running the whole duration for bot
        if results_count > 0:
            logging.info(f"Length of items are: {results_count}")
            return results
        else:
            logging.error(f"Length of items are: {results_count}")
            raise CloseSpider("No results")

    except Exception as error:
        logging.error(error)


if __name__ == "__main__":
    spider_name = "emag_products"
    # url = "https://www.emag.ro/hard-disk-uri-notebook/vendor/emag/c"

    try:
        crawl(spider_name)
    except Exception as error:
        logging.error(error)
