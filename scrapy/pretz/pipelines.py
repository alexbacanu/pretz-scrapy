# Define your item pipelines here
import json
import os
import time
from datetime import datetime

import redis
from pymongo import MongoClient, UpdateOne

from pretz.settings import DEV_TAG, MONGODB_COLL, MONGODB_DB


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

        # Format url to be compatible with Scrapy-Redis
        url = {"url": item["response_url"]}

        # Add urls to Redis using sets (pipeline)
        self.pipe.lpush(spider_key, json.dumps(url))

        return item

    def close_spider(self, spider):
        # Commit pipeline
        self.pipe.delete(f"emag_products{DEV_TAG}:dupefilter")
        self.pipe.execute()


class MongoDBProductsPipeline(object):
    def __init__(self):
        # Initialize MongoDB
        client = MongoClient(os.getenv("MONGODB_URI"))

        validator = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["pID", "pName"],
                "properties": {
                    "pID": {
                        "bsonType": "string",
                        "description": "Product ID - Required.",
                        "uniqueItems": True,
                    },
                    "pStore": {
                        "bsonType": "string",
                        "description": "Product Store - Optional.",
                    },
                    "pName": {
                        "bsonType": "string",
                        "description": "Product Name - Required.",
                    },
                    "pLink": {
                        "bsonType": "string",
                        "description": "Product Link - Optional.",
                    },
                    "pImg": {
                        "bsonType": ["string", "null"],
                        "description": "Product Image - Optional.",
                    },
                    "pCategory": {
                        "bsonType": "string",
                        "description": "Product Category - Optional.",
                    },
                    "pReviews": {
                        "bsonType": ["number", "null"],
                        "description": "Product Reviews - Optional.",
                    },
                    "pStars": {
                        "bsonType": ["number", "null"],
                        "description": "Product Stars - Optional.",
                    },
                    "pGeniusTag": {
                        "bsonType": ["bool", "null"],
                        "description": "Product Genius Tag - Optional.",
                    },
                    "pUsedTag": {
                        "bsonType": ["bool", "null"],
                        "description": "Product Used Tag - Optional.",
                    },
                    "priceCurrent": {
                        "bsonType": ["number", "null"],
                        "description": "Price Current - Optional.",
                    },
                    "priceRetail": {
                        "bsonType": ["number", "null"],
                        "description": "Price Retail - Optional.",
                    },
                    "priceSlashed": {
                        "bsonType": ["number", "null"],
                        "description": "Price Slashed - Optional.",
                    },
                    "priceUsed": {
                        "bsonType": ["number", "null"],
                        "description": "Price Used - Optional.",
                    },
                    "crawledAt": {
                        "bsonType": "date",
                        "description": "Crawled At - Optional.",
                    },
                    "timeseries": {
                        "bsonType": "object",
                        "description": "Product Timeseries - Optional.",
                        "properties": {
                            "priceDate": {
                                "bsonType": "date",
                                "description": "Price Date - Optional.",
                            },
                            "priceCurrent": {
                                "bsonType": ["number", "null"],
                                "description": "Price Current - Optional.",
                            },
                            "priceRetail": {
                                "bsonType": ["number", "null"],
                                "description": "Price Retail - Optional.",
                            },
                            "priceSlashed": {
                                "bsonType": ["number", "null"],
                                "description": "Price Slashed - Optional.",
                            },
                            "priceUsed": {
                                "bsonType": ["number", "null"],
                                "description": "Price Used - Optional.",
                            },
                        },
                    },
                },
            }
        }

        # Select database and collection
        db = client[MONGODB_DB]
        self.collection = db[MONGODB_COLL]

        try:
            db.validate_collection(MONGODB_COLL)["valid"]
        except:
            print("Creating collection using schema validation")
            db.create_collection(MONGODB_COLL, validator=validator)

        # Init an empty array for bulk operations
        self.requests = []
        self.batch_size = 2 * 1000
        self.start = time.time()

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
            UpdateOne({"pID": product_id}, {"$set": product_dict}, upsert=True),
        )

        # Append an UpdateOne request to the array (update only timeseries inside item dictionary)
        self.requests.append(
            UpdateOne(
                {"pID": product_id},
                {"$set": {f"timeseries.{date_time}": timeseries}},
            ),
        )

        if (len(self.requests) % self.batch_size) == 0:
            self.collection.bulk_write(self.requests, ordered=True)
            print(f"Inserted {len(self.requests)} items")
            self.requests.clear()

        return item

    def close_spider(self, spider):
        self.collection.bulk_write(self.requests, ordered=True)
        print(f"Inserted {len(self.requests)} items")
        self.requests.clear()
        self.end = time.time()
        print(f"{self.end - self.start}s elapsed")


class PretzPipeline:
    def process_item(self, item, spider):
        return item
