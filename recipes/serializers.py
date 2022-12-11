from rest_framework import serializers

from recipes.models import Recipe


class UserRecipeSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        fields = ('id', 'author', 'title', 'description', 'created_at', 'ingredients')
        model = Recipe
        read_only_fields = ['author']


class AdminModeratorRecipeSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        fields = ('id', 'author', 'title', 'description', 'created_at', 'updated_at', 'ingredients')
        model = Recipe
        read_only_fields = ['author']
