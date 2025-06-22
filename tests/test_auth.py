import pytest
import requests
import allure
from endpoints import LOGIN


@allure.feature("Авторизация пользователя")
class TestAuth:

    @allure.story("Успешный вход под существующим пользователем")
    def test_login_existing_user(self, registered_user):
        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
        response = requests.post(LOGIN, json=login_data)
        assert response.status_code == 200
        response_json = response.json()
        assert response_json.get("success") is True
        assert "accessToken" in response_json

    @allure.story("Вход с неверным логином и паролем")
    @pytest.mark.parametrize("email,password", [
        ("nonexistent@example.com", "wrongpass"),
        ("", "somepassword"),
        ("user@example.com", ""),
    ])
    def test_login_invalid_credentials(self, email, password):
        login_data = {
            "email": email,
            "password": password
        }
        response = requests.post(LOGIN, json=login_data)
        assert response.status_code in (401, 403)
        response_json = response.json()
        assert response_json.get("success") is False
