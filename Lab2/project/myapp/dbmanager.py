import MySQLdb as mdb
import xml.etree.ElementTree as ET
import sys
import time


class DataBase:
    def __init__(self):
        self.con = mdb.connect('localhost', 'root', '1111', 'DBlab2')

    def get_table(self, name):
        with self.con:
            cur = self.con.cursor()
            cur.execute("SELECT * FROM " + name)
            return cur.fetchall()

    def get_bestsellers(self):
        with self.con:
            cur = self.con.cursor()
            cur.execute("SELECT * FROM  Product INNER JOIN Producer ON Product.producer_id=Producer.id  WHERE Product.bestseller=1 ")
            return cur.fetchall()

    def get_product_table(self):
        with self.con:
            cur = self.con.cursor()
            cur.execute("SELECT * FROM Product INNER JOIN Producer ON Product.producer_id=Producer.id")
            return cur.fetchall()

    def get_list_of_products(self):
        with self.con:
            cur = self.con.cursor()
            cur.execute("SELECT title FROM Product")
            return cur.fetchall()

    def get_order_table(self):
        with self.con:
            cur = self.con.cursor()
            cur.execute("SELECT * FROM `Order` INNER JOIN Product ON `Order`.product_id=Product.id INNER JOIN Client ON `Order`.client_id=Client.id")
            return cur.fetchall()

    def parse_xml(self):
        tree = ET.parse('bdlaba2.xml')
        root = tree.getroot()
        with self.con:
            cur = self.con.cursor()
            cur.execute("SET FOREIGN_KEY_CHECKS = 0")
            cur.execute("SET AUTOCOMMIT = 0")
            cur.execute("START TRANSACTION")
            cur.execute("TRUNCATE Producer")
            cur.execute("TRUNCATE Product")
            # cur.execute("TRUNCATE `Order`")
            cur.execute("TRUNCATE Client")
            cur.execute("SET FOREIGN_KEY_CHECKS = 1")
            cur.execute("COMMIT")
            cur.execute("SET AUTOCOMMIT = 1")
            for child in root:
                if child.tag == "providers":
                    for producer in child:
                        cur.execute(
                            "INSERT INTO Producer (title, country) VALUES('" + producer.attrib["title"] + "','" +
                            producer.attrib["country"] + "')")
                if child.tag == "products":
                    for product in child:
                        cur.execute(
                            "INSERT INTO Product (producer_id, title, bestseller, description, price) VALUES('" + product.attrib["producer_id"] + "','" +
                            product.attrib["title"] + "','" + product.attrib["bestseller"] + "','" + product.attrib["description"] + "','" + product.attrib["price"] + "')")
                if child.tag == "clients":
                    for client in child:
                        cur.execute(
                            "INSERT INTO Client (name, location) VALUES('" +
                            client.attrib["username"] + "','" +
                            client.attrib["location"] + "')")

    def insert_producer(self,request):
        with self.con:
            cur = self.con.cursor()
            cur.execute(
                "INSERT INTO Producer (title, country) VALUES('" + request["title"] + "','" +
                request["country"] + "')")

    def make_order(self,request):
        with self.con:
            date = time.strftime("%Y/%m/%d")
            cur = self.con.cursor()
            product_name = request["product_name"]
            cur.execute("SELECT id FROM Product WHERE  title='" + product_name + "' ")
            answer_one = cur.fetchone()
            for a in answer_one:
                id_of_product = str(a)
            print id_of_product
            user_name = request["username"]
            cur.execute("SELECT id FROM Client WHERE  name='" + user_name + "' ")
            answer_two = cur.fetchone()
            for a in answer_two:
                user_id = str(a)
            print user_id
            cur.execute(
                "INSERT INTO `Order` (product_id, client_id, date, count) VALUES('" + id_of_product + "','" +
                user_id + "','" + date + "','" + request["count"] + "')")

    def insert_product(self, request):
        with self.con:
            cur = self.con.cursor()
            producer_name = request["producer_name"]
            cur.execute("SELECT id FROM Producer WHERE  title='"+ producer_name +"' ")
            answer = cur.fetchone()
            for a in answer:
                id = str(a)
            cur.execute(
                "INSERT INTO Product (producer_id, title, bestseller, description, price) VALUES('" + id + "','" +
                request["title"] + "','" + request["bestseller"] + "','" + request["description"] + "','" + request["price"]  + "')")

    def edit_product(self, request):
        with self.con:
            cur = self.con.cursor()
            producer_name = request["producer_name"]
            cur.execute("SELECT id FROM Producer WHERE  title='" + producer_name + "' ")
            answer = cur.fetchone()
            for a in answer:
                id = str(a)
            cur.execute('UPDATE Product SET producer_id = {0}, title = "{1}"\
                , bestseller = {2} , description = "{3}" , price = {4}  Where title ="{5}"' \
                        .format(id, request["titleNew"], request["bestseller"], \
                                request["description"], request["price"], request["titleOld"]))


    def edit_order(self,request):
        with self.con:
            date = time.strftime("%Y/%m/%d")
            cur = self.con.cursor()
            product_name = request["product_nameold"]
            cur.execute("SELECT id FROM Product WHERE  title='" + product_name + "' ")
            answer_one = cur.fetchone()
            for a in answer_one:
                product_id = str(a)
            user_name = request["username"]
            cur.execute("SELECT id FROM Client WHERE  name='" + user_name + "' ")
            answer_two = cur.fetchone()
            for a in answer_two:
                user_id = str(a)
            cur.execute('UPDATE `Order` SET product_id = {0} \
                ,client_id = {1}, date = "{2}" , count = "{3}"  Where id ="{4}"' \
                        .format(product_id,user_id, date, \
                              request["count"], request["number"]))


    def delete_order(self,request):
        with self.con:
            cur = self.con.cursor()
            cur.execute("DELETE FROM `Order` Where id ='" + request["number"] + "'  ")


    def search_bool_mode(self,request):
        with self.con:
            print request["title"]
            cur = self.con.cursor()
            cur.execute("SELECT * FROM Product INNER JOIN Producer ON Product.producer_id=Producer.id  WHERE MATCH(Product.title) AGAINST('+{0}'  IN BOOLEAN MODE ) ".format(request["title"]))
            return cur.fetchall()

    def search_phrase(self, request):
        with self.con:
            print request["title"]
            cur = self.con.cursor()
            cur.execute(
                "SELECT * FROM Product INNER JOIN Producer ON Product.producer_id=Producer.id  WHERE MATCH(Product.title) AGAINST(' \"{0}\"'  IN BOOLEAN MODE ) ".format(
                    request["title"]))
            # cur.execute("SELECT * FROM Product INNER JOIN Producer ON Product.producer_id=Producer.id  WHERE Product.title LIKE '{0}%'".format(request["title"]))

            #  LOCATE('{0}',Product.title)".format(request["title"]))
            return cur.fetchall()


    def filtred_products(self, request):
        with self.con:
            cur = self.con.cursor()
            cur.execute(
                'SELECT * FROM Product INNER JOIN Producer ON Product.producer_id=Producer.id  WHERE price >= "{0}" and price <= "{1}"'.format(request["from"], request["to"]))
            return cur.fetchall()

dat = DataBase()
dat.parse_xml()


