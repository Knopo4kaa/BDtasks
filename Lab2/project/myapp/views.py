from django.shortcuts import render
from django.http import HttpResponseRedirect
from .dbmanager import DataBase
from .dbmongomanager import Database

db = DataBase()
database = Database()


def orders(request):
    orders_ = [order for order in database.db.Order.find().limit(50)]
    clients = [order for order in database.db.Client.find()]
    products = [order for order in database.db.Product.find()]
    # for order in orders_:
    #     print order
    if request.method == "POST":
        result_of_orders = database.sum_of_orders()
        result_of_buying = database.count_by_date()
        result_of_products = database.analize_orders()
        # print result_of_products
        return render(request, 'myapp/home.html', {'response': {'orders': orders_, 'clients': clients,
                                                                'products': products, 'results_of_orders': result_of_orders.find(),
                                                                'results_of_buying': result_of_buying.find(),
                                                                'results_of_products': result_of_products}})
    return render(request, 'myapp/home.html', {'response': {'orders': orders_, 'clients': clients,
                                                            'products': products}})


def producers_page(request):
    return render(request, 'myapp/index.html',  {'response': {'producers': database.db.Producer.find()}})


def clients_page(request):
    return render(request, 'myapp/clients.html',  {'response': {'clients': database.db.Client.find()}})


def products_page(request):
    return render(request, 'myapp/products.html',  {'response': {'products': database.db.Product.find()}})


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

