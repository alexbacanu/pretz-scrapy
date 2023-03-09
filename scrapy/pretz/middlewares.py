from urllib.parse import urlparse

from redis import Redis
from scrapy.exceptions import NotConfigured
from scrapy.extensions.httpcache import DummyPolicy

# Add fallbacks?
# 'crawlbase', 'proxiesapi.com', 'scrape-it.cloud', 'scrape.do', 'scraperapi.com', 'scraperbox.com', 'scrapeup.com', 'scrapingant.com', 'scrapingbee.com', 'scrapingdog.com', 'webscraping.ai', 'wintr.com', 'zenrows.com', 'zenscrape.com', 'webshare.io'


class WebShareMiddleware:
    def __init__(self, webshare_user, webshare_pass):
        self.webshare_user = webshare_user
        self.webshare_pass = webshare_pass

    @classmethod
    def from_crawler(cls, crawler):
        try:
            webshare_user = crawler.settings.get("WEBSHARE_USER")
            webshare_pass = crawler.settings.get("WEBSHARE_PASS")
        except KeyError:
            raise NotConfigured("WEBSHARE_USER or WEBSHARE_PASS are not set!")
        return cls(webshare_user, webshare_pass)

    def process_request(self, request, spider):
        try:
            request.meta[
                "proxy"
            ] = f"http://{self.webshare_user}:{self.webshare_pass}@p.webshare.io:80/"
        except Exception as e:
            spider.logger.error(f"WebShareMiddleware failed: {e}")
            return None


# This will not be used anymore after 06/03/2023
# class ScrapeDoMiddleware:
#     def __init__(self, scrapedo_key):
#         self.scrapedo_key = scrapedo_key

#     @classmethod
#     def from_crawler(cls, crawler):
#         try:
#             scrapedo_key = crawler.settings.get("SCRAPEDO_API_KEY")
#         except KeyError:
#             raise NotConfigured("SCRAPEDO_API_KEY is not set!")
#         return cls(scrapedo_key)

#     def process_request(self, request, spider):
#         try:
#             request.meta[
#                 "proxy"
#             ] = f"http://{self.scrapedo_key}:render=false@proxy.scrape.do:8080"
#         except Exception as e:
#             spider.logger.error(f"ScrapeDoMiddleware failed: {e}")
#             return None


class FailedUrlsMiddleware:
    def __init__(self, redis_uri):
        self.redis_uri = redis_uri

    @classmethod
    def from_crawler(cls, crawler):
        try:
            redis_uri = crawler.settings.get("REDIS_URI")
        except KeyError:
            raise NotConfigured("REDIS_URI is not set!")
        return cls(redis_uri)

    def process_response(self, request, response, spider):
        try:
            r = Redis.from_url(self.redis_uri, decode_responses=True)

            netloc = urlparse(request.url).netloc
            failed_url = ""
            if netloc == "fenrir.altex.ro":
                failed_url = request.url.split("/", 5)[-1]
            if netloc == "www.emag.ro":
                failed_url = request.url.split("/", 4)[-1]

            r.sadd(f"{spider.name}:failed_urls", failed_url)
        except Exception as e:
            spider.logger.error(f"FailedUrlsMiddleware failed: {e}")
            return response
        return response


class CachePolicy(DummyPolicy):
    def should_cache_response(self, response, request):
        return response.status == 200
