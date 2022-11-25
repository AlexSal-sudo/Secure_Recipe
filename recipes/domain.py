from dataclasses import dataclass
import re
from django.core.exceptions import ValidationError
from typeguard import typechecked


@typechecked
@dataclass(frozen=True)
class Name:
    value: str

    def __post_init__(self):
        if not (0 < len(self.value) < 30):
            raise ValidationError("Name must be between 1-30 character")
        if not re.match(r'[a-zA-Z]', self.value):
            raise ValidationError("Name not valid")


@typechecked
@dataclass(frozen=True)
class Unit:
    value: str

    __myUnit = ["liters", "kilograms", "grams", "g", "l", "kg", "n/a"]

    def __post_init__(self):
        if not (0 < len(self.value) <= 10):
            raise ValidationError("Unit must be between 1-10 character")
        if not re.match(r'[a-zA-Z\/]', self.value):
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