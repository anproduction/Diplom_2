import pytest
import requests
import allure

from endpoints import REGISTER

@allure.feature("Регистрация пользователя")
@allure.story("Создание уникального пользователя")
def test_create_unique_user(unique_user_data):
    response = requests.post(REGISTER, json=unique_user_data)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("success") is True


@allure.feature("Регистрация пользователя")
@allure.story("Создание пользователя, который уже зарегестрирован")
def test_create_existing_user(registered_user):
    response = requests.post(REGISTER, json=registered_user)
    assert response.status_code in (403, 409)
    response_json = response.json()
    assert response_json.get("success") is False


@pytest.mark.parametrize("missing_field", ["email", "password", "name"])
@allure.feature("Регистрация пользователя")
@allure.story("Создание пользователя с пропущенным обязательным полем")
def test_create_user_missing_field(unique_user_data, missing_field):
    data = unique_user_data.copy()
    data.pop(missing_field)
    response = requests.post(REGISTER, json=data)
    assert response.status_code in (400, 422)
    response_json = response.json()
    assert response_json.get("success") is False
