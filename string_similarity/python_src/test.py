#!/usr/bin/env python
# -*- coding: utf-8 -*-


from solr_app_match import *
from solr_app_match_spell import *
from solr_app_match_str_spell import *

reload(sys)
sys.setdefaultencoding('utf-8')



testin_file = "../data/test.in"
testout_file = "../data/test.out"
tmp = "../data/tmp_str"
rst_file = open(testout_file, 'w')

idx = 1
with io.open(testin_file, encoding="utf-8") as fin:
    test_len = len(fin.readlines())
with io.open(testin_file, encoding="utf-8") as fin:
    for line in fin.readlines():
        instr = line.strip("\n").strip()
        result = solr_app_match_str_spell(instr, tmp)
        print >> rst_file, result + "\n" + "\n"
        print str(idx) + "/" + str(test_len)
        idx += 1

fin.close()
rst_file.close()
os.remove(tmp)
