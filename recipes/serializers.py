from rest_framework import serializers

from recipes.models import Recipe


class UserRecipeSerializer(serializers.ModelSerializer):
    #username = serializers.CharField(source='author.username', read_only=True)
    class Meta:
        fields = ('id', 'author', 'title', 'description', 'created_at', 'ingredients')
        model = Recipe
        read_only_fields = ['author']

    def validate_author(self, value):
        if self.context['request'].user != value:
            raise serializers.ValidationError("You do not have permission to perform this action")
        return value


class AdminRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'author', 'title', 'description', 'created_at', 'updated_at', 'ingredients')
        model = Recipe
        read_only_fields = ['author']

