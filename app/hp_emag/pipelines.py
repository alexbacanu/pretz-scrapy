# Define your item pipelines here
# Don't forget to add your pipeline to the ITEM_PIPELINES setting

import os

import redis
from redis.commands.json.path import Path


class DefaultValuesPipeline(object):
    def process_item(self, item, spider):
        # Make items have a default value (which is 0)
        for field in item.fields:
            item.setdefault(field, 0)

        return item


class RedisPipelineProductsTS(object):
    def open_spider(self, spider):
        self.r = redis.Redis.from_url(os.environ.get("RURL_GO_FREE"), decode_responses=True)
        self.pipe = self.r.pipeline()

    def close_spider(self, spider):
        self.pipe.execute()

    def process_item(self, item, spider):
        # List of item ids to be iterated
        prices = ["rrp", "full", "price"]

        # Add prices to Redis using Timeseries (pipeline)
        for price in prices:
            key_id = f'ts_{price}:{item["id"]}'

            # try:
            #     get_last_price = self.r.ts().get(key_id)[1]
            # except redis.exceptions.ResponseError:
            #     print("Key does not exist")

            # if get_last_price != item[price]:
            #     # id, timestamp, value, chunk_size
            self.pipe.ts().add(key_id, item["crawled"], item[price], chunk_size=128)

        return item


class RedisPipelineProductsJSON(object):
    def open_spider(self, spider):
        self.r = redis.Redis.from_url(os.environ.get("RURL_GH_FREE"), decode_responses=True)
        self.pipe = self.r.pipeline()

    def close_spider(self, spider):
        self.pipe.execute()

    def process_item(self, item, spider):
        # Add scraped items to Redis using JSON (pipeline)
        product = {}

        for k, v in item.items():
            product[k] = v if v is not None else ""

        self.pipe.json().set(f'json:{item["id"]}', Path.rootPath(), product)

        return item


class RedisPipelineSitemap(object):
    def open_spider(self, spider):
        self.r = redis.Redis.from_url(os.environ.get("RURL_GH_FREE"), decode_responses=True)
        self.pipe = self.r.pipeline()

    def close_spider(self, spider):
        self.pipe.execute()

    def process_item(self, item, spider):
        # Key name seen in Redis
        spider_key = f"{spider.name}:start_urls"

        # Add urls to Redis using sets (pipeline)
        self.pipe.sadd(spider_key, item["url"])

        return item
