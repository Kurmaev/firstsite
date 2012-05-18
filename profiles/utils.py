# -*- coding: utf-8 -*-
"""
Utility functions for retrieving and generating forms for the
site-specific user profile model specified in the
``AUTH_PROFILE_MODULE`` setting.

"""
from django.contrib.auth.models import User
from django import forms
from django.conf import settings
from django.db.models import get_model

from django.contrib.auth.models import SiteProfileNotAvailable


def get_profile_model():
    """
    Return the model class for the currently-active user profile
    model, as defined by the ``AUTH_PROFILE_MODULE`` setting. If that
    setting is missing, raise
    ``django.contrib.auth.models.SiteProfileNotAvailable``.
    
    """
    if (not hasattr(settings, 'AUTH_PROFILE_MODULE')) or \
           (not settings.AUTH_PROFILE_MODULE):
        raise SiteProfileNotAvailable
    profile_mod = get_model(*settings.AUTH_PROFILE_MODULE.split('.'))
    if profile_mod is None:
        raise SiteProfileNotAvailable   
    return profile_mod

def get_profile_form():
    """
    Return a form class (a subclass of the default ``ModelForm``)
    suitable for creating/editing instances of the site-specific user
    profile model, as defined by the ``AUTH_PROFILE_MODULE``
    setting. If that setting is missing, raise
    ``django.contrib.auth.models.SiteProfileNotAvailable``.
    
    """
    profile_mod = get_profile_model()

    class _ProfileForm(forms.ModelForm):

        first_name = forms.CharField(label="Фамилия",help_text='',required=False)
        last_name = forms.CharField(label="Имя",help_text='',required=False)

        class Meta:
            model = profile_mod
            exclude = ('user',)
            fields = ('first_name', 'last_name', 'birthday', 'view_birthday',
                                'about')
            widgets = {
                'about': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
                'birthday': forms.DateInput(attrs={'class':'date-pick'}),
            }

        def __init__(self, *args, **kwargs):
            super(_ProfileForm, self).__init__(*args, **kwargs)
            try:
                self.fields['first_name'].initial = self.instance.user.first_name
                self.fields['last_name'].initial = self.instance.user.last_name
            except User.DoesNotExist:
                pass

        def save(self, *args, **kwargs):
            """
            Update the primary email address on the related User object as well.
            """
            self.clean_first_name = self.cleaned_data.get('first_name','')
            self.clean_last_name = self.cleaned_data.get('last_name','')
            u = self.instance.user
            if self.clean_first_name:
                u.first_name = self.clean_first_name
            if self.clean_last_name:
                u.last_name = self.clean_last_name
            if (self.clean_first_name or self.clean_last_name):
                u.save()
            profile = super(_ProfileForm, self).save(*args,**kwargs)
            return profile
    return _ProfileForm
