import defusedxml.ElementTree as ET
from honestprice.items import EmagSitemapItem
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
            yield Request(child[0].text, self.parse)

    def parse(self, response):
        """Get all links from request that contains /vendor/emag/c and laptop"""
        print(f"emag_sitemap.py:    Crawling {response.url}")

        tree = ET.fromstring(response.text)

        for child in tree:
            if child[0].text.endswith("/vendor/emag/c"):  # TODO: temporary filter
                item = EmagSitemapItem()
                item["response_status"] = response.status
                item["response_category"] = child[0].text.split("/")[3]
                item["response_url"] = child[0].text

                yield item
