from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path('map/', views.map, name="map"),
]