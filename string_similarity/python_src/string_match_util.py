#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
import os
import io
import string
from utils.format_util import *
from utils.digit2zh import *

reload(sys)
sys.setdefaultencoding('utf-8')


def split_string(instr):
    """
    拆分中英文混合的字符串

    Example：
        Input: 'a魏和河this is a test'
        Output: ['a', '魏', '和', '河', 'this', 'is', 'a', 'test']
    """
    if not isinstance(instr, unicode):
        instr = unicode(instr, 'utf-8')

    rst = []
    str_past = ""
    en_flag = 0
    idx = 0
    for uchar in instr:
        idx += 1
        if is_chinese(uchar):
            if en_flag == 1:
                rst.append(str_past.encode("utf-8"))
                str_past = ""
                en_flag = 0
            rst.append(uchar.encode("utf-8"))
        elif is_other(uchar):
            if en_flag == 1:
                rst.append(str_past.encode("utf-8"))
                str_past = ""
                en_flag = 0
        else:
            str_past += uchar
            en_flag = 1
            if idx == len(instr):
                rst.append(str_past.encode("utf-8"))
                str_past = ""
                en_flag = 0

    return rst


def wer_list(r, h):
    """
    计算两个列表的WER

    Input:
        - r, 参考字符串列表, eg.["青", "花", "瓷"]
        - h, 测试字符串列表, eg.["青", "花"]
    Output: WER的值, 不需要经过归一化(除以refstr的长度)
    """
    # initialisation
    d = numpy.zeros((len(r) + 1) * (len(h) + 1), dtype=numpy.uint8)
    d = d.reshape((len(r) + 1, len(h) + 1))
    for i in range(len(r) + 1):
        for j in range(len(h) + 1):
            if i == 0:
                d[0][j] = j
            elif j == 0:
                d[i][0] = i

    # computation
    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            if r[i - 1] == h[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                substitution = d[i - 1][j - 1] + 1
                insertion = d[i][j - 1] + 1
                deletion = d[i - 1][j] + 1
                d[i][j] = min(substitution, insertion, deletion)

    return d[len(r)][len(h)]


def wer_str(refstr, hypstr):
    """
    计算两个字符串的WER

    Input:
        - refstr, 参考字符串, eg."青花瓷"
        - hypstr, 测试字符串, eg."青花"
    Output: WER的值, 不需要经过归一化(除以refstr的长度), eg. wer("青花瓷", "青花") = 1
    """

    # 归一化字符串
    refstr = norm_pre(refstr.decode("utf-8"))
    hypstr = norm_pre(hypstr.decode("utf-8"))

    # 拆分字符串为列表
    ref_lst = split_string(refstr)
    hyp_lst = split_string(hypstr)

    # 计算WER值
    rst = wer_list(ref_lst, hyp_lst)

    return rst


def wer_spell_str(refstr, hypstr):
    """
    计算两个拼音字符串的WER

    Input:
        - refstr, 参考字符串, eg."q ing h ua c iy"
        - hypstr, 测试字符串, eg."q ing h ua"
    Output: WER的值, 不需要经过归一化(除以refstr的长度), eg. wer("青花瓷", "青花") = 1
    """

    # 拆分字符串为列表
    ref_lst = refstr.split()
    hyp_lst = hypstr.split()

    # 计算WER值
    rst = wer_list(ref_lst, hyp_lst)

    return rst


def str_pre_norm(in_file, norm_file, clean_file):
    """
    预处理:
        全角转半角，繁体转简体
        删除标点符号
        判断是否包含了非[中|英|数字|空格]的字符，若包含，则删除
        删除空行
        判断是否为空文件，若为空，则不需要进行后续的操作. 在空文件的情况下，给出提示信息
        数字转汉字，只需要一种转换方法，example：666 → 六六六

    Input:
        - in_file
    Output: W
        - norm_file, 预处理 + 清洗之后的文件
        - clean_file, 预处理之后, 有效的原始文件, 与in_file的差别是不包含不符合要求的items

    """
    rstfile = open(norm_file, 'w')
    backupfile = open(clean_file, 'w')
    flag = 0
    with io.open(in_file, encoding='utf-8') as fin:
        for line in fin.readlines():
            line = line.strip('\n').strip('\t').strip()
            raw_line = line

            # 全角转半角，繁体转简体
            line = norm_pre(line)

            # 删除标点符号
            table = string.maketrans("", "")
            line = line.translate(table, string.punctuation)

            # 去除空行，并且不处理英文|中文之外的语种
            if line == '' or is_other_wspace_str(line):
                continue

            # 数字转汉字，只需要一种转换方法
            line = d2zh(line, "pure")

            flag = 1
            # 输出至文件
            rstfile.writelines(line+"\n")
            backupfile.writelines(raw_line + "\n")

    # 在空文件的情况下，给出提示信息
    if flag == 0:
        print "No valid string to process."
        return False

    # 删除最后一个空行
    rstfile.seek(-1, os.SEEK_END)
    rstfile.truncate()
    rstfile.close()
    # 删除最后一个空行
    backupfile.seek(-1, os.SEEK_END)
    backupfile.truncate()
    backupfile.close()
    return True


def strQ2B_file(in_file, outfile):
    """
    对文件，全角转半角

    """
    rstfile = open(outfile, 'w')
    flag = 0
    with io.open(in_file, encoding='utf-8') as fin:
        for line in fin.readlines():
            line = line.strip('\n').strip('\t').strip()

            if line == '':
                continue

            # 全角转半角
            line = strQ2B(line)
            flag = 1
            rstfile.writelines(line+"\n")

    # 在空文件的情况下，给出提示信息
    if flag == 0:
        print "seg result is Null."
        return False

    # 删除最后一个空行
    rstfile.seek(-1, os.SEEK_END)
    rstfile.truncate()
    rstfile.close()

    return True


def str2spell_file(clean_file, norm_file, seg_file, str2spell_f, dict_file):
    """
    根据分词结果，字符串转拼音串
    注：暂时不考虑tone，不考虑多音的情况

    Input:
        - clean_file, 原始文件, 经过预处理筛选
        - norm_file, 预处理 + 清洗之后的文件
        - seg_file, norm_file对应的分词结果文件
        - dict_file, 字典
    Output: str2spell_f, 字符串转拼音串的结果文件
        输出格式： 原始字符串 \t 拼音串
    Return: list, example:
            [u'test	test']
            [u'abc	abc', u'all is good	all is good']
    """

    return_rst = []

    # 得到字典, 对多音字情况，只考虑第一个，即暂时不考虑多音情况
    language_dict = {}
    with io.open(dict_file, encoding='utf-8') as fin:
        for line in fin.readlines():
            line = line.strip('\n').strip('\t').strip().split("\t")
            zhongwen_item = line[0].strip()
            pinyin_item = line[1].strip()

            if zhongwen_item == '':
                continue

            if zhongwen_item not in language_dict:
                language_dict[zhongwen_item] = pinyin_item
    fin.close()

    # 得到原始字符串与分词的输入字符串之间的映射关系，行数相同
    # + 需要考虑分词的输入字符串与输出字符串之间的关系：大写转小写 & 删除空格
    raw_dict = {}
    with io.open(clean_file, encoding='utf-8') as fc, io.open(norm_file, encoding='utf-8') as fn:
        fc_list = fc.readlines()
        fn_list = fn.readlines()
        for idx in range(len(fn_list)):
            # key需要转换，考虑分词的输入字符串与输出字符串之间的关系：大写转小写 & 删除空格
            key = lowerstr(fn_list[idx].strip("\n").strip("\r").strip()).replace(" ", "")
            val = fc_list[idx].strip("\n").strip("\r").strip()
            raw_dict[key] = val
    fc.close()
    fn.close()

    # 根据分词的结果，得到对应的拼音串
    rstfile = open(str2spell_f, 'w')
    with io.open(seg_file, encoding='utf-8') as fs:
        fs_list = fs.readlines()
        for idx in range(len(fs_list)):
            seg_lst = fs_list[idx].strip('\n').strip('\t').strip().split()
            pinyin_lst = []
            for x in seg_lst:
                # 对英文字符，保持英文字符的形式，而不是拼音
                if is_alphabet_str(x):
                    pinyin_lst.append(x)
                else:
                    pinyin_lst.append(language_dict[x])
            # 映射成原始字符串
            fn_item = "".join(seg_lst)
            fc_item = raw_dict[fn_item]
            result = fc_item + "\t" + " ".join(pinyin_lst)
            return_rst.append(result)

            rstfile.writelines(result + "\n")

    fs.close()
    del raw_dict
    del language_dict
    # 删除最后一个空行
    rstfile.seek(-1, os.SEEK_END)
    rstfile.truncate()
    rstfile.close()

    return return_rst
