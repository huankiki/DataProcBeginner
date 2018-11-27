#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import io
reload(sys)
sys.setdefaultencoding('utf-8')

def acc_eval(ref_file, test_file):
	"""
	计算:
	test相对于ref的准确率
	Return: 准确率, 判断的向量

	"""
	# convert to absolute dir
	ref_file = os.path.abspath(ref_file)
	test_file = os.path.abspath(test_file)

	with io.open(ref_file, encoding="utf-8") as fref, io.open(test_file, encoding="utf-8") as ftest:
		ref_list = fref.readlines()
		test_list = ftest.readlines()

	fref.close()
	ftest.close()

	result_vec = []
	correct_cnt = 0
	cnt = 0
	for i in range(len(ref_list)):
		ref = ref_list[i].strip("\n")
		test = test_list[i].strip("\n")
		test_all = test.split("\t")
		if not ref:
			break
		cnt += 1
		if ref in test_all:
			result_vec.append(1)
			correct_cnt += 1
		else:
			result_vec.append(0)
			# print ref, test

	return correct_cnt, cnt, result_vec


def eval(ref_file, base_file, test_file, testcase):
	"""
	计算:
	1) test相对于ref的准确率,以及test与base相比,准确率的提升
	2) test相对于base, 正确→ 错误, 错误→ 正确, 错误仍然错误, 三种情况的分析  

	"""

	# convert to absolute dir
	ref_file = os.path.abspath(ref_file)
	base_file = os.path.abspath(base_file)
	test_file = os.path.abspath(test_file)
	testcase = os.path.abspath(testcase)

	# base acc eval
	base_acc_cnt, base_cnt, base_vec = acc_eval(ref_file, base_file)

	# test acc eval
	test_acc_cnt, test_cnt, test_vec = acc_eval(ref_file, test_file)

	print str(base_acc_cnt) + "/" + str(base_cnt)
	print str(test_acc_cnt) + "/" + str(test_cnt)
	print

	# compare base and test eval results
	if base_cnt != test_cnt:
		return -1
	
	fp_dict = []	# right to wrong
	fp_dict.append("right to wrong")
	tn_dict = []	# wrong to wrong
	tn_dict.append("wrong to wrong")
	fn_dict = []	# wrong to right
	fn_dict.append("wrong to right")

	with io.open(ref_file, encoding="utf-8") as fref, io.open(test_file, encoding="utf-8") as ftest:
		ref_list = fref.readlines()
		test_list = ftest.readlines()
	with io.open(base_file, encoding="utf-8") as fbase, io.open(testcase, encoding="utf-8") as ftestcase:
		base_list = fbase.readlines()
		testcase_list = ftestcase.readlines()

	for i in range(test_cnt):
		if base_vec[i] == 1 and test_vec[i] == 0:	# right to wrong
			rst = testcase_list[i].strip("\n") + "\t" + ref_list[i].strip("\n") + "\t" + base_list[i].strip("\n").replace("\t", "/") + "\t" + test_list[i].strip("\n").replace("\t", "/")
			fp_dict.append(rst)
		elif base_vec[i] == 0 and test_vec[i] == 0:	# wrong to wrong
			rst = testcase_list[i].strip("\n") + "\t" + ref_list[i].strip("\n") + "\t" + base_list[i].strip("\n").replace("\t", "/") + "\t" + test_list[i].strip("\n").replace("\t", "/")
			tn_dict.append(rst)
		elif base_vec[i] == 0 and test_vec[i] == 1:	# wrong to right
			rst = testcase_list[i].strip("\n") + "\t" + ref_list[i].strip("\n") + "\t" + base_list[i].strip("\n").replace("\t", "/") + "\t" + test_list[i].strip("\n").replace("\t", "/")
			fn_dict.append(rst)
		else:
			pass

	for i in [fp_dict, tn_dict, fn_dict]:
		for j in i:
			print j
		print



if __name__ == '__main__':
	if len(sys.argv) < 5:
		print 'Usage: %s ref base test testcase' % sys.argv[0]
		sys.exit(1)

	"""
	计算:
	1) test相对于ref的准确率,以及test与base相比,准确率的提升
	2) test相对于base, 正确→ 错误, 错误→ 正确, 错误仍然错误, 三种情况的分析  
    """
	
	eval(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])


