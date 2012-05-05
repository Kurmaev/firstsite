# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from eventcrawler.items import EventcrawlerItem

class EventSpider(CrawlSpider):
    name = "eventcrawler"
    allowed_domains = ["omskcult.ru"]
    start_urls = ["http://www.omskcult.ru/user/gallery/"]

    rules = (Rule(SgmlLinkExtractor(allow=('events/\d+'), deny=('events/\d+/comments/')), callback='parse_item'),)
 
    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        item = EventcrawlerItem()

        text = hxs.select('//div[@class="event_text"]//p/text()').extract()
        text_utf = ''
        for i in text:
            text_utf += i
        item['text'] = text_utf
        
        name = hxs.select('//div[@class="event_title"]//h1//b/text()').extract()
        name_utf = ''
        for i in name:
            name_utf += i
        item['name'] = name_utf

        return item
