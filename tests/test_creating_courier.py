import allure
import pytest
import requests
import random
import string


def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


@allure.title("Создание курьера")
class TestCourierCreation:

    @allure.title("Курьера можно создать")
    def test_courier_can_be_created(self, courier_data):
        response = requests.post(
            'https://qa-scooter.praktikum-services.ru/api/v1/courier',
            data=courier_data
        )
        assert response.status_code == 201, f"Курьер не создан. Код ответа: {response.status_code}"


    @allure.title("нельзя создать двух одинаковых курьеров")
    def test_cannot_create_two_couriers(self, courier_data):
        response_1 = requests.post(
            'https://qa-scooter.praktikum-services.ru/api/v1/courier',
            data=courier_data
        )
        assert response_1.status_code == 201, "Первый курьер не создан"
        response_2 = requests.post(
            'https://qa-scooter.praktikum-services.ru/api/v1/courier',
            data=courier_data
        )
        assert response_2.status_code == 409, f"Ожидался код 409, получен: {response_2.status_code}"


    @allure.title('Чтобы создать курьера, нужно передать все обязательные поля')
    def test_pass_all_required_fields(self, courier_data):
        payload_no_login = {
            "password": courier_data["password"],
            "firstName": courier_data["firstName"]
        }
        response = requests.post(
            'https://qa-scooter.praktikum-services.ru/api/v1/courier',
            data=payload_no_login
        )
        assert response.status_code == 400, f"Ожидался код 400 без login, получен: {response.status_code}"
        payload_no_password = {
            "login": courier_data["login"],
            "firstName": courier_data["firstName"]
        }
        response = requests.post(
            'https://qa-scooter.praktikum-services.ru/api/v1/courier',
            data=payload_no_password
        )
        assert response.status_code == 400, f"Ожидался код 400 без password, получен: {response.status_code}"
        payload_no_first_name = {
            "login": courier_data["login"],
            "password": courier_data["password"]
        }
        response = requests.post(
            'https://qa-scooter.praktikum-services.ru/api/v1/courier',
            data=payload_no_first_name
        )
        assert response.status_code == 201, f"Ожидался код 201 без firstName, получен: {response.status_code}"


    @allure.title("Запрос возвращает правильный код ответа")
    def test_correct_response_code(self, courier_data):
        response = requests.post(
            'https://qa-scooter.praktikum-services.ru/api/v1/courier',
            data=courier_data
        )
        assert response.status_code == 201, f"Ожидался код 201, получен: {response.status_code}"


    @allure.title("успешный запрос возвращает {\"ok\":true}")
    def test_successful_request(self, courier_data):
        response = requests.post(
            'https://qa-scooter.praktikum-services.ru/api/v1/courier',
            data=courier_data
        )
        assert response.status_code == 201, f"Курьер не создан. Код ответа: {response.status_code}"
        assert response.json() == {"ok": True}, f"Ожидался {{\"ok\":true}}, получен: {response.json()}"


    @allure.title("Если одного из полей нет, запрос возвращает ошибку")
    def test_missing_field_returns_error(self, courier_data):
        response = requests.post(
            'https://qa-scooter.praktikum-services.ru/api/v1/courier',
            data={"password": courier_data["password"], "firstName": courier_data["firstName"]}
        )
        assert response.status_code == 400, f"Ожидался код 400, получен: {response.status_code}"
        response = requests.post(
            'https://qa-scooter.praktikum-services.ru/api/v1/courier',
            data={"login": courier_data["login"], "firstName": courier_data["firstName"]}
        )
        assert response.status_code == 400, f"Ожидался код 400, получен: {response.status_code}"
        response = requests.post(
            'https://qa-scooter.praktikum-services.ru/api/v1/courier',
            data={"login": courier_data["login"], "password": courier_data["password"]}
        )
        assert response.status_code == 201, f"Ожидался код 201 без firstName, получен: {response.status_code}"


    @allure.title("Если создать пользователя с логином, который уже есть, возвращается ошибка")
    def test_if_the_username_is_the_same_an_error_appears(self, courier_data):
        response_1 = requests.post(
            'https://qa-scooter.praktikum-services.ru/api/v1/courier',
            data=courier_data
        )
        assert response_1.status_code == 201, "Первый курьер не создан"
        response_2 = requests.post(
            'https://qa-scooter.praktikum-services.ru/api/v1/courier',
            data=courier_data
        )
        assert response_2.status_code == 409, f"Ожидался код 409, получен: {response_2.status_code}"



