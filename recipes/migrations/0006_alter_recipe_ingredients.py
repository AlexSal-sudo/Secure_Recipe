# Generated by Django 4.1.3 on 2022-11-28 11:40

from django.db import migrations
import jsonfield.fields
import recipes.validators


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_alter_recipe_ingredients'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=jsonfield.fields.JSONField(default=list, validators=[recipes.validators.JSONSchemaValidator(limit_value={'description': 'The ingredients list', 'items': {'maxProperties': 3, 'properties': {'name': {'description': 'The name of the ingredient', 'maxLen': 30, 'minLen': 1, 'pattern': '^[a-zA-Z]+', 'type': 'string'}, 'quantity': {'description': 'The quantity of the ingredient', 'maximum': 1000, 'minimum': 0, 'type': 'number'}, 'unit': {'description': 'The unit of the ingredient', 'enum': ['liters', 'kilograms', 'grams', 'g', 'l', 'kg', 'n/a'], 'type': 'string'}}, 'required': ['name', 'quantity', 'unit'], 'type': 'object'}, 'minItems': 1, 'schema': 'http://json-schema.org/draft-07/schema#', 'type': 'array'}), recipes.validators.unique_ingredients]),
        ),
    ]
