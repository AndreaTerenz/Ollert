from django.urls import path

from website.views import *
from . import views

urlpatterns = [
    # GET
    path('', views.homepage, name="homepage"),
    path('board/<str:name>', board, name="get-board"),
    path('register', views.register_request, name="register"),
    path('login', views.login_request, name="login"),
    path('profile', views.profile, name="profile"),
    path('logout', views.logout_request, name="logout"),

    # POST
    path('create_board', views.create_board, name='make-board'),
    path('delete_board', views.delete_board, name='delete-board'),
    path('edit_board', views.edit_board, name="edit-board"),

    path('create_board_content', views.create_board_content, name='create-board-content'),
    path('delete_board_content', views.delete_board_content, name='delete-board-content'),
    path('edit_board_content', views.edit_board_content, name='edit-board-content'),

    path('create_category', views.create_category, name='create-category'),
    path('delete_category', views.delete_category, name='delete-category'),
    path('rename_category', views.rename_category, name='rename-category'),

    path('edit_password', views.change_password, name='edit-password')
]
