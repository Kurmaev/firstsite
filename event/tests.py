# -*- coding: utf-8 -*-
from event.models import Event, Category
from django.test import TestCase
import datetime
from django.contrib.auth.models import User
from django.utils import formats
from django.utils.translation import activate
from django.core.urlresolvers import reverse

class AddEventTestCase(TestCase):
    def setUp(self):
        User.objects.create_user("test2","test@test.com","passwd")
        response = self.client.post('/accounts/login/', {'username': 'test2', 
                                    'password': 'passwd'})
        self.assertRedirects(response, "/")
        activate('ru-ru')
        self.page_add = reverse('add_event')
        self.category = Category(shortname = u"cinema", rusname = u"Кино",
description = u"Все о кино и кинотеатрах")
        self.category.save()

    def tearDown(self):
        self.client.post('/accounts/logout/')
        activate('en-us')

    def test_add_ok_data(self):
        today = datetime.date.today() 
        response = self.client.post(self.page_add, {'name':'uniquename',
                    'date_start':today,'date_end':today,'category':1,
                    'text':'this is test text'})
        self.assertRedirects(response, reverse('view_more', args=('uniquename',)))

        response = self.client.post(reverse('view_more', args=('uniquename',)))
        formated_today =  formats.date_format(today, 'DATE_FORMAT')
 
        self.assertContains(response, formated_today, count=3, status_code=200,
                             html=False)
        self.assertContains(response, 'Uniquename',status_code=200, html=False)
        self.assertContains(response, 'test2',status_code=200, html=False)
        self.assertContains(response, 'this is test text',status_code=200, 
                            html=False)

    def test_add_2times_name(self):
        response = self.client.post(self.page_add, {'name':'uniquename',
            'date_start':'20.12.2012','date_end':'20.12.2012',
            'category':1,'text':'this is test text'})
        self.assertRedirects(response, reverse('view_more', args=('uniquename',)))

        response = self.client.post(self.page_add, {'name':'uniquename',
            'date_start':'20.12.2012','date_end':'20.12.2012',
            'category':1, 'text':'this is test text'})

        self.assertContains(response, u"Event с таким Name уже существует.")

    def test_add_empty_data(self):
        response = self.client.post(self.page_add, {'name':'',
'date_start':'','category':'','text':''})
        self.assertContains(response, u"Обязательное поле.", count=4)

    def test_add_wrong_date(self):
        response = self.client.post(self.page_add, {'name':'',
'date_start':'123456','category':'','text':''})
        self.assertContains(response, u"Введите правильную дату.")

    def test_not_login(self):
        self.client.post('/accounts/logout/')
        response = self.client.post(self.page_add)
        self.failIf(response.status_code==200)


#class HomepageTestCase(TestCase):
#    def setUp(self):
#        self.category = Category(shortname = u"cinema", rusname = u"Кино",
#description = u"Все о кино и кинотеатрах")
#        self.category.save()


#    def test_view_today_event(self):
#        x = Event(name=u"Балет", text=u"123", date_start=datetime.date.today(), 
#                    date_end=datetime.date.today(),category=self.category, 
#                    added_by=u'admin')
#        x.created = 
#        x.save()

#        y = Event(name=u"Titanes", text=u"456",
#                    date_start=datetime.date.today() + datetime.timedelta(1), 
#                    date_end=datetime.date.today() + datetime.timedelta(1), 
#                    category=self.category, added_by=u'admin')
#        y.save()

#        response = self.client.get("/") 
#        print response
#        self.assertContains(response, "Балет")
#        self.assertContains(response, "Titanes")
#        self.assertContains(response, 'today">')

#        str_response = str(response)
#        today_string = str_response.find('today">')
#        today_event = str_response.find(">Балет</a>")

#        self.failIf( future_event < today_string )
#        self.failIf( today_event < today_string)
#        self.failIf( future_event < today_event)

#    def test_view_past_event(self):
#        x = Event(name=u"Балет", text=u"123", date_start=datetime.date.today(), 
#                    date_end=datetime.date.today()+ datetime.timedelta(-1),
#                    category=self.category, added_by=u'admin')
#        x.save()
#        response = self.client.get("/")
#        self.assertNotContains(response, "Балет")

