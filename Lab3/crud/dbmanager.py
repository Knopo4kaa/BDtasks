from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.code import Code
from bson.son import SON
import time
import random


class Database:

	def __init__(self):
		self.client = MongoClient()
		self.db = self.client.bdlab2
		# self.fill_products()
		# self.create_collections_if_not_exists()

	def fill_products(self):
		product_titles = [
			'Xiaomi Redmi 3s 16GB Gold',
			'Sony Xperia Z5 Dual Premium Black ',
			'Apple iPhone 5s 32GB Space Gray ',
			'Meizu M2 16GB White ',
			'Asus Zenfone Max (ZC550KL-6B043WW) Dual Sim White',
			'Sigma mobile X-treme IT67 Dual Sim Orange ',
			'Doogee Y300 Black',
			'Acer Liquid Z520 DualSim Black',
			'Keneksi Art M1 Red',
			'Huawei P9 Titanium Grey',
			'LG G5 SE Titan',
			'Blackview BV5000 Sunny Orange',
			'Sigma mobile X-treme PQ25 Black ',
			'Keneksi E2 Black',
			'Meizu Pro 5 32GB White',
			'Lenovo A7000 White',
			'Philips Xenium V377 Dual Sim Black-Red ',
			'Coolpad MAX Gold',
			'Coolpad Torino S Gold',
			'Gigabyte Gsmart Alto A2 DualSim Black ',
			'Acer Liquid Z330 DualSim Black'
		]
		producers = [producer for producer in self.db.Producer.find()]
		for i in range(0, 50000):
			producer = producers[random.randint(0, len(producers)-1)]
			product_title = product_titles[random.randint(0, len(product_titles)-1)]
			product_title += ' ' + str(random.randint(0, 8)) + product_title[0]
			price = random.randint(100, 1000)
			product = {'title': product_title, 'producer': producer, 'price': price}
			self.db.Product.insert(product)


	# def fill_db(self):
	# 	clients = [client for client in self.db.Client.find()]
	# 	products = [product for product in self.db.Product.find()]
	# 	for i in xrange(0, 50000):
	# 		selected_products = []
	# 		random_client = clients[random.randint(0, len(clients) - 1)]
	# 		count_of_products = random.randint(2, 7)
	# 		for _ in range(0, count_of_products):
	# 			selected_products.append(products[random.randint(0, len(products) - 1)])
	#
	# 		order = {'product': selected_products, 'client': random_client, 'date': time.strftime('%d/%m/%Y')}
	# 		self.db.Order.insert(order)

	def insert_order(self, dict):
		client = self.db.Client.find_one({'_id':ObjectId(dict['client_id'])})
		list_of_products = []
		for product_id in dict.getlist('product_id'):
			product = self.db.Product.find_one({'_id': ObjectId(product_id)})
			list_of_products.append(product)
		order = {'product': list_of_products, 'client': client, 'date': time.strftime('%d/%m/%Y')}
		self.db.Order.insert(order)

	def delete_order(self, order_id):
		self.db.Order.delete_one({'_id':ObjectId(order_id)})

	def delete_product(self, product_id):
		deleted_product = self.db.Product.find_one({'_id': ObjectId(product_id)})
		self.db.Product.delete_one(deleted_product)
		return deleted_product

	def edit_order(self, dict):
		client = self.db.Client.find_one({'_id': ObjectId(dict['client_id'])})
		list_of_products = []
		for product_id in dict.getlist('product_id'):
			product = self.db.Product.find_one({'_id': ObjectId(product_id)})
			list_of_products.append(product)
		self.db.Order.update_one({'_id': ObjectId(dict['order_id'])}, {'$set': {'client': client,
		                                                                      'product': list_of_products}})

	def search_products(self, product_name):
		# client = self.db.Client.find_one({'_id': ObjectId(dict['searched_client_id'])})
		return [product for product in self.db.Product.find({'$text': {'$search': product_name}})]

	def sum_of_orders(self):
		map = Code("""
				   function(){
					  var clientName = this.client.name;
					  this.product.forEach(function(z) {
						emit(clientName, z.price);
					});
		           };
		           """)

		reduce = Code("""
					  function(key, valuesPrices){
						var sum = 0;
						for (var i = 0; i < valuesPrices.length; i++) {
						  sum += valuesPrices[i];
						}
						return sum;
		              };
		              """)
		results = self.db.Order.map_reduce(map, reduce, "results_")
		# for doc in results.find():
		# 	print doc
		return results

	def analize_orders(self):
		pipeline = [
			{"$unwind": "$product"},
			{"$group": {"_id": "$product.title", "count": {"$sum": 1}}},
			{"$sort": SON([("count", -1)])}
		]
		return list(self.db.Order.aggregate(pipeline))

	def count_by_date(self):
		map = Code("""
				   function(){
					  emit(this.date, 1);
		           };
		           """)

		reduce = Code("""
					  function(key, valuesPrices){
						var sum = 0;
						for (var i = 0; i < valuesPrices.length; i++) {
						  sum += valuesPrices[i];
						}
						return sum;
		              };
		              """)
		results = self.db.Order.map_reduce(map, reduce, "product_analysis")
		return results