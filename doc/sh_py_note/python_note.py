#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string
import sys

###############################
# 设置默认编码
reload(sys)
sys.setdefaultencoding('utf-8')

##############################
# 判断是否为unicode编码 def func_example(instr):
    """
    function doc string
    """
    if not isinstance(instr, unicode):
        instr = unicode(instr, 'utf-8')

    rstring = ""
    #########################
    ## function body
    #########################
    
    rstring = rstring.encode("utf-8")
    return rstring

##############################
# 删除英文标点符号, 其中line必须为str类型，不能是unicode，所以一般要line.encode("utf-8")
table = string.maketrans("", "")
line = line.translate(table, string.punctuation)

##############################
# Python中调用shell命令
cmd = "cat " + file_name + ";echo"
os.system(cmd)
##############################
# 在Python中删除和拷贝文件
from shutil import copyfile
copyfile(des_file, source_file)
os.remove(file_name)


