import redis
import json


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

	def cache_data(self, name, key, data):
		serializable_data = []
		for document in data:
			document['_id'] = str(document['_id'])
			document['producer']['_id'] = str(document['producer']['_id'])
			# json_doc = json.dumps(document)
			serializable_data.append(document)
		self.r.hset(name, key, json.dumps(serializable_data))

	def clear_cache(self, name, product):
		product['_id'] = str(product['_id'])
		product['producer']['_id'] = str(product['producer']['_id'])
		product = json.dumps(product)
		hash_data = self.r.hgetall(name)
		for key, value in hash_data.items():
			if product in value:
				self.r.hdel(name, key)

	def search(self, name, key):
		data = self.r.hget(name, key)
		# print (data)
		if data:
			return json.loads(data)

	def fulltext_search(self, words):
		products = []
		for index in self.r.sinter(words):
			data = self.r.hget('products', index)
			if data:
				products.append(data)
		return products

	def print_all_hashes(self):
		print (self.r.hgetall('products'))