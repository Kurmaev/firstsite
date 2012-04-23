# -*- coding: utf-8 -*-
from event.models import Event
from django.test import TestCase
import datetime
from django.contrib.auth.models import User       
from django.utils import formats
from django.utils.translation import activate

class HomepageTestCase(TestCase):
    fixtures = ['test_home.xml']
    
    def test_view_today_event(self):
        x = Event.objects.get(name="Балет")
        x.date = datetime.date.today()
        x.save()

        x = Event.objects.get(name="Titanes")
        x.date = datetime.date.today() + datetime.timedelta(1)
        x.save()

        response = self.client.get("/") 
        
        self.assertContains(response, "Балет")
        self.assertContains(response, "Titanes")


        str_response = str(response)
        future_string = str_response.find("<h3>Cобытия, которые нас ждут\
   в ближайшем будущем:</h3>")
        today_event = str_response.find(">Балет</a>")
        future_event = str_response.find(">Titanes</a>")

        self.failIf( today_event > future_event)
        self.failIf( future_string > future_event)
        self.failIf( today_event > future_event)

    def test_view_past_event(self):
        x = Event.objects.get(name="Балет")
        x.date = datetime.date.today() + datetime.timedelta(-1)
        x.save()
        response = self.client.get("/")
        self.assertNotContains(response, "Балет")

class AddEventTestCase(TestCase):
    def setUp(self):
        User.objects.create_user("test2","test@test.com","passwd")
        response = self.client.post('/accounts/login/', {'username': 'test2', 
							'password': 'passwd'})
        self.assertRedirects(response, "/")
        activate('ru-ru')

    def tearDown(self):
        self.client.post('/accounts/logout/')
        activate('en-us')

    def test_add_ok_data(self):
        today = datetime.date.today() 
        response = self.client.post('/add_event/', {'name':'uniquename',
'date':today,'category':1,'text':'this is test text'})
        self.assertContains(response, u"Событие успешно добавлено!")

        response = self.client.post('/events/uniquename/')
        formated_today =  formats.date_format(today, 'DATE_FORMAT')
 
        self.assertContains(response, formated_today, count=3, status_code=200,
                             html=False)
        self.assertContains(response, 'Uniquename',status_code=200, html=False)
        self.assertContains(response, 'test2',status_code=200, html=False)
        self.assertContains(response, 'this is test text',status_code=200, 
                            html=False)

    def test_add_2times_name(self):
        response = self.client.post('/add_event/', {'name':'uniquename',
'date':'20.12.2012','category':1,'text':'this is test text'})
        self.assertContains(response, u"Событие успешно добавлено!")

        response = self.client.post('/add_event/', {'name':'uniquename',
'date':'20.12.2012','category':1,'text':'this is test text'})
        self.assertNotContains(response, u"Событие успешно добавлено!")

        self.assertContains(response, u"Event с таким Name уже существует.")

    def test_add_empty_data(self):
        response = self.client.post('/add_event/', {'name':'',
'date':'','category':'','text':''})
        self.assertContains(response, u"Обязательное поле.", count=4)

    def test_add_wrong_date(self):
        response = self.client.post('/add_event/', {'name':'',
'date':'123456','category':'','text':''})
        self.assertContains(response, u"Введите правильную дату.")

    def test_not_login(self):
        self.client.post('/accounts/logout/')
        response = self.client.post('/add_event/')
        self.failIf(response.status_code==200)
