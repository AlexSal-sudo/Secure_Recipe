from django.core.validators import BaseValidator
from django.core.exceptions import ValidationError
from .domain import Unit, Name, Quantity, Ingredient
import jsonschema


def validate_ingredient(): pass


def unique_ingredients(list_of_ingredients: list):
    for i in range(len(list_of_ingredients) - 1):
        if list_of_ingredients[i]["name"] == list_of_ingredients[i + 1]["name"]:
            name = list_of_ingredients[i]["name"]
            raise ValidationError(f"Please, there is a redundant ingredient: {name.upper()}")


class JSONSchemaValidator(BaseValidator):
    def compare(self, value, schema):
        try:
            jsonschema.validate(value, schema)
        except jsonschema.exceptions.ValidationError as e:
            raise ValidationError(e.message)
