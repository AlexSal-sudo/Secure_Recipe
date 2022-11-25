from django.contrib import admin
from recipes.models import Ingredient
from recipes.models import Recipe

admin.site.register(Ingredient)
admin.site.register(Recipe)
