import defusedxml.ElementTree as ET
from pretz.items import GenericSitemapItem
from pretz.settings import DEV_TAG
from scrapy.spiders import Spider


class AltexSitemapSpider(Spider):
    name = f"altex_sitemap{DEV_TAG}"
    allowed_domains = ["altex.ro"]
    start_urls = ["https://altex.ro/sitemaps/categories/categories_altex.xml"]

    custom_settings = {
        "ITEM_PIPELINES": {
            "pretz.pipelines.RedisPipeline": 650,
        },
    }

    def parse(self, response):
        self.logger.info(f"[Spider->Sitemap] Parsing xml from {response.url}")

        tree = ET.fromstring(response.text)

        for child in tree:
            if child[0].text.endswith("/cpl/") and child[3].text != "0.4":

                item = GenericSitemapItem()
                item["response_status"] = response.status
                item["response_category"] = child[0].text.split("/")[3]
                item["response_url"] = child[0].text

                yield item
