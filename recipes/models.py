from django.contrib.auth import get_user_model
from django.db import models

from .domain import Name
from .validators import validate_ingredient
import jsonfield


class Recipe(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ingredients = jsonfield.JSONField(default=dict, validators=[validate_ingredient])
    print(ingredients.)

    # steps = ArrayField(models.CharField(max_length=160))
    def __str__(self):
        return self.title
