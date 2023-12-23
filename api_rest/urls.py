from django.contrib import admin
from django.urls import path, include
from api_rest.api import viewsets

urlpatterns = [
    path('link-search/<str:chavepix>', viewsets.get_chave_pix),
    path('send-pix/', viewsets.send_pix),
    path('get-pix/<str:endtoend>', viewsets.get_lan_pix),
]