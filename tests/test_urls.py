import json

import pytest
from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework.status import HTTP_403_FORBIDDEN
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
        response = client.get(path)
        assert response.status_code == HTTP_403_FORBIDDEN
