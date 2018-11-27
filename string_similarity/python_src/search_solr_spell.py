#!/usr/bin/env python
# -*- coding: utf-8 -*-

import chardet
import requests
import json
import sys
import os
from utils.format_util import *

reload(sys)
sys.setdefaultencoding('utf-8')

url_body = 'http://10.10.10.102:8984/solr/resource/select?q=(title_spell:'
url_dict = {
  "title_spell": "uuu gui sai pao",
  "start": 0,
  "rows": 10
}


def search_solr_spell(query_str, out_file, count=10):
    """
    根据字符串和数据库的检索结果，计算字符串和拼音串的WER
    Input:
        - query_str, 输入字符串
        - cand_f, 检索的列表文件
    Return：经过排序的打分结果, 字符串形式
        Abc	str	spell
        abc	1	0
    """

    result = ""

    # convert to absolute dir
    out_file = os.path.abspath(out_file)
    rst_file = open(out_file, 'w')

    url_dict["rows"] = count
    url_dict["title_spell"] = query_str
    url = url_body + str_escape_solr(url_dict["title_spell"]) + ")&start=0&rows=" + str(url_dict["rows"])
    #print url

    response = requests.get(url)
    rst = json.loads(response.text)
    if rst["response"]["numFound"] == 0:
        print "no search result"
        return -1
    rst = rst["response"]["docs"]
    # print rst
    # 返回信息
    for idx in range(len(rst)):
        title = rst[idx]["title"]
        title_spell = "None"
        if "title_phoneme" in rst[idx]:
            if rst[idx]["title_phoneme"]:
                title_spell = rst[idx]["title_phoneme"]
        result += title + "\t" + title_spell + "\n"
        # result += title + "\t" + title_spell + "\t" + str(rst[idx]["id"]) + "\n"
    print >> rst_file, result.strip("\n")

    return result.strip("\n")




if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Usage: %s in_str out_file [count]' % sys.argv[0]
        sys.exit(1)

    """
    根据输入字符串检索，得到title字段文件
    resouce检索的api，封装之后的api
    count的默认值为30

    """

    # 初始化
    if len(sys.argv) == 3:
      count = 10
    else:
      count = sys.argv[3]


    in_str = sys.argv[1]
    out_file = sys.argv[2]

    # search
    result = search_solr_spell(in_str, out_file, count)
    print result

