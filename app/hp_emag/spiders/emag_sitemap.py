import defusedxml.ElementTree as ET
from hp_emag.items import EmagSitemapItem
from scrapy.spiders import CrawlSpider, Request


class EmagSitemapSpider(CrawlSpider):
    name = "emag_sitemap"
    allowed_domains = ["emag.ro"]
    start_urls = ["https://www.emag.ro/sitemaps/category-filters-index.xml"]

    custom_settings = {
        "ITEM_PIPELINES": {
            "hp_emag.pipelines.AmazonDynamoDBSitemapPipeline": 250,
        },
    }

    def parse_start_url(self, response):
        """Get all sitemaps in first crawl and yield request for each one"""
        tree = ET.fromstring(response.text)
        for child in tree:
            yield Request(child[0].text, self.parse)

    def parse(self, response):
        """Get all links from request that contains /vendor/emag/c"""
        tree = ET.fromstring(response.text)
        for child in tree:
            if child[0].text.endswith("/vendor/emag/c"):
                item = EmagSitemapItem()
                # status 0 = unprocessed, 1 = processing
                item["status_code"] = 0
                item["crawled_urls"] = child[0].text

                yield item
