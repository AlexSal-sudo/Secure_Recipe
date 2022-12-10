import re

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models.functions import Lower
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Recipe
from .domain import Name, Title, JsonHandler
from .permissions import IsModeratorOrAdmin
from .serializers import UserRecipeSerializer, AdminModeratorRecipeSerializer

ORDER_BY_TITLE = 'title'
ORDER_BY_DATA = 'created_at'


def sort_by(sort_value: str, objects, serializer):
    queryset = objects.order_by(Lower(sort_value))
    serializer = serializer(queryset, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


class PublicRecipeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return AdminModeratorRecipeSerializer
        return UserRecipeSerializer

    @action(detail=False, methods=['GET'], url_path='by-author/(?P<name>[^/.]+)', url_name='filter-author')
    def all_recipe_by_author(self, request, name=None):
        if len(name) > 150 or not re.match(r'^[a-zA-Z0-9@.+\-_]+$', name):
            return Response(data='Please, enter a valid user', status=status.HTTP_400_BAD_REQUEST)

        user = get_user_model().objects.filter(username=name)

        if user:
            queryset = Recipe.objects.filter(author=user[0].pk)
            serializer = self.get_serializer(queryset, many=True)
            if serializer.data:
                return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data='Sorry, cannot find recipes written by this author', status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['GET'], url_path='by-ingredient/(?P<name>[^/.]+)', url_name='filter-ingredient')
    def all_recipe_by_ingredient(self, request, name=None):
        try:
            n = Name(name.lower())
        except ValidationError as e:
            return Response(data=e.message, status=status.HTTP_400_BAD_REQUEST)

        queryset = Recipe.objects.all()
        output = []
        for recipe in queryset:
            try:
                if JsonHandler.create_recipe_from_json(self.get_serializer(recipe).data).has_name_in_ingredients(n):
                    output.append(self.get_serializer(recipe).data)
            except ValidationError as e:
                return Response(data=e.message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if output:
            return Response(data=output, status=status.HTTP_200_OK)

        return Response(data="Sorry, there is no recipe with this ingredient", status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['GET'], url_path='by-title/(?P<title>[^/.]+)', url_name='filter-title')
    def all_recipe_by_title(self, request, title=None):
        try:
            Title(title)
        except ValidationError as e:
            return Response(data=e.message, status=status.HTTP_400_BAD_REQUEST)

        queryset = Recipe.objects.filter(title__icontains=title)
        serializer = self.get_serializer(queryset, many=True)
        if serializer.data:
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data='Sorry, there is no recipe with this title', status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['GET'], url_path='sort-by-title', url_name='sort-title')
    def sort_recipe_by_title(self, request):
        return sort_by(ORDER_BY_TITLE, Recipe.objects.all(), self.get_serializer_class())

    @action(detail=False, methods=['GET'], url_path='sort-by-date', url_name='sort-date')
    def sort_recipe_by_date(self, request):
        return sort_by(ORDER_BY_DATA, Recipe.objects.all(), self.get_serializer_class())


class PrivateRecipeViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsModeratorOrAdmin]

    def get_serializer_class(self):
        if self.request.user.is_superuser or self.request.user.groups.filter(name='recipe_moderators').exists():
            return AdminModeratorRecipeSerializer
        return UserRecipeSerializer

    def create(self, request, *args, **kwargs):
        if 'ingredients' not in request.data:
            return Response(data="Please add at least one ingredient", status=status.HTTP_400_BAD_REQUEST)
        if 'author' in request.data:
            if not re.match(r'^\d+$', str(request.data['author'])):
                return Response(data="Please enter a valid author", status=status.HTTP_400_BAD_REQUEST)
            elif int(request.data['author']) != self.request.user.pk:
                return Response(status=status.HTTP_403_FORBIDDEN)

        return super(PrivateRecipeViewSet, self).create(request, *args, **kwargs)

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def get_queryset(self):
        return Recipe.objects.all() if self.request.user.is_superuser or self.request.user.groups.filter(
            name='recipe_moderators').exists() else Recipe.objects.filter(author=self.request.user)

    @action(detail=False, methods=['GET'], url_path='sort-by-title', url_name='sort-title')
    def sort_recipe_by_title(self, request):
        return sort_by(ORDER_BY_TITLE, self.get_queryset(), self.get_serializer_class())

    @action(detail=False, methods=['GET'], url_path='sort-by-date', url_name='sort-date')
    def sort_recipe_by_date(self, request):
        return sort_by(ORDER_BY_DATA, self.get_queryset(), self.get_serializer_class())

    @action(detail=False, methods=['GET'], url_path='is-moderator', url_name='moderator')
    def is_moderator(self, request):
        if not self.request.user.is_superuser and not self.request.user.groups.filter(
                name='recipe_moderators').exists():
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        return Response(data={'is_admin': self.request.user.is_superuser}, status=status.HTTP_200_OK)
