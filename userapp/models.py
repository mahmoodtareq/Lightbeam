from django.db import models
from datetime import datetime

from .verify import *

# Create your models here.

class User(models.Model):
    # id : integer
    ROLES = (
        ('U', 'User'),
        ('A', 'Admin'),
        ('M', 'Moderator')
    )

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    student_id = models.CharField(max_length=7, unique=True)       # 1305011 style
    password = models.CharField(max_length=30)
    mobile_no = models.CharField(max_length=11, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_picture/', default='profile_picture/default-user.png')
    role = models.CharField(max_length=1, default='U', choices=ROLES)

    def __str__(self):
        return self.student_id

    def save(self, *args, **kwargs):
        if (verifyUser(self)):
            super(User, self).save(*args, **kwargs)
        else:
            raise Exception
            'user information is invalid'



class Author(models.Model):
    # id : integer
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Book(models.Model):
    # id : integer
    APROVAL_STATUSES = (
        ('P', 'Pending Approval'),
        ('A', 'Approved'),
    )
    name = models.CharField(max_length=50)
    authors = models.ManyToManyField(Author)
    cover_picture = models.ImageField(upload_to='book_picture/', default='book_picture/default-book.png')
    approval_status = models.CharField(max_length=1, default='A', choices=APROVAL_STATUSES)

    def __str__(self):
        return self.name


class Product(models.Model):
    # id : integer
    PRINT_STATUSES = (
        ('A', 'American'),
        ('I', 'Indian'),
        ('P', 'Photocopy'),
    )
    CONDITIONS = (
        ('G', 'Good'),
        ('M', 'Medium'),
        ('B', 'Bad'),
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    print_status = models.CharField(max_length=1, null=True, blank=True, choices=PRINT_STATUSES)
    condition = models.CharField(max_length=1, null=True, blank=True, choices=CONDITIONS)
    edition = models.IntegerField(null=True, blank=True)
    price = models.IntegerField(default=0)
    date_time = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        unique_together = (("owner", "book"),)

    def __str__(self):
        return self.book.name + ' from ' + self.owner.student_id

    def save(self, *args, **kwargs):
        if (verifyProduct(self)):
            super(Product, self).save(*args, **kwargs)
        else:
            raise Exception
            'product information is invalid'


class Serial(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    serial_no = models.IntegerField()

    class Meta:
        unique_together = (("product", "user"),)

    def __str__(self):
        return self.product.book.name + ' - ' + self.user.student_id + ' - ' + str(self.serial_no)

    def save(self, *args, **kwargs):
        if (self.serial_no > 0):
            super(Serial, self).save(*args, **kwargs)
        else:
            raise Exception
            'serial information is invalid'


class CurrentHolder(models.Model):
    # serial = models.ForeignKey(Serial, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, unique=True)
    holder = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.product.book.name + ' - ' + self.holder.student_id
