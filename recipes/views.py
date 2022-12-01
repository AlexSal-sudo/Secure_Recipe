from rest_framework import viewsets, permissions

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

    #
    # TODO Use action to filter recipes by author or get all
    # def get_queryset(self):
    #     if self.request.user.is_superuser:
    #         return Recipe.objects.all()
    #     return Recipe.objects.all().filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

