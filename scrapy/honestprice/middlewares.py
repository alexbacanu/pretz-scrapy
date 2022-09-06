# Define here the models for your spider middleware
#
import logging
import os

from google.cloud import firestore
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.http import Request
from scrapy.spidermiddlewares.httperror import HttpError
from scrapy.utils.project import get_project_settings


class RetryHTTPErrors(RetryMiddleware):
    def process_response(self, request, response, spider):
        # test for captcha page
        if response.status == 511:
            spider.logger.error("511 error: %s", spider.name)
            logger = logging.getLogger()
            logger.error("511 Error")
            reason = "511 Error"
            return self._retry(request, reason, spider) or response
        return response


class HandleHTTPErrors(object):
    def process_spider_input(self, response, spider):
        if response.status == 511:
            logging.warning("511 Error", exc_info=True)
            raise HttpError(response, "511 Error")
        return None


class ScrapeAPIProxyMiddleware(object):
    @classmethod
    def process_request(self, request, spider):
        print(f"middlewares.py: Proxy ScrapeAPI on: {request.url}")
        request.meta[
            "proxy"
        ] = f"http://scraperapi.autoparse=true:{os.getenv('PROXY_SCRAPERAPI_KEY')}@proxy-server.scraperapi.com:8001"


class WebShareProxyMiddleware(object):
    def process_request(self, request, spider):
        print(f"middlewares.py: Proxy WebShare on: {request.url}")
        request.meta[
            "proxy"
        ] = f"http://{os.getenv('PROXY_WEBSHARE_USER')}:{os.getenv('PROXY_WEBSHARE_PASS')}@p.webshare.io:80/"


class EmagCookiesMiddleware(object):
    @classmethod
    def process_request(self, request, spider):
        request.cookies["listingPerPage"] = 100


class AmazonDynamoDBStartUrlsMiddleware:
    pass


class AzureCosmosDBStartUrlsMiddleware:
    pass


class GoogleFirestoreStartUrlsMiddleware:
    def __init__(self):
        # Initialize Firestore Client
        self.fdb = firestore.Client()
        self.batch = self.fdb.batch()

    def process_start_requests(self, start_requests, spider):
        # Get url count from settings
        url_count = get_project_settings().get("START_URLS_COUNT")

        # Reference to startUrls collection
        start_urls_ref = self.fdb.collection("startUrls").document("emgStart")

        # Retain only the first x(url_count) urls
        start_urls_list = start_urls_ref.get().to_dict()["response_url"][:url_count]

        for request in start_urls_list:
            # Delete the array from firestore
            # TODO: Temporary
            # self.batch.update(
            #     start_urls_ref, {"response_url": firestore.ArrayRemove([request])}
            # )
            yield Request(url=request)

        # Commit batch
        self.batch.commit()


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
