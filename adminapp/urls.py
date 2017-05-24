from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^administration/', views.administration, name='administration'),
    url(r'^administration-users/', views.users, name='users'),
    url(r'administration-book-approvals/', views.book_approvals, name='book_approvals'),
    url(r'administration-approve-book/', views.approve_book, name='approve_book'),
    url(r'^administration-change-role/', views.change_role, name='change_role'),
    url(r'^administration-remove-user/', views.remove_user, name='remove_user'),
]