# Define here the models for your scraped items
import re
from datetime import datetime

from itemloaders.processors import MapCompose, TakeFirst
from scrapy import Field, Item
from w3lib.html import remove_tags


def current_date(text):
    return datetime.now().isoformat()


def remove_newline(text):
    return text.replace("\n", "")


def remove_vendor(text):
    remove_vendor = text.split("-")
    clean_category = remove_vendor[0].strip()
    return clean_category


def filter_pricing(text):
    remove_tags_re = (
        re.sub(re.compile("<.*?>"), "", text).replace(".", "").replace(",", ".")
    )
    digits_only = [float(s) for s in re.findall(r"-?\d+\.?\d*", remove_tags_re)]
    return digits_only


def filter_text(text):
    digits_only = re.findall("(\d+)", str(text))[0]
    return int(digits_only)


def filter_image(text):
    url = re.findall("https?://[^)]+", text)[0]
    return url


class EmagProductsItem(Item):
    pID = Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst(),
    )
    pStore = Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst(),
    )
    pName = Field(
        input_processor=MapCompose(remove_tags, remove_newline),
        output_processor=TakeFirst(),
    )
    pLink = Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst(),
    )
    pImg = Field(
        input_processor=MapCompose(filter_image),
        output_processor=TakeFirst(),
    )
    pCategory = Field(
        input_processor=MapCompose(remove_vendor),
        output_processor=TakeFirst(),
    )
    pReviews = Field(
        input_processor=MapCompose(filter_text),
        output_processor=TakeFirst(),
    )
    pStars = Field(
        input_processor=MapCompose(filter_text),
        output_processor=TakeFirst(),
    )
    pGeniusTag = Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst(),
    )
    pUsedTag = Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst(),
    )
    priceCurrent = Field(
        input_processor=MapCompose(filter_pricing),
        output_processor=TakeFirst(),
    )
    priceRetail = Field(
        input_processor=MapCompose(filter_pricing),
        output_processor=TakeFirst(),
    )
    priceSlashed = Field(
        input_processor=MapCompose(filter_pricing),
        output_processor=TakeFirst(),
    )
    priceUsed = Field(
        input_processor=MapCompose(filter_pricing),
        output_processor=TakeFirst(),
    )
    crawledAt = Field(
        input_processor=MapCompose(current_date),
        output_processor=TakeFirst(),
    )
    # TODO: Add more fields
    # productStock = Field(
    #     input_processor=MapCompose(),
    #     output_processor=TakeFirst(),
    # )


class EmagSitemapItem(Item):
    response_status = Field()
    response_category = Field()
    response_url = Field()
