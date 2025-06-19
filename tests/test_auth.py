import pytest
import requests
import allure
from endpoints import LOGIN

@allure.feature("Авторизация пользователя")
@allure.story("Успешный вход под существующим пользователем")
def test_login_existing_user(registered_user):
    login_data = {
        "email": registered_user["email"],
        "password": registered_user["password"]
    }
    response = requests.post(LOGIN, json=login_data)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("success") is True
    assert "accessToken" in response_json


@allure.feature("Авторизация пользователя")
@allure.story("Вход с неверным логином и паролем")
@pytest.mark.parametrize("email,password", [
    ("nonexistent@example.com", "wrongpass"),
    ("", "somepassword"),
    ("user@example.com", ""),
])
def test_login_invalid_credentials(email, password):
    login_data = {
        "email": email,
        "password": password
    }
    response = requests.post(LOGIN, json=login_data)
    assert response.status_code == 401 or response.status_code == 403
    response_json = response.json()
    assert response_json.get("success") is False
