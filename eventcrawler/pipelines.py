# -*- coding: utf-8 -*-

import datetime
from event.models import Event,Category
from django.db.utils import IntegrityError
from scrapy.exceptions import DropItem
from hashlib import sha1

class EventcrawlerPipeline(object):
    def __init__(self):
        self.category = Category.objects.get(shortname='gallery')
        
    def process_item(self, item, spider):
        pic_name = "%s%s.jpg" % ('images/full/', 
                                sha1(item['image_urls'][0]).hexdigest())


        event = Event(text=item['text'],name=item['name'],
                        date_start=item['date_start'], date_end=item['date_end'],
                        category=self.category, added_by='admin',
                        place=item['place_time'], picture=pic_name)
        try:
            event.save()
        except IntegrityError:
            raise DropItem("Error")
        return item
