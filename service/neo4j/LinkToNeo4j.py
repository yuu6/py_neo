# -*- coding:utf-8 -*-
"""
@Time:2018/11/8 16:48
@Author:yuhongchao
"""
from neo4j.v1 import GraphDatabase
from .CreateGraph import create_graph

class LinkToNeo(object):

	def __init__(self, uri, user, password):
		self._driver = GraphDatabase.driver(uri, auth=(user, password))

	def close(self):
		self._driver.close()

	def print_greeting(self, message):
		with self._driver.session() as session:
			greeting = session.write_transaction(self._create_and_return_greeting, message)
			print(greeting)

	def create_graph(self):
		with self._driver.session() as session:
			session.write_transaction()
			# print(greeting)

	@staticmethod
	def _create_and_return_greeting(tx, message):
		result = tx.run("CREATE (a:Greeting) "
						"SET a.message = $message "
						"RETURN a.message + ', from node ' + id(a)", message=message)
		return result.single()[0]

if __name__ == "__main__":
	# 连接neo4j
	ltn = LinkToNeo("bolt://127.0.0.1:7687", "neo4j", "root")
	ltn.print_greeting("你好啊")
	# py_neo()