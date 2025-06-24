import pytest
import requests
import allure
from endpoints import REGISTER


@allure.feature("Регистрация пользователя")
class TestUser:

    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self, unique_user_data):
        with allure.step("Отправка POST-запроса на регистрацию нового пользователя"):
            response = requests.post(REGISTER, json=unique_user_data)

        with allure.step("Проверка успешной регистрации"):
            assert response.status_code == 200
            response_json = response.json()
            assert response_json.get("success") is True

    @allure.title("Создание пользователя, который уже зарегистрирован")
    def test_create_existing_user(self, registered_user):
        with allure.step("Отправка POST-запроса на регистрацию уже существующего пользователя"):
            response = requests.post(REGISTER, json=registered_user)

        with allure.step("Проверка отказа в регистрации уже зарегистрированного пользователя"):
            assert response.status_code in (403, 409)
            response_json = response.json()
            assert response_json.get("success") is False

    @allure.title("Создание пользователя с пропущенным обязательным полем")
    @pytest.mark.parametrize("missing_field, expected_status", [
        ("email", 400),
        ("password", 400),
        ("name", 400),
    ])
    def test_create_user_missing_field(self, unique_user_data, missing_field, expected_status):
        with allure.step(f"Удаление обязательного поля '{missing_field}' из данных пользователя"):
            data = unique_user_data.copy()
            data.pop(missing_field)

        with allure.step("Отправка POST-запроса на регистрацию с неполными данными"):
            response = requests.post(REGISTER, json=data)

        with allure.step("Проверка, что регистрация отклонена с ожидаемым кодом ответа"):
            assert response.status_code == expected_status
            response_json = response.json()
            assert response_json.get("success") is False
