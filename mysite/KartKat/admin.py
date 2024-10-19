from django.contrib import admin
from KartKat.models import GroceryItem, ShoppingList, Inventory

# Register your models here.
admin.site.register(ShoppingList)
admin.site.register(GroceryItem)
admin.site.register(Inventory)