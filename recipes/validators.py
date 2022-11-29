from django.core.validators import BaseValidator
from django.core.exceptions import ValidationError
from .domain import Unit, Name, Quantity, Ingredient
import jsonschema


def unique_ingredients(list_of_ingredients: list):
    for i in range(len(list_of_ingredients)):
        for j in range(len(list_of_ingredients)):
            if i != j and list_of_ingredients[i]['name'] == list_of_ingredients[j]['name']:
                raise ValidationError(
                    f"There are some redundant ingredients! <{list_of_ingredients[i]['name'].upper()}>")


class JSONSchemaValidator(BaseValidator):
    def compare(self, value, schema):
        try:
            jsonschema.validate(value, schema)
        except jsonschema.exceptions.ValidationError as e:
            raise ValidationError(e.message)
