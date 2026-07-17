import allure
import pytest
import requests
from config import COURIER_LOGIN_ENDPOINT
from generators import generate_random_string


@allure.feature('Авторизация курьера')
class TestCourierLogin:

    @allure.title("Для авторизации нужно передать все обязательные поля")
    @pytest.mark.parametrize(
        "missing_field, expected_status",
        [("login", 400), ("password", 400)],
        ids=["missing_login", "missing_password"],
    )
    def test_authorization_without_required_fields_returns_an_error(
        self, payload_without_field, missing_field, expected_status
    ):
        data = payload_without_field(missing_field)
        response = requests.post(COURIER_LOGIN_ENDPOINT, data=data)

        assert response.status_code == expected_status, (
            f"Ожидался код {expected_status}, получен: {response.status_code}. "
            f"Тело: {response.text}"
        )
        body = response.json()
        assert isinstance(body, dict)
        assert "error" in body or "message" in body

    @allure.title("Система вернёт ошибку, если неправильно указать логин или пароль")
    @pytest.mark.parametrize(
        "wrong_login_value, wrong_password_value, expected_status",
        [
            ("wrong_login", "{password}", 404),
            ("{login}", "wrong_password", 404),
        ],
        ids=["wrong_login", "wrong_password"],
    )
    def test_wrong_login_or_password_returns_error(
        self, create_courier, wrong_login_value, wrong_password_value, expected_status
    ):
        login = wrong_login_value.format(login=create_courier["login"], password=create_courier["password"])
        password = wrong_password_value.format(login=create_courier["login"], password=create_courier["password"])

        response = requests.post(
            COURIER_LOGIN_ENDPOINT,
            data={"login": login, "password": password},
        )

        assert response.status_code == expected_status, (
            f"Ожидался код {expected_status}, получен: {response.status_code}"
        )
        body = response.json()
        assert isinstance(body, dict)
        assert "error" in body or "message" in body


    @allure.title("Если какого-то поля нет, запрос возвращает ошибку")
    def test_missing_field_returns_error(self):
        response = requests.post(
            COURIER_LOGIN_ENDPOINT,
            data={"password": generate_random_string(10)},
        )
        assert response.status_code == 400, (
            f"Ожидался 400 без login, получен: {response.status_code}, тело: {response.text}"
        )
        body = response.json()
        assert isinstance(body, dict)
        assert "error" in body or "message" in body
        response = requests.post(
            COURIER_LOGIN_ENDPOINT,
            data={"login": generate_random_string(10)},
        )
        assert response.status_code == 400, (
            f"Ожидался 400 без password, получен: {response.status_code}, тело: {response.text}"
        )
        body = response.json()
        assert isinstance(body, dict)
        assert "error" in body or "message" in body


    @allure.title("Если авторизоваться под несуществующим пользователем, запрос возвращает ошибку")
    def test_authorization_under_a_non_existent_user(self):
        response = requests.post(
            COURIER_LOGIN_ENDPOINT,
            data={
                "login": generate_random_string(10),
                "password": generate_random_string(10),
            },
        )
        assert response.status_code == 404, (
            f"Ожидался 404 для несуществующего пользователя, получен: {response.status_code}"
        )
        body = response.json()
        assert isinstance(body, dict)
        assert "error" in body or "message" in body

        
    @allure.title("Успешный запрос возвращает id")
    def test_successful_request_returns_the_id(self, create_courier):
        response = requests.post(
            COURIER_LOGIN_ENDPOINT,
            data=create_courier
        )
        assert response.status_code == 200, f"Курьер не авторизовался. Код: {response.status_code}"
        body = response.json()
        assert isinstance(body, dict), "Тело ответа должно быть JSON-объектом"
        assert "id" in response.json(), "В ответе нет id курьера"
        assert response.json()["id"] is not None, "id курьера не должен быть None"