# Define here the models for your scraped items
import re
import time
from decimal import Decimal

from itemloaders.processors import MapCompose, TakeFirst
from scrapy import Field, Item
from w3lib.html import remove_tags


def current_date(text):
    return str(round(time.time()))


def remove_newline(text):
    return text.replace("\n", "")


def filter_pricing(text):
    replace_text = text.replace(".", "").replace("<sup>", ".")
    remove_tag = re.sub(re.compile("<.*?>"), "", replace_text)
    digits_only = [Decimal(s) for s in re.findall(r"-?\d+\.?\d*", remove_tag)]
    return digits_only


class EmagProductsItem(Item):
    name = Field(input_processor=MapCompose(remove_tags, remove_newline), output_processor=TakeFirst())
    id = Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    rrp = Field(input_processor=MapCompose(filter_pricing), output_processor=TakeFirst())
    full = Field(input_processor=MapCompose(filter_pricing), output_processor=TakeFirst())
    price = Field(input_processor=MapCompose(filter_pricing), output_processor=TakeFirst())
    link = Field(input_processor=MapCompose(), output_processor=TakeFirst())
    img = Field(input_processor=MapCompose(), output_processor=TakeFirst())
    crawled = Field(input_processor=MapCompose(current_date), output_processor=TakeFirst())


class EmagSitemapItem(Item):
    status = Field()
    url = Field()
