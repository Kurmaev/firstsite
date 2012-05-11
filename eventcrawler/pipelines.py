# -*- coding: utf-8 -*-

import datetime
from event.models import Event,Category
from django.db.utils import IntegrityError
from scrapy.exceptions import DropItem
from hashlib import sha1

class EventcrawlerPipeline(object):
    def __init__(self):
        self.category =\
        {
            'gallery':Category.objects.get(shortname='gallery'),
            'cinema':Category.objects.get(shortname='cinema'),
            'concert':Category.objects.get(shortname='concert'),
            'other':Category.objects.get(shortname='other'),
        }
        self.today = datetime.date.today()

    def process_item(self, item, spider):
        if item['date_end'] >= self.today:
            if len(item['image_urls']):
                pic_name = "%s%s.jpg" % ('images/full/', 
                                    sha1(item['image_urls'][0]).hexdigest())
            else:
                pic_name = ''
            try:
                event = Event.objects.get(name=item['name'])
            except:
                event = 0
            
            if event:
                if event.date_end < item['date_end']:
                    event.date_end = item['date_end']
            else:
                event = Event(
                        text=item['text'],name=item['name'],
                        date_start=item['date_start'], date_end=item['date_end'],
                        category=self.category.get(item['category'], self.category['other']), 
                        added_by='admin', place=item['place_time'], picture=pic_name)

            try:
                event.save()
            except IntegrityError:
                raise DropItem("Error")

        else:
            raise DropItem("Event too old")

        return item
