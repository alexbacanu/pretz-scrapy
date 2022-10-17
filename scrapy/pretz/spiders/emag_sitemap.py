import defusedxml.ElementTree as ET
from pretz.items import EmagSitemapItem
from pretz.settings import SPIDER_DOMAINS, SPIDER_SITEMAP, SPIDER_START_URLS
from scrapy.spiders import CrawlSpider, Request


class EmagSitemapSpider(CrawlSpider):
    name = SPIDER_SITEMAP
    allowed_domains = [SPIDER_DOMAINS]
    start_urls = [SPIDER_START_URLS]

    custom_settings = {
        "ITEM_PIPELINES": {
            "pretz.pipelines.RedisSitemapPipeline": 650,
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
