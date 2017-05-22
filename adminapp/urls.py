from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^administration/', views.administration, name='administration'),
    url(r'^administration-admins/', views.admins, name='admins'),
]