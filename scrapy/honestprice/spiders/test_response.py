import scrapy


class TestResponseSpider(scrapy.Spider):
    name = "test_response"
    allowed_domains = ["whatismybrowser.com"]
    start_urls = [
        "https://www.whatismybrowser.com/",
    ]
    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            "honestprice.middlewares.WebShareProxyMiddleware": 130,
            # "honestprice.middlewares.ScrapeAPIProxyMiddleware": 150,
        }
    }

    def parse(self, response):
        self.logger.info("Parsing page: %s", response.url)
        print(response.css("#ip-address").get())
