import defusedxml.ElementTree as ET
from honestprice.items import EmagSitemapItem
from scrapy.spidermiddlewares.httperror import HttpError
from scrapy.spiders import CrawlSpider, Request


class EmagSitemapSpider(CrawlSpider):
    name = "emag_sitemap"
    for_spider = "emag_products"
    allowed_domains = ["emag.ro"]
    start_urls = ["https://www.emag.ro/sitemaps/category-filters-index.xml"]

    custom_settings = {
        "ITEM_PIPELINES": {
            "honestprice.pipelines.GoogleTasksPipeline": 650,
            # "honestprice.pipelines.GoogleFirestoreSitemapPipeline": 250,
        },
    }

    def parse_start_url(self, response):
        """Get all sitemaps in first crawl and yield request for each one"""

        tree = ET.fromstring(response.text)

        for child in tree:
            yield Request(
                url=child[0].text, callback=self.parse, errback=self.error_function
            )

    def parse(self, response):
        """Get all links from request that contains /vendor/emag/c and laptop"""
        print(f"emag_sitemap.py:    Crawling {response.url}")

        tree = ET.fromstring(response.text)

        for child in tree:
            if child[0].text.endswith("/vendor/emag/c"):  # TODO: Temp
                if "laptopuri" in child[0].text:  # TODO: Temp
                    item = EmagSitemapItem()
                    item["response_status"] = response.status
                    item["response_category"] = child[0].text.split("/")[3]
                    item["response_url"] = child[0].text

                    yield item

    def error_function(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error("HttpError on %s", response.url)
