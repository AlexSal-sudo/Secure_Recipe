from typing import Callable
import re
from django.core.exceptions import ValidationError
from .domain import Unit, Name, Quantity, Ingredient


def validate_ingredient(list_of_ingredients: dict):
    for ingredient in list_of_ingredients:
        Ingredient(Name(ingredient), Quantity(list_of_ingredients[ingredient][0]),
                   Unit(list_of_ingredients[ingredient][1]))
