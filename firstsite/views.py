# -*- coding: utf-8 -*-



from django.template.response import TemplateResponse
from event.models import Event
import datetime
from django.http import HttpResponse
import json

def randpage(request):
    today = datetime.date.today()
### Delete after show!!!!
    from django.core.cache import cache
    cache.clear()
    list_events = Event.objects.raw('select * from event_event where date_end>=\
"%s" order by rand() LIMIT 5'% (today.isoformat()))

    return TemplateResponse(request,'main/home.html',{'list_events':list_events,})

def testpage(request):
    return TemplateResponse(request,'test.html')

decode_month = { u'января':1,
          u'февраля':2,
          u'марта':3,
          u'апреля':4,
          u'мая':5,
          u'июня':6,
          u'июля':7,
          u'августа':8,
          u'сентября':9,
          u'октября':10,
          u'ноября':11,
          u'декабря':12,
}

weekday =[u'Понедельник', u'Вторник', u'Среда', u'Четверг', u'Пятница', u'Суббота', u'Воскресенье']
encode_month = [u'', u'Январь', u'Февраль',u'Март',u'Апрель',u'Май',u'Июнь',u'Июль',u'Август',u'Сентябрь',u'Октябрь',u'Ноябрь',u'Декабрь']
encode_months = [u'', u'января', u'февраля',u'марта',u'апреля',u'мая',u'июня',u'июля',u'августа',u'сентября',u'октября',u'ноября',u'декабря']

def ajaxpage(request):


    date = int(request.GET['d'])
    mon = decode_month[request.GET['m']]
    year = int(request.GET['y'])
    offset = int(request.GET['o'])
    zz =  datetime.date(year, mon, date)
    new_zz = zz + datetime.timedelta(days=offset)
    
    week = weekday[new_zz.weekday()];
    month_year = u"%s %s" % (encode_month[new_zz.month], new_zz.year)
    date = u"%s %s %s г." % (new_zz.day, encode_months[new_zz.month], new_zz.year)
    text = {'weekday': week,'month_year':month_year,'date':date,'big_num':new_zz.day}

    return HttpResponse(json.dumps(text), content_type="application/json")

