from django.template.response import TemplateResponse
from event.models import Event
import datetime

def randpage(request):
    today = datetime.date.today()
### Delete after show!!!!
    from django.core.cache import cache
    cache.clear()
    list_events = Event.objects.raw('select * from event_event where date_end>=\
"%s" order by rand() LIMIT 5'% (today.isoformat()))

    return TemplateResponse(request,'main/home.html',{'list_events':list_events,})
