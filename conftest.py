import pytest
import requests
from endpoints import REGISTER
from helpers import random_email, random_password, random_name  # импортируем функции генерации


@pytest.fixture
def unique_user_data():
    return {
        "email": random_email(),
        "password": random_password(),
        "name": random_name()
    }


@pytest.fixture
def registered_user(unique_user_data):
    response = requests.post(REGISTER, json=unique_user_data)
    assert response.status_code == 200
    assert response.json().get("success") is True
    return unique_user_data
