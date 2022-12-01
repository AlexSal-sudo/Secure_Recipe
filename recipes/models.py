from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import JSONField

from .validators import check_not_none_and_unique_ingredients, JSONSchemaValidator

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
    ingredients = JSONField(default=list,
                            validators=[JSONSchemaValidator(limit_value=INGREDIENTS_SCHEMA),
                                        check_not_none_and_unique_ingredients])

    def __str__(self):
        return self.title


