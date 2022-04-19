import scrapy


class TestResponseSpider(scrapy.Spider):
    name = "test_response"
    allowed_domains = ["xhaus.com"]
    start_urls = [
        "http://www.xhaus.com/headers",
    ]
    custom_settings = {
        "SPIDER_MIDDLEWARES": {
            "honestprice.middlewares.ScrapeAPIProxyMiddleware": 150,
        }
    }

    def parse(self, response):
        self.logger.info("Parsing page: %s", response.url)

        print(response.css("table").get())
