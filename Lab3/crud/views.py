from django.shortcuts import render
from django.http import HttpResponseRedirect
from .dbmanager import Database
from .cashemanager import Cache
from datetime import datetime
import json

database = Database()
cache = Cache()


def orders(request):
    # page_number = int(page_number)
    orders_ = [order for order in database.db.Order.find().limit(50)]
    clients = [order for order in database.db.Client.find()]
    products = [order for order in database.db.Product.find().limit(50)]
    if request.method == "POST":
        result_of_orders = database.sum_of_orders()
        result_of_buying = database.count_by_date()
        result_of_products = database.analize_orders()
        return render(request, 'crud/home.html', {'response': {'orders': orders_, 'clients': clients,
                                                                'products': products, 'results_of_orders': result_of_orders.find(),
                                                                'results_of_buying': result_of_buying.find(),
                                                                'results_of_products': result_of_products}})
    return render(request, 'crud/home.html', {'response': {'orders': orders_, 'clients': clients,
                                                            'products': products}})


def producers_page(request):
    return render(request, 'crud/index.html',  {'response': {'producers': database.db.Producer.find()}})


def clients_page(request):
    return render(request, 'crud/clients.html',  {'response': {'clients': database.db.Client.find()}})


def products_page(request):
    search = False
    if request.method == 'POST':
        product_title = request.POST['product_name'].lower()

        # words = set(product_title.split(' '))
        t0 = datetime.now()
        products = cache.search(product_title)
        dt1 = datetime.now() - t0

        if not products:
            t0 = datetime.now()
            products = database.search_products(product_title)
            dt2 = datetime.now() - t0
            if products:
                cache.cache_data(product_title, products)
                print ('Loaded from database!')
                print ("Database search: {}".format(dt2.total_seconds()))
        else:
            json_products = []
            for product in products:
                json_products.append(json.loads(product))
            products = json_products
            print ('Loaded from cache!')
            print ("Cache search: {}".format(dt1.total_seconds()))
        search = True
    else:
        products = [order for order in database.db.Product.find().limit(50)]
    return render(request, 'crud/products.html',  {'response': {'products': products,'flag': search}})


def make_order(request):
    if request.method == "POST":
        if request.POST["client_id"] != "" and request.POST["product_id"] != "":
            database.insert_order(request.POST)
        return HttpResponseRedirect('/')


def edit_order(request):
    if request.method == "POST":
        if request.POST["order_id"] != "" and request.POST["client_id"] != "" and request.POST["product_id"] != "":
            database.edit_order(request.POST)
        return HttpResponseRedirect('/')


def delete_order(request):
    if request.method == "POST":
        if request.POST["order_to_delete"] != "":
            database.delete_order(request.POST["order_to_delete"])
        return HttpResponseRedirect('/')


def delete_product(request):
    if request.method == "POST":
        if request.POST["product_to_delete"]:
            product_id = request.POST['product_to_delete']
            product = database.delete_product(product_id)
            cache.clear_cache(product)
        return HttpResponseRedirect('/products')