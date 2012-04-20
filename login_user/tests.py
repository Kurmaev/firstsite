# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.test import TestCase
from django.contrib.auth.forms import AuthenticationForm
from django.conf import global_settings
from django.test.utils import override_settings

class SimpleTest(TestCase):
        
    def test_existing(self):
        
        User.objects.create_user("test2","test@test.com","passwd")
        response = self.client.post("/accounts/login/")
        assert(response._request.user.is_anonymous())
        response = self.client.post('/accounts/login/', {'username': 'test2', 
							'password': 'passwd'})
        self.assertRedirects(response, "/")


    def test_not_exsisting_username_form(self): 
        form = AuthenticationForm(data={'username': '',
                                        'password': 'alice@example.com',})
        self.failIf(form.is_valid())
        self.assertEqual(form.errors['username'],
                         [u"Обязательное поле."])


    def test_not_exsisting_password_form(self): 
        form = AuthenticationForm(data={'username': 'password',
                                        'password': '',})
        self.failIf(form.is_valid())
        self.assertEqual(form.errors['password'],
                         [u"Обязательное поле."]) 


    def test_not_exsisting_password_username_form(self): 
        form = AuthenticationForm(data={'username': '','password': '',})
        self.failIf(form.is_valid())
        self.assertEqual(form.errors['username'],
                         [u"Обязательное поле."])

        self.assertEqual(form.errors['password'],
                         [u"Обязательное поле."])


    def test_not_exsisting_form(self): 
        form = AuthenticationForm(data={'username': 'alice','password': 'alice',})
        self.failIf(form.is_valid())
        self.assertEqual(form.errors['__all__'],
                         [u'Пожалуйста, введите верные имя пользователя\
 и пароль. Помните, оба поля чувствительны к регистру.'])


    def test_not_exsisting(self): 
        response = self.client.post('/accounts/login/', 
                                    {'username': 'john', 'password': 'smith'})
        self.assertContains(response, u'Пожалуйста, введите верные имя пользователя\
 и пароль. Помните, оба поля чувствительны к регистру.', 
        count=None, status_code=200, html=False)


    def test_not_exsisting_password_username(self):
        with self.settings(LANGUAGE_CODE = 'ru-ru'): 
            response = self.client.post('/accounts/login/', 
                                        {'username': '', 'password': ''})
            self.assertContains(response, u"Обязательное поле.", 
            count=2, status_code=200, html=False)


    def test_not_exsisting_password(self): 
        response = self.client.post('/accounts/login/', 
                                    {'username': '123', 'password': ''})
        self.assertContains(response, u"Обязательное поле.", 
        count=None, status_code=200, html=False)


    def test_not_exsisting_username(self): 
        response = self.client.post('/accounts/login/', 
                                    {'username': '', 'password': '123'})
        self.assertContains(response, u"Обязательное поле.", 
        count=None, status_code=200, html=False)
