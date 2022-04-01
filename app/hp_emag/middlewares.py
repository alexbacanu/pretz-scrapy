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

        self.su_table = self.dynamodb.Table("emag-start_urls")

    def process_start_requests(self, start_requests, spider):
        # Statuses:
        # not crawled:  0
        # error code:   response.status

        # How many start_requests
        start_urls_pops = 4

        # Pop x entries from database and return their value
        for _ in range(start_urls_pops):
            get_url = self.su_table.update_item(
                Key={
                    "status_code": 0,
                },
                UpdateExpression="REMOVE crawled_urls[0]",
                ReturnValues="UPDATED_OLD",
            )["Attributes"]["crawled_urls"][0]

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
            ExpressionAttributes={
                "#cu": "crawled_urls",
            },
            ExpressionAttributeValues={
                ":el": [],
                ":cu": [response.url],
            },
        )


class AzureStartUrlsMiddleware:
    pass
