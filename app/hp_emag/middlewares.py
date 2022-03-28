# Define here the models for your spider middleware
import logging

import boto3
from botocore.config import Config
from scrapy.http import Request

# import os


logger = logging.getLogger(__name__)


class AmazonStartUrlsMiddleware:
    # pylint: disable=unused-argument
    def __init__(self):
        # Init DB
        self.dynamodb = boto3.resource(
            "dynamodb",
            region_name="eu-central-1",
            config=Config(retries={"max_attempts": 20, "mode": "adaptive"}),
        )

        self.start_urls_table = self.dynamodb.Table("emag-start_urls")

    def process_start_requests(self, start_requests, spider):
        # Statuses:
        # 0 - not crawled
        # 1 - crawled
        # response.status - error code

        # How many start_requests
        start_urls_pops = 4

        # proxy = {
        #     "proxy": f"http://scraperapi.autoparse=true:{os.getenv('SCRAPEAPI_KEY')}@proxy-server.scraperapi.com:8001"
        # }

        # Pop x entries from database and return their value
        for _ in range(start_urls_pops):
            get_url = self.start_urls_table.update_item(
                Key={"status_code": 0},
                ReturnValues="UPDATED_OLD",
                UpdateExpression="REMOVE crawled_urls[0]",
            )["Attributes"]["crawled_urls"][0]

            yield Request(url=get_url)

    def process_spider_exception(self, response, exception, spider):
        # XXX: Still testing
        logger.exception("Exception in spider %s on %s: %s", spider.name, response.url, response.status)

        # Add crawled_urls to database with status 2
        self.start_urls_table.put_item(
            Item={
                "status_code": response.status,
                "crawled_urls": [response.url],
            },
            ConditionExpression="attribute_not_exists(status_code) AND attribute_not_exists(crawled_urls)",
        )
