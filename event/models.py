# -*- coding: utf-8 -*-
from django.db import models
from pytils.translit import slugify
import datetime
from lxml.html.clean import Cleaner

class Category(models.Model):
    shortname = models.CharField(max_length=10, unique=True)
    rusname = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=200)

    def __unicode__(self):
        return self.shortname

class Event(models.Model):
    name = models.CharField(max_length=100, unique=True)
    date_start = models.DateField()
    date_end = models.DateField(blank=True)
    category = models.ForeignKey(Category)
    text = models.CharField(max_length=5000)
    place = models.CharField(max_length=512,blank=True, \
                                verbose_name="Where and which time")
    picture = models.ImageField(upload_to='images/', blank=True)
    slug = models.SlugField(max_length=100, editable=False, blank=True,
                            unique=True)
    created = models.DateField(auto_now_add=True)
    changed = models.DateField(auto_now=True)
    added_by = models.CharField(max_length=100,editable=False, blank=True)

    def get_category(self):
        return self.category.shortname
    get_category.short_description = 'category'

    def save(self, *args, **kwargs):
        self.clean()
        self.slug = slugify(self.name)
        super(Event, self).save(*args, **kwargs)

    def clean(self):
        from django.core.exceptions import ValidationError
        #удаление лишних пробелов из имени
        new_name = self.name
        new_name = new_name.split()
        self.name = ' '.join(new_name)
        #sanitize html
        if self.text:
        #если текста нет, ошибка уже будет поймана
            c = Cleaner(allow_tags=['b','p','br','a','div','strong'], 
                                    remove_unknown_tags=False)
            self.text = c.clean_html(self.text)
        #replace <b> tag 
        #self.text = self.text.replace('<b>','<strong>')
        #self.text = self.text.replace('</b>','</strong>')
        #check or set date_end
        if self.date_end:
            if self.date_start > self.date_end:
                raise ValidationError('date end early than date start')
        else:
            self.date_end = self.date_start

    def is_today(self):
        return (self.date_start == datetime.date.today()) &\
                 (self.date_end == datetime.date.today())
    def is_one_day(self):
        return (self.date_start == self.date_end) 

    def __unicode__(self):
        return self.name
