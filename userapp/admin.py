from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Product)
admin.site.register(Serial)
admin.site.register(CurrentHolder)
admin.site.register(Category)
