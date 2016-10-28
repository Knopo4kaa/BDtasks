import redis
import json
import ast


class Cache:

	def __init__(self):
		self.r = redis.Redis(host='localhost', port=6379)
		self.current_index = 0
		self.r.flushall()

	def indexing(self, data):
		for index, document in enumerate(data, self.current_index):
			document.pop('_id', None)
			document['producer'].pop('_id', None)
			self.current_index += 1
			self.r.hset('products', index, json.dumps(document))
			for word in document['title'].split(' '):
				self.r.sadd(word, index)

	def cache_data(self, key, data):
		changed_products = []
		for document in data:
			document.pop('_id', None)
			document['producer'].pop('_id', None)
			changed_products.append(json.dumps(document))
		self.r.sadd(key, *changed_products)

	def clear_cache(self, product):
		product.pop('_id', None)
		product['producer'].pop('_id', None)
		product = json.dumps(product)
		for key in self.r.scan(0)[1]:
			if product in list(self.r.smembers(key)):
				self.r.delete(key)
				continue

	def search(self, key):
		products = list(self.r.smembers(key))
		return products

	def fulltext_search(self, words):
		products = []
		for index in self.r.sinter(words):
			data = self.r.hget('products', index)
			if data:
				products.append(data)
		return products

	def print_all_hashes(self):
		print (self.r.hgetall('products'))