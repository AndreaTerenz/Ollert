from django.urls import path

from website.views import *
from . import views

urlpatterns = [
    path('', landing, name="landing_page"),
    path('board/<str:title>', board),
    path('board', board_debug), # TODO: puramente per debug, togliere appena non serve più
    path('register/', views.registrationPage),

]
