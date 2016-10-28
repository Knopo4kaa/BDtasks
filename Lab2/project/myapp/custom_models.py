import datetime


class Client:

	def __init__(self, name_, age_):
		self.name = name_
		self.age = age_

	def __str__(self):
		return self.name


class Order:

	def __init__(self, product_, client_, count_):
		self.product = product_
		self.client = client_
		self.date = datetime.datetime.now()
		self.count = count_

	def __str__(self):
		return "Client {} bought {} in count {}.".format(self.client, self.product, self.count)


class Producer:

	def __init__(self, title_, country_):
		self.title = title_
		self.country = country_

	def __str__(self):
		return self.title


class Product:

	def __init__(self, producer_, title_, description_, price_):
		self.producer = producer_
		self.title = title_
		self.description = description_
		self.price = price_

	def __str__(self):
		return self.title
