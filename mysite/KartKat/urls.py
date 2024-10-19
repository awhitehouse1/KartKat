from django.contrib import admin
from django.urls import path,include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    path('app/',include('auth_app.urls')),

    path('', TemplateView.as_view(template_name='index.html'), name="index"),
    path('accounts/', include('allauth.urls')),
    path('logout', LogoutView.as_view()),
    path("", views.index, name="index"),
    path("", views.shopping_list, name="index"),
    path('shopping-list/delete-item/<int:item_id>/', views.delete_item, name='delete_item'),
    path('shopping-list/delete-list/<int:list_id>/', views.delete_list, name='delete_list'),
]