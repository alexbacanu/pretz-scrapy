import scrapy


class EmagSitemapSpider(scrapy.Spider):
    name = 'emag_sitemap'
    allowed_domains = ['emag.ro']
    start_urls = ['http://emag.ro/']

    def parse(self, response):
        pass
