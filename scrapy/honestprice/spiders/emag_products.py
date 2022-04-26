from honestprice.items import EmagProductsItem
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
            # "honestprice.middlewares.AmazonDynamoDBPipeline": 200,
            # "honestprice.middlewares.AzureCosmosDBPipeline": 200,
            "honestprice.middlewares.GoogleFirestoreStartUrlsMiddleware": 200,
        },
        "ITEM_PIPELINES": {
            "honestprice.pipelines.DefaultValuesPipeline": 150,
            # "honestprice.pipelines.AmazonDynamoDBPipeline": 250,
            # "honestprice.pipelines.AzureCosmosDBPipeline": 250,
            "honestprice.pipelines.GoogleFirestoreProductsPipeline": 250,
        },
    }

    def parse_start_url(self, response):
        self.logger.info("Getting header from: %s", response.url)

        header = response.css("div.js-head-title")

        self.logger.info(
            "Category: %s",
            header.css("span.title-phrasing-xl::text").get(),
        )
        self.logger.info(
            "Items: %s",
            header.css("span.title-phrasing-sm::text").get(),
        )

        return Request(url=response.url, callback=self.parse_page, dont_filter=True)

    def parse_page(self, response):
        self.logger.info("Parsing page: %s", response.url)

        products = response.css("div.card-v2")

        for product in products:

            itemloader = ItemLoader(item=EmagProductsItem(), selector=product)

            itemloader.add_value("product_crawled", "")
            itemloader.add_css("product_name", ".card-v2-title")
            itemloader.add_css("product_id", "div.card-v2-atc::attr(data-pnk)")
            itemloader.add_css("product_link", "a.card-v2-thumb::attr(href)")
            itemloader.add_css("product_img", "img.w-100::attr(src)")
            itemloader.add_css("price_rrp", "span.rrp-lp30d-content:nth-child(1)")
            itemloader.add_css("price_old", "span.rrp-lp30d-content:nth-child(2)")
            itemloader.add_css("price_new", "p.product-new-price")

            yield itemloader.load_item()
