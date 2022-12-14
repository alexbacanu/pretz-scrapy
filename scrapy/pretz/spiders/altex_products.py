from datetime import datetime

from pretz.custom import SimpleRedisCrawlSpider
from pretz.items import GenericProductsItem
from pretz.settings import DEV_TAG
from scrapy.loader import ItemLoader
from scrapy.spiders import Request


class AltexProductsSpider(SimpleRedisCrawlSpider):
    name = f"altex_products{DEV_TAG}"

    sitemap_name = f"altex_sitemap{DEV_TAG}"
    database_name = f"products{DEV_TAG}"
    api_website = "https://fenrir.altex.ro/catalog/category/"

    allowed_domains = ["altex.ro"]

    custom_settings = {
        "ITEM_PIPELINES": {
            "pretz.pipelines.MongoPipeline": 250,
        },
        # Fenrir doesn't have robots.txt
        "ROBOTSTXT_OBEY": False,
    }

    def parse_start_url(self, response):
        self.logger.info(f"[Spider->Products] Getting pages from {response.url}")

        # JSON response
        json_response = response.json()

        # Get total pages
        total_pages = json_response.get("meta").get("total_pages")

        # Create an array of requests
        requests_array = [f"{response.url}?page={i}" for i in range(1, total_pages + 1)]

        # Generate requests
        for request in requests_array:
            yield Request(url=request, callback=self.parse_page)

    def parse_page(self, response):
        self.logger.info(f"[Spider->Products] Crawling {response.url}")

        # JSON response
        json_response = response.json()

        # Get products
        products = json_response.get("products")

        # Get category
        category = json_response.get("category").get("name")

        # Get breadcrumbs
        breadcrumbs = json_response.get("breadcrumbs")
        breadcrumbs_list = [o["name"] for o in breadcrumbs]

        if products:
            for product in products:
                itemloader = ItemLoader(item=GenericProductsItem(), selector=product)

                # pID
                itemloader.add_value("pID", f"atx:{product.get('sku')}")

                # pName
                itemloader.add_value("pName", product.get("name"))

                # # pNameTags
                # itemloader.add_value("pNameTags", product.get("name"))

                # pLink
                itemloader.add_value("pLink", f"https://altex.ro/{product.get('url_key')}")

                # pImg
                itemloader.add_value("pImg", f"https://lcdn.altex.ro{product.get('image')}")

                # pCategoryTrail
                itemloader.add_value("pCategoryTrail", breadcrumbs_list)

                # pCategory
                itemloader.add_value("pCategory", category)

                # pBrand
                itemloader.add_value("pBrand", product.get("brand_name"))

                # pVendor
                itemloader.add_value("pVendor", product.get("price_seller_name"))

                # pStock
                if product.get("stock_status") == 1 and product.get("pickup_is_in_stock") == 1:
                    itemloader.add_value("pStock", "În stoc")

                if product.get("stock_status") == 1 and product.get("pickup_is_in_stock") == 0:
                    itemloader.add_value("pStock", "Exclusiv online")

                if product.get("stock_status") == 0 and product.get("pickup_is_in_stock") == 1:
                    itemloader.add_value("pStock", "În anumite magazine")

                if product.get("stock_status") == 0 and product.get("pickup_is_in_stock") == 0:
                    itemloader.add_value("pStock", "Stoc epuizat")

                # pReviews
                itemloader.add_value("pReviews", product.get("reviews_count"))

                # pStars
                if product.get("reviews_count") != 0:
                    itemloader.add_value(
                        "pStars",
                        product.get("reviews_value") / product.get("reviews_count"),
                    )

                # priceCurrent
                itemloader.add_value("priceCurrent", product.get("price"))

                # priceRetail
                itemloader.add_value("priceRetail", product.get("msrp_price"))

                # priceSlashed
                itemloader.add_value("priceSlashed", product.get("regular_price"))

                # crawledAt
                itemloader.add_value("crawledAt", datetime.utcnow())

                # Load items
                yield itemloader.load_item()
