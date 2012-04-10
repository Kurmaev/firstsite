"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client

class SimpleTest(TestCase):
    fixtures = ['login_user/test_login.xml']
    def setUp(self):      
        self.c = Client()

    def test_not_existing(self):
        response = self.c.post("/accounts/login/")
        assert(response._request.user.is_anonymous())
        response = self.c.post('/accounts/login/', {'username': 'john', 'password': 'smith'})
        assert(response._request.user.is_anonymous())

    def test_existing(self):
        response = self.c.post("/accounts/login/")
        assert(response._request.user.is_anonymous())
        response = self.c.post('/accounts/login/', {'username': 'testUser', 'password': '123'})
        print response
        self.assertRedirects(response, "/")


