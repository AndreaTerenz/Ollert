from django.test import SimpleTestCase
from website.views import *
from django.urls import reverse, resolve


class TestUrls(SimpleTestCase):

    def test_homepage_url_is_resolved(self):
        url = reverse('homepage')
        print(resolve(url))
        self.assertEqual(resolve(url).func, homepage)

    def test_register_url_is_resolved(self):
        url = reverse('register')
        print(resolve(url))
        self.assertEqual(resolve(url).func, register_request)

    def test_login_url_is_resolved(self):
        url = reverse('login')
        print(resolve(url))
        self.assertEqual(resolve(url).func, login_request)

    def test_create_board_url_is_resolved(self):
        url = reverse('make-board')
        print(resolve(url))
        self.assertEqual(resolve(url).func, create_board)


