import defusedxml.ElementTree as ET
from pretz.items import GenericSitemapItem
from pretz.settings import DEV_TAG
from scrapy.spiders import Request, Spider


class EmagSitemapSpider(Spider):
    name = f"emag_sitemap{DEV_TAG}"
    allowed_domains = ["emag.ro"]
    start_urls = ["https://www.emag.ro/sitemaps/category-filters-index.xml"]

    custom_settings = {
        "ITEM_PIPELINES": {
            "pretz.pipelines.RedisPipeline": 650,
        },
    }

    def parse(self, response):
        self.logger.info(f"[Spider->Sitemap] Getting xml from {response.url}")

        tree = ET.fromstring(response.text)

        for child in tree:
            yield Request(url=child[0].text, callback=self.parse_item)

    def parse_item(self, response):
        self.logger.info(f"[Spider->Sitemap] Parsing xml from {response.url}")

        tree = ET.fromstring(response.text)

        for child in tree:
            if child[0].text.endswith("/vendor/emag/c"):
                item = GenericSitemapItem()
                item["response_status"] = response.status
                item["response_category"] = child[0].text.split("/", 3)[3]
                item["response_url"] = child[0].text
                yield item
