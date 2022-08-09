# Define here the models for your scraped items
import datetime
import re

from itemloaders.processors import MapCompose, TakeFirst
from scrapy import Field, Item
from w3lib.html import remove_tags

# from decimal import Decimal


def current_date(text):
    return datetime.datetime.now(tz=datetime.timezone.utc)


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


class EmagProductsItem(Item):
    crawledAt = Field(
        input_processor=MapCompose(current_date),
        output_processor=TakeFirst(),
    )
    productID = Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst(),
    )
    productName = Field(
        input_processor=MapCompose(remove_tags, remove_newline),
        output_processor=TakeFirst(),
    )
    productLink = Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst(),
    )
    productImg = Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst(),
    )
    productCategory = Field(
        input_processor=MapCompose(remove_vendor),
        output_processor=TakeFirst(),
    )
    productPrice = Field(
        input_processor=MapCompose(filter_pricing),
        output_processor=TakeFirst(),
    )
    geniusTag = Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst(),
    )
    slashedPrice = Field(
        input_processor=MapCompose(filter_pricing),
        output_processor=TakeFirst(),
    )
    retailPrice = Field(
        input_processor=MapCompose(filter_pricing),
        output_processor=TakeFirst(),
    )


class EmagSitemapItem(Item):
    response_status = Field()
    response_url = Field()
    response_category = Field()
