import random
import string

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"
CREATE_COURIER_URL = f"{BASE_URL}/courier"
LOGIN_COURIER_URL = f"{BASE_URL}/courier/login"
ORDERS_URL = f"{BASE_URL}/orders"


def generate_random_string(length: int = 10) -> str:
    chars = string.ascii_lowercase + string.digits
    return "".join(random.choices(chars, k=length))