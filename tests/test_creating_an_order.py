import allure
import pytest
import requests

from data import order_data
from helpers import ORDERS_URL

@allure.feature("Создание заказа")
class TestCreateOrder:

    @pytest.mark.parametrize(
        "color",
        [["BLACK"], ["GREY"], ["BLACK", "GREY"], None],
        ids=["black", "grey", "both", "no_color"],
    )
    @allure.title("Создание заказа")
    def test_create_order(self, color):
        payload = order_data.copy()
        payload["color"] = color
        response = requests.post(ORDERS_URL, json=payload)
        assert response.status_code == 201, (
            f"Ожидался 201, получен: {response.status_code}. Тело: {response.text}"
        )
        body = response.json()
        assert isinstance(body, dict), "Тело ответа должно быть JSON-объектом"
        assert "track" in body, "В ответе нет track"
        assert body["track"] is not None, "track не должен быть None"
        assert isinstance(body["track"], int), "track должен быть числом"