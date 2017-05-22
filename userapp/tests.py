from django.test import TestCase
import unittest
from .verify import *
from .models import *


class TestEmail(unittest.TestCase):
    def test_email_1(self):
        assert verifyEmail('abc@gmail.com')

    def test_email_2(self):
        assert not verifyEmail('abs')

    def test_email_3(self):
        assert not verifyEmail('')

    def test_email_4(self):
        assert not verifyEmail('a@com')

    def test_email_5(self):
        assert not verifyEmail('a.com')


class TestProduct(unittest.TestCase):
    def setUp(self):
        # self.owner = User()
        # self.book = Book()
        self.product1 = Product(edition=0)
        self.product2 = Product(price=0)
        self.product3 = Product(edition=-1)
        self.product4 = Product(price=-1)
        self.product5 = Product(edition=2)
        self.product6 = Product(price=10)

    def tearDown(self):
        del self.product1
        del self.product2
        del self.product3
        del self.product4
        del self.product5
        del self.product6

    def test_product_1(self):
        assert verifyProduct(self.product1)

    def test_product_2(self):
        assert verifyProduct(self.product2)

    def test_product_3(self):
        assert not verifyProduct(self.product3)

    def test_product_4(self):
        assert not verifyProduct(self.product4)

    def test_product_5(self):
        assert verifyProduct(self.product5)

    def test_product_6(self):
        assert verifyProduct(self.product6)


