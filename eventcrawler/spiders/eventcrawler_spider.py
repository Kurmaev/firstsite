# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from eventcrawler.items import EventcrawlerItem
import datetime

class EventSpider(CrawlSpider):
    name = "eventcrawler"
    allowed_domains = ["omskcult.ru"]
    start_urls = ["http://www.omskcult.ru/user/gallery/"]

    rules = (
    Rule(SgmlLinkExtractor(allow=('events/\d+'), deny=('events/\d+/comments/')),
         callback='parse_item'),
         )
    findmonth = {u'января': 1,
                u'февраля' : 2,
                u'марта' : 3,
                u'апреля' : 4,
                u'мая' : 5,
                u'июня' : 6,
                u'июля' : 7,
                u'августа' : 8,
                u'сентября' : 9,
                u'октября' : 10,
                u'ноября' : 11,
                u'декабря' : 12,
}

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        item = EventcrawlerItem()

        text = hxs.select('//div[@class="event_text"]//p').extract()
        text_utf = ''
        for i in text:
            text_utf += i
        item['text'] = text_utf

        place = hxs.select("//div[@class='times_place']//tr[@class='times_last']\
//td[@class='t2']//a/text()").extract()[0]
        time = hxs.select("//div[@class='times_place']//tr[@class='times_last']\
//td[@class='t3']//span/text()").extract()[0]
        item['place_time'] = ''.join((place,', ',time))

        name = hxs.select('//div[@class="event_title"]//h1//b/text()').extract()
        name_utf = ''
        for i in name:
            name_utf += i
        item['name'] = name_utf

        item['image_urls'] = hxs.select('//div[@class="event_image"]/img/\
@src').extract()
        item['image_urls'] = ["http://"+EventSpider.allowed_domains[0] +\
 item['image_urls'][0]]

        date_to_parse = hxs.select('//table[@class="times_table"]//tr[@class=""]\
//td/b/text()').extract()[0]
        item['date_start'], item['date_end'] = self.date_parsing(date_to_parse)
        
        return item

    def date_parsing(self, date_to_parse):
        date_to_parse = date_to_parse.split()
        year = datetime.date.today().year
        day_start = int(date_to_parse[1])
        if date_to_parse[2] == u'\u2014':
        #[вт, 5, -, вт, 8, мая]
            month_start = month_end = self.findmonth[date_to_parse[5]]
            day_end = int(date_to_parse[4])
        else:
            month_start = self.findmonth[date_to_parse[2]]
            if date_to_parse.__len__() >3:
                #[вт, 5, апреля, -, вт, 8, мая]
                month_end = self.findmonth[date_to_parse[6]]
                day_end = int(date_to_parse[5])
            else:
                #[вт, 5, апреля]
                month_end = month_start
                day_end= day_start

        return datetime.date(year,month_start,day_start),\
                datetime.date(year,month_end,day_end)

