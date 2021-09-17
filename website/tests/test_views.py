from django.contrib import auth
from django.contrib.auth import login
from django.test import TestCase, Client
from django.urls import reverse
from icecream import ic

from website.models import *
import json

from website.utils import *


class TestViews(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username="test1",
            email="test@test.com",
            password="7heg0rg8re7"
        )
        self.userProfile = UserProfile.objects.create(user=self.user)

    def test_register(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'access/register.html')

    def test_login(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'access/login.html')

    def test_board_list(self):
        self.client.force_login(self.user)

        board_data = {
            "name": "test-board",
            "description": "Board di prova",
            "category": "NaN",
            "favorite": True
        }

        # Creazione board
        response = self.client.post(reverse('make-board'), json.dumps(board_data), content_type="application/json")
        b: Board = Board.objects.get(name=board_data["name"], user=self.userProfile)

        self.assertEqual(b.name, board_data["name"])
        self.assertEqual(get_username(b.user), "test1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profile/profile-boards-list.html")
        #

        # Creazione lista
        list_data = {
            "target_type": "list",
            "owner": self.user.username,
            "target_id": {
                "target_id_board": board_data["name"]
            },
            "new_data": {
                "list_name": "test-list"
            }
        }

        response = self.client.post(reverse('create-board-content'), json.dumps(list_data),
                                    content_type="application/json")

        b: Board = Board.objects.get(name=board_data["name"], user=self.userProfile)
        l: List = get_list_in_board(0, b)

        self.assertIsNotNone(l)
        self.assertEqual(b.lists_count, 1)
        self.assertEqual(l.title, list_data["new_data"]["list_name"])
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "board/list.html")
        #

        # Eliminazione board
        response = self.client.post(reverse('delete-board'), json.dumps({"name": board_data["name"]}),
                                    content_type="application/json")

        self.assertIsNone(get_board(name=board_data["name"], user=self.userProfile))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profile/profile-boards-list.html")
        #

    def test_new_category(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse('create-category'), json.dumps({
            "new_cat_name": "test-category"
        }), content_type="application/json")

        self.assertIsNotNone(Category.objects.get(name="test-category", user=self.userProfile))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profile/profile-category-list.html")
