from django.db import models

# Create your models here.
class GroceryItem(models.Model):
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=200)
    is_woman_owned = models.BooleanField()
    min_price = models.FloatField(max_digits=10, decimal_places=2)
    max_price = models.FloatField(max_digits=10, decimal_places=2)
    calories = models.IntegerField(default=0)
    protein = models.FloatField(max_length=5, decimal_places=2)
    fat = models.FloatField(max_length=5, decimal_places=2)
    carbs = models.FloatField(max_length=5, decimal_places=2)
    calcium = models.FloatField(max_length=5, decimal_places=2)
    vitamin_d = models.FloatField(max_length=5, decimal_places=2)
    vitamin_b12 = models.FloatField(max_length=5, decimal_places=2)
    type = models.CharField(max_length=200)