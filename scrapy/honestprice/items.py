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


def filter_pricing(text):
    remove_tags_re = re.sub(re.compile("<.*?>"), "", text).replace(",", ".")
    digits_only = [float(s) for s in re.findall(r"-?\d+\.?\d*", remove_tags_re)]
    return digits_only


class EmagProductsItem(Item):
    product_crawled = Field(
        input_processor=MapCompose(current_date),
        output_processor=TakeFirst(),
    )
    product_name = Field(
        input_processor=MapCompose(remove_tags, remove_newline),
        output_processor=TakeFirst(),
    )
    product_id = Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst(),
    )
    product_link = Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst(),
    )
    product_img = Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst(),
    )
    price_rrp = Field(
        input_processor=MapCompose(filter_pricing),
        output_processor=TakeFirst(),
    )
    price_old = Field(
        input_processor=MapCompose(filter_pricing),
        output_processor=TakeFirst(),
    )
    price_new = Field(
        input_processor=MapCompose(filter_pricing),
        output_processor=TakeFirst(),
    )


class EmagSitemapItem(Item):
    response_status = Field()
    response_url = Field()
    response_category = Field()
