# Define your item pipelines here
# Don't forget to add your pipeline to the ITEM_PIPELINES setting

import boto3
from boto3.dynamodb.conditions import Key


class DefaultValuesPipeline(object):
    # pylint: disable=unused-argument
    def process_item(self, item, spider):
        # Make items have a default value (which is 0)
        for field in item.fields:
            item.setdefault(field, 0)

        return item


class AmazonDynamoDBItemsPipeline(object):
    # pylint: disable=unused-argument
    def __init__(self):
        # Init DB
        self.dynamodb = boto3.resource("dynamodb", region_name="eu-central-1")
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
                "date": item["crawled"],
                "rrp": item["rrp"],
                "full": item["full"],
                "price": item["price"],
            }
        )
        # Add values in a list for emag-products
        self.products_items.append(
            {
                "id": item["id"],
                "name": item["name"],
                "rrp": item["rrp"],
                "full": item["full"],
                "price": item["price"],
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
        self.dynamodb = boto3.resource("dynamodb", region_name="eu-central-1")
        self.start_urls_table = self.dynamodb.Table("emag-start_urls")
        self.start_urls_items = []

        self.response = self.start_urls_table.query(KeyConditionExpression=Key("status").eq(0))

    def close_spider(self, spider):
        # Write all items to emag-start_urls after spider is finished
        if self.response["Count"] == 0:
            with self.start_urls_table.batch_writer() as batch:
                batch.put_item(
                    Item={
                        "status": 0,
                        "crawled_urls": self.start_urls_items,
                    }
                )

    def process_item(self, item, spider):
        # Add values in a list for emag-start_urls
        self.start_urls_items.extend(
            {
                item["url"],
            }
        )
        return item
