from redis import Redis


# emag_products uses this
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


# emag_products uses this
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
        # Called with the response returned from the downloader.
        if response.status not in range(200, 399):
            # Add failed urls
            self.r.sadd(f"{spider.name}:failed_urls", response.url)

        return response


# emag_products uses this
class EmagCookiesMiddleware:
    def process_request(self, request, spider):
        # Set cookies to display 100 items per page
        request.cookies["listingPerPage"] = 100
        return None
