import random
import string

def random_email():
    return f"user_{''.join(random.choices(string.ascii_lowercase + string.digits, k=8))}@example.com"

def random_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=12))

def random_name():
    return "User" + ''.join(random.choices(string.ascii_letters, k=6))
