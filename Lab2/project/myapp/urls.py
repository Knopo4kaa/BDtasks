from django.conf.urls import url
from django.contrib import admin
from  . import  views

urlpatterns = [
    url(r'^$', views.orders, name="home_page"),
    url(r'^producers_page', views.producers_page, name="producers_page"),
    url(r'^products', views.products_page , name='products_page'),
    url(r'^clients', views.clients_page , name='clients_page'),
    # url(r'^insert_producer', views.insert_producer, name='insert_producer'),
    # url(r'^insert_product', views.insert_product, name='insert_product'),
    # url(r'^edit_product', views.edit_product, name='edit_product'),
    # url(r'^show_bestsellers', views.bestseller_products_page , name='show_bestsellers'),
    url(r'^make_order', views.make_order, name='make_order'),
    url(r'^edit_order', views.edit_order, name='edit_order'),
    url(r'^delete_order', views.delete_order, name='delete_order'),
    # url(r'^search_bool_mode', views.search_bool_mode, name='search_bool_mode'),
    # url(r'^filtred_products', views.filtred_products, name='filtred_products'),
    # url(r'^search_phrase', views.search_phrase, name='search_phrase'),
]