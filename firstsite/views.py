# -*- coding: utf-8 -*-
import calendar

from django.template.response import TemplateResponse
from event.models import Event
import datetime
from django.http import HttpResponse
import json
from event.utils import getPage
from django.db.models import Q

def randpage(request):
    today = datetime.date.today()
### Delete after show!!!!
    from django.core.cache import cache
    cache.clear()
    list_events = Event.objects.raw('select * from event_event where date_end>=\
"%s" order by rand() LIMIT 5'% (today.isoformat()))

    return TemplateResponse(request,'main/home.html',{'list_events':list_events,})

def testpage(request):
    filter_id = ''

#    if True:
    if request.is_ajax():

        offset = int(request.GET.get('o', 0 ))
        date = request.GET.get('d','')
        year = int(request.GET['y'])
        filter_id = request.GET.get('f', '' )

        
        if date:
            mon = decode_month[request.GET['m']]
        else:
            mon = decode_months[request.GET['m']]


        cookies = request.COOKIES.get('item_filter', '')
        cookies_arr = cookies.split('|')
        if '' in cookies_arr:
            cookies_arr.remove('')

        if filter_id:
            if filter_id in cookies_arr:
                cookies_arr.remove(filter_id)
            else:
                cookies_arr.append(filter_id)


        present_date =    datetime.date(year, mon, 1)
        if offset:
            if offset > 0:
                pr_w, pr_m_d = calendar.monthrange(present_date.year, present_date.month)
                present_date = present_date + datetime.timedelta(days = pr_m_d)
            else:
                present_date = present_date - datetime.timedelta(days = 1)
                present_date = datetime.date(present_date.year, present_date.month, 1)

        print present_date

        future_date =    present_date + datetime.timedelta(hours=24*32)
        past_date =    present_date - datetime.timedelta(days = 1)

        p_w, p_m_d = calendar.monthrange(past_date.year, past_date.month)
        pr_w, pr_m_d = calendar.monthrange(present_date.year, present_date.month)
        f_w, f_m_d = calendar.monthrange(future_date.year, future_date.month)

        present_date_end = datetime.date(present_date.year, present_date.month, pr_m_d)

        rez = []

        day = p_m_d - pr_w
        year = past_date.year
        month = past_date.month


#        print "past date: %s " % (past_date)
#        print "present date: %s " % (present_date)
#        print "future date: %s " % (future_date)

#        print "past count date: %s " % (p_m_d)
#        print "present count date: %s " % (pr_m_d)
#        print "future count date: %s " % (f_m_d)


#        print "past_start_week: %s " % (p_w)
#        print "present_start_week: %s " % (pr_w)
#        print "future_start_week: %s " % (f_w)
#        print "first week range: %s " % (range(1,x))
#        print "last week range: %s " % (range(1,8-f_w))

        for i in range(1,pr_w+1):
            rez.append([year, month, day+i, -1])

        year = present_date.year
        month = present_date.month
        date = '%s-%02d' % (year, month)

        for i in range(1,pr_m_d+1):
            search_date = '%s-%02d' % (date, i)
            count = Event.objects.filter(date_start__lte=search_date)\
.filter(date_end__gte=search_date).exclude(category__id__in=cookies_arr).count()
            rez.append([year, month, i, count])

        year = future_date.year
        month = future_date.month

        if f_w:
            for i in range(1,8-f_w):
                rez.append([year, month, i, -1])

        count = Event.objects.filter(date_start__lte=present_date_end).filter(date_end__gte=present_date)\
.exclude(category__id__in=cookies_arr).count()

        
        month_year = u" %s %s" % (encode_month[present_date.month], present_date.year)
        print month_year

        data = {'month_year':month_year, 'objects':rez, 'count':count}


        x = HttpResponse(json.dumps(data), content_type="application/json")
        if filter_id:
            x.set_cookie('item_filter', u'|'.join(cookies_arr), expires=future_date)

        return x

    else:

        return TemplateResponse(request,'test_month.html')


big_date = datetime.datetime(2022,1,1)

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

decode_months = { u'Январь':1,
          u'Февраль':2,
          u'Март':3,
          u'Апрель':4,
          u'Май':5,
          u'Июнь':6,
          u'Июль':7,
          u'Август':8,
          u'Сентябрь':9,
          u'Октябрь':10,
          u'Ноябрь':11,
          u'Декабрь':12,
}

weekday =[u'Понедельник', u'Вторник', u'Среда', u'Четверг', u'Пятница', u'Суббота', u'Воскресенье']
encode_month = [u'', u'Январь', u'Февраль',u'Март',u'Апрель',u'Май',u'Июнь',u'Июль',u'Август',u'Сентябрь',u'Октябрь',u'Ноябрь',u'Декабрь']
encode_months = [u'', u'января', u'февраля',u'марта',u'апреля',u'мая',u'июня',u'июля',u'августа',u'сентября',u'октября',u'ноября',u'декабря']

def ajaxpage(request):
    """
    Простой запрос возвращает страницу с сегодняшними событиями.
    Ajax + mode = 1 - возвращает данные для календаря
    Ajax + mode = 0 - возвращает данные для дня
    """
    filter_id = ''
    mode = ''
#####################################################################
## если Ajax, парсим входные данные. Иначе - получаем текущую дату ##
#####################################################################
    if request.is_ajax():

        date = request.GET.get('d','')
        year = int(request.GET['y'])
        offset = int(request.GET.get('o', 0 ))
        filter_id = request.GET.get('f', '' )
        mode = int(request.GET['mode'])


    #####################################################
    ## Если 1, парсим дату для месяца, иначе - для дня ##
    #####################################################
        if mode:
            if date:
                mon = decode_month[request.GET['m']]
            else:
                mon = decode_months[request.GET['m']]
        else:
            try:
                # запрос пришел с дня
                mon = decode_month[request.GET['m']]
            except KeyError:
                try:
                    # запрос пришел с календаря
                    mon = decode_months[request.GET['m']]
                except KeyError:
                    # запрос пришел с ячейки календаря
                    mon = int(request.GET['m'])

            in_date = datetime.date(year, mon, int(date))
            if offset:
                new_date = in_date + datetime.timedelta(days=offset)
            else:
                new_date = in_date

    else:
        new_date = datetime.date.today()

#################
## Парсим куки ##
#################
    cookies = request.COOKIES.get('item_filter', '')
    cookies_arr = cookies.split('|')
    if '' in cookies_arr:
        cookies_arr.remove('')

    if filter_id:
        if filter_id in cookies_arr:
            cookies_arr.remove(filter_id)
        else:
            cookies_arr.append(filter_id)

    if mode and request.is_ajax():
#######################################################
## Если условие верно, собираем данные для календаря ##
#######################################################

    ########################################################
    ## Выбираем, какой месяц отображаем с учетом смещения ##
    ########################################################
        present_date =    datetime.date(year, mon, 1)
        if offset:
            if offset > 0:
                pr_w, pr_m_d = calendar.monthrange(present_date.year, present_date.month)
                present_date = present_date + datetime.timedelta(days = pr_m_d)
            else:
                present_date = present_date - datetime.timedelta(days = 1)
                present_date = datetime.date(present_date.year, present_date.month, 1)

        print present_date

    ##################################################################################
    ## Получаем следующий и предыдущий месяц, количество дней и день недели 1 чисел ##
    ##################################################################################

        future_date = present_date + datetime.timedelta(hours=24*32)
        past_date = present_date - datetime.timedelta(days = 1)

        p_w, p_m_d = calendar.monthrange(past_date.year, past_date.month)
        pr_w, pr_m_d = calendar.monthrange(present_date.year, present_date.month)
        f_w, f_m_d = calendar.monthrange(future_date.year, future_date.month)

        present_date_end = datetime.date(present_date.year, present_date.month, pr_m_d)

        rez = []


    ##############################################################
    ## Получаем список дней предыдущего месяца на первой неделе ##
    ##############################################################

        day = p_m_d - pr_w
        year = past_date.year
        month = past_date.month

        for i in range(1,pr_w+1):
            rez.append([year, month, day+i, -1])

        year = present_date.year
        month = present_date.month
        date = '%s-%02d' % (year, month)


    ######################################################################
    ## Получаем список дней текущего месяца и количество событий на них ##
    ######################################################################

        for i in range(1,pr_m_d+1):
            search_date = '%s-%02d' % (date, i)
            count = Event.objects.filter(date_start__lte=search_date)\
.filter(date_end__gte=search_date).exclude(category__id__in=cookies_arr).count()
            rez.append([year, month, i, count])

    ################################################################
    ## Получаем список дней следующего месяца на последней неделе ##
    ################################################################
        year = future_date.year
        month = future_date.month

        if f_w:
            for i in range(1,8-f_w):
                rez.append([year, month, i, -1])

    #########################################################################
    ## Получаем общее количество событий, необходимые строковые переменные ##
    ## ставим куки, если они менялись. Возвращаем полученные данные        ##
    #########################################################################
        count = Event.objects.filter(date_start__lte=present_date_end).filter(date_end__gte=present_date)\
.exclude(category__id__in=cookies_arr).count()

        ######################################################################
        ## Дата обязательно начинается с 1 пробела! этот пробел при разборе ##
        ## строки в js идет в переменную day и все парсится правильно       ##
        ######################################################################
        month_year = u" %s %s г." % (encode_month[present_date.month], present_date.year)

        data = {'month_year':month_year, 'objects':rez, 'count':count}

        x = HttpResponse(json.dumps(data), content_type="application/json")
        if filter_id:
            x.set_cookie('item_filter', u'|'.join(cookies_arr), expires=future_date)

        return x

    else:
#############################################################################
## Если условие неверно, собираем данные для ajax дня или для сегодняшнего ##
#############################################################################


    ###############################################################################
    ## Получаем события за день, применяем pagination, генерим нужные переменные ##
    ###############################################################################
        obj = Event.objects.filter(date_start__lte=new_date)\
.filter(date_end__gte=new_date).order_by('-created','-date_start')\
.exclude(category__id__in=cookies_arr)

        len_obj = obj.count()

        obj = getPage(request, obj, 6)

        week = weekday[new_date.weekday()];
        month_year = u"%s %s" % (encode_month[new_date.month], new_date.year)
        date = u"%s %s %s г." % (new_date.day, encode_months[new_date.month], new_date.year)
        data = {'weekday': week,'month_year':month_year,'date':date,'big_num':new_date.day,'page':obj.number, 'has_next':obj.has_next(), 'has_prev':obj.has_previous(), 'len_obj':len_obj}


        if request.is_ajax():
        ####################################################################
        ## Если Ajax запрос, возращаем события, переменные в json формате ##
        ## Если простой запрос, рендерим шаблон и возвращаем его          ##
        ####################################################################

            rez_obj = []

            for i in obj.object_list:
                rez_obj.append([i.name, i.slug, str(i.picture)])

            data.update({'objects':rez_obj})
            x = HttpResponse(json.dumps(data), content_type="application/json")
            if filter_id:
                x.set_cookie('item_filter', u'|'.join(cookies_arr), expires=big_date)

            return x
        else:
            data.update({'objects':obj.object_list})
        return TemplateResponse(request,'test_month.html', data)


