import allure
import pytest
import requests
from helpers import CREATE_COURIER_URL
from helpers import LOGIN_COURIER_URL



@allure.title("Создание курьера")
class TestCourierCreation:

    @allure.title("Курьера можно создать")
    def test_courier_can_be_created(self, courier_data):
        response = requests.post(CREATE_COURIER_URL, data=courier_data)
        assert response.status_code == 201, (
            f"Ожидался 201, получен: {response.status_code}. Тело: {response.text}"
        )
        body = response.json()
        assert isinstance(body, dict), "Тело ответа должно быть JSON-объектом"


    @allure.title("нельзя создать двух одинаковых курьеров")
    def test_cannot_create_two_couriers(self, create_courier):
        response = requests.post(CREATE_COURIER_URL, data=create_courier)
        assert response.status_code == 409, (
            f"Ожидался 409, получен: {response.status_code}. Тело: {response.text}"
        )
        body = response.json()
        assert isinstance(body, dict), "Тело ответа должно быть JSON-объектом"
        assert "code" in body and body["code"] == 409, "В ответе должен быть code 409"
        assert "message" in body, "В ответе должно быть поле message"
        msg = body["message"].lower()
        expected_keywords = [
                "логин уже используется",
                "логин уже занят",
                "логин уже существует",
                ]
        assert (keyword in msg for keyword in expected_keywords), (
            f"Текст ошибки не содержит ожидаемых слов. Получено: {body['message']}")


    @allure.title('Чтобы создать курьера, нужно передать все обязательные поля')
    @pytest.mark.parametrize(
        "missing_field",
        ["login", "password"],
        ids=["missing_login", "missing_password"],
    )
    def test_pass_all_required_fields(self, payload_without_field, missing_field):
        payload = payload_without_field(missing_field)
        response = requests.post(CREATE_COURIER_URL, data=payload)
        assert response.status_code == 400, (
            f"Ожидался 400 без {missing_field}, получен: {response.status_code}. "
            f"Тело: {response.text}"
        )
        body = response.json()
        assert isinstance(body, dict), "Тело ответа должно быть JSON-объектом"


    @allure.title("Если авторизоваться под несуществующим пользователем, запрос возвращает ошибку")
    def test_authorization_of_a_non_existent_user(self, courier_data):
        response = requests.post(
            LOGIN_COURIER_URL,
            data={
                "login": courier_data["login"],
                "password": courier_data["password"],
            },
        )
        assert response.status_code == 404, (
            f"Ожидался код 404, получен: {response.status_code}. "
            f"Тело: {response.text}"
        )
        body = response.json()
        assert isinstance(body, dict), "Тело ответа должно быть JSON-объектом"
        assert "message" in body or "error" in body, (
            "В ответе должно быть поле message или error"
        )


    


    



