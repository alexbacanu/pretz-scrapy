from datetime import datetime

from pretz.custom import SimpleRedisCrawlSpider
from pretz.items import GenericProductsItem
from pretz.settings import DEV_TAG
from rapidfuzz import process
from rapidfuzz.fuzz import partial_ratio
from scrapy.loader import ItemLoader
from scrapy.spiders import Request


class EmagProductsSpider(SimpleRedisCrawlSpider):
    name = f"emag_products{DEV_TAG}"

    sitemap_name = f"emag_sitemap{DEV_TAG}"
    database_name = f"products{DEV_TAG}"
    api_website = "https://www.emag.ro/search-by-url?source_id=7&page[limit]=100&url=/"

    allowed_domains = ["emag.ro"]

    custom_settings = {
        "ITEM_PIPELINES": {
            "pretz.pipelines.MongoPipeline": 250,
        },
    }

    def parse_start_url(self, response):
        self.logger.info(f"[Spider->Products] Getting headers from {response.url}")

        # JSON response
        json_response = response.json()

        # Get total pages
        total_pages = json_response.get("data").get("pagination").get("pages")[-1].get("id")

        if total_pages == 1:
            yield Request(url=response.url, callback=self.parse_page)

        if total_pages > 1:
            # Strip /c from the end
            new_response = response.url.rsplit("/", 1)[0]

            # Generate requests based on number of pages
            requests_array = [f"{new_response}/p{i}/c" for i in range(2, total_pages + 1)]

            # Insert first page (does not use /p{i}/c)
            requests_array.insert(0, response.url)

            for request in requests_array:
                yield Request(url=request, callback=self.parse_page)

    def parse_page(self, response):
        self.logger.info(f"[Spider->Products] Crawling {response.url}")

        # JSON response
        json_response = response.json()

        # Get products
        products = json_response.get("data").get("items")

        # Get category
        category = json_response.get("data").get("category").get("name")

        # Get brands
        filters_array = json_response.get("data").get("filters").get("items")
        try:
            brands_array = next(element.get("items") for element in filters_array if element["name"] == "Brand")
        except StopIteration:
            brands_array = []
        choices = [o.get("name") for o in brands_array]

        # Get breadcrumbs
        breadcrumbs_list = json_response.get("data").get("category").get("trail").split("/")

        if products:
            for product in products:
                itemloader = ItemLoader(item=GenericProductsItem(), selector=product)

                # pID
                itemloader.add_value("pID", f"emg:{product.get('part_number_key')}")

                # pName
                itemloader.add_value("pName", product.get("name"))

                # # pNameTags
                # itemloader.add_value("pNameTags", product.get("name"))

                # pLink
                itemloader.add_value("pLink", f"https://emag.ro/{product.get('url').get('path')}")

                # pImg
                itemloader.add_value("pImg", product.get("image").get("original"))

                # pCategoryTrail
                itemloader.add_value("pCategoryTrail", breadcrumbs_list)

                # pCategory
                itemloader.add_value("pCategory", category)

                # pBrand
                extracted_brand = process.extractOne(product.get("name"), choices, scorer=partial_ratio)
                itemloader.add_value("pBrand", extracted_brand[0] if extracted_brand else None)
                # Debug
                if extracted_brand and extracted_brand[1] < 91:
                    self.logger.warning(product.get("name"))
                    self.logger.warning(extracted_brand)

                # pVendor
                itemloader.add_value("pVendor", product.get("offer").get("vendor").get("name").get("display"))

                # pStock
                itemloader.add_value("pStock", product.get("offer").get("availability").get("text"))

                # pReviews
                itemloader.add_value("pReviews", product.get("feedback").get("reviews").get("count"))

                # pStars
                itemloader.add_value("pStars", product.get("feedback").get("rating"))

                # priceCurrent
                itemloader.add_value("priceCurrent", product.get("offer").get("price").get("current"))

                # priceRetail
                itemloader.add_value(
                    "priceRetail",
                    product.get("offer").get("price").get("recommended_retail_price").get("amount"),
                )

                # priceSlashed
                itemloader.add_value(
                    "priceSlashed",
                    product.get("offer").get("price").get("lowest_price_30_days").get("amount"),
                )

                # crawledAt
                itemloader.add_value("crawledAt", datetime.utcnow())

                # Load items
                yield itemloader.load_item()
