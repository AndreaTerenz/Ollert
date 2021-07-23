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
    
    path('create_board/<str:name>/<str:cat>/<str:f>', views.create_board, name='make-board'),
    #path('create_scheda/<str:name>/<str:description>', views.create_scheda, name='make_scheda')
]
