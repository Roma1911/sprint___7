import allure
import pytest
import requests
from data import order_data

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1/orders"

@pytest.mark.parametrize(
    "color",
    [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        None
    ],
    ids=["black", "grey", "both", "no_color"]
)
@allure.title("Создание заказа")
def test_create_order(color):
    payload = order_data.copy()
    if color is not None:
        payload["color"] = color
    response = requests.post(BASE_URL, json=payload)
    assert response.status_code == 201, f"Ожидался 201, получен: {response.status_code}"
    assert "track" in response.json(), "В ответе нет track"
    assert response.json()["track"] is not None, "track не должен быть None"