import pytest

from django.core.exceptions import ValidationError
from mixer.backend.django import mixer


def test_recipe_title_of_length_31_raise_exception(db):
    recipe = mixer.blend('recipes.Recipe', title='TEST' * 20)
    with pytest.raises(ValidationError) as err:
        recipe.full_clean()


def test_recipe_title_not_only_char_raise_exception(db):
    recipe = mixer.blend('recipes.Recipe', title='Test')
    with pytest.raises(ValidationError) as err:
        recipe.full_clean()


def test_recipe_description_of_length_101_raise_exception(db):
    recipe = mixer.blend('recipes.Recipe', description='T' * 101)
    with pytest.raises(ValidationError) as err:
        recipe.full_clean()


def test_recipe_description_not_only_char_raise_exception(db):
    recipe = mixer.blend('recipes.Recipe', description='T2316215EST')
    with pytest.raises(ValidationError) as err:
        recipe.full_clean()


def test_recipe_ingredients_not_array_type_raise_exception(db):
    recipe = mixer.blend('recipes.Recipe', ingredients="TEST")
    with pytest.raises(ValidationError) as err:
        recipe.full_clean()


def test_recipe_ingredients_without_name_raise_exception(db):
    recipe = mixer.blend('recipes.Recipe', ingredients=[{
        "unit": "g",
        "quantity": 40
    }])
    with pytest.raises(ValidationError) as err:
        recipe.full_clean()


def test_recipe_ingredients_without_unit_raise_exception(db):
    recipe = mixer.blend('recipes.Recipe', ingredients=[{
        "name": "test",
        "unit": "g",
        "quantity": 40
    }])
    with pytest.raises(ValidationError) as err:
        recipe.full_clean()
