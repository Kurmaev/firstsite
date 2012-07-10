# -*- coding: utf-8 -*-
from celery.decorators import task, periodic_task

#@periodic_task(run_every=crontab(minute=0, hour=13)#подстроено под сервер,00 Омск
#def clear_cache():
#    from django.core.cache import cache
#    cache.clear()

#проверить на сервере
#@periodic_task(run_every=crontab(minute=0, hour=15)#02.00 Omsk
#def run_scrapy():
#    import subprocess
#    MY_PATH = os.path.dirname(__file__)
#    subprocess.call([os.path.join(MY_PATH,'run_scrapy.sh'),])
