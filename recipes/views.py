import re

from django.core.exceptions import ValidationError
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Recipe
from .domain import Name, Title, JsonHandler
from .permissions import IsDeleter
from .serializers import UserRecipeSerializer
from .serializers import AdminRecipeSerializer


class PublicRecipeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return AdminRecipeSerializer
        return UserRecipeSerializer

    @action(detail=False, methods=['GET'], url_path='by-author/(?P<pk>[^/.]+)', url_name='filter-author')
    def all_recipe_by_author(self, request, pk=None):
        if not re.match(r'^\d+$', pk):
            return Response(data="Please enter a valid author", status=status.HTTP_400_BAD_REQUEST)

        queryset = Recipe.objects.filter(author=pk)
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
                if JsonHandler.create_recipe_from_json(self.get_serializer(recipe).data).has_name_in_ingredient(n):
                    output.append(self.get_serializer(recipe).data)
            except ValidationError as e:
                return Response(data=e.message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if output:
            return Response(data=output, status=status.HTTP_200_OK)

        return Response(data="Sorry, there is no recipe with this ingredient", status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['GET'], url_path='by-title/(?P<title>[^/.]+)', url_name='filter-title')
    def all_recipe_by_title(self, request, title=None):
        try:
            t = Title(title)
        except ValidationError as e:
            return Response(data=e.message, status=status.HTTP_400_BAD_REQUEST)

        queryset = Recipe.objects.filter(title__icontains=title)
        serializer = self.get_serializer(queryset, many=True)
        if serializer.data:
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data='Sorry, there is no recipe with this title', status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['GET'], url_path='sort-by-title', url_name='sort-title')
    def sort_recipe_by_title(self, request):
        queryset = Recipe.objects.all().order_by('title').values()
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], url_path='sort-by-date', url_name='sort-date')
    def sort_recipe_by_date(self, request):
        queryset = Recipe.objects.all().order_by('-created_at').values()
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class PrivateRecipeViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsDeleter]

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return AdminRecipeSerializer
        return UserRecipeSerializer

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def get_queryset(self):
        return Recipe.objects.all() if self.request.user.is_superuser else Recipe.objects.filter(
            author=self.request.user)

    @action(detail=False, methods=['GET'], url_path='sort-by-title', url_name='sort-title')
    def sort_recipe_by_title(self, request):
        queryset = self.get_queryset().order_by('title').values()
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], url_path='sort-by-date', url_name='sort-date')
    def sort_recipe_by_date(self, request):
        queryset = self.get_queryset().order_by('-created_at').values()
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
