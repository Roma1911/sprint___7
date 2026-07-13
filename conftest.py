import allure
import pytest
import requests
import random
import string


def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


@pytest.fixture
def courier_data():
    return {
        "login": generate_random_string(10),
        "password": generate_random_string(10),
        "firstName": generate_random_string(10)
    }
    

@pytest.fixture
def create_courier():
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    courier = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    
    create_response = requests.post(
        'https://qa-scooter.praktikum-services.ru/api/v1/courier',
        data=courier
    )
    if create_response.status_code != 201:
        raise Exception(f"Не удалось создать курьера. Код: {create_response.status_code}")
    
    yield courier
    try:
        login_response = requests.post(
            'https://qa-scooter.praktikum-services.ru/api/v1/courier/login',
            data={"login": login, "password": password}
        )
        if login_response.status_code == 200:
            courier_id = login_response.json().get("id")
            
            if courier_id:
                requests.delete(
                    f'https://qa-scooter.praktikum-services.ru/api/v1/courier/{courier_id}'
                )
    except Exception:
        pass