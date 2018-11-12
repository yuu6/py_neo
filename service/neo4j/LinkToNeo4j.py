# -*- coding:utf-8 -*-
"""
@Time:2018/11/8 16:48
@Author:yuhongchao
"""
from neo4j.v1 import GraphDatabase
import pandas as pd
import numpy as np

# 将交易关系以及属性存储到neo4j数据库里面
# 之后还要将嫌疑值存储在其中

class LinkToNeo(object):

	def __init__(self, uri, user, password):
		self._driver = GraphDatabase.driver(uri, auth=(user, password))

	def close(self):
		self._driver.close()

	def create_graph(self):
		with self._driver.session() as session:
			greeting = session.write_transaction(self._create_graph,self.get_info())
			print(greeting)

	@staticmethod
	def _create_graph(tx,mess):
		tx.run(mess)

	def get_info(self):
		links = pd.read_pickle("basicData/links.pickle")
		nodes = pd.read_pickle("basicData/nodes.pickle")
		l_d = pd.DataFrame(links[1:, :], columns=["GF_NSRSBH", "XF_NSRSBH", "JE"])
		n_d = pd.DataFrame(nodes[1:, :], columns=["NSRSBH", "Nsrdzdah", "nsrmc", "Scjydz", "Fddbrmc"])

		n = np.array(n_d)
		l = np.array(l_d)
		res_str = ""
		for i in range(1, n.__len__()):
			a_tuple = n[i]
			a_str = "CREATE ({}:Company {} nsrmc: '{}', nsrdzdah: '{}',nsrsbh:'{}', Scjydz: '{}', Fddbrmc:'{}'{})".format(
				"n" + str(a_tuple[0]), "{", a_tuple[2], a_tuple[1], a_tuple[0], a_tuple[3], a_tuple[4], "}")
			# /print(a_str)
			res_str += a_str
		for i in range(1, l.__len__()):
			a_tuple = l[i]
			# print(a_tuple)
			a_str = "create  ({})-[:JIAOYI {}JE:{}{}]->({})".format(
				"n" + str(a_tuple[0]), "{", round(a_tuple[2]), "}", "n" + str(a_tuple[1]))
			print(a_str)
			res_str += a_str
		return res_str+";"



if __name__ == "__main__":
	# 连接neo4j
	ltn = LinkToNeo("bolt://127.0.0.1:7687", "neo4j", "yuu6")
	ltn.create_graph()
# py_neo()
