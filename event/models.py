from django.db import models

class Category(models.Model):
    shortname = models.CharField(max_length=10, unique=True)
    rusname = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=200)

    def __unicode__(self):
        return self.shortname

class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()   
    category = models.ForeignKey(Category)
    text = models.CharField(max_length=1024)
    picture = models.ImageField(upload_to='images/', blank=True)
    
    def get_category(self):
        return self.category.shortname
    get_category.short_description = 'category'

    def get_pic(self):
        if self.picture:
            return '<img id="'+str(self.id)+'" src="/'+ str(self.picture) +'" alt="" width="200" class="leftimg">'
        else:
            return ""

    get_pic.short_description = 'small pic'
    get_pic.allow_tags = True

    def __unicode__(self):
        return self.name
