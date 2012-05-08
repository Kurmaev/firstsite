# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class EventcrawlerItem(Item):
        name = Field()
        text = Field()
        date_start = Field()
        date_end = Field()
        place_time = Field()
        image_urls = Field()
        images = Field()
