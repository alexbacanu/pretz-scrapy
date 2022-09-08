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
        },
    }

    def parse_start_url(self, response):
        self.logger.info(f"Getting xml from {response.url}")

        tree = ET.fromstring(response.text)

        for child in tree:
            yield Request(url=child[0].text, callback=self.parse)

    def parse(self, response):
        self.logger.info(f"Parsing xml from {response.url}")

        tree = ET.fromstring(response.text)

        for child in tree:
            if child[0].text.endswith("/vendor/emag/c"):  # TODO: Temp
                if "telefoane-mobile" in child[0].text:  # TODO: Temp
                    item = EmagSitemapItem()
                    item["response_status"] = response.status
                    item["response_category"] = child[0].text.split("/")[3]
                    item["response_url"] = child[0].text

                    yield item
