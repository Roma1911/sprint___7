import allure
import pytest
import requests
from helpers import LOGIN_COURIER_URL, generate_random_string


@allure.feature('Авторизация курьера')
class TestCourierLogin:

    @allure.title("Для авторизации нужно передать все обязательные поля")
    @pytest.mark.parametrize(
        "missing_field",
        ["login", "password"],
        ids=["missing_login", "missing_password"],
    )
    def test_authorization_without_required_fields_returns_an_error(
        self, payload_without_field, missing_field):
        payload = payload_without_field(missing_field)
        response = requests.post(LOGIN_COURIER_URL, data=payload)
        assert response.status_code == 400, (
            f"Ожидался 400 без {missing_field}, получен: {response.status_code}. "
            f"Тело: {response.text}"
        )
        body = response.json()
        assert isinstance(body, dict), "Тело ответа должно быть JSON-объектом"


    @allure.title("Неверный логин или пароль возвращает ошибку")
    @pytest.mark.parametrize(
        "payload",
        [
            {"login": "wrong_login", "password": "{password}"},
            {"login": "{login}", "password": "wrong_password"},
        ],
        ids=["wrong_login", "wrong_password"],
    )
    def test_wrong_login_or_password_returns_error(self, create_courier, payload):
        data = {
            "login": payload["login"].format(
                login=create_courier["login"],
                password=create_courier["password"],
            ),
            "password": payload["password"].format(
                login=create_courier["login"],
                password=create_courier["password"],
            ),
        }
        response = requests.post(LOGIN_COURIER_URL, data=data)
        assert response.status_code == 404, (
            f"Ожидался 404, получен: {response.status_code}. Тело: {response.text}"
        )
        body = response.json()
        assert isinstance(body, dict), "Тело ответа должно быть JSON-объектом"
        

    @allure.title("Успешный запрос возвращает id")
    def test_successful_request_returns_the_id(self, create_courier):
        response = requests.post(
            LOGIN_COURIER_URL,
            data={
                "login": create_courier["login"],
                "password": create_courier["password"],
            },
        )
        assert response.status_code == 200, (
            f"Ожидался 200, получен: {response.status_code}. Тело: {response.text}"
        )
        body = response.json()
        assert isinstance(body, dict), "Тело ответа должно быть JSON-объектом"
        assert "id" in body, "В ответе нет id"
        assert body["id"] is not None, "id не должен быть None"