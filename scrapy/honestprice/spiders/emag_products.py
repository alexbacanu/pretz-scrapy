from honestprice.items import EmagProductsItem
from scrapy import signals
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spidermiddlewares.httperror import HttpError
from scrapy.spiders import CrawlSpider, Request, Rule


# TODO: Disable robots.txt request
# TODO: Fix 71/72 products
class EmagProductsSpider(CrawlSpider):
    name = "emag_products"
    allowed_domains = ["emag.ro"]
    rules = (
        Rule(
            LinkExtractor(allow=(r"/c$"), restrict_css=("a.js-change-page")),
            callback="parse_page",
            errback="error_function",
            follow=True,
        ),
    )

    custom_settings = {
        "ITEM_PIPELINES": {
            "honestprice.pipelines.DefaultValuesPipeline": 150,
            "honestprice.pipelines.GoogleFirestoreProductsPipeline": 250,
            # "honestprice.pipelines.TypesenseProductsPipeline": 280,
        },
    }

    def __init__(self, *args, **kwargs):
        super(EmagProductsSpider, self).__init__(*args, **kwargs)
        self.start_urls = [kwargs.get("start_url")]

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

        yield Request(
            url=response.url, callback=self.parse_page, errback=self.error_function
        )

    def parse_page(self, response):
        self.logger.info("Parsing page: %s", response.url)

        print(f"emag_products.py: Crawling {response.url}")

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

            # Image tag
            image = product.css("img.w-100::attr(src)").get()
            if image != None:
                itemloader.add_css("productImg", "img.w-100::attr(src)")
            else:
                itemloader.add_css("productImg", "div.bundle-image::attr(style)")

            # Rating
            ratings = product.css("div.card-v2-rating").get()
            if ratings != None and "star-rating-text" in ratings:
                itemloader.add_css("productStars", "span.average-rating.semibold::text")
                itemloader.add_css(
                    "productReviews", "span.visible-xs-inline-block::text"
                )
            else:
                itemloader.add_value("productStars", 0)
                itemloader.add_value("productReviews", 0)

            itemloader.add_value("crawledAt", "")
            itemloader.add_css("productID", "div.card-v2-atc::attr(data-pnk)")
            itemloader.add_css("productName", ".card-v2-title")
            itemloader.add_css("productLink", "a.card-v2-thumb::attr(href)")
            itemloader.add_value("productCategory", self.category)

            itemloader.add_css("retailPrice", "span.rrp-lp30d-content:nth-child(1)")
            itemloader.add_css("slashedPrice", "span.rrp-lp30d-content:nth-child(2)")

            # TODO: Add more fields
            # itemloader.add_value("productStock", "span.visible-xs-inline-block::text")

            # Load items
            yield itemloader.load_item()

    def error_function(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error("HttpError on %s", response.url)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(EmagProductsSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        stats = spider.crawler.stats.get_stats()
        if "item_scraped_count" in stats:
            numcount = str(stats["item_scraped_count"])
            print(f"count_scrapy:   {numcount}")

        try:
            print(f"count_website:  {self.items}")
        except:
            print(f"count_website:  0")
        print("---------------------------------")
