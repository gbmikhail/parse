# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst


def process_price(value):
    value = int(value.replace(' ', ''))
    return value


def process_feature(value):
    # value = int(value.replace(' ', ''))
    return value


class LeroymerlinParserItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(process_price))
    photos = scrapy.Field()
    url = scrapy.Field()
    feature = scrapy.Field(input_processor=MapCompose(process_feature))

