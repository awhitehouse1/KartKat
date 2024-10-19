from django.db import models

# Create your models here.

class ShoppingList(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class ShoppingListItem(models.Model):
    shopping_list = models.ForeignKey(ShoppingList, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
