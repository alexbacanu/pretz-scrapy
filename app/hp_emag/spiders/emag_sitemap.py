from hp_emag.items import EmagSitemapItem
from bs4 import BeautifulSoup
from scrapy import Spider


class EmagSitemapSpider(Spider):
    name = "emag_sitemap"
    allowed_domains = ["emag.ro"]
    # TODO: Get first index.xml and then 0.xml in case there are multiple files
    start_urls = ["https://www.emag.ro/sitemaps/categories-0.xml"]

    custom_settings = {
        "SPIDER_MIDDLEWARES": {},
        "DOWNLOADER_MIDDLEWARES": {},
        "ITEM_PIPELINES": {
            "hp_emag.pipelines.RedisPipelineSitemap": 250,
        },
    }

    def parse(self, response):
        # Find all objects in response text with <loc> tag
        sp = BeautifulSoup(response.text, "lxml")
        links = sp.find_all("loc")

        for link in links:
            # Declare items
            item = EmagSitemapItem()
            item["url"] = link.text

            yield item
