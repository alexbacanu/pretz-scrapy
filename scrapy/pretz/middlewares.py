import os

import redis
from scrapy.http import Request

from pretz.settings import DEV_TAG, REDIS_URL_COUNT, REDIS_URL_KEY


class StartUrlsMiddleware(object):
    def __init__(self):
        # Initialize Redis
        self.r = redis.Redis.from_url(os.getenv("REDIS_URL"), decode_responses=True)

    def process_start_requests(self, start_requests, spider):
        # Key name to fetch start urls
        url_key = REDIS_URL_KEY

        # Pop entry(ies) from Redis and get their value
        start_requests = self.r.spop(url_key, count=REDIS_URL_COUNT)
        for request in start_requests:
            yield Request(url=request)


class FailedUrlsMiddleware(object):
    def __init__(self):
        # Initialize Redis
        self.r = redis.Redis.from_url(os.getenv("REDIS_URL"), decode_responses=True)

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.
        if response.status not in range(200, 399):
            # Key name to store failed urls
            spider_key = f"{spider.name}{DEV_TAG}:failed_urls"

            # Add failed urls
            self.r.sadd(spider_key, response.url)

        return response


class ScrapeDoProxyMiddleware(object):
    @classmethod
    def process_request(self, request, spider):
        # Set proxy to ScrapeDo
        # spider.logger.info(f"Proxy ScrapeDo on: {request.url}")
        request.meta[
            "proxy"
        ] = f"http://{os.getenv('PROXY_SCRAPEDO_KEY')}:render=false@proxy.scrape.do:8080"


class EmagCookiesMiddleware(object):
    @classmethod
    def process_request(self, request, spider):
        # Set cookies to display 100 items per page (reduces requests)
        request.cookies["listingPerPage"] = 100
