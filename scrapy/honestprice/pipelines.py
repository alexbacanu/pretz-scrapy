# Define your item pipelines here
import logging
import os
from datetime import datetime

import redis
from constants import DEV_TAG, MONGODB_COLL, MONGODB_DB
from pymongo import MongoClient, UpdateOne
from pymongo.errors import BulkWriteError


class DefaultValuesPipeline(object):
    def process_item(self, item, spider):
        # Set default values to null for all fields
        for field in item.fields:
            item.setdefault(field, None)
            item.setdefault("pStars", 0)
            item.setdefault("pReviews", 0)
        return item


class RedisSitemapPipeline(object):
    def __init__(self):
        # Initialize Redis
        r = redis.Redis.from_url(os.getenv("REDIS_URL"), decode_responses=True)

        # Set up pipeline for bulk operations
        self.pipe = r.pipeline()

    def process_item(self, item, spider):
        # Key name seen in Redis
        spider_key = f"{spider.name}{DEV_TAG}:start_urls"

        # Add urls to Redis using sets (pipeline)
        self.pipe.sadd(spider_key, item["response_url"])

        return item

    def close_spider(self, spider):
        # Commit pipeline
        try:
            self.pipe.execute()
        except redis.ResponseError as ex:
            logging.error(ex)


class MongoDBProductsPipeline(object):
    def __init__(self):
        # Initialize MongoDB
        client = MongoClient(os.getenv("MONGODB_URI"))

        # Select database and collection
        db = client[MONGODB_DB]
        self.collection = db[MONGODB_COLL]

        # Init an empty array for bulk operations
        self.requests = []

    def process_item(self, item, spider):
        # Get current time as "2022-09-07"
        date_time = datetime.now().astimezone().strftime("%Y-%m-%d")

        # Create a new product dictionary
        product_dict = dict(item)

        # Product id
        product_id = item["pID"]

        # Define timeseries
        timeseries = {
            "priceDate": item["crawledAt"],
            "priceCurrent": item["priceCurrent"],
            "priceRetail": item["priceRetail"],
            "priceSlashed": item["priceSlashed"],
            "priceUsed": item["priceUsed"],
        }

        # Append an UpdateOne request to the array (item dictionary)
        self.requests.append(
            UpdateOne({"pid": product_id}, {"$set": product_dict}, upsert=True),
        )

        # Append an UpdateOne request to the array (update only timeseries inside item dictionary)
        self.requests.append(
            UpdateOne(
                {"pid": product_id},
                {"$set": {f"timeseries.{date_time}": timeseries}},
            ),
        )

        return item

    def close_spider(self, spider):
        try:
            self.collection.bulk_write(self.requests, ordered=True)
        except BulkWriteError as bwe:
            logging.error(bwe.details)


class HonestpricePipeline:
    def process_item(self, item, spider):
        return item
