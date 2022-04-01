# Define your item pipelines here
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
import logging

import boto3
from boto3.dynamodb.conditions import Key
from botocore.config import Config

logger = logging.getLogger(__name__)


class DefaultValuesPipeline(object):
    # pylint: disable=unused-argument
    def process_item(self, item, spider):
        # Make items have a default value (which is 0)
        for field in item.fields:
            item.setdefault(field, 0)

        return item


class DynamoDBPipeline:
    # TODO: Write as a single pipeline for both spiders
    # https://github.com/Thormod/scrapy-demo/blob/c0fcd7004496acd320d7f28c64b7d85e5cb0adfe/scrapyTutorial/pipelines.py

    pass


class AmazonDynamoDBItemsPipeline(object):
    # pylint: disable=unused-argument
    def __init__(self):
        # Init DB
        self.dynamodb = boto3.resource(
            "dynamodb",
            region_name="eu-central-1",
            config=Config(retries={"max_attempts": 20, "mode": "adaptive"}),
        )

        self.timeseries_table = self.dynamodb.Table("emag-timeseries")
        self.timeseries_items = []
        self.products_table = self.dynamodb.Table("emag-products")
        self.products_items = []

    def close_spider(self, spider):
        # Write all items to emag-timeseries after spider is finished
        with self.timeseries_table.batch_writer() as batch:
            for i, _ in enumerate(self.timeseries_items):
                batch.put_item(self.timeseries_items[i])

        # Write all items to emag-products after spider is finished
        with self.products_table.batch_writer() as batch:
            for i, _ in enumerate(self.products_items):
                batch.put_item(self.products_items[i])

    def process_item(self, item, spider):
        # Add values in a list for emag-timeseries
        self.timeseries_items.append(
            {
                "id": item["id"],
                "crawled": item["crawled"],
                "price_rrp": item["price_rrp"],
                "price_full": item["price_full"],
                "price_std": item["price_std"],
            }
        )
        # Add values in a list for emag-products
        self.products_items.append(
            {
                "id": item["id"],
                "name": item["name"],
                "price_rrp": item["price_rrp"],
                "price_full": item["price_full"],
                "price_std": item["price_std"],
                "link": item["link"],
                "img": item["img"],
                "crawled": item["crawled"],
            }
        )

        return item


class AmazonDynamoDBSitemapPipeline(object):
    # pylint: disable=unused-argument
    def __init__(self):
        # Init DB
        self.dynamodb = boto3.resource(
            "dynamodb",
            region_name="eu-central-1",
            config=Config(retries={"max_attempts": 20, "mode": "adaptive"}),
        )

        self.su_table = self.dynamodb.Table("emag-start_urls")
        self.su_query = self.su_table.query(KeyConditionExpression=Key("status_code").eq(0))[
            "Items"
        ][0]["crawled_urls"]

        self.start_urls_items = []

    def close_spider(self, spider):
        # Write all items to emag-start_urls after spider is finished
        if len(self.su_query) == 0:
            # with self.start_urls_table.batch_writer() as batch:
            self.su_table.put_item(
                Item={
                    "status_code": 0,
                    "crawled_urls": self.start_urls_items,
                }
            )

    def process_item(self, item, spider):
        # Add values in a list for emag-start_urls
        self.start_urls_items.extend(
            {
                item["crawled_urls"],
            }
        )
        return item


class AzureCosmosDBItemsPipeline(object):
    pass


class AzureCosmosDBSitemapPipeline(object):
    pass
