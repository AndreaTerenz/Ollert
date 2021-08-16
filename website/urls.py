from django.urls import path, register_converter

from website.views import *
from . import views


urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('board/<str:name>', board, name="get-board"),
    path('register/', views.register_request, name="register"),
    path('login/', views.login_request, name="login"),
    path('profile/', views.profile, name="profile"),
    path('logout/', views.logout_request, name="logout"),
    
    path('create_board/', views.create_board, name='make-board'),
    path('delete_board/', views.delete_board, name='delete-board'),
    path('create_card/<str:board>', views.create_card, name='make_card'),
    path('edit/', views.change_password, name='change_password')
]
