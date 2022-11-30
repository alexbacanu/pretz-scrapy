from datetime import datetime

from pretz.helpers import cleanup, generate_stats, timeseries_array, validator
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
        self.coll = self.db[spider.database_name]

        # Validate or create collection
        try:
            # Check for DB/Collection
            self.db.validate_collection(spider.database_name)["valid"]
        except:
            # Create DB/Collection
            self.db.create_collection(spider.database_name, validator=validator)

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

        # Append an UpdateOne request to the array (item dictionary)
        self.requests.append(
            UpdateOne(
                {"pID": item.get("pID")},
                [
                    {"$set": product_dict},
                    {
                        "$set": {f"timeseries.{date_time}": timeseries},
                    },
                    timeseries_array,
                    generate_stats,
                    cleanup,
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
