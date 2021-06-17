from django.urls import path

from website.views import *
from . import views

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('board/<str:title>', board),
    path('board', board_debug), # TODO: puramente per debug, togliere appena non serve più
    path('register/', views.register_request, name="register"),
    path('login/', views.login_request, name="login"),
    path('profile/', views.profile, name="profile"),
    path('logout/', views.logout_request, name="logout"),
    #path('homepage/', views.homepage, name="homepage"),

]
