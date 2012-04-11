"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client

class SimpleTest(TestCase):
    fixtures = ['login_user/fixtures/test_login.xml']
    def test_not_existing(self):
        response = self.client.post("/accounts/login/")
        assert(response._request.user.is_anonymous())
        response = self.client.post('/accounts/login/', {'username': 'john', 'password': 'smith'})
        assert(response._request.user.is_anonymous())

    def test_existing(self):
        response = self.client.post("/accounts/login/")
        assert(response._request.user.is_anonymous())
        response = self.client.post('/accounts/login/', {'username': 'testUser', 'password': '123'})
        self.assertRedirects(response, "/")


