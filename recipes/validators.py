from django.core.validators import BaseValidator
from django.core.exceptions import ValidationError
import jsonschema


def check_not_none_and_unique_ingredients(list_of_ingredients: list):
    if type(list_of_ingredients) is not list:
        raise ValidationError("Please, fill the ingredients properly")
    for i in range(len(list_of_ingredients)):
        for j in range(len(list_of_ingredients)):
            if i != j and list_of_ingredients[i]['name'] == list_of_ingredients[j]['name']:
                raise ValidationError(
                    f"There are some redundant ingredients! <{list_of_ingredients[i]['name'].upper()}>")


class JSONSchemaValidator(BaseValidator):
    def compare(self, value: list, schema):
        try:
            jsonschema.validate(value, schema)
        except jsonschema.exceptions.ValidationError as e:
            raise ValidationError(e.schema['error_msg'] if 'error_msg' in e.schema else e.message)
