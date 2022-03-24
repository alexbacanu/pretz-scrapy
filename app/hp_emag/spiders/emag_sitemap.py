from bs4 import BeautifulSoup
from hp_emag.items import EmagSitemapItem
from scrapy import Spider


class EmagSitemapSpider(Spider):
    name = "emag_sitemap"
    allowed_domains = ["emag.ro"]
    # TODO: Get first index.xml and then 0.xml in case there are multiple files
    start_urls = ["https://www.emag.ro/sitemaps/categories-0.xml"]

    custom_settings = {
        "ITEM_PIPELINES": {
            "hp_emag.pipelines.AmazonDynamoDBSitemapPipeline": 250,
        },
    }

    def parse(self, response):
        # Find all objects in response text with <loc> tag
        soup = BeautifulSoup(response.text, "lxml")
        links = soup.find_all("loc")

        for link in links:
            # Declare items
            # Statuses
            # 0 - Unprocessed
            # 1 - Processing
            item = EmagSitemapItem()
            item["url"] = link.text
            item["status"] = 0

            yield item
