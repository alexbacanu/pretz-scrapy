from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from hp_emag.items import EmagProductsItem
from scrapy.loader import ItemLoader


class EmagProductsSpider(CrawlSpider):
    name = "emag_products"
    allowed_domains = ["emag.ro"]
    start_urls = []

    rules = (
        Rule(
            LinkExtractor(allow=(r"/c$"), restrict_css=("a.js-change-page")),
            callback="parse_start_url",
            follow=True,
        ),
    )

    def parse_start_url(self, response):
        self.logger.info("Visited %s", response.url)
        products = response.css("div.card-v2")

        for product in products:
            itemloader = ItemLoader(item=EmagProductsItem(), selector=product)

            # Product selectors
            itemloader.add_css("name", "a.card-v2-title::text")
            itemloader.add_css("id", "div.card-v2-atc::attr(data-pnk)")
            itemloader.add_css("rrp", "span.rrp-lp30d-content:nth-child(1)")
            itemloader.add_css("full", "span.rrp-lp30d-content:nth-child(2)")
            itemloader.add_css("price", "p.product-new-price")

            itemloader.add_css("link", "a.card-v2-thumb::attr(href)")
            itemloader.add_css("img", "img.w-100::attr(src)")

            itemloader.add_value("crawled", "")

            yield itemloader.load_item()

    # TODO: Try to fix this
    # def parse_title(self, response):
    #     self.logger.info("Visited %s", response.url)
    #     self.logger.info("Category %s", response.css("span.title-phrasing-xl::text"))
    #     self.logger.info("Items %s", response.css("span.title-phrasing-sm::text"))