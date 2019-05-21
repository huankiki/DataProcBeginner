# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html


from scrapy.item import Item,Field

class JianshuitItem(Item):
    user = Field()
    time = Field()
    title = Field()
    view = Field()
    comment = Field()
    like = Field()
    gain = Field()
    pass
