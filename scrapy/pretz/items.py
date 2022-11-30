import re

from itemloaders.processors import MapCompose, TakeFirst

from scrapy import Field, Item


def remove_newline(text):
    return text.replace("\n", "").strip()


def generate_tags(text):
    stripped_text = re.sub(r"[^A-Za-z0-9 ]+", "", text)
    return stripped_text.split(" ")


def filter_image(text):
    url = re.findall(r"https?://[^)]+", text)[0]
    return url


def remove_vendor(text):
    remove_vendor = text.split("-")
    clean_category = remove_vendor[0].strip()
    return clean_category


def filter_text(text):
    digits_only = re.findall(r"-?\d+\.?\d*", str(text))[0]
    return float(digits_only)


def filter_pricing(text):
    remove_tags_re = (
        re.sub(re.compile(r"<.*?>"), "", text).replace(".", "").replace(",", ".")
    )
    digits_only = [float(s) for s in re.findall(r"-?\d+\.?\d*", remove_tags_re)]
    return digits_only


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
