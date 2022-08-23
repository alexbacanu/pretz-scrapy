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
        self.category = header.css("span.title-phrasing-xl::text").get()
        self.items = header.css("span.title-phrasing-sm::text").get()

        self.logger.info(
            "Category: %s",
            self.category,
        )
        self.logger.info(
            "Items: %s",
            self.items,
        )

        return Request(url=response.url, callback=self.parse_page, dont_filter=True)

    def parse_page(self, response):
        self.logger.info("Parsing page: %s", response.url)

        products = response.css("div.card-v2-wrapper")

        for product in products:
            # Skip objects with no ID
            if product.css("div.card-v2-atc::attr(data-pnk)").get() == None:
                return

            itemloader = ItemLoader(item=EmagProductsItem(), selector=product)

            # Used tag
            used = product.css(
                "div.mrg-btm-xxs.semibold.font-size-sm.text-success::text"
            ).get()
            if used == "RESIGILAT":
                itemloader.add_value("usedTag", True)
                itemloader.add_css("usedPrice", "p.product-new-price")
            else:
                itemloader.add_value("usedTag", False)
                itemloader.add_css("productPrice", "p.product-new-price")

            # Genius tag
            genius = product.css("div.card-v2-badges").get()
            if genius != None and "badge-genius" in genius:
                itemloader.add_value("geniusTag", True)
            else:
                itemloader.add_value("geniusTag", False)

            itemloader.add_value("crawledAt", "")
            itemloader.add_css("productID", "div.card-v2-atc::attr(data-pnk)")
            itemloader.add_css("productName", ".card-v2-title")
            itemloader.add_css("productLink", "a.card-v2-thumb::attr(href)")
            itemloader.add_css("productImg", "img.w-100::attr(src)")
            itemloader.add_value("productCategory", self.category)
            itemloader.add_css("productStars", "span.average-rating.semibold::text")
            itemloader.add_css("productReviews", "span.visible-xs-inline-block::text")
            # TODO: Add more fields
            # itemloader.add_value("productStock", "span.visible-xs-inline-block::text")
            itemloader.add_css("retailPrice", "span.rrp-lp30d-content:nth-child(1)")
            itemloader.add_css("slashedPrice", "span.rrp-lp30d-content:nth-child(2)")

            # Load items
            yield itemloader.load_item()
