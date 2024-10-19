from django.urls import path

from . import views

urlpatterns = [
    path("", views.shopping_list, name="index"),
    path('create-shopping-list/', views.create_shopping_list, name='create_shopping_list'),
]