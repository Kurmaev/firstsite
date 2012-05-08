# Scrapy settings for eventcrawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
import sys, os
from pprint import pprint as p

BOT_NAME = 'eventcrawler'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['eventcrawler.spiders']
NEWSPIDER_MODULE = 'eventcrawler.spiders'
USER_AGENT = 'Mozilla/5.0 (Ubuntu; X11; Linux x86_64; rv:9.0.1)\
 Gecko/20100101 Firefox/9.0.1 FirePHP/0.6'


CONCURRENT_REQUESTS = 1
DOWNLOAD_DELAY = 5


ITEM_PIPELINES = [
    'scrapy.contrib.pipeline.images.ImagesPipeline',
    'eventcrawler.pipelines.EventcrawlerPipeline',
    ]


def setup_django_env(path):
    import imp
    from django.core.management import setup_environ
    import os
    print path
    f, filename, desc = imp.find_module('settings', [path])
    project = imp.load_module('settings', f, filename, desc) 
    print '~'*100
    print project
    print dir(project)
    setup_environ(project)

current_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(current_dir, 'eventcrawler'))
django_app = os.path.join(current_dir, 'firstsite')
setup_django_env(django_app)

IMAGES_STORE = os.path.join(current_dir,'media','images')
