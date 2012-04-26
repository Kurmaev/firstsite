# -*- coding: utf-8 -*-
from django.db import models
from pytils.translit import slugify
import datetime

class Category(models.Model):
    shortname = models.CharField(max_length=10, unique=True)
    rusname = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=200)

    def __unicode__(self):
        return self.shortname

class Event(models.Model):
    name = models.CharField(max_length=100, unique=True)
    date = models.DateField()   
    category = models.ForeignKey(Category)
    text = models.CharField(max_length=1024)
    picture = models.ImageField(upload_to='images/', blank=True)
    slug = models.SlugField(max_length=100, editable=False, blank=True, unique=True)
    created = models.DateField(auto_now_add=True)
    changed = models.DateField(auto_now=True)
    added_by = models.CharField(max_length=100,editable=False, blank=True)

    def get_category(self):
        return self.category.shortname
    get_category.short_description = 'category'
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Event, self).save(*args, **kwargs)
    
    def clean(self):
        new_name = self.name
        new_name = new_name.lower().capitalize().split()
        self.name = ' '.join(new_name)

    def is_today(self):
        if (self.date == datetime.date.today()):
            return True
        else:
            return False
        
    def __unicode__(self):
        return self.name
