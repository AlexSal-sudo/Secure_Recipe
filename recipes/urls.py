from django.urls import path
from rest_framework.routers import SimpleRouter

from recipes.views import RecipeViewSet, PrivateRecipeViewSet

router = SimpleRouter()
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('personal-area', PrivateRecipeViewSet, basename='personal-area')
urlpatterns = router.urls
