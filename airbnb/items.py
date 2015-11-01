# -*- coding: utf-8 -*-
from scrapy.item import Item, Field


class AirbnbItem(Item):
    name = Field()
    user_url = Field()
    room_url = Field()
    room_type = Field()
    summary = Field()
    address = Field()
    image = Field()
    price = Field()
    coin = Field()
    reviews = Field()
