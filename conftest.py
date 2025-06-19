import pytest
import requests
import random
import string

from endpoints import REGISTER

def random_email():
    return f"user_{''.join(random.choices(string.ascii_lowercase + string.digits, k=8))}@example.com"

def random_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=12))

def random_name():
    return "User" + ''.join(random.choices(string.ascii_letters, k=6))

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
