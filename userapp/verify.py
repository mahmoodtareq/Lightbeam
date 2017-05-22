import re
from .models import *

def verifyEmail(email):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False
    return True


def verifyUser(user):
    return verifyEmail(user.email)


def verifyProduct(product):
    return (product.edition == None or (product.edition >= 0 and product.edition <= 99)) and product.price >= 0
