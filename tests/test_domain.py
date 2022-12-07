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
