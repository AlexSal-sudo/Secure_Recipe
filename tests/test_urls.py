import json

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_200_OK
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
