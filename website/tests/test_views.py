from django.contrib import auth
from django.contrib.auth import login
from django.test import TestCase, Client
from django.urls import reverse
from website.models import *
import json

from website.utils import get_username


class TestViews(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username="test1",
            email="test@test.com",
            password="7heg0rg8re7"
        )
        self.userProfile = UserProfile.objects.create(user=self.user)
        self.username = "testuser"
        self.email = "259723@studenti.unimore.it"
        self.password = "qw98745c"

    def test_register(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'access/register.html')

    def test_login(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'access/login.html')

    def test_create_board(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('make-board'), json.dumps({
            "name": "thnithroneppje",
            "description": "Board di prova",
            "category": "NaN",
            "favorite": True
        }), content_type="application/json")

        b:Board = Board.objects.get(name="thnithroneppje", description="Board di prova")
        self.assertEqual(b.name, "thnithroneppje")
        self.assertEqual(get_username(b.user), "test1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profile/profile-boards-list.html")
