import defusedxml.ElementTree as ET
from pretz.items import EmagSitemapItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Request, Rule


class EmagSitemapSpider(CrawlSpider):
    name = "emag_sitemap"
    allowed_domains = ["emag.ro"]
    start_urls = ["https://www.emag.ro/sitemaps/category-filters-index.xml"]

    rules = (Rule(LinkExtractor(), callback="parse_item", follow=True),)

    custom_settings = {
        "ITEM_PIPELINES": {
            "pretz.pipelines.RedisPipeline": 650,
        },
    }

    def parse_start_url(self, response):
        self.logger.info(f"[Spider->Sitemap] Getting xml from {response.url}")

        tree = ET.fromstring(response.text)

        for child in tree:
            yield Request(url=child[0].text, callback=self.parse_item)

    def parse_item(self, response):
        self.logger.info(f"[Spider->Sitemap] Parsing xml from {response.url}")

        tree = ET.fromstring(response.text)

        for child in tree:
            if child[0].text.endswith("/vendor/emag/c"):
                item = EmagSitemapItem()
                item["response_status"] = response.status
                item["response_category"] = child[0].text.split("/")[3]
                item["response_url"] = child[0].text

                yield item
