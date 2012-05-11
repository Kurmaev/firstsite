# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from eventcrawler.items import EventcrawlerItem
import datetime

today = datetime.date.today()
this_month = datetime.date( today.year , today.month, 1).isoformat()
class EventSpider(CrawlSpider):
    name = "eventcrawler"
    allowed_domains = ["omskcult.ru"]
    start_urls = [
                    ''.join(("http://www.omskcult.ru/user/gallery/",
                            this_month,'/month/eventsort',)),
                    ''.join(("http://www.omskcult.ru/user/concert/",
                            this_month,'/month/eventsort',)),
                    ''.join(("http://www.omskcult.ru/user/cinema/",
                            this_month,'/month/eventsort',)),

]

    rules = (

    Rule(SgmlLinkExtractor(allow=('/user/\w+/\d+-\d+-\d+/month/eventsort',),
                            deny=(''.join(('/user/\w+/',this_month,
                                            '/month/eventsort')),),
                            unique=True,),
        follow=True),

    Rule(SgmlLinkExtractor(allow=('events/\d+'), deny=('events/\d+/comments/')),
         callback='parse_item'),

)

    findmonth = {
                u'января': 1,
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

        item['category'] = hxs.select("//div[@class='icon']//a[@href]")\
.extract()[0].split('/')[2]

        text = hxs.select('//div[@class="event_text"]//p').extract()
        item['text'] = ' '.join(text)

        name = hxs.select('//div[@class="event_title"]//h1//b/text()').extract()
        item['name'] = ' '.join(name)

        item['image_urls'] = hxs.select('//div[@class="event_image"]/img/\
@src').extract()
        if len(item['image_urls']):
            item['image_urls'] = (''.join(("http://",
                    EventSpider.allowed_domains[0], item['image_urls'][0])),)

        place = hxs.select("//div[@class='times_place']//tr\
//td[@class='t2']//a/text()").extract()

        time = hxs.select("//div[@class='times_place']//tr\
//td[@class='t3']//span/text()").extract()

        date_to_parse = hxs.select('//table[@class="times_table"]//tr\
//td/b/text()').extract()

        if item['category'] == u'cinema':
            item['date_start'] = self.date_parse_cinema(date_to_parse[0])
            item['date_end'] = self.date_parse_cinema(date_to_parse[-1])
            if place:
                item['place_time'] = ', '.join(set(place))
            else:
                item['place_time'] = ''
        else:
            item['date_start'], item['date_end'] =\
                                         self.date_parsing(date_to_parse[0])
            if place:
                item['place_time'] = ', '.join((place[0],time[0],))
            else:
                item['place_time'] = ''

        return item

    def date_parsing(self, date_to_parse):
        date_to_parse = date_to_parse.split()
        if date_to_parse[0] == u'Сегодня,':
            date_to_parse = date_to_parse[1:]
        year = datetime.date.today().year
        day_start = int(date_to_parse[1])
        if date_to_parse[2] == u'\u2014':
        #[вт, 5, -, вт, 8, мая]
            month_start = month_end = self.findmonth[date_to_parse[5]]
            day_end = int(date_to_parse[4])
        else:
            month_start = self.findmonth[date_to_parse[2]]
            if len(date_to_parse) >3:
                #[вт, 5, апреля, -, вт, 8, мая]
                month_end = self.findmonth[date_to_parse[6]]
                day_end = int(date_to_parse[5])
            else:
                #[вт, 5, апреля]
                month_end = month_start
                day_end= day_start
        return datetime.date(year,month_start,day_start),\
                datetime.date(year,month_end,day_end)

    def date_parse_cinema(self, date_to_parse):
        date_to_parse = date_to_parse.split()
        if date_to_parse[0] == u'Сегодня,':
            date_to_parse = date_to_parse[1:]
        #[вт, 5, апреля]
        year = datetime.date.today().year
        day = int(date_to_parse[1])
        month = self.findmonth[date_to_parse[2]]

        return datetime.date(year,month,day)
