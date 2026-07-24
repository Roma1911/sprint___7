
import pytest
import requests
from helpers import (
    CREATE_COURIER_URL,
    LOGIN_COURIER_URL,
    DELETE_COURIER_URL,
    generate_random_string,
)


@pytest.fixture
def courier_data():
    return {
        "login": generate_random_string(10),
        "password": generate_random_string(10),
        "firstName": generate_random_string(10),
    }
    

@pytest.fixture
def create_courier(courier_data):
    response = requests.post(CREATE_COURIER_URL, data=courier_data)
    assert response.status_code == 201, (
        f"Не удалось создать курьера. Код: {response.status_code}, "
        f"Ответ: {response.text}"
    )
    yield courier_data
    login_response = requests.post(
        LOGIN_COURIER_URL,
        data={
            "login": courier_data["login"],
            "password": courier_data["password"],
        },
    )
    if login_response.status_code == 200:
        token = login_response.json().get("accessToken")
        if token:
            requests.delete(
                DELETE_COURIER_URL,
                headers={"Authorization": f"Bearer {token}"},
            )

    
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


