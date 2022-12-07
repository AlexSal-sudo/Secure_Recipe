import pytest

from recipes.domain import *


class TestDomainPrimitives:
    def test_title(self):
        wrong_values = ['Title' * 20, '123Title', '__TITLE__']
        for value in wrong_values:
            with pytest.raises(ValidationError):
                Title(value)

        right_values = ['Title', 'Example of Title', 'My personal Title']
        for value in right_values:
            assert Title(value).value == value

    def test_description_syntax(self):
        wrong_values = ['Desc' * 800, 'DESC____?', '?___TEST']
        for value in wrong_values:
            with pytest.raises(ValidationError):
                Description(value)

        right_values = ['Description', 'The cake need 30min of oven', 'Be careful the cake will burn!']
        for value in right_values:
            assert Description(value).value == value

    def test_name_of_ingredient_syntax(self):
        wrong_values = ['Banana' * 20, '_Banana_123', 'Test_for_name']
        for value in wrong_values:
            with pytest.raises(ValidationError):
                Name(value)

        right_values = ['Pasta al ragù', 'Banana', 'Test']
        for value in right_values:
            assert Name(value).value == value

    def test_name_of_ingredient_are_equal(self):
        assert Name('Banana') != Name('Melon')

    def test_quantity_must_not_be_negative(self):
        with pytest.raises(ValidationError):
            Quantity(-1)

    def test_quantity_must_not_exceed_1000(self):
        with pytest.raises(ValidationError):
            Quantity(1001)

    def test_unit_must_not_an_empty_string(self):
        with pytest.raises(ValidationError):
            Unit('')

    def test_unit_must_not_exceed_3_character(self):
        with pytest.raises(ValidationError):
            Unit('kg__')

    def test_unit_must_not_be_different_than_kg_g_l_cl_ml_cup_na(self):
        with pytest.raises(ValidationError):
            Unit('lt')

    def test_ingredient_format(self):
        ingredient = Ingredient(Name("Banana"), Quantity(20), Unit("kg"))
        assert ingredient.name == Name("Banana")
        assert ingredient.quantity == Quantity(20)
        assert ingredient.unit == Unit("kg")

    def test_ingredient_eq(self):
        assert Ingredient(Name("Banana"), Quantity(20), Unit("kg")) == Ingredient(Name("Banana"), Quantity(60),
                                                                                  Unit("kg"))

    @pytest.fixture()
    def ingredients(self):
        return [Ingredient(Name("Banana"), Quantity(20), Unit("g")),
                Ingredient(Name("Apple"), Quantity(2), Unit("kg")),
                Ingredient(Name("Pineapple"), Quantity(20), Unit("g"))]

    def test_recipe_cannot_be_built_without_builder(self):
        with pytest.raises(ValidationError):
            recipe = Recipe(Title("Title"), Description("Description"), datetime.now().date())

    def test_recipe_builder_has_at_least_one_ingredient(self):
        recipe_builder = Recipe.Builder(Title("Title"), Description("Description"), datetime.now().date())
        with pytest.raises(ValidationError):
            recipe_builder.build()
        recipe_builder.with_ingredient(Ingredient(Name("Banana"), Quantity(20), Unit("kg")))
        recipe_builder.build()

    def test_recipe_cannot_contain_duplicates(self):
        recipe_builder = Recipe.Builder(Title("Title"), Description("Description"), datetime.now().date())
        with pytest.raises(ValidationError):
            recipe_builder.with_ingredient(Ingredient(Name("Banana"), Quantity(20), Unit("kg"))).with_ingredient(
                Ingredient(Name("Banana"), Quantity(20), Unit("kg")))

    def test_recipe_add_ingredient(self, ingredients):
        recipe_builder = Recipe.Builder(Title("Title"), Description("Description"), datetime.now().date())
        for ingredient in ingredients:
            recipe_builder.with_ingredient(ingredient)

        recipe = recipe_builder.build()
        assert recipe.ingredients() == 3
        assert recipe.ingredient(0) == ingredients[0]

    def test_recipe_remove_ingredient(self, ingredients):
        recipe_builder = Recipe.Builder(Title("Title"), Description("Description"), datetime.now().date())
        for ingredient in ingredients:
            recipe_builder.with_ingredient(ingredient)

        recipe_builder.with_out_ingredient(ingredients[0])
        recipe = recipe_builder.build()
        assert recipe.ingredients() == 2
        with pytest.raises(ValidationError):
            recipe.ingredient(2)

    def test_recipe_remove_ingredient_not_contained(self, ingredients):
        recipe_builder = Recipe.Builder(Title("Title"), Description("Description"), datetime.now().date())
        for ingredient in ingredients:
            recipe_builder.with_ingredient(ingredient)
        with pytest.raises(ValidationError):
            recipe_builder.with_out_ingredient(Ingredient(Name("Melon"), Quantity(2), Unit("kg")))

    def test_recipe_remove_ingredient_from_empty_recipe(self, ingredients):
        recipe_builder = Recipe.Builder(Title("Title"), Description("Description"), datetime.now().date())
        for ingredient in ingredients:
            recipe_builder.with_ingredient(ingredient)
        recipe_builder.build()
        with pytest.raises(ValidationError):
            recipe_builder.with_out_ingredient(ingredients[0])

    def test_recipe_add_ingredient_from_empty_recipe(self, ingredients):
        recipe_builder = Recipe.Builder(Title("Title"), Description("Description"), datetime.now().date())
        for ingredient in ingredients:
            recipe_builder.with_ingredient(ingredient)
        recipe_builder.build()
        with pytest.raises(ValidationError):
            recipe_builder.with_ingredient(ingredients[0])

    def test_recipe_has_name_in_ingredients(self, ingredients):
        recipe_builder = Recipe.Builder(Title("Title"), Description("Description"), datetime.now().date())
        for ingredient in ingredients:
            recipe_builder.with_ingredient(ingredient)

        recipe = recipe_builder.build()
        assert recipe.has_name_in_ingredients(Name('Banana'))
        assert not recipe.has_name_in_ingredients(Name('Melon'))

    def test_build_an_empty_recipe_raise_exception(self, ingredients):
        recipe_builder = Recipe.Builder(Title("Title"), Description("Description"), datetime.now().date())
        for ingredient in ingredients:
            recipe_builder.with_ingredient(ingredient)
        recipe_builder.build()
        with pytest.raises(ValidationError):
            recipe_builder.build()

    def test_json_handler_create_recipe_from_json(self):
        recipe = JsonHandler.create_recipe_from_json({
            "title": "Ricetta Gelosa",
            "description": "Ricetta....",
            "created_at": "2022-12-01",
            "ingredients": [
                {
                    "name": "uova",
                    "quantity": 200,
                    "unit": "g"
                }
            ]
        })
        assert recipe.ingredients() == 1
        assert recipe.has_name_in_ingredients(Name("uova"))
