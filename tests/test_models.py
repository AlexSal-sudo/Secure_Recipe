import pytest

from django.core.exceptions import ValidationError
from mixer.backend.django import mixer


@pytest.fixture()
def ingredient():
    yield [{"name": "Eggs", "unit": "g", "quantity": 20}]


def test_recipe_title_of_length_31_raise_exception(db, ingredient):
    recipe = mixer.blend('recipes.Recipe', title='TEST' * 20, description='TEST', ingredients=ingredient)
    with pytest.raises(ValidationError) as err:
        recipe.full_clean()


def test_recipe_title_not_only_char_raise_exception(db, ingredient):
    recipe = mixer.blend('recipes.Recipe', title='Test1231', description='TEST', ingredients=ingredient)
    with pytest.raises(ValidationError) as err:
        recipe.full_clean()


def test_recipe_description_of_length_501_raise_exception(db, ingredient):
    recipe = mixer.blend('recipes.Recipe', title='Test', description='TEST' * 501, ingredients=ingredient)
    with pytest.raises(ValidationError) as err:
        recipe.full_clean()


def test_recipe_ingredients_not_array_type_raise_exception(db):
    recipe = mixer.blend('recipes.Recipe', title='Test', description='TEST', ingredients="TEST")
    with pytest.raises(ValidationError) as err:
        recipe.full_clean()


def test_recipe_ingredients_empty_array_raise_exception(db):
    recipe = mixer.blend('recipes.Recipe', title='Test', description='TEST', ingredients=[])
    with pytest.raises(ValidationError) as err:
        recipe.full_clean()


def test_recipe_ingredients_without_name_raise_exception(db):
    recipe = mixer.blend('recipes.Recipe', title='Test', description='TEST', ingredients=[{
        "unit": "g",
        "quantity": 40
    }])
    with pytest.raises(ValidationError) as err:
        recipe.full_clean()


def test_recipe_ingredients_without_unit_raise_exception(db):
    recipe = mixer.blend('recipes.Recipe', title='Test', description='TEST', ingredients=[{
        "name": "test",
        "quantity": 40
    }])
    with pytest.raises(ValidationError) as err:
        recipe.full_clean()


def test_recipe_ingredients_without_quantity_raise_exception(db):
    recipe = mixer.blend('recipes.Recipe', title='Test', description='TEST', ingredients=[{
        "name": "test",
        "unit": "g",
    }])
    with pytest.raises(ValidationError) as err:
        recipe.full_clean()


def test_recipe_ingredients_name_not_only_char_raise_exception(db):
    recipe = mixer.blend('recipes.Recipe', title='Test', description='TEST', ingredients=[{
        "name": "23test32",
        "unit": "g",
        "quantity": 40
    }])
    with pytest.raises(ValidationError) as err:
        recipe.full_clean()


def test_recipe_ingredients_name_of_length_31_raise_exception(db):
    recipe = mixer.blend('recipes.Recipe', title='Test', description='TEST', ingredients=[{
        "name": "A" * 31,
        "unit": "g",
        "quantity": 40
    }])
    with pytest.raises(ValidationError) as err:
        recipe.full_clean()


def test_recipe_ingredients_dont_contain_duplicates(db):
    recipe = mixer.blend('recipes.Recipe', title='Test', description='TEST', ingredients=[{
        "name": "A",
        "unit": "g",
        "quantity": 40
    },
        {
            "name": "A",
            "unit": "g",
            "quantity": 40
        }
    ])
    with pytest.raises(ValidationError) as err:
        recipe.full_clean()


def test_recipe_ingredients_quantity_of_1001_raise_exception(db):
    recipe = mixer.blend('recipes.Recipe', title='Test', description='TEST', ingredients=[{
        "name": "test",
        "unit": "g",
        "quantity": 1001
    }])
    with pytest.raises(ValidationError) as err:
        recipe.full_clean()


def test_recipe_ingredients_negative_quantity_raise_exception(db):
    recipe = mixer.blend('recipes.Recipe', title='Test', description='TEST', ingredients=[{
        "name": "test",
        "unit": "g",
        "quantity": -10
    }])
    with pytest.raises(ValidationError) as err:
        recipe.full_clean()


def test_recipe_ingredients_quantity_is_string_raise_exception(db):
    recipe = mixer.blend('recipes.Recipe', title='Test', description='TEST', ingredients=[{
        "name": "test",
        "unit": "g",
        "quantity": "20"
    }])
    with pytest.raises(ValidationError) as err:
        recipe.full_clean()


def test_recipe_ingredients_unit_different_from_g_kg_l_na_raise_exception(db):
    recipe = mixer.blend('recipes.Recipe', title='Test', description='TEST', ingredients=[{
        "name": "test",
        "unit": "test",
        "quantity": 20
    }])
    with pytest.raises(ValidationError) as err:
        recipe.full_clean()


def test_recipe_ingredients_more_than_three_parameters_raise_exception(db):
    recipe = mixer.blend('recipes.Recipe', title='Test', description='TEST', ingredients=[{
        "name": "test",
        "unit": "g",
        "quantity": 20,
        "prova": 222
    }])
    with pytest.raises(ValidationError) as err:
        recipe.full_clean()


def test_recipe_is_well_formatted_not_raise_exception(db, ingredient):
    recipe = mixer.blend('recipes.Recipe', title='A title', description='My description', ingredients=ingredient)
    recipe.full_clean()


def test_recipe_str_return_title(db, ingredient):
    recipe = mixer.blend('recipes.Recipe', title='A title', description='My description', ingredients=ingredient)
    recipe.full_clean()
    assert recipe.__str__() == "A title"
