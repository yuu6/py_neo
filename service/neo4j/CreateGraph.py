# -*- coding:utf-8 -*-
"""
@Time:2018/11/8 17:06
@Author:yuhongchao
"""
import pandas as pd
import os
import cx_Oracle
import numpy as np


def get_link():
	filenames = os.listdir("../data/links")
	res_lis = set()
	res = np.array(['GF_NSRSBH', 'XF_NSRSBH', 'JE'])
	for file in filenames:
		str = "../data/links/" + file
		temp = pd.read_pickle(str)
		print(temp.columns)
		res = np.vstack([res, temp])
	pd.to_pickle(res, "links.pickle")


def get_node():
	filenames = os.listdir("../data/links")
	res_lis = set()
	for file in filenames:
		str = "../data/links/" + file
		temp = pd.read_pickle(str)
		res_lis = res_lis | set(temp["GF_NSRSBH"])
		res_lis = res_lis | set(temp["XF_NSRSBH"])
	# pass
	print(res_lis)

	node_res = np.array(["Nsrsbh", "Nsrdzdah", "nsrmc", "Scjydz", "Fddbrmc"])
	for i in res_lis:
		mess = get_mess(i)
		print(len(node_res))
		if mess != None:
			temp_arr = np.array([i, mess[3], mess[0], mess[1], mess[2]])
			node_res = np.vstack([node_res, temp_arr])
		else:
			temp_arr = np.array([i, None, None, None, None])
			node_res = np.vstack([node_res, temp_arr])

	pd.to_pickle(node_res, "nodes.pickle")


def get_mess(v):
	sql = """
		select dn.nsrmc,Dn.Scjydz,Dn.Fddbrmc,Dn.Nsrdzdah
		from DJ_NSRXX dn
		WHERE dn.nsrsbh ='{}'""".format(v)
	# cur.executemany("""
	#        select dn.NSRMC,ll.VERTEXID,FDDBRMC,HY_DM,Dn.Scjydz from (select * from  LG_GROUNDTRUTH) ll left
	#        join DJ_NSRXX dn on ll.NSRDZDAH=dn.NSRDZDAH where ll.Vertexid=(:0)""", v_list)
	print(sql)
	cur.execute(sql)
	res = cur.fetchall()
	print(res)
	return res[0] if len(res) >= 1 else None


if __name__ == "__main__":
	# 获得数据库的连接
	con = cx_Oracle.connect('tax/taxgm2016@192.168.16.186/tax', encoding='utf8')
	cur = con.cursor()

	get_node()

	# 释放数据库的连接
	cur.close()
	con.close()
	# get_link()

	# links = pd.read_pickle("links.pickle")
	# l_pd = pd.DataFrame(links)
	# print(l_pd)
# nodes = pd.read_pickle("nodes.pickle")
# l_pd = pd.DataFrame(nodes)
# print(nodes)
