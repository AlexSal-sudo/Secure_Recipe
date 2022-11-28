from rest_framework import serializers

from recipes.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('author', 'title', 'description', 'created_at', 'ingredients')
        model = Recipe
