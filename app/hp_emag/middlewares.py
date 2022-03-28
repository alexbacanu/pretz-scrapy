# Define here the models for your spider middleware
import logging
import os

import boto3
from scrapy.http import Request

logger = logging.getLogger(__name__)


class AmazonStartUrlsMiddleware:
    # pylint: disable=unused-argument
    def __init__(self):
        # Init DB
        self.dynamodb = boto3.resource("dynamodb", region_name="eu-central-1")
        self.start_urls_table = self.dynamodb.Table("emag-start_urls")

    def process_start_requests(self, start_requests, spider):
        # How many start_requests
        start_urls_pops = 4

        # proxy = {
        #     "proxy": f"http://scraperapi.autoparse=true:{os.getenv('SCRAPEAPI_KEY')}@proxy-server.scraperapi.com:8001"
        # }

        # Pop x entries from database and return their value
        for _ in range(start_urls_pops):
            get_url = self.start_urls_table.update_item(
                Key={"status": 0},
                ReturnValues="UPDATED_OLD",
                UpdateExpression="REMOVE crawled_urls[0]",
            )["Attributes"]["crawled_urls"][0]

            split_request = get_url.rsplit("/", 1)
            request = f"{split_request[0]}/vendor/emag/c"

            yield Request(url=request)
