from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^administration/', views.administration, name='administration'),
    url(r'^administration-users/', views.users, name='users'),
    url(r'^administration-change-role/', views.change_role, name='change_role'),
    url(r'^administration-remove-user/', views.remove_user, name='remove_user'),
]