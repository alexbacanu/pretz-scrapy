from redis import Redis
from scrapy.extensions.httpcache import DummyPolicy


class ScrapeDoMiddleware:
    def __init__(self, scrapedo_key):
        self.scrapedo_key = scrapedo_key

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            scrapedo_key=crawler.settings.get("SCRAPEDO_KEY"),
        )

    def process_request(self, request, spider):
        # Set proxy
        request.meta["proxy"] = f"http://{self.scrapedo_key}:render=false@proxy.scrape.do:8080"
        return None


class FailedUrlsMiddleware:
    def __init__(self, redis_url):
        self.redis_url = redis_url
        self.r = Redis.from_url(self.redis_url, decode_responses=True)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            redis_url=crawler.settings.get("REDIS_URI"),
        )

    def process_response(self, request, response, spider):

        failed_url = response.url

        if response.url.split("/")[2] == "fenrir.altex.ro":
            failed_url = response.url.split("/", 5)[-1]

        if response.url.split("/")[2] == "www.emag.ro":
            failed_url = response.url.split("/", 4)[-1]

        # Called with the response returned from the downloader.
        if response.status not in range(200, 399):
            # Add failed urls
            self.r.sadd(f"{spider.name}:failed_urls", failed_url)

        return response


class EmagCookiesMiddleware:
    def process_request(self, request, spider):
        # Set cookies to display 100 items per page
        request.cookies["listingPerPage"] = 100
        return None


class CachePolicy(DummyPolicy):
    def should_cache_response(self, response, request):
        return response.status == 200
