import re

from itemloaders.processors import MapCompose, TakeFirst

from scrapy import Field, Item


def to_lowercase(text):
    return text.lower()


def generate_tags(text):
    stripped_text = re.sub(r"[^A-Za-z0-9 ]+", "", text)
    return stripped_text.split(" ")


class GenericProductsItem(Item):
    pID = Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst(),
    )
    pName = Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst(),
    )
    # pNameTags = Field(
    #     input_processor=MapCompose(),
    # )
    pLink = Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst(),
    )
    pImg = Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst(),
    )
    pCategoryTrail = Field(
        input_processor=MapCompose(),
    )
    pCategory = Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst(),
    )
    pBrand = Field(
        input_processor=MapCompose(to_lowercase),
        output_processor=TakeFirst(),
    )
    pVendor = Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst(),
    )
    pStock = Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst(),
    )
    pReviews = Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst(),
    )
    pStars = Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst(),
    )
    priceCurrent = Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst(),
    )
    priceRetail = Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst(),
    )
    priceSlashed = Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst(),
    )
    priceUsed = Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst(),
    )
    crawledAt = Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst(),
    )

    # emag specific
    pGeniusTag = Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst(),
    )
    pUsedTag = Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst(),
    )


class GenericSitemapItem(Item):
    response_status = Field()
    response_category = Field()
    response_url = Field()
