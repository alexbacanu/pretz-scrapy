import defusedxml.ElementTree as ET
from constants import EMAG_SPIDER_SITEMAP
from honestprice.items import EmagSitemapItem
from scrapy.spiders import CrawlSpider, Request


class EmagSitemapSpider(CrawlSpider):
    name = EMAG_SPIDER_SITEMAP
    allowed_domains = ["emag.ro"]
    start_urls = ["https://www.emag.ro/sitemaps/category-filters-index.xml"]

    custom_settings = {
        "ITEM_PIPELINES": {
            "honestprice.pipelines.RedisSitemapPipeline": 650,
        },
        "SPIDERMON_ENABLED": False,
    }

    def parse_start_url(self, response):
        self.logger.info("─" * 82)
        self.logger.info(f"[Spider->Sitemap] Getting xml from {response.url}")

        tree = ET.fromstring(response.text)

        for child in tree:
            yield Request(url=child[0].text, callback=self.parse)

    def parse(self, response):
        self.logger.info(f"[Spider->Sitemap] Parsing xml from {response.url}")

        tree = ET.fromstring(response.text)

        for child in tree:
            if child[0].text.endswith("/vendor/emag/c"):  # TODO: Temp
                # if "telefoane-mobile" in child[0].text:  # TODO: Temp
                item = EmagSitemapItem()
                item["response_status"] = response.status
                item["response_category"] = child[0].text.split("/")[3]
                item["response_url"] = child[0].text

                yield item
