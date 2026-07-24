import random
import string

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"
CREATE_COURIER_URL = f"{BASE_URL}/courier"
LOGIN_COURIER_URL = f"{BASE_URL}/courier/login"
DELETE_COURIER_URL = f"{BASE_URL}/courier"
ORDERS_URL = f"{BASE_URL}/orders"


def generate_random_string(length=10):
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return "".join(random.choice(letters) for _ in range(length))