from django.db import *
from .models import *


def searchAll(key, id):
    return (searchBook(key, id) | searchAuthor(key, id) | searchCategory(key, id)).distinct()


def searchBook(key, id):
    return Product.objects.filter(book__name__icontains=key).exclude(owner__id=id)


def searchAuthor(key, id):
    return Product.objects.filter(book__authors__name__icontains=key).exclude(owner__id=id)


def searchCategory(key, id):
    return Product.objects.filter(book__categories__name__icontains=key).exclude(owner__id=id)
