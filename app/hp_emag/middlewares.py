# Define here the models for your spider middleware
import logging
import os

import boto3
from botocore.config import Config
from scrapy.http import Request
from scrapy.utils.project import get_project_settings

logger = logging.getLogger(__name__)

class ScrapeAPIProxyMiddleware(object):
    def process_request(self, request, spider):
        request.meta["proxy"] = f"http://scraperapi.autoparse=true:{os.getenv('SCRAPEAPI_KEY')}@proxy-server.scraperapi.com:8001"

class AmazonStartUrlsMiddleware:

    # pylint: disable=unused-argument
    def __init__(self):
        # Init DB
        self.dynamodb = boto3.resource(
            "dynamodb",
            region_name="eu-central-1",
            config=Config(retries={"max_attempts": 20, "mode": "adaptive"}),
        )

        self.su_table = self.dynamodb.Table("emag-start_urls")

    def process_start_requests(self, start_requests, spider):
        settings = get_project_settings()

        # TODO: I don't like this approach, make it better
        if spider.name == "emag_products":
            status_code_val = 0
        else:
            status_code_val = 511

        # Pop x entries from database and return their value
        for _ in range(settings.get("START_URLS_COUNT")):
            try:
                get_url = self.su_table.update_item(
                    Key={
                        "status_code": status_code_val,
                    },
                    UpdateExpression="REMOVE crawled_urls[0]",
                    ReturnValues="UPDATED_OLD",
                )["Attributes"]["crawled_urls"][0]
            except KeyError:
                logger.info("No more start_urls to crawl")
                break

            yield Request(url=get_url)

    def process_spider_exception(self, response, exception, spider):
        logger.exception(
            "Exception in spider %s on %s: %s",
            spider.name,
            response.url,
            response.status,
        )

        # This will append the crawled_urls to the status_code key if it doesn't exist already
        # TODO: prevent duplicates
        self.su_table.update_item(
            Key={
                "status_code": response.status,
            },
            UpdateExpression="SET #cu = list_append(if_not_exists(#cu, :el), :cu)",
            ExpressionAttributeNames={
                "#cu": "crawled_urls",
            },
            ExpressionAttributeValues={
                ":el": [],
                ":cu": [response.url],
            },
        )


class AzureStartUrlsMiddleware:
    pass
