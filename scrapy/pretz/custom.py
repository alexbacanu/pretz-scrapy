from collections.abc import Iterable
from time import time

from redis import Redis
from scrapy.exceptions import DontCloseSpider
from scrapy.http import FormRequest
from scrapy.spiders import CrawlSpider, Spider

from scrapy import signals


# A ultra minimal implementation of Scrapy-Redis
class RedisMixin(object):
    # Crawler
    crawler = None

    # Idle times
    idle_start_time = int(time())
    max_idle_time = None

    # Redis client
    r = None
    sitemap_name = None
    api_website = None
    redis_url = None
    redis_key = None
    redis_batch_size = None

    def setup_redis(self, crawler):
        # Do this once
        if self.r is not None:
            return

        # Get crawler attr
        if crawler is None:
            crawler = getattr(self, "crawler")
        if crawler is None:
            raise ValueError("Crawler is required")

        # Get REDIS_URI
        self.redis_url = crawler.settings.get("REDIS_URI")
        if self.redis_url is None:
            raise ValueError("REDIS_URI settings is required")

        # Get spider name
        self.redis_key = f"{self.sitemap_name}:start_urls"
        if self.redis_key is None:
            raise ValueError("Spider name is missing")

        # Get api website name
        self.api_website = self.api_website
        if self.api_website is None:
            raise ValueError("api_website from spider is missing")

        # Get CONCURRENT_REQUESTS
        self.redis_batch_size = crawler.settings.get("CONCURRENT_REQUESTS")
        if self.redis_batch_size is None:
            raise ValueError("CONCURRENT_REQUESTS settings is required")

        # Get MAX_IDLE_TIME
        self.idle_max_time = crawler.settings.get("MAX_IDLE_TIME")
        if self.idle_max_time is None:
            raise ValueError("MAX_IDLE_TIME settings is required")

        # Initialize Redis
        self.r = Redis.from_url(self.redis_url, decode_responses=True)

        # spider_idle method called when spider has no requests left
        crawler.signals.connect(self.spider_idle, signal=signals.spider_idle)
        crawler.signals.connect(
            self.response_received, signal=signals.response_received
        )

    def start_requests(self):
        return self.next_requests()

    def next_requests(self):
        if self.r is None:
            raise ValueError("Redis connection settings are required")

        if self.redis_key is None:
            raise ValueError("Spider name is missing")

        requests_found = 0
        requests = self.r.spop(self.redis_key, self.redis_batch_size)

        if requests is not None and isinstance(requests, Iterable):
            for request in requests:
                if isinstance(request, str) and "http://" in request:
                    yield FormRequest(request, dont_filter=True)
                    requests_found += 1
                else:
                    yield FormRequest(
                        f"{self.api_website}{request}",
                        dont_filter=True,
                    )
                    requests_found += 1

        if requests_found:
            self.logger.info(f"Read {requests_found} requests from '{self.redis_key}'")  # type: ignore

    def schedule_next_requests(self):
        if self.crawler is None:
            raise ValueError("Crawler is required")

        for req in self.next_requests():
            self.crawler.engine.crawl(req)

    def spider_idle(self):
        if self.redis_key is None:
            raise ValueError("Spider name is missing")

        self.schedule_next_requests()

        # Refresh on count how many items left
        if self.r is not None and self.r.scard(self.redis_key) > 0:
            self.idle_start_time = int(time())

        self.idle_duration = int(time()) - self.idle_start_time

        if self.idle_max_time != 0 and self.idle_duration >= self.idle_max_time:
            self.logger.info(  # type: ignore
                f"No more requests found, closing spider after {self.idle_duration}s of inactivity"
            )
            return

        raise DontCloseSpider

    def response_received(self):
        self.idle_start_time = int(time())


class SimpleRedisSpider(RedisMixin, Spider):
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        obj = super(SimpleRedisSpider, cls).from_crawler(crawler, *args, **kwargs)
        obj.setup_redis(crawler)
        return obj


class SimpleRedisCrawlSpider(RedisMixin, CrawlSpider):
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        obj = super(SimpleRedisCrawlSpider, cls).from_crawler(crawler, *args, **kwargs)
        # TypeError, something to do with MRO
        obj.setup_redis(crawler)  # type: ignore
        return obj
