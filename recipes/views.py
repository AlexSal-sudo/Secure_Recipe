from django.core.exceptions import ValidationError
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Recipe
from .domain import Name, create_recipe_fromJSON, Title
from .permissions import IsAuthorOrReadOnly
from .serializers import UserRecipeSerializer
from .serializers import AdminRecipeSerializer


# Create your views here.
class RecipeViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return AdminRecipeSerializer
        return UserRecipeSerializer

    def perform_create(self, serializer):
        if not self.request.user.is_superuser:
            serializer.save(author=self.request.user)

    @action(detail=False, methods=['GET'], url_path='by-author/(?P<pk>[^/.]+)')
    def all_recipe_by_author(self, request, pk=None):
        if not isinstance(pk, int):
            return Response(data="Please enter a valid author", status=status.HTTP_400_BAD_REQUEST)

        queryset = Recipe.objects.filter(author=pk)
        serializer = self.get_serializer(queryset, many=True)
        if serializer.data:
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data='Sorry, cannot find recipes written by this author', status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['GET'], url_path='by-ingredient/(?P<name>[^/.]+)')
    def all_recipe_by_ingredient(self, request, name=None):
        try:
            n = Name(name)
        except ValidationError as e:
            return Response(data=e.message, status=status.HTTP_400_BAD_REQUEST)

        queryset = Recipe.objects.all()
        output = []
        for recipe in queryset:
            try:
                if create_recipe_fromJSON(self.get_serializer(recipe).data).has_name_in_ingredient(n):
                    output.append(self.get_serializer(recipe).data)
            except ValidationError as e:
                return Response(data=e.message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if output:
            return Response(data=output, status=status.HTTP_200_OK)

        return Response(data="Sorry, there is no recipe with this ingredient", status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['GET'], url_path='by-title/(?P<title>[^/.]+)')
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

    @action(detail=False, methods=['GET'], url_path='sort-by-title')
    def sort_recipe_by_title(self, request):
        queryset = Recipe.objects.all().order_by('title').values()
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], url_path='sortByDate')
    def sort_recipe_by_date(self, request):
        queryset = Recipe.objects.all().order_by('-created_at').values()
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
