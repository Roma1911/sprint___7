import allure
import pytest
import requests
import random
import string

def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


@allure.feature('Авторизация курьера')
class TestCourierLogin:

    @allure.title("Курьер может авторизоваться")
    def test_courier_can_login(self, create_courier):
        response = requests.post(
            'https://qa-scooter.praktikum-services.ru/api/v1/courier/login',
            data=create_courier
        )
        assert response.status_code == 200, f"Курьер не авторизовался. Код: {response.status_code}"
        assert "id" in response.json(), "В ответе нет id курьера"


    @allure.title("Для авторизации нужно передать все обязательные поля")
    def test_authorization_with_the_required_fields(self, create_courier):
        response = requests.post(
            'https://qa-scooter.praktikum-services.ru/api/v1/courier/login',
            data={"password": create_courier["password"]}
        )
        assert response.status_code == 400, f"Ожидался код 400 без login, получен: {response.status_code}"
        response = requests.post(
            'https://qa-scooter.praktikum-services.ru/api/v1/courier/login',
            data={"login": create_courier["login"]}
        )
        assert response.status_code == 400, f"Ожидался код 400 без password, получен: {response.status_code}"
       

    @allure.title("Система вернёт ошибку, если неправильно указать логин или пароль")
    def test_wrong_login_or_password_returns_error(self, create_courier):
        response = requests.post(
            'https://qa-scooter.praktikum-services.ru/api/v1/courier/login',
            data={"login": create_courier["login"], "password": "wrong_password"}
        )
        assert response.status_code == 404, f"Ожидался код 404, получен: {response.status_code}"
        response = requests.post(
            'https://qa-scooter.praktikum-services.ru/api/v1/courier/login',
            data={"login": "wrong_login", "password": create_courier["password"]}
        )
        assert response.status_code == 404, f"Ожидался код 404, получен: {response.status_code}"


    @allure.title("Если какого-то поля нет, запрос возвращает ошибку")
    def test_missing_field_returns_error(self):
        login = generate_random_string(10)
        password = generate_random_string(10)
        response = requests.post(
            'https://qa-scooter.praktikum-services.ru/api/v1/courier/login',
            data={"password": password}
        )
        assert response.status_code == 400, f"Ожидался код 400, получен: {response.status_code}"
        response = requests.post(
            'https://qa-scooter.praktikum-services.ru/api/v1/courier/login',
            data={"login": login}
        )
        assert response.status_code == 400, f"Ожидался код 400, получен: {response.status_code}"


    @allure.title("Если авторизоваться под несуществующим пользователем, запрос возвращает ошибку")
    def test_authorization_under_a_non_existent_user(self):
        login = generate_random_string(10)
        password = generate_random_string(10)

        response = requests.post(
            'https://qa-scooter.praktikum-services.ru/api/v1/courier/login',
            data={"login": login, "password": password}
        )

        assert response.status_code == 404, f"Ожидался код 404, получен: {response.status_code}"


    @allure.title("Успешный запрос возвращает id")
    def test_successful_request_returns_the_id(self, create_courier):
        response = requests.post(
            'https://qa-scooter.praktikum-services.ru/api/v1/courier/login',
            data=create_courier
        )
        assert response.status_code == 200, f"Курьер не авторизовался. Код: {response.status_code}"
        assert "id" in response.json(), "В ответе нет id курьера"
        assert response.json()["id"] is not None, "id курьера не должен быть None"