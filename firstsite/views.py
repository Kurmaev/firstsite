from django.template.response import TemplateResponse
from event.models import Event
import datetime

def randpage(request):
    #FIXME: Rewrite this
    today = datetime.date.today()

#    raw_sql = '(select t1.id, name, slug, text, date_start, date_end, picture \
#FROM event_event as t1 JOIN (SELECT max(ID)*RAND() AS ID FROM event_event) AS t2\
# ON t1.ID >= t2.ID where date_end>= "%s" LIMIT 1)' % (today.isoformat()) 

#    list_events = Event.objects.raw(' UNION '.join((raw_sql,raw_sql,raw_sql,
#                                                           raw_sql,raw_sql)))

    list_events = Event.objects.raw('select * from event_event where date_end>=\
"%s" order by rand() LIMIT 5'% (today.isoformat()))

    return TemplateResponse(request,'main/home.html',{'list_events':list_events,})
