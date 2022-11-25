from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.db import models


class Ingredient(models.Model):
    product = models.CharField(max_lenght=25)
    quantity = models.PositiveIntegerField(default=0)


class Recipe(models.Model):
    title = models.CharField(max_lenght=50)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ingredients = ArrayField(Ingredient)
    steps = ArrayField(models.CharField(max_length=160))

    def __str__(self):
        return self.title
