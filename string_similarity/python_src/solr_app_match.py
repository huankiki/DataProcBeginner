#!/usr/bin/env python
# -*- coding: utf-8 -*-

from str2spell import *
from search_solr import *

reload(sys)
sys.setdefaultencoding('utf-8')

COUNT = 100
none_wer = 100


def solr_app_match(query_str, result_f):
    """
    根据字符串和数据库的检索结果，计算字符串和拼音串的WER
    其中检索结果是基于solr的，带有title_spell
    Input:
        - query_str, 输入字符串
        - cand_f, 检索的列表文件，带有title_spell
    Return：经过排序的打分结果, 字符串形式
        Abc	str	spell
        abc	1	0
    """
    #################################################
    # 初始化                                         #
    #################################################
    # convert to absolute dir
    result_f = os.path.abspath(result_f)

    # 创建tmp文件, 用于str2spell函数的输出
    output_path = os.path.abspath(os.path.dirname(result_f))
    tmp_f = output_path + os.path.sep + "tmp.lst"
    cand_f = output_path + os.path.sep + "cand.lst"

    #################################################
    # query_str的拼音串
    # 检索的列表文件 cand_f的拼音串
    #################################################
    query_str_spell = str2spell(query_str, tmp_f, "str", "spell")
    if query_str_spell == -1:
        print "str2spell %s failed." % query_str
        sys.exit(1)

    ref_spell = query_str_spell[0].split("\t")[1]

    query_str_phoneme = str2spell(query_str, tmp_f, "str", "phoneme")
    if query_str_phoneme == -1:
        print "str2spell %s failed." % query_str
        sys.exit(1)

    ref_str = query_str
    ref_phoneme = query_str_phoneme[0].split("\t")[1]
    print ref_str, ref_spell, ref_phoneme

    flag = search_solr(ref_str, cand_f, count=COUNT)
    if flag == "-1":
        sys.exit(0)
    cand_spell = []
    with io.open(cand_f, encoding="utf-8") as fc:
        for line in fc.readlines():
            line_lst = line.strip("\n").strip().split("\t")
            title = line_lst[0]
            title_spell = line_lst[1]
            cand_spell.append(title + "\t" + title_spell)
    fc.close()

    #################################################
    # 计算WER
    #################################################
    mat_rst = numpy.zeros((len(cand_spell), 2))
    result = ""
    result_head = query_str + "\tstr\t" + "spell" + "\n"

    for idx in range(len(cand_spell)):
        hyp_str = cand_spell[idx].split("\t")[0]
        hyp_spell = cand_spell[idx].split("\t")[1]

        mat_rst[idx][0] = wer_str(ref_str, hyp_str)
        if hyp_spell == "None":
            result += hyp_str + "\t" + str(int(mat_rst[idx][0])) + "\t" + str(none_wer) + "\n"
            continue

        mat_rst[idx][1] = wer_str(ref_phoneme, hyp_spell)
        result += hyp_str + "\t" + str(int(mat_rst[idx][0])) + "\t" + str(int(mat_rst[idx][1])) + "\n"

    result = result.strip("\n")

    rst_file = open(tmp_f, 'w')
    print >> rst_file, result

    tmp2_f = output_path + os.path.sep + "tmp2.lst"
    rst_file = open(tmp2_f, 'w')
    print >> rst_file, result_head

    # 删除最后一个空行
    rst_file.seek(-1, os.SEEK_END)
    rst_file.truncate()
    rst_file.close()

    #################################################
    # 排序
    #################################################
    shell_cmd = "cat " + tmp_f + " | sort -k3n,3 -k2n,2 " + " -o " + result_f
    os.system(shell_cmd)
    shell_cmd = "head -n 100 " + result_f + " > " + tmp_f
    os.system(shell_cmd)
    shell_cmd = "cat " + tmp2_f + " " + tmp_f + " > " + result_f
    os.system(shell_cmd)

    # 删除中间文件
    os.remove(tmp_f)
    os.remove(tmp2_f)
    os.remove(cand_f)
    #################################################
    # return
    #################################################
    result = ""
    with io.open(result_f, encoding="utf-8") as fc:
        for line in fc.readlines():
            result += line.strip("\n").strip() + "\n"

    fc.close()
    return result.strip("\n")




if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Usage: %s in_str result_file ' % sys.argv[0]
        sys.exit(1)

    """
    根据字符串和数据库的检索结果，计算字符串和拼音串的WER
    Input:
        - in_str, 输入字符串
        - in_file, 检索的列表文件
    Return：经过排序的打分结果, 字符串形式

    """
    result = solr_app_match(sys.argv[1], sys.argv[2])

    print result





