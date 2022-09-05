import base64

import functions_framework
import scrapydo

from scrapy.spiderloader import SpiderLoader
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings


# Triggered from a message on a Cloud Pub/Sub topic.
@functions_framework.cloud_event
def crawl_pubsub(cloud_event):
    # Configure logging
    configure_logging({"LOG_FORMAT": "%(levelname)s: %(message)s"})

    # Print out the data from Pub/Sub, to prove that it worked
    spider_name = base64.b64decode(cloud_event.data["message"]["data"]).decode()

    if "url" in cloud_event.data["message"]:
        url = base64.b64decode(cloud_event.data["message"]["url"]).decode()
    else:
        url = cloud_event.data["message"]["url"] = ""

    # Testing
    # spider_name = "emag_products"
    # url = "https://www.emag.ro/laptopuri/vendor/emag/c"

    # Initialize Scrapydo
    scrapydo.setup()

    # # Get project settings
    project_settings = get_project_settings()

    # # Load spiders
    spider_loader = SpiderLoader(project_settings)
    spider_run = spider_loader.load(spider_name)

    # # Run spiders
    print(f"main.py:    Crawling {spider_name} on {url}")
    scrapydo.run_spider(spider_run, settings=project_settings, start_url=url)


if __name__ == "__main__":
    # crawl_pubsub("YAS")
    pass
