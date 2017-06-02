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
    url(r'^search/', views.search, name='search'),
    url(r'^notifications/', views.notifications, name='notifications'),
    url(r'^search-books/', views.search_books, name='search_books'),
    url(r'^user-requests/', views.user_requests, name='user_requests'),
    url(r'^book-request/', views.book_request, name="book_request"),
    url(r'^save-profile/', views.save_profile, name="save-profile"),
    url(r'^view-book/(?P<product_id>[0-9]+)$', views.view_book, name='view_book'),
    url(r'^user/(?P<user_id>[0-9]+)$', views.profile, name='profile'),
    url(r'^confirm-product/', views.confirm_product, name='confirm_product'),
    url(r'^delete-product/', views.delete_product, name='delete_product'),
]