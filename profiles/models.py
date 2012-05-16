# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    birthday = models.DateField(blank=True, verbose_name="Дата рождения")
    view_birthday = models.BooleanField(default=True, 
                                        verbose_name="Дата рождения видна всем")

    about = models.CharField(max_length=300,
                                verbose_name="О себе", blank=True)

    def get_absolute_url(self):
        return ('profiles_profile_detail', (), { 'username': self.user.username })
    get_absolute_url = models.permalink(get_absolute_url)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
