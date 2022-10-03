# Define here the models for your spider middleware
import os

import redis
from scrapy.http import Request


class FailedUrlsMiddleware(object):
    def __init__(self):
        self.r = redis.Redis.from_url(os.getenv("REDIS_URL"), decode_responses=True)

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.
        if response.status not in range(200, 399):
            # Key name seen in Redis
            spider_key = f"{spider.name}:failed_urls"

            # Add urls to Redis using sets (pipeline)
            self.r.sadd(spider_key, response.url)

        return response


class EmagCookiesMiddleware(object):
    @classmethod
    def process_request(self, request, spider):
        # Set cookies to display 100 items per page (for fewer requests)
        request.cookies["listingPerPage"] = 100


class ScrapeAPIProxyMiddleware(object):
    @classmethod
    def process_request(self, request, spider):
        # spider.logger.info(f"Proxy ScrapeAPI on: {request.url}")
        request.meta[
            "proxy"
        ] = f"http://scraperapi.autoparse=true:{os.getenv('PROXY_SCRAPERAPI_KEY')}@proxy-server.scraperapi.com:8001"


class ScrapeDoProxyMiddleware(object):
    @classmethod
    def process_request(self, request, spider):
        # spider.logger.info(f"Proxy ScrapeDo on: {request.url}")
        request.meta[
            "proxy"
        ] = f"http://{os.getenv('PROXY_SCRAPEDO_KEY')}:render=false@proxy.scrape.do:8080"


class WebShareProxyMiddleware(object):
    @classmethod
    def process_request(self, request, spider):
        # spider.logger.info(f"Proxy WebShare on: {request.url}")
        request.meta[
            "proxy"
        ] = f"http://{os.getenv('PROXY_WEBSHARE_USER')}:{os.getenv('PROXY_WEBSHARE_PASS')}@p.webshare.io:80/"


class StartUrlsMiddleware:
    def __init__(self):
        self.r = redis.Redis.from_url(os.getenv("REDIS_URL"), decode_responses=True)

    def process_start_requests(self, start_requests, spider):
        # Key name seen in Redis
        url_key = "emag_sitemap:start_urls"

        # Remove entry(ies - watch count) from Redis and get their value
        start_requests = self.r.spop(url_key, count=1)
        for request in start_requests:
            yield Request(url=request)


# class RetryHTTPErrors(RetryMiddleware):
#     def process_response(self, request, response, spider):
#         if response.status == 511:
#             spider.logger.info(f"Retrying with ScrapeAPI on: {request.url}")

#             reason = "511 error"
#             spider.logger.error("511 error")

#             return self._retry(request, reason, spider) or response
#         return response


# class ProxyPageProxyMiddleware(object):
#     @classmethod
#     def process_request(self, request, spider):
#         spider.logger.info(f"Proxy ProxyPage on: {request.url}")
#         request.meta[
#             "proxy"
#         ] = f"https://api.proxypage.io/v1/tier2random?type=HTTP&latency=1000&ssl=True"
#         request.headers["api_key"] = os.getenv("PROXY_PROXYPAGE_KEY")
#         request.headers["Content-Type"] = "application/x-www-form-urlencoded"


# class ProxiesAPIProxyMiddleware(object):
#     @classmethod
#     def process_request(self, request, spider):
#         spider.logger.info(f"Proxy ProxiesAPI on: {request.url}")
#         request.meta[
#             "proxy"
#         ] = f"http://api.proxiesapi.com/?auth_key={os.getenv('PROXY_PROXIESAPI_KEY')}"


# class HonestpriceSpiderMiddleware:
#     # Not all methods need to be defined. If a method is not defined,
#     # scrapy acts as if the spider middleware does not modify the
#     # passed objects.

#     @classmethod
#     def from_crawler(cls, crawler):
#         # This method is used by Scrapy to create your spiders.
#         s = cls()
#         crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#         return s

#     def process_spider_input(self, response, spider):
#         # Called for each response that goes through the spider
#         # middleware and into the spider.

#         # Should return None or raise an exception.
#         return None

#     def process_spider_output(self, response, result, spider):
#         # Called with the results returned from the Spider, after
#         # it has processed the response.

#         # Must return an iterable of Request, or item objects.
#         for i in result:
#             yield i

#     def process_spider_exception(self, response, exception, spider):
#         # Called when a spider or process_spider_input() method
#         # (from other spider middleware) raises an exception.

#         # Should return either None or an iterable of Request or item objects.
#         pass

#     def process_start_requests(self, start_requests, spider):
#         # Called with the start requests of the spider, and works
#         # similarly to the process_spider_output() method, except
#         # that it doesn’t have a response associated.

#         # Must return only requests (not items).
#         for r in start_requests:
#             yield r

#     def spider_opened(self, spider):
#         spider.logger.info("Spider opened: %s" % spider.name)


# class HonestpriceDownloaderMiddleware:
#     # Not all methods need to be defined. If a method is not defined,
#     # scrapy acts as if the downloader middleware does not modify the
#     # passed objects.

#     @classmethod
#     def from_crawler(cls, crawler):
#         # This method is used by Scrapy to create your spiders.
#         s = cls()
#         crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#         return s

#     def process_request(self, request, spider):
#         # Called for each request that goes through the downloader
#         # middleware.

#         # Must either:
#         # - return None: continue processing this request
#         # - or return a Response object
#         # - or return a Request object
#         # - or raise IgnoreRequest: process_exception() methods of
#         #   installed downloader middleware will be called
#         return None

#     def process_response(self, request, response, spider):
#         # Called with the response returned from the downloader.

#         # Must either;
#         # - return a Response object
#         # - return a Request object
#         # - or raise IgnoreRequest
#         return response

#     def process_exception(self, request, exception, spider):
#         # Called when a download handler or a process_request()
#         # (from other downloader middleware) raises an exception.

#         # Must either:
#         # - return None: continue processing this exception
#         # - return a Response object: stops process_exception() chain
#         # - return a Request object: stops process_exception() chain
#         pass

#     def spider_opened(self, spider):
#         spider.logger.info("Spider opened: %s" % spider.name)
