import allure
import requests


class TestGetOrders:

    @allure.title('Получение списка заказов')
    def test_get_orders_returns_list(self):
        response = requests.get("https://qa-scooter.praktikum-services.ru/api/v1/orders")
        assert response.status_code == 200, f"Ожидался 200, получен: {response.status_code}"
        assert "orders" in response.json(), "В ответе нет поля orders"
        assert isinstance(response.json()["orders"], list), "orders должен быть списком"