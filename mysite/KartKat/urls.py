from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [

    path('app/',include('auth_app.urls')),

    path('accounts/', include('allauth.urls')),
    path('add_item/', views.shopping_list, name='add_item'),
    path('logout', views.logout_view, name='logout'),
    path("", views.shopping_list, name="index"),
    path('shopping-list/delete-item/<int:item_id>/', views.delete_item, name='delete_item'),
    path('shopping-list/delete-list/<int:list_id>/', views.delete_list, name='delete_list'),
    path('delete-crossed-off-items/', views.delete_crossed_off_items, name='delete_crossed_off_items'),
    path('map/', views.map, name="map"),
    path("rewards", views.rewards, name="rewards"),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('save-recipe/', views.save_recipe, name='save_recipe'),
    path('recipes/', views.recipe_list, name='recipe_list'),
    path('delete-recipe/<int:recipe_id>/', views.delete_recipe, name='delete_recipe'),
]