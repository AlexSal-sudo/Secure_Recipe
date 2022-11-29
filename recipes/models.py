from django.contrib.auth import get_user_model
from django.db import models
from django.core.exceptions import ValidationError

from .validators import unique_ingredients, JSONSchemaValidator
import jsonfield

INGREDIENTS_SCHEMA = {
    "schema": "http://json-schema.org/draft-07/schema#",
    "description": "The ingredients list",
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "name": {"description": "The name of the ingredient", "type": 'string', 'minLen': 1, 'maxLen': 30,
                     'pattern': "^[a-zA-Z]+$"},
            "quantity": {"description": "The quantity of the ingredient", "type": 'number', "minimum": 0,
                         "maximum": 1000},
            "unit": {"description": "The unit of the ingredient", "type": 'string',
                     'enum': ["g", "l", "kg", "n/a"]}
        },
        "required": ["name", "quantity", "unit"],
        "maxProperties": 3
    },
    "minItems": 1
}


class Recipe(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ingredients = jsonfield.JSONField(default=list,
                                      validators=[JSONSchemaValidator(limit_value=INGREDIENTS_SCHEMA),
                                                  unique_ingredients])

    def __str__(self):
        return self.title

    def clean(self):
        if not self.ingredients:
            raise ValidationError("Please add at least one ingredient")
        super(Recipe, self).clean()

    def save(self, *args, **kwargs):
        if not self.is_cleaned:
            self.full_clean()
        super(Recipe, self).save(*args, **kwargs)
