from django.db import models

class Category(models.Model):
    shortname = models.CharField(max_length=10)
    description = models.CharField(max_length=200)


class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()   
    category = models.ManyToManyField(Category)
    text = models.CharField(max_length=1024)
    picture = models.ImageField(upload_to='/pic')
