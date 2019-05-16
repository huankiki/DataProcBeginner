#coding:utf-8

import re
import io
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def str2spell(instr):
	"""
	把solr搜索url中的title字段体替换成title_spell字段
	其中title字段只能位于精确匹配中的q=()
	同时应保证: (1)fq=()中的title字段不替换;(2)albumtitles不受影响
	:param instr: solr url, eg: q=(albumtitles:青花瓷 OR title:七里香)&fq=(!title:稻香)
	:return: q=(albumtitles:青花瓷 OR title_spell:SPELL)&fq=(!title:稻香)
	"""
	p = r"(?<!f)(q=[^=]*?)title:.*?([ )])"
	pattern = re.compile(p)
	# m = re.search(pattern, instr)
	# print m.group(0)

	outstr = re.sub(pattern, r'\1title_spell:SPELL\2', instr)
	print outstr
	# print re.sub(pattern,r'\1', instr)
	# print re.sub(pattern,r'\2', instr)

###### test
# python2 demo_regex.py > ./test/url.sub
testf = "./test/url"
with io.open(testf, encoding="utf-8") as fin:
	for line in fin.readlines():
		line = line.strip("\n")
		if line:
			str2spell(line)
