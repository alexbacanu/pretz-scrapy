from datetime import datetime

from pymongo import MongoClient, UpdateOne
from redis import Redis


# emag_products uses this
class DefaultValuesPipeline:
    def process_item(self, item, spider):
        for field in item.fields:
            # Set default values to null for all fields
            item.setdefault(field, None)

            # Set default values to 0 for these fields
            item.setdefault("pStars", 0)
            item.setdefault("pReviews", 0)
        return item


# emag_products uses this
class MongoPipeline:
    def __init__(self, mongo_uri, mongo_db, mongo_coll):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_coll = mongo_coll

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DB"),
            mongo_coll=crawler.settings.get("MONGO_COLL"),
        )

    def open_spider(self, spider):
        # Initialize MongoDB
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.coll = self.db[self.mongo_coll]

        # Schema validation
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

        # Validate or create collection
        try:
            self.db.validate_collection(self.mongo_coll)["valid"]
        except:
            self.db.create_collection(self.mongo_coll, validator=validator)

        # Init an empty array for bulk operations
        self.requests = []
        self.batch_size = 2 * 1000

    def close_spider(self, spider):
        # Commit bulk operations
        self.coll.bulk_write(self.requests, ordered=True)

        # Clear array after commit
        self.requests.clear()

    def process_item(self, item, spider):
        # Get current time as "2022-09-07"
        date_time = datetime.now().astimezone().strftime("%Y-%m-%d")

        # Create a new dictionary
        product_dict = dict(item)

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
            UpdateOne(
                {"pID": item["pID"]},
                [
                    {"$set": product_dict},
                    {"$set": {f"timeseries.{date_time}": timeseries}},
                ],
                upsert=True,
            ),
        )

        # Commit when reach batch size
        if (len(self.requests) % self.batch_size) == 0:
            self.coll.bulk_write(self.requests, ordered=True)

            # Clear array after commit
            self.requests.clear()

        return item


# emag_sitemap uses this
class RedisPipeline:
    def __init__(self, redis_url, spider_key):
        self.redis_url = redis_url
        self.spider_key = spider_key

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            redis_url=crawler.settings.get("REDIS_URI"),
            spider_key=crawler.settings.get("REDIS_START_URLS"),
        )

    def open_spider(self, spider):
        # Initialize Redis
        self.r = Redis.from_url(self.redis_url, decode_responses=True)

        # Set up pipeline for bulk operations
        self.pipe = self.r.pipeline()

    def close_spider(self, spider):
        # Commit pipeline
        self.pipe.execute()

    def process_item(self, item, spider):
        # Format url to be compatible with Scrapy-Redis
        # url = {"url": item["response_url"]}

        self.pipe.sadd(self.spider_key, item["response_url"])

        return item
