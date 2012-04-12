# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.test import TestCase
from django.contrib.auth.forms import AuthenticationForm

class SimpleTest(TestCase):
    fixtures = ['login_user/fixtures/test_login.xml']

    def test_existing(self):
        response = self.client.post("/accounts/login/")
        assert(response._request.user.is_anonymous())
        response = self.client.post('/accounts/login/', {'username': 'testUser', 'password': '123'})
        self.assertRedirects(response, "/")

    def test_not_exsisting_username_form(self): 
        User.objects.create_user('alice', 'alice@example.com', 'secret')

        form = AuthenticationForm(data={'username': '',
                                        'password': 'alice@example.com',
})
        self.failIf(form.is_valid())
        self.assertEqual(form.errors['username'],
                         [u"Обязательное поле."])

    def test_not_exsisting_password_form(self): 
        User.objects.create_user('alice', 'alice@example.com', 'secret')

        form = AuthenticationForm(data={'username': 'password',
                                        'password': '',
})
        self.failIf(form.is_valid())
        self.assertEqual(form.errors['password'],
                         [u"Обязательное поле."]) 

    def test_not_exsisting_password_username_form(self): 
        User.objects.create_user('alice', 'alice@example.com', 'secret')

        form = AuthenticationForm(data={'username': '',
                                        'password': '',
})
        self.failIf(form.is_valid())
        self.assertEqual(form.errors['username'],
                         [u"Обязательное поле."])

        self.assertEqual(form.errors['password'],
                         [u"Обязательное поле."])

    def test_not_exsisting_form(self): 
        User.objects.create_user('alice', 'alice@example.com', 'secret')

        form = AuthenticationForm(data={'username': 'alice',
                                        'password': 'alice',
})
        self.failIf(form.is_valid())
        self.assertEqual(form.errors['__all__'],
                         [u'Пожалуйста, введите верные имя пользователя и пароль. Помните, оба поля чувствительны к регистру.'])


