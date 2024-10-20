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

class GroceryItem(models.Model):
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=200)
    is_woman_owned = models.BooleanField()
    min_price = models.DecimalField(max_digits=10, decimal_places=2)
    max_price = models.DecimalField(max_digits=10, decimal_places=2)
    calories = models.IntegerField(default=0)
    protein = models.DecimalField(max_digits=5, decimal_places=2)
    fat = models.DecimalField(max_digits=5, decimal_places=2)
    carbs = models.DecimalField(max_digits=5, decimal_places=2)
    calcium = models.DecimalField(max_digits=5, decimal_places=2)
    vitamin_d = models.DecimalField(max_digits=5, decimal_places=2)
    vitamin_b12 = models.DecimalField(max_digits=5, decimal_places=2)
    type = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    name = models.CharField(max_length=200)
    ingredients = models.TextField()
    steps = models.TextField()

    def __str__(self):
        return self.name

class Inventory(models.Model):
    store_name = models.CharField(max_length=200)
    grocery_item = models.ForeignKey(GroceryItem, on_delete=models.CASCADE)  # Link to GroceryItem
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.store_name
    
class Reward(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    unlocked = models.BooleanField(default=False)
    link = models.CharField(max_length=200)

    def __str__(self):
        return self.name

