from datetime import datetime

from pretz.helpers import cleanup, generate_stats, timeseries_to_arr, validator
from pymongo import ASCENDING, DESCENDING, TEXT, MongoClient, UpdateOne
from redis import Redis


class DefaultValuesPipeline:
    def process_item(self, item, spider):
        for field in item.fields:
            # Set default values to null for all fields
            item.setdefault(field, None)

        return item


class MongoPipeline:
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DB"),
        )

    def open_spider(self, spider):
        # Initialize MongoDB
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        collections = self.db.list_collection_names()

        if spider.database_name in collections:
            # Get a reference to the "products" collection
            self.products = self.db[spider.database_name]
        else:
            # Create the "products" collection if it does not exist
            self.db.create_collection(
                spider.database_name, validator=validator, validationAction="warn"
            )

            self.products = self.db[spider.database_name]

            self.products.create_index([("pName", TEXT)])
            self.products.create_index([("pID", ASCENDING)], sparse=True)
            self.products.create_index([("priceCurrent", ASCENDING)], sparse=True)
            self.products.create_index([("crawledAt", DESCENDING)], sparse=True)
            self.products.create_index([("stats.updatedAt", DESCENDING)], sparse=True)

        # Init an empty array for bulk operations
        self.product_requests = []
        # self.store_requests = []
        # self.prices_requests = []
        self.batch_size = 2 * 1000

    def close_spider(self, spider):
        # Commit bulk operations
        self.products.bulk_write(self.product_requests, ordered=True)

        # Clear array after commit
        self.product_requests.clear()

    def process_item(self, item, spider):
        # Get current time as "2022-09-07"
        # !This is not UTC
        date_time = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M")

        # Create a new dictionary
        product_dict = dict(item)

        # Define timeseries
        timeseries_all = {
            "pVendor": item.get("pVendor"),
            "priceDate": item.get("crawledAt"),
            "priceCurrent": item.get("priceCurrent"),
            "priceRetail": item.get("priceRetail"),
            "priceSlashed": item.get("priceSlashed"),
            "priceUsed": item.get("priceUsed"),
        }

        # Remove null values
        timeseries = {k: v for k, v in timeseries_all.items() if v is not None}

        self.product_requests.append(
            UpdateOne(
                {"pID": item.get("pID")},
                [
                    {
                        "$set": product_dict,
                    },
                    {
                        "$set": {f"timeseries.{date_time}": timeseries},
                    },
                    {
                        "$set": timeseries_to_arr,
                    },
                    {
                        "$set": generate_stats,
                    },
                    {
                        "$set": cleanup,
                    },
                ],
                upsert=True,
            ),
        )

        # Commit when reach batch size
        if (len(self.product_requests) % self.batch_size) == 0:
            self.products.bulk_write(self.product_requests, ordered=True)

            # Clear array after commit
            self.product_requests.clear()

        return item


class RedisPipeline:
    def __init__(self, redis_url):
        self.redis_url = redis_url

    @classmethod
    def from_crawler(cls, crawler):
        return cls(redis_url=crawler.settings.get("REDIS_URI"))

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

        self.pipe.sadd(f"{spider.name}:start_urls", item.get("response_category"))

        return item
