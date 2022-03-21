# Define here the models for your spider middleware
import os

import redis
from scrapy.http import Request


class StartUrlsMiddleware:
    def __init__(self):
        self.r = redis.Redis.from_url(os.environ.get("RURL_GH_FREE"), decode_responses=True)

    def process_start_requests(self, start_requests, spider):
        # Key name seen in Redis
        url_key = "emag_sitemap:start_urls"

        # meta = {"proxy": config("SCRAPEAPI_URL")}
        meta = {}

        # Remove entry(ies - watch count) from Redis and get their value
        start_requests = self.r.spop(url_key, count=1)

        for request in start_requests:
            # Add vendor/emag/ in url
            split_request = request.rsplit("/", 1)
            request = f"{split_request[0]}/vendor/emag/c"

            yield Request(url=request, meta=meta)
