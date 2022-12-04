import json
from unittest.mock import patch, Mock

import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, \
    HTTP_204_NO_CONTENT, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.test import APIClient


@pytest.fixture
def recipes(db):
    return [mixer.blend('recipes.Recipe', title='My first recipe', description='First description',
                        ingredients=[{"name": "Eggs", "unit": "g", "quantity": 40}]),
            mixer.blend('recipes.Recipe', title='My second recipe', description='Second description',
                        ingredients=[{"name": "Water", "unit": "l", "quantity": 1}]),
            mixer.blend('recipes.Recipe', title='My third recipe', description='Third description',
                        ingredients=[{"name": "Tomato", "unit": "kg", "quantity": 1}])
            ]


def get_client(user=None):
    res = APIClient()
    if user is not None:
        res.force_login(user)
    return res


def parse(response):
    response.render()
    content = response.content.decode()
    return json.loads(content)


def contains(response, key, value):
    obj = parse(response)
    if key not in obj:
        return False
    return value in obj[key]


@pytest.mark.django_db
class TestUserRecipeViewSet:
    def test_anon_user_cant_make_post_request(self):
        path = reverse('recipes-list')
        client = get_client()
        response = client.post(path)
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_anon_user_cant_make_put_request(self):
        path = reverse('recipes-list')
        client = get_client()
        response = client.put(path)
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_anon_user_cant_make_delete_request(self):
        path = reverse('recipes-list')
        client = get_client()
        response = client.delete(path)
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_anon_user_can_make_get_request(self, recipes):
        path = reverse('recipes-list')
        client = get_client()
        response = client.get(path)
        assert response.status_code == HTTP_200_OK
        obj = parse(response)
        assert len(obj) == len(recipes)

    def test_anon_user_can_filter_by_author(self, recipes):
        path = reverse('recipes-filter-author', kwargs={'pk': '2'})
        client = get_client()
        response = client.get(path)
        assert response.status_code == HTTP_200_OK

    def test_anon_user_can_filter_by_title(self, recipes):
        path = reverse('recipes-filter-title', kwargs={'title': 'My first recipe'})
        client = get_client()
        response = client.get(path)
        assert response.status_code == HTTP_200_OK

    def test_anon_user_can_filter_by_ingredient(self, recipes):
        path = reverse('recipes-filter-ingredient', kwargs={'name': 'eggs'})
        client = get_client()
        response = client.get(path)
        assert response.status_code == HTTP_200_OK

    def test_anon_user_can_sort_recipes_by_date(self):
        path = reverse('recipes-sort-date')
        client = get_client()
        response = client.get(path)
        assert response.status_code == HTTP_200_OK

    def test_anon_user_can_sort_recipes_by_title(self):
        path = reverse('recipes-sort-title')
        client = get_client()
        response = client.get(path)
        assert response.status_code == HTTP_200_OK

    def test_logged_user_get_list(self, recipes):
        path = reverse('recipes-list')
        user = mixer.blend(get_user_model())
        client = get_client(user)
        response = client.get(path)
        assert response.status_code == HTTP_200_OK
        obj = parse(response)
        assert len(obj) == len(recipes)

    # TODO RIGUARDARE QUESTO TEST
    def test_logged_user_can_make_post_request(self):
        path = reverse('recipes-list')
        user = mixer.blend(get_user_model())
        client = get_client(user)
        recipe = {'title': "Test", 'description': 'My test recipe'}
        response = client.post(path, recipe)
        assert response.status_code == HTTP_201_CREATED

    #TODO CHECK BETTER

    # def test_logged_user_cant_post_recipe_with_the_name_of_other_user(self, recipes):
    #     path = reverse('recipes-list')
    #     user = mixer.blend(get_user_model())
    #     client = get_client(user)
    #     recipe = {'author': 2, 'title': "Test", 'description': 'My test recipe'}
    #     response = client.post(path, recipe)
    #     assert response.status_code == HTTP_403_FORBIDDEN

    def test_logged_user_cant_delete_recipe_of_other_user(self, recipes):
        path = reverse('recipes-detail', kwargs={'pk': recipes[0].pk})
        user = mixer.blend(get_user_model())
        client = get_client(user)
        response = client.delete(path)
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_logged_user_cant_delete_his_recipes(self, db):
        user = mixer.blend(get_user_model())
        recipe = mixer.blend('recipes.Recipe', author=user, title='My test recipe', description='test description',
                             ingredients=[{"name": "Eggs", "unit": "g", "quantity": 40}])
        path = reverse('recipes-detail', kwargs={'pk': recipe.pk})
        client = get_client(user)
        response = client.delete(path)
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_logged_user_can_filter_recipes_by_author(self, recipes):
        path = reverse('recipes-filter-author', kwargs={'pk': '2'})
        user = mixer.blend(get_user_model())
        client = get_client(user)
        response = client.get(path)
        assert response.status_code == HTTP_200_OK

    def test_logged_user_can_filter_recipes_by_title(self, recipes):
        path = reverse('recipes-filter-title', kwargs={'title': 'My first recipe'})
        user = mixer.blend(get_user_model())
        client = get_client(user)
        response = client.get(path)
        assert response.status_code == HTTP_200_OK

    def test_logged_user_can_filter_recipes_by_ingredient(self, recipes):
        path = reverse('recipes-filter-ingredient', kwargs={'name': 'eggs'})
        user = mixer.blend(get_user_model())
        client = get_client(user)
        response = client.get(path)
        assert response.status_code == HTTP_200_OK

    def test_logged_user_can_sort_recipes_by_date(self):
        path = reverse('recipes-sort-date')
        user = mixer.blend(get_user_model())
        client = get_client(user)
        response = client.get(path)
        assert response.status_code == HTTP_200_OK

    def test_logged_user_can_sort_recipes_by_title(self):
        path = reverse('recipes-sort-title')
        user = mixer.blend(get_user_model())
        client = get_client(user)
        response = client.get(path)
        assert response.status_code == HTTP_200_OK

    def test_every_user_must_enter_a_valid_title_when_looking_for_recipes(self):
        path = reverse('recipes-filter-title', kwargs={'title': 'I0NV4L1D'})
        user = mixer.blend(get_user_model())
        non_client = get_client()
        client = get_client(user)
        non_response = non_client.get(path)
        response = client.get(path)
        assert non_response.status_code == HTTP_400_BAD_REQUEST
        assert response.status_code == HTTP_400_BAD_REQUEST

    def test_every_user_must_enter_a_valid_author_when_looking_for_recipes(self):
        path = reverse('recipes-filter-author', kwargs={'pk': 'I0NV4L1D'})
        non_client = get_client()
        user = mixer.blend(get_user_model())
        client = get_client(user)
        non_response = non_client.get(path)
        response = client.get(path)
        assert non_response.status_code == HTTP_400_BAD_REQUEST
        assert response.status_code == HTTP_400_BAD_REQUEST

    def test_every_user_must_enter_a_valid_ingredient_name_when_looking_for_recipes(self):
        path = reverse('recipes-filter-ingredient', kwargs={'name': 'I0NV4L1D'})
        user = mixer.blend(get_user_model())
        client = get_client(user)
        non_client = get_client()
        non_response = non_client.get(path)
        response = client.get(path)
        assert non_response.status_code == HTTP_400_BAD_REQUEST
        assert response.status_code == HTTP_400_BAD_REQUEST

    def test_every_user_search_for_non_existent_author_receive_not_found_recipes(self):
        path = reverse('recipes-filter-author', kwargs={'pk': 5})
        user = mixer.blend(get_user_model())
        client = get_client(user)
        non_client = get_client()
        non_response = non_client.get(path)
        response = client.get(path)
        assert non_response.status_code == HTTP_204_NO_CONTENT
        assert response.status_code == HTTP_204_NO_CONTENT

    def test_every_user_search_for_non_existent_title_receive_not_found_recipes(self):
        path = reverse('recipes-filter-title', kwargs={'title': 'NONEXISTENT'})
        user = mixer.blend(get_user_model())
        client = get_client(user)
        non_client = get_client()
        non_response = non_client.get(path)
        response = client.get(path)
        assert non_response.status_code == HTTP_204_NO_CONTENT
        assert response.status_code == HTTP_204_NO_CONTENT

    def test_every_user_search_for_non_existent_ingredient_receive_not_found_recipes(self):
        path = reverse('recipes-filter-ingredient', kwargs={'name': 'NONEXISTENT'})
        user = mixer.blend(get_user_model())
        client = get_client(user)
        non_client = get_client()
        non_response = non_client.get(path)
        response = client.get(path)
        assert non_response.status_code == HTTP_204_NO_CONTENT
        assert response.status_code == HTTP_204_NO_CONTENT

    @patch('recipes.views.create_recipe_fromJSON', side_effect=ValidationError("ERROR"))
    def test_every_user_if_there_was_internal_error_then_it_is_notified(self, mock: Mock, recipes):
        path = reverse('recipes-filter-ingredient', kwargs={'name': 'eggs'})
        user = mixer.blend(get_user_model())
        client = get_client(user)
        non_client = get_client()
        non_response = non_client.get(path)
        response = client.get(path)
        assert non_response.status_code == HTTP_500_INTERNAL_SERVER_ERROR
        assert response.status_code == HTTP_500_INTERNAL_SERVER_ERROR

    def test_admin_can_delete_recipes_of_every_user(self, recipes):
        path = reverse('recipes-detail', kwargs={'pk': recipes[0].pk})
        user = mixer.blend(get_user_model())
        user.is_superuser = True
        user.is_staff = True
        user.save()
        admin = get_client(user)
        response = admin.delete(path)
        assert response.status_code == HTTP_204_NO_CONTENT

    def test_admin_can_get_recipes_with_every_field(self, recipes):
        path = reverse('recipes-list')
        user = mixer.blend(get_user_model())
        user.is_superuser = True
        user.is_staff = True
        user.save()
        admin = get_client(user)
        response = admin.get(path)
        assert response.status_code == HTTP_200_OK
        obj = parse(response)
        assert all(['updated_at' in recipe and 'author' in recipe for recipe in obj])
