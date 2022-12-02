from django.db.models import Q
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Recipe
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
        serializer.save(author=self.request.user)

    # TODO Use the correct serializer
    @action(detail=False, methods=['GET'], url_path='byAuthor/(?P<pk>[^/.]+)')
    def all_recipe_by_author(self, request, pk=None):
        queryset = Recipe.objects.filter(author=pk)
        serializer = UserRecipeSerializer(queryset, many=True)
        if serializer.data:
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data='Sorry, cannot find recipes written by the user', status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['GET'], url_path='byIngredient/(?P<name>[^/.]+)')
    def all_recipe_by_ingredient(self, request, name=None):
        queryset = Recipe.objects.filter(ingredients__name__icontains=[{'name': name}])
        serializer = UserRecipeSerializer(queryset, many=True)
        if serializer.data:
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data='Sorry, there is no recipe with this ingredient', status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['GET'], url_path='byTitle/(?P<title>[^/.]+)')
    def all_recipe_by_title(self, request, title=None):
        queryset = Recipe.objects.filter(title__contains=title)
        serializer = UserRecipeSerializer(queryset, many=True)
        if serializer.data:
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data='Sorry, there is no recipe with this title', status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['GET'], url_path='sortByTitle')
    def sort_recipe_by_title(self, request):
        queryset = Recipe.objects.all().order_by('title').values()
        serializer = UserRecipeSerializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], url_path='sortByDate')
    def sort_recipe_by_date(self, request):
        queryset = Recipe.objects.all().order_by('-created_at').values()
        serializer = UserRecipeSerializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
