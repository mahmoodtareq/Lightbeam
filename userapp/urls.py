from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/', views.register, name='register'),
    url(r'^home/', views.home, name='home'),
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^add-book/', views.add_book, name='add_book'),
    url(r'^add-new-book/', views.add_new_book, name='add_new_book'),
    url(r'^get-book-suggestion/', views.get_book_suggestion, name='get_book_suggestion'),
    url(r'^add-product/', views.add_product, name='add_product'),
    url(r'^user-books/', views.user_books, name='user_books'),
    url(r'^notifications/', views.notifications, name='notifications'),
    url(r'^search-books/', views.search_books, name='search_books'),
    url(r'^user-requests/', views.user_requests, name='user_requests'),
]