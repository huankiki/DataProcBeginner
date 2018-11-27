#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
from langconv import *

reload(sys)
sys.setdefaultencoding('utf-8')


def str_escape_solr(instr):
    """
    在特殊字符前加转义字符, 在solr检索时
    + – && || ! ( ) { } [ ] ^ " ~ * ? : \     外加 空格

    Input: 字符串
    """
    def fun(m):
        return "\\" + m.group().upper()

    pat = re.compile("[+\\\\\-&|!(){}\[\]^\"~*?:\\s]")
    return pat.sub(fun, instr)


def strQ2B(ustring):
    """
    全角转半角

    Input: 字符串
    """
    if not isinstance(ustring, unicode):
        ustring = unicode(ustring, 'utf-8')

    rstring = ""
    ustring = ustring
    for uchar in ustring:
        inside_code=ord(uchar)
        if inside_code == 12288:                              #全角空格直接转换
            inside_code = 32
        elif (inside_code >= 65281 and inside_code <= 65374): #全角字符（除空格）根据关系转化
            inside_code -= 65248

        rstring += unichr(inside_code)
    rstring = rstring.encode("utf-8")
    return rstring


def tradition2simple(sentence):
    """
    将繁体字转为简体字

    Input: sentence, 待转换的句子、字符串
    Return: 转换为简体字之后的句子、字符串
    """
    if not isinstance(sentence, unicode):
        sentence = unicode(sentence, 'utf-8')

    sentence = Converter('zh-hans').convert(sentence)
    return sentence.encode("utf-8")


def upperstr(string):
    """
    英文小写转大写

    """

    string = string.upper()
    return string


def lowerstr(string):
    """
    英文大写转小写

    """

    string = string.lower()
    return string


def delstr(string, pattern):
    """
    删除匹配的字符串
    pattern可以是一个模式，即一个字符串，比如'\(.*\)'
    pattern也可以是一个模式列表，每个元素是一个字符串，比如['^.*:', '\(.*\)', '\[.*\]', '【.*】']
    """

    if isinstance(pattern, str):
        string = re.sub(r'(?:%s)'%(pattern), "", string.encode("utf-8"))
    if isinstance(pattern, list):
        for i in range(len(pattern)):
            pat = pattern[i]
            string = re.sub(r'(?:%s)'%(pat), "", string.encode("utf-8"))

    # 清除字符串之后，可能存在多余的"\t"，将之替换成空格
    string = string.replace("\t", " ")

    return string


def delspace(string):
    """
    删除字符串中的空格，英文单词之间的空格保留
    同时将英文单词之间只保留一个空格
    """

    pattern = u"(?<=[\u4e00-\u9fa5])\s+(?=[\u4e00-\u9fa5])"  # 中文-中文
    string = re.sub(pattern, "", string.decode("utf-8"))

    pattern = u"(?<=[\u4e00-\u9fa5])\s+(?=[\w])"  # 中文-英文/数字
    string = re.sub(pattern, "", string.decode("utf-8"))

    pattern = u"(?<=[\w])\s+(?=[\u4e00-\u9fa5])"  # 英文/数字-中文
    string = re.sub(pattern, "", string.decode("utf-8"))

    # 英文单词之间的空格只保留1个
    pattern = u"(?<=[\w])\s+(?=[\w])"
    string = re.sub(pattern, " ", string.decode("utf-8"))

    # 删除数字前多余的0，比如: "第011集" converted to "第011集"
    pattern = u"(?<=[^\d])0+(?=[1-9])"
    string = re.sub(pattern, "", string.decode("utf-8"))

    return string


def spec_proc(string):
    """
    (上|下|数字)这种情况需要:1)去除括号；2)额外保存一份括号前的item
    """

    out_string = string  # eg.故事(上)

    pat = r"\([上中下\d]+\)"
    pattern = re.compile(pat)
    matcher = re.search(pattern, string.encode('utf-8'))

    if matcher:
        spec_str = matcher.group(0)  # eg. (上)
        spec_substr = spec_str.strip("(").strip(")")  # eg. 上
        spec_substr = re.sub(r'^0+', '', spec_substr) # 02 to 2, 删除数字前的多余"0"
        key_string = string.replace(spec_str, "")  # eg. 故事

        out_string = key_string + "/" + key_string + spec_substr  # 故事/故事上

    return out_string


def split_line(inlist, icol=0, SPLITOR='\t'):
    """
    别名的数据，保存每个别名成一个item

    Input: list
    Output: str

    后续需要支持icol为一个列表，即支持多列的别名判断和处理
    """

    outline = ""
    if "/" or "+" in inlist[icol]:
        line_alias = re.split('/|\+', inlist[icol])
        line_new = inlist[:]
        # 另外保存别名
        for na in range(len(line_alias)):
            if len(line_alias[na].strip('\n').strip('\t').strip().decode('utf-8')) >1:
                line_new[icol] = line_alias[na].strip()
                outline += SPLITOR.join(line_new) + "\n"
    else:
        # 合并成一行
        outline = SPLITOR.join(inlist)
    if outline == "":
        return None
    outline = outline.strip("\n")
    return outline


def norm_pre(string):
    """
    自定义归一化，包括：[按照所列顺序]
    - 全角转半角
    - 繁体转简体
    - 大写转小写(暂时忽略)

    Input: 字符串、句子
    Return: 归一化之后的句子
    """
    string = strQ2B(string)		# 全角转半角
    string = tradition2simple(string)		# 繁体转简体
    # string = lowerstr(string)		# 大写转小写

    return string


def is_chinese(uchar):
    """判断一个unicode是否是汉字"""
    if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
        return True
    else:
        return False


def is_number(uchar):
    """判断一个unicode是否是数字"""
    if uchar >= u'\u0030' and uchar<=u'\u0039':
        return True
    else:
        return False


def is_alphabet(uchar):
    """判断一个unicode是否是英文字母"""
    if (uchar >= u'\u0041' and uchar <= u'\u005a') or (uchar >= u'\u0061' and uchar <= u'\u007a'):
        return True
    else:
        return False


def is_other(uchar):
    """判断是否非汉字，数字和英文字符"""
    if not (is_chinese(uchar) or is_number(uchar) or is_alphabet(uchar)):
        return True
    else:
        return False



def is_other_wspace(uchar):
    """判断字符是否非汉字，数字和英文字符，空字符"""
    if not (is_chinese(uchar) or is_number(uchar) or is_alphabet(uchar) or uchar == u'\u0020'):
        return True
    else:
        return False


def is_other_wspace_str(instr):
    """判断字符串是否非汉字，数字和英文字符，空字符"""
    if not isinstance(instr, unicode):
        instr = unicode(instr, 'utf-8')

    for uchar in instr:
        if is_other_wspace(uchar):
            return True

    return False


def is_alphabet_str(instr):
    """判断字符串是否英文字符串"""
    if not isinstance(instr, unicode):
        instr = unicode(instr, 'utf-8')

    for uchar in instr:
        if not is_alphabet(uchar):
            return False

    return True
