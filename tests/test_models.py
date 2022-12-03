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


def test_recipe_ingredients_empty_array_raise_exception(db):
    recipe = mixer.blend('recipes.Recipe', ingredients=[])
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
        "quantity": 40
    }])
    with pytest.raises(ValidationError) as err:
        recipe.full_clean()


def test_recipe_ingredients_without_quantity_raise_exception(db):
    recipe = mixer.blend('recipes.Recipe', ingredients=[{
        "name": "test",
        "unit": "g",
    }])
    with pytest.raises(ValidationError) as err:
        recipe.full_clean()


def test_recipe_ingredients_name_not_only_char_raise_exception(db):
    recipe = mixer.blend('recipes.Recipe', ingredients=[{
        "name": "23test32",
        "unit": "g",
        "quantity": 40
    }])
    with pytest.raises(ValidationError) as err:
        recipe.full_clean()


def test_recipe_ingredients_name_of_length_31_raise_exception(db):
    recipe = mixer.blend('recipes.Recipe', ingredients=[{
        "name": "A"*31,
        "unit": "g",
        "quantity": 40
    }])
    with pytest.raises(ValidationError) as err:
        recipe.full_clean()


def test_recipe_ingredients_quantity_of_1001_raise_exception(db):
    recipe = mixer.blend('recipes.Recipe', ingredients=[{
        "name": "test",
        "unit": "g",
        "quantity": 1001
    }])
    with pytest.raises(ValidationError) as err:
        recipe.full_clean()


def test_recipe_ingredients_quantity_is_string_raise_exception(db):
    recipe = mixer.blend('recipes.Recipe', ingredients=[{
        "name": "test",
        "unit": "g",
        "quantity": "20"
    }])
    with pytest.raises(ValidationError) as err:
        recipe.full_clean()


def test_recipe_ingredients_unit_different_from_g_kg_l_na_raise_exception(db):
    recipe = mixer.blend('recipes.Recipe', ingredients=[{
        "name": "test",
        "unit": "test",
        "quantity": 20
    }])
    with pytest.raises(ValidationError) as err:
        recipe.full_clean()
