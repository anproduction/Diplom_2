import requests
import allure
from endpoints import ORDER_CREATE, LOGIN
from test_data import VALID_INGREDIENTS, INVALID_INGREDIENTS


@allure.feature("Создание заказа")
class TestOrder:

    @allure.story("Создание заказа с авторизацией и ингредиентами")
    def test_create_order_authorized_with_ingredients(self, registered_user):
        login_response = requests.post(
            LOGIN,
            json={"email": registered_user["email"], "password": registered_user["password"]}
        )
        assert login_response.status_code == 200
        token = login_response.json().get("accessToken")
        assert token is not None

        headers = {"Authorization": token}
        order_data = {"ingredients": VALID_INGREDIENTS}

        response = requests.post(ORDER_CREATE, json=order_data, headers=headers)
        assert response.status_code == 200
        resp_json = response.json()
        assert resp_json.get("success") is True
        assert "order" in resp_json

    @allure.story("Создание заказа без авторизации")
    def test_create_order_without_authorization(self):
        order_data = {"ingredients": VALID_INGREDIENTS}
        response = requests.post(ORDER_CREATE, json=order_data)
        assert response.status_code in (200, 401)
        resp_json = response.json()
        assert "success" in resp_json

    @allure.story("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, registered_user):
        login_response = requests.post(
            LOGIN,
            json={"email": registered_user["email"], "password": registered_user["password"]}
        )
        token = login_response.json().get("accessToken")
        headers = {"Authorization": token}
        order_data = {"ingredients": []}
        response = requests.post(ORDER_CREATE, json=order_data, headers=headers)
        assert response.status_code in (400, 422)
        resp_json = response.json()
        assert resp_json.get("success") is False

    @allure.story("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_with_invalid_ingredients(self, registered_user):
        login_response = requests.post(
            LOGIN,
            json={"email": registered_user["email"], "password": registered_user["password"]}
        )
        token = login_response.json().get("accessToken")
        headers = {"Authorization": token}
        order_data = {"ingredients": INVALID_INGREDIENTS}
        response = requests.post(ORDER_CREATE, json=order_data, headers=headers)
        assert response.status_code in (400, 500)
        resp_json = response.json()
        assert resp_json.get("success") is False
