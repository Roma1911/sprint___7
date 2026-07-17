
import pytest
import requests
import random
import string


BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"
CREATE_COURIER_URL = f"{BASE_URL}/courier"
LOGIN_COURIER_URL = f"{BASE_URL}/courier/login"


def generate_random_string(length: int = 10) -> str:
    chars = string.ascii_lowercase + string.digits
    return "".join(random.choices(chars, k=length))


@pytest.fixture
def courier_data():
    return {
        "login": generate_random_string(10),
        "password": generate_random_string(10),
        "firstName": generate_random_string(10),
    }
    

@pytest.fixture
def create_courier(courier_data):
    """Создаёт курьера и гарантированно удаляет его после теста."""
    response = requests.post(CREATE_COURIER_URL, data=courier_data)
    if response.status_code != 201:
        raise Exception(
            f"Не удалось создать курьера. Код: {response.status_code}, "
            f"Ответ: {response.text}"
        )

    created = response.json()
    result = {
        **courier_data,
    }
    yield result
    
@pytest.fixture
def payload_without_field():
    def _make_payload(missing_field: str):
        base = {
            "login": generate_random_string(10),
            "password": generate_random_string(10),
            "firstName": generate_random_string(10),
        }
        base.pop(missing_field, None)
        return base

    return _make_payload


