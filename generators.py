import random
import string

def generate_random_string(length=10):
    chars = string.ascii_lowercase + string.digits
    return "".join(random.choices(chars, k=length))