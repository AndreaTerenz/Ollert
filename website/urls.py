from django.urls import path

from website.views import *

urlpatterns = [
    path('', landing, name="landing_page"),
    path('board/<str:title>', board),
    path('board', board_debug), # TODO: puramente per debug, togliere appena non serve più
]
