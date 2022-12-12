from dataclasses import dataclass, field, InitVar
import re
from datetime import date, datetime
from typing import List, Dict, Any, Optional
from django.core.exceptions import ValidationError
from typeguard import typechecked


@typechecked
@dataclass(frozen=True)
class Title:
    value: str

    def __post_init__(self):
        if not (0 < len(self.value) < 30):
            raise ValidationError("Title must be between 1-30 character")
        if not re.match(r'^[a-zA-Z ]+$', self.value):
            raise ValidationError("Title is not syntactically correct")


@typechecked
@dataclass(frozen=True)
class Description:
    value: str

    def __post_init__(self):
        if not (0 < len(self.value) < 500):
            raise ValidationError("Description must be between 1-500 character")
        if not re.match(r'^[a-zA-Z0-9À-ú \'!;.,\n]+$', self.value):
            raise ValidationError("Description is not syntactically correct")


@typechecked
@dataclass(frozen=True)
class Name:
    value: str

    def __post_init__(self):
        if not (0 < len(self.value) < 30):
            raise ValidationError("Name of the ingredient must be between 1-30 character")
        if not re.match(r'^[a-zA-ZÀ-ú ]+$', self.value):
            raise ValidationError("Name of the ingredient is not syntactically correct")

    def __eq__(self, other):
        return self.value.lower() == other.value.lower()


@typechecked
@dataclass(frozen=True)
class Quantity:
    value: int

    def __post_init__(self):
        if not (0 < self.value <= 1000):
            raise ValidationError("Quantity of the ingredient must be between 1-1000")


@typechecked
@dataclass(frozen=True)
class Unit:
    value: str

    __myUnit = ['kg', 'g', 'l', 'cl', 'ml', 'cup', 'n/a']

    def __post_init__(self):
        if not (0 < len(self.value) <= 3):
            raise ValidationError("Unit of the ingredient must be between 1-3 character")
        if self.value not in self.__myUnit:
            raise ValidationError(f"Unit of the ingredient must be one of this: {self.__myUnit}")


@typechecked
@dataclass(frozen=True)
class Ingredient:
    name: Name
    quantity: Quantity
    unit: Unit

    def __eq__(self, other):
        return self.name == other.name


@typechecked
@dataclass(frozen=True)
class Recipe:
    title: Title
    description: Description
    created_at: date
    __ingredients: List[Ingredient] = field(default_factory=list, repr=False, init=False)
    __map_of_ingredients: Dict[Name, Ingredient] = field(default_factory=dict, repr=False, init=False)
    create_key: InitVar[Any] = field(default='None')

    def __post_init__(self, create_key: Any):
        self.__check_key(create_key)

    def __check_key(self, create_key):
        if not Recipe.Builder.is_valid_key(create_key):
            raise ValidationError("Unable to create a recipe")

    def ingredients(self) -> int:
        return len(self.__ingredients)

    @typechecked()
    def ingredient(self, index: int) -> Ingredient:
        if not 0 <= index < len(self.__ingredients):
            raise ValidationError("There isn't this ingredient")
        return self.__ingredients[index]

    @typechecked()
    def has_name_in_ingredients(self, name: Name) -> bool:
        for ingredient in self.__ingredients:
            if ingredient.name == name:
                return True
        return False

    @typechecked()
    def _add_ingredient(self, ingredient: Ingredient, create_key: Any) -> None:
        self.__check_key(create_key)
        if ingredient.name in self.__map_of_ingredients:
            raise ValidationError("Please, there are two same ingredient")
        self.__ingredients.append(ingredient)
        self.__map_of_ingredients[ingredient.name] = ingredient

    @typechecked()
    def _has_at_least_one_ingredient(self) -> int:
        return len(self.__ingredients) >= 1

    @typechecked()
    def remove_ingredient(self, ingredient: Ingredient, create_key: Any) -> None:
        self.__check_key(create_key)
        if ingredient.name not in self.__map_of_ingredients:
            raise ValidationError("The ingredient is not contained in the recipe")
        self.__ingredients.remove(ingredient)
        del self.__map_of_ingredients[ingredient.name]

    @typechecked
    @dataclass()
    class Builder:
        __recipe: Optional['Recipe']
        __create_key = object()

        def __init__(self, title: Title, description: Description, created_at: date):
            self.__recipe = Recipe(title, description, created_at, self.__create_key)

        @staticmethod
        def is_valid_key(key: Any) -> bool:
            return key == Recipe.Builder.__create_key

        @typechecked()
        def with_ingredient(self, ingredient: Ingredient) -> 'Recipe.Builder':
            if not self.__recipe:
                raise ValidationError("Unable to create the recipe")
            self.__recipe._add_ingredient(ingredient, self.__create_key)
            return self

        @typechecked()
        def with_out_ingredient(self, ingredient: Ingredient) -> 'Recipe.Builder':
            if not self.__recipe:
                raise ValidationError("Unable to create the recipe")
            self.__recipe.remove_ingredient(ingredient, self.__create_key)
            return self

        @typechecked()
        def build(self) -> 'Recipe':
            if not self.__recipe:
                raise ValidationError("Unable to create the recipe")
            if not self.__recipe._has_at_least_one_ingredient():
                raise ValidationError("Please insert at least one ingredient")
            final_recipe, self.__recipe = self.__recipe, None
            return final_recipe


@typechecked
@dataclass(frozen=True)
class JsonHandler:
    @staticmethod
    def create_ingredients_from_json(ingredient) -> Ingredient:
        return Ingredient(Name(ingredient['name']), Quantity(ingredient['quantity']), Unit(ingredient['unit']))

    @staticmethod
    def create_recipe_from_json(json):
        new_recipe = Recipe.Builder(Title(json['title']), Description(json['description']),
                                    datetime.strptime(json['created_at'], '%Y-%m-%d').date())
        for ingredient in json['ingredients']:
            new_recipe = new_recipe.with_ingredient(JsonHandler.create_ingredients_from_json(ingredient))
        new_recipe = new_recipe.build()
        return new_recipe
