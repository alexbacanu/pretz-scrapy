from honestprice.items import EmagProductsItem
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Request, Rule


class EmagProductsSpider(CrawlSpider):
    name = "emag_products"
    allowed_domains = ["emag.ro"]
    start_urls = []

    rules = (
        Rule(
            LinkExtractor(allow=(r"/c$"), restrict_css=("a.js-change-page")),
            callback="parse_page",
            follow=True,
        ),
    )

    custom_settings = {
        "ITEM_PIPELINES": {
            "honestprice.pipelines.DefaultValuesPipeline": 150,
            "honestprice.pipelines.OracleProductsPipeline": 250,
            # "honestprice.pipelines.PrismaProductsPipeline": 250,
        },
        "SPIDER_MIDDLEWARES": {
            "honestprice.middlewares.StartUrlsMiddleware": 110,
        },
    }

    # def __init__(self, *args, **kwargs):
    #     super(EmagProductsSpider, self).__init__(*args, **kwargs)
    #     self.start_urls = [kwargs.get("start_url")]

    def parse_start_url(self, response):
        self.logger.info(f"Getting headers from {response.url}")

        # Select category and items
        header = response.css("div.js-head-title")
        self.category = header.css("span.title-phrasing-xl::text").get()
        self.items = header.css("span.title-phrasing-sm::text").get()

        # Logs again
        self.logger.info(f"Category: {self.category}")
        self.logger.info(f"Items: {self.items}")

        # Return
        yield Request(url=response.url, callback=self.parse_page, dont_filter=True)

    def parse_page(self, response):
        # Logs
        self.logger.info(f"Crawling {response.url}")

        # Define selectors
        products = response.css("div.card-v2-wrapper")

        for product in products:
            # Skip objects with no ID
            if product.css("div.card-v2-atc::attr(data-pnk)").get() is None:
                return

            # Define selectors
            itemloader = ItemLoader(item=EmagProductsItem(), selector=product)

            # pID
            itemloader.add_css("pID", "div.card-v2-atc::attr(data-pnk)")

            # pStore
            itemloader.add_value("pStore", "emag")

            # pName
            itemloader.add_css("pName", ".card-v2-title")

            # pLink
            itemloader.add_css("pLink", "a.card-v2-thumb::attr(href)")

            # pImg
            image = product.css("img.w-100::attr(src)").get()
            if image is not None:
                itemloader.add_css("pImg", "img.w-100::attr(src)")
            else:
                itemloader.add_css("pImg", "div.bundle-image::attr(style)")

            # pCategory
            itemloader.add_value("pCategory", self.category)

            # pReviews / pStars
            ratings = product.css("div.card-v2-rating").get()
            if ratings is not None and "star-rating-text" in ratings:
                itemloader.add_css("pReviews", "span.visible-xs-inline-block::text")
                itemloader.add_css("pStars", "span.average-rating.semibold::text")
            else:
                itemloader.add_value("pReviews", 0)
                itemloader.add_value("pStars", 0)

            # pGeniusTag
            genius = product.css("div.card-v2-badges").get()
            if genius is not None and "badge-genius" in genius:
                itemloader.add_value("pGeniusTag", True)
            else:
                itemloader.add_value("pGeniusTag", False)

            # pUsedTag / priceCurrent / priceUsed
            used = product.css(
                "div.mrg-btm-xxs.semibold.font-size-sm.text-success::text"
            ).get()
            if used == "RESIGILAT":
                itemloader.add_value("pUsedTag", True)
                itemloader.add_css("priceUsed", "p.product-new-price")
            else:
                itemloader.add_value("pUsedTag", False)
                itemloader.add_css("priceCurrent", "p.product-new-price")

            # priceRetail
            itemloader.add_css("priceRetail", "span.rrp-lp30d-content:nth-child(1)")

            # priceSlashed
            itemloader.add_css("priceSlashed", "span.rrp-lp30d-content:nth-child(2)")

            # crawledAt
            itemloader.add_value("crawledAt", "")

            # TODO: Add more fields
            # itemloader.add_value("productStock", "span.visible-xs-inline-block::text")

            # Load items
            yield itemloader.load_item()
