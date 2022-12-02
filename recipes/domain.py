from dataclasses import dataclass, field
import re
from typing import List

from django.core.exceptions import ValidationError
from typeguard import typechecked


@typechecked
@dataclass(frozen=True)
class Name:
    value: str

    def __post_init__(self):
        if not (0 < len(self.value) < 30):
            raise ValidationError("Name must be between 1-30 character")
        if not re.match(r'^[a-zA-Z]+$', self.value):
            raise ValidationError("Name is not syntactically")


@typechecked
@dataclass(frozen=True)
class Title:
    value: str

    def __post_init__(self):
        if not (0 < len(self.value) < 30):
            raise ValidationError("Name must be between 1-30 character")
        if not re.match(r'^[a-zA-Z]+$', self.value):
            raise ValidationError("Name is not syntactically")


@typechecked
@dataclass(frozen=True)
class Unit:
    value: str

    __myUnit = ["g", "l", "kg", "n/a"]

    def __post_init__(self):
        if not (0 < len(self.value) <= 10):
            raise ValidationError("Unit must be between 1-10 character")
        if not re.match(r'^[a-zA-Z\/]', self.value):
            raise ValidationError("Unit not syntactically correct")
        if self.value.lower() not in self.__myUnit:
            raise ValidationError(f"Unit must be one of this: {self.__myUnit}")


@typechecked
@dataclass(frozen=True)
class Quantity:
    value: int

    def __post_init__(self):
        if not (0 < self.value <= 1000):
            raise ValidationError("Quantity must be between 1-1000")


@typechecked
@dataclass(frozen=True)
class Ingredient:
    name: Name
    quantity: Quantity
    unit: Unit

    @property
    def ingredient_name(self):
        return self.name

    @property
    def ingredient_quantity(self):
        return self.quantity

    @property
    def ingredient_unit(self):
        return self.unit

    def __eq__(self, other):
        return self.name == other.name


@typechecked
@dataclass(frozen=True)
class Description:
    value: str

    def __post_init__(self):
        if not (0 < len(self.value) < 100):
            raise ValidationError("Name must be between 1-100 character")
        if not re.match(r'^[a-zA-Z ,\.;]+$', self.value):
            raise ValidationError("Name is not syntactically")


@typechecked
@dataclass(frozen=True)
class Recipe:
    title: Title
    description: Description
    __list_of_ingredients: List[Ingredient] = field(default_factory=list, init=False)

    def check_if_has_ingredient(self, ingredient: Ingredient):
        return ingredient in self.__list_of_ingredients

    def add_ingredient(self, ingredient: Ingredient):
        self.__list_of_ingredients.append(ingredient)


def create_recipe_fromJSON(json_recipe: dict):
    recipe = Recipe(Title(json_recipe['title']), Description(json_recipe['description']))
    for ingredient in json_recipe['ingredient']:
        recipe.add_ingredient(create_ingredient_fromJSON(ingredient))


def create_ingredient_fromJSON(json_ingredient: dict):
    return Ingredient(Name(json_ingredient['name']), Quantity(json_ingredient['quantity']),
                      Unit(json_ingredient['unit']))
