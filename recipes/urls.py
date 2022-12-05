from django.urls import path
from rest_framework.routers import SimpleRouter

from recipes.views import RecipeViewSet

router = SimpleRouter()
router.register('', RecipeViewSet, basename='recipes')
urlpatterns = router.urls
