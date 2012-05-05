# -*- coding: utf-8 -*-

import datetime
from event.models import Event,Category
from django.db.utils import IntegrityError
from scrapy.exceptions import DropItem

class EventcrawlerPipeline(object):
    def __init__(self):
        self.category = Category.objects.get(shortname='cinema')
        
    def process_item(self, item, spider):

        category = Category.objects.get(shortname='cinema')
        event = Event(text=item['text'],name=item['name'],date=datetime.date.today(), category=self.category)
        event.save()
        try:
            event.save()
        except IntegrityError:
            raise DropItem("Error")
        return item
