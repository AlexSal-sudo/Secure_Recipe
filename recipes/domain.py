from dataclasses import dataclass, field
import re
from typing import List, Callable
from django.core.exceptions import ValidationError
from typeguard import typechecked


@typechecked
def pattern(regex: str) -> Callable[[str], bool]:
    r = re.compile(regex)

    def res(value):
        return bool(r.fullmatch(value))

    res._name_ = f'pattern({regex})'
    return res


@typechecked
@dataclass(frozen=True)
class Name:
    value: str

    def __post_init__(self):
        if not (0 < len(self.value) < 30):
            raise ValidationError("Name of the ingredient must be between 1-30 character")
        if not re.match(r'^[a-zA-ZÀ-ú ]+$', self.value):
            raise ValidationError("Name of the ingredient is not syntactically correct")


@typechecked
@dataclass(frozen=True)
class Unit:
    value: str

    __myUnit = ["g", "l", "kg", "n/a"]

    def __post_init__(self):
        if not (0 < len(self.value) <= 10):
            raise ValidationError("Unit of the ingredient must be between 1-10 character")
        if not re.match(r'^[a-zA-Z\/]', self.value):
            raise ValidationError("Unit of the ingredient not syntactically correct")
        if self.value.lower() not in self.__myUnit:
            raise ValidationError(f"Unit of the ingredient must be one of this: {self.__myUnit}")


@typechecked
@dataclass(frozen=True)
class Quantity:
    value: int

    def __post_init__(self):
        if not (0 < self.value <= 1000):
            raise ValidationError("Quantity of the ingredient must be between 1-1000")


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
            raise ValidationError("Description must be between 1-100 character")
        if not re.match(r'^\D+$', self.value):
            raise ValidationError("Description is not syntactically correct")


@typechecked
@dataclass(frozen=True)
class Title:
    value: str

    def __post_init__(self):
        if not (0 < len(self.value) < 30):
            raise ValidationError("Title must be between 1-30 character")
        if not re.match(r'^[a-zA-Z ]+$', self.value):
            print(self.value)
            raise ValidationError("Title is not syntactically correct")


@typechecked
@dataclass(frozen=True)
class Recipe:
    title: Title
    description: Description
    __list_of_ingredients: List[Ingredient] = field(default_factory=list, init=False)

    @typechecked()
    def has_name_in_ingredient(self, name: Name) -> bool:
        for ingredient in self.__list_of_ingredients:
            if ingredient.name == name:
                return True
        return False

    @typechecked()
    def add_ingredient(self, ingredient: Ingredient):
        self.__list_of_ingredients.append(ingredient)

    @typechecked()
    def remove_ingredient(self, ingredient: Ingredient):
        self.__list_of_ingredients.remove(ingredient)


@typechecked
def create_recipe_fromJSON(json_recipe: dict) -> Recipe:
    recipe = Recipe(Title(json_recipe['title']), Description(json_recipe['description']))
    for ingredient in json_recipe['ingredients']:
        recipe.add_ingredient(create_ingredient_fromJSON(ingredient))

    return recipe


@typechecked
def create_ingredient_fromJSON(json_ingredient: dict) -> Ingredient:
    return Ingredient(Name(json_ingredient['name'].lower()), Quantity(json_ingredient['quantity']),
                      Unit(json_ingredient['unit']))
