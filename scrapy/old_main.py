import functions_framework
import scrapydo

from scrapy.spiderloader import SpiderLoader
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings


@functions_framework.http
def scheduled_cloud_crawl(data, context, spider_name):
    # Configure logging
    configure_logging({"LOG_FORMAT": "%(levelname)s: %(message)s"})

    # Initialize Scrapydo
    scrapydo.setup()

    # Get project settings
    project_settings = get_project_settings()

    # Load spiders
    spider_loader = SpiderLoader(project_settings)
    spider_run = spider_loader.load(spider_name)

    # Run spiders
    scrapydo.run_spider(spider_run, settings=project_settings)

    # Return response
    return "Success!"


@functions_framework.http
def triggered_cloud_crawl(data, spider_name):
    # Configure logging
    configure_logging({"LOG_FORMAT": "%(levelname)s: %(message)s"})

    # Initialize Scrapydo
    scrapydo.setup()

    # Get project settings
    project_settings = get_project_settings()

    # Load spiders
    spider_loader = SpiderLoader(project_settings)
    spider_run = spider_loader.load(spider_name)

    # Run spiders
    scrapydo.run_spider(spider_run, settings=project_settings)

    # Return response
    return "Success!"


def cloud_crawl_sitemap(data, context):
    spider_name = "emag_sitemap"
    scheduled_cloud_crawl(data, context, spider_name)


def cloud_crawl_products(data):
    spider_name = "emag_products"
    triggered_cloud_crawl(data, spider_name)
