from hp_emag.items import EmagProductsItem
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Request, Rule


class EmagProductsSpider(CrawlSpider):
    # pylint: disable=abstract-method
    name = "emag_products"
    allowed_domains = ["emag.ro"]

    rules = (
        Rule(
            LinkExtractor(allow=(r"/c$"), restrict_css=("a.js-change-page")),
            callback="parse_page",
            follow=True,
        ),
    )

    custom_settings = {
        "SPIDER_MIDDLEWARES": {
            "hp_emag.middlewares.AmazonStartUrlsMiddleware": 905,
        },
        "ITEM_PIPELINES": {
            "hp_emag.pipelines.DefaultValuesPipeline": 300,
            "hp_emag.pipelines.AmazonDynamoDBItemsPipeline": 305,
        },
    }

    def parse_start_url(self, response):
        self.logger.info("Getting header from: %s", response.url)

        header = response.css("div.js-head-title")

        self.logger.info("Category: %s", header.css("span.title-phrasing-xl::text").get())
        self.logger.info("Items: %s", header.css("span.title-phrasing-sm::text").get())

        return Request(url=response.url, callback=self.parse_page, dont_filter=True)

    def parse_page(self, response):
        self.logger.info("Parsing page: %s", response.url)

        products = response.css("div.card-v2")

        for product in products:

            itemloader = ItemLoader(item=EmagProductsItem(), selector=product)

            itemloader.add_css("name", ".card-v2-title")
            itemloader.add_css("id", "div.card-v2-atc::attr(data-pnk)")
            itemloader.add_css("price_rrp", "span.rrp-lp30d-content:nth-child(1)")
            itemloader.add_css("price_full", "span.rrp-lp30d-content:nth-child(2)")
            itemloader.add_css("price_std", "p.product-new-price")
            itemloader.add_css("link", "a.card-v2-thumb::attr(href)")
            itemloader.add_css("img", "img.w-100::attr(src)")
            itemloader.add_value("crawled", "")

            yield itemloader.load_item()
