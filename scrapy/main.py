import base64

import functions_framework
import scrapydo

# from scrapy.spiderloader import SpiderLoader
# from scrapy.utils.project import get_project_settings


# Triggered from a message on a Cloud Pub/Sub topic.
@functions_framework.cloud_event
def crawl_pubsub(cloud_event):

    # Print out the data from Pub/Sub, to prove that it worked
    spider_name = base64.b64decode(cloud_event.data["message"]["data"])
    print("HERE BE SPIDERS")
    print(spider_name)

    # Initialize Scrapydo
    scrapydo.setup()

    # Get project settings
    # project_settings = get_project_settings()

    # Load spiders
    # spider_loader = SpiderLoader(project_settings)
    # spider_run = spider_loader.load(spider_name)

    # Run spiders
    # scrapydo.run_spider(spider_run, settings=project_settings)


# def cloud_crawl_sitemap(data, context):
#     spider_name = "emag_sitemap"
#     scheduled_cloud_crawl(data, context, spider_name)


# def cloud_crawl_products(data):
#     spider_name = "emag_products"
#     triggered_cloud_crawl(data, spider_name)
