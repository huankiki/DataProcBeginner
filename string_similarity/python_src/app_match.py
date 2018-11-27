#!/usr/bin/env python
# -*- coding: utf-8 -*-

from str2spell import *

reload(sys)
sys.setdefaultencoding('utf-8')


# local_path = os.path.abspath(os.path.dirname(__file__))
# title_pinyin_dict = os.path.abspath(local_path+os.path.sep+".."+os.path.sep+"dict/title.dict")


def app_match(query_str, cand_f):
    """
    根据字符串和数据库的检索结果，计算字符串和拼音串的WER
    Input:
        - query_str, 输入字符串
        - cand_f, 检索的列表文件
    Return：经过排序的打分结果, 字符串形式
        Abc	str	spell
        abc	1	0
    """
    #################################################
    # 初始化                                         #
    #################################################
    # convert to absolute dir
    cand_f = os.path.abspath(cand_f)

    # 创建tmp文件, 用于str2spell函数的输出
    input_path = os.path.abspath(os.path.dirname(cand_f))
    tmp_f = input_path + os.path.sep + "tmp"

    #################################################
    # query_str的拼音串
    # 检索的列表文件 cand_f的拼音串
    #################################################
    query_str_spell = str2spell(query_str, tmp_f, "str")
    if query_str_spell == -1:
        print "str2spell %s failed." % query_str
        sys.exit(1)
    cand_spell = str2spell(cand_f, tmp_f, "file")
    if query_str_spell == -1:
        print "str2spell %s failed." % cand_f
        sys.exit(1)

    #################################################
    # 计算WER
    #################################################
    mat_rst = numpy.zeros((len(cand_spell), 2))
    result = ""
    result += query_str + "\tstr\t" + "spell" + "\n"

    ref_str = query_str
    ref_spell = query_str_spell[0].split("\t")[1]
    for idx in range(len(cand_spell)):
        hyp_str = cand_spell[idx].split("\t")[0]
        hyp_pinyin = cand_spell[idx].split("\t")[1]

        mat_rst[idx][0] = wer_str(ref_str, hyp_str)
        mat_rst[idx][1] = wer_str(ref_spell, hyp_pinyin)
        result += hyp_str + "\t" + str(int(mat_rst[idx][0])) + "\t" + str(int(mat_rst[idx][1])) + "\n"

    return result


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Usage: %s in_str in_file ' % sys.argv[0]
        sys.exit(1)

    """
    根据字符串和数据库的检索结果，计算字符串和拼音串的WER
    Input:
        - in_str, 输入字符串
        - in_file, 检索的列表文件
    Return：经过排序的打分结果, 字符串形式

    """
    result = app_match(sys.argv[1], sys.argv[2])

    print result





