from django.urls import path

from . import views

urlpatterns = [
    path("", views.shopping_list, name="index"),
    path('shopping-list/delete-item/<int:item_id>/', views.delete_item, name='delete_item'),
    path('shopping-list/delete-list/<int:list_id>/', views.delete_list, name='delete_list'),
    path('chatbot/', views.chatbot, name='chatbot'),
]