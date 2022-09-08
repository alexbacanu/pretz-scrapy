import asyncio
import base64
import logging

import functions_framework
import scrapydo

from scrapy.exceptions import CloseSpider
from scrapy.spiderloader import SpiderLoader
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings


async def crawl_async(cloud_event):
    try:
        # Enable scrapy logs
        configure_logging({"LOG_FORMAT": "%(levelname)s: %(message)s"})

        # Decode spider_name
        spider_name = base64.b64decode(cloud_event.data["message"]["data"]).decode()

        # Decode url (if exists)
        if "url" in cloud_event.data["message"]:
            url = base64.b64decode(cloud_event.data["message"]["url"]).decode()
        else:
            url = cloud_event.data["message"]["url"] = ""

        # Log start of script
        logging.info(f"Crawling {spider_name} on {url}")

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
            start_url=url,
            return_crawler=True,
        )

        # Get number of items scraped
        results_count = len(results.items)

        # Log number of items scraped
        # This check keeps running the whole duration for bot
        # This helps Google Tasks
        if results_count > 0:
            logging.info(f"Length of items are: {results_count}")
            return results
        else:
            logging.error(f"Length of items are: {results_count}")
            raise CloseSpider("No results")

    except Exception as error:
        logging.error(error)


# Triggered from a message on a Cloud Pub/Sub topic.
@functions_framework.cloud_event
def crawl_pubsub(cloud_event):
    # Make crawling async (TODO: does it work?)
    async_task = crawl_async(cloud_event)
    asyncio.run(async_task)


if __name__ == "__main__":
    # Testing script locally, need to fix replacing .data
    spider_name = "emag_products"
    url = "https://www.emag.ro/laptopuri/vendor/emag/c"

    # Encode spider and url names
    spider_b64 = base64.b64encode(spider_name.encode("utf-8")).decode("ascii")
    url_b64 = base64.b64encode(url.encode("utf-8")).decode("ascii")

    # Simulate cloud function event
    cloud_event = {
        "message": {
            "data": spider_b64,
            "url": url_b64,
        }
    }

    # Start crawling
    async_task = crawl_async(cloud_event)
    asyncio.run(async_task)
