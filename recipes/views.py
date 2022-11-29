from django.shortcuts import render
from rest_framework import viewsets
from .models import Recipe
from .permissions import IsAuthorOrReadOnly
from .serializers import RecipeSerializer


# Create your views here.
class RecipeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
