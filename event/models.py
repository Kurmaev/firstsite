from django.db import models

class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    category = models.CharField(max_length=10)
    text = models.CharField(max_length=1024)
    picture = models.ImageField(upload_to='/pic')
