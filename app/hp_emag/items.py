# Define here the models for your scraped items
#

from itemloaders.processors import MapCompose, TakeFirst
from scrapy.item import Item, Field
from w3lib.html import remove_tags
import time
import re


def current_date(text):
    return round(time.time())


def filter_pricing(text):
    replace_text = text.replace(".", "").replace("<sup>", ".")
    remove_tag = re.sub(re.compile("<.*?>"), "", replace_text)
    digits_only = [float(s) for s in re.findall(r"-?\d+\.?\d*", remove_tag)]
    return digits_only


class EmagProductsItem(Item):
    name = Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    id = Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    rrp = Field(
        input_processor=MapCompose(filter_pricing), output_processor=TakeFirst()
    )
    full = Field(
        input_processor=MapCompose(filter_pricing), output_processor=TakeFirst()
    )
    price = Field(
        input_processor=MapCompose(filter_pricing), output_processor=TakeFirst()
    )
    link = Field(input_processor=MapCompose(), output_processor=TakeFirst())
    img = Field(input_processor=MapCompose(), output_processor=TakeFirst())
    crawled = Field(
        input_processor=MapCompose(current_date), output_processor=TakeFirst()
    )


class EmagSitemapItem(Item):
    url = Field()


class HpEmagItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
