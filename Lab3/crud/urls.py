from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.orders, name="home_page"),
    url(r'^producers_page', views.producers_page, name="producers_page"),
    url(r'^products', views.products_page , name='products_page'),
    url(r'^clients', views.clients_page , name='clients_page'),
    url(r'^make_order', views.make_order, name='make_order'),
    url(r'^edit_order', views.edit_order, name='edit_order'),
    url(r'^delete_order', views.delete_order, name='delete_order'),
    url(r'^delete_product', views.delete_product, name='delete_product'),
]