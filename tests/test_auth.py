import pytest
import requests
import allure
from endpoints import LOGIN
from data import INVALID_LOGIN_CREDENTIALS


@allure.feature("Авторизация пользователя")
class TestAuth:

    @allure.title("Успешный вход под существующим пользователем")
    def test_login_existing_user(self, registered_user):
        with allure.step("Формирование данных для логина"):
            login_data = {
                "email": registered_user["email"],
                "password": registered_user["password"]
            }

        with allure.step(f"Отправка POST-запроса на {LOGIN}"):
            response = requests.post(LOGIN, json=login_data)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200

        with allure.step("Проверка тела ответа на успешную авторизацию"):
            response_json = response.json()
            assert response_json.get("success") is True
            assert "accessToken" in response_json

    @allure.title("Вход с неверным логином и паролем")
    @pytest.mark.parametrize("email,password", INVALID_LOGIN_CREDENTIALS)
    def test_login_invalid_credentials(self, email, password):
        with allure.step("Формирование данных для логина с невалидными данными"):
            login_data = {
                "email": email,
                "password": password
            }

        with allure.step(f"Отправка POST-запроса на {LOGIN} с невалидными данными"):
            response = requests.post(LOGIN, json=login_data)

        with allure.step("Проверка, что авторизация отклонена"):
            assert response.status_code in (401, 403)
            response_json = response.json()
            assert response_json.get("success") is False
