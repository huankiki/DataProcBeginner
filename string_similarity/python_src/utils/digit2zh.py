#!/usr/bin/evn python
# -*- coding: utf-8 -*-


import re
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


CMBER = "/"
num = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九']
kin = ['十', '百', '千', '万', '零']


def sadd(x):
    x.reverse()
    if len(x) >= 2:
        x.insert(1, kin[0])
        if len(x) >= 4:
            x.insert(3, kin[1])
            if len(x) >= 6:
                x.insert(5, kin[2])
                if len(x) >= 8:
                    x.insert(7, kin[3])
                    if len(x) >= 10:
                        x.insert(9, kin[0])
                        if len(x) >= 12:
                            x.insert(11, kin[1])

    x = fw(x)
    x = d1(x)
    x = d2(x)
    x = dl(x)
    return x


def rankis(string):
    rank = ""
    i = list(string)
    for j in i:
        i[(i.index(j))] = num[int(j)]
    i = sadd(i)
    rank += i
    return rank


def d1(x):
    if '零' in x:
        a = x.index('零')
        if a == 0:
            del x[0]
            d1(x)
        else:
            if x[a + 2] in ['十', '百', '千', '万', '零']:
                if x[a + 1] != '万':
                    del x[a + 1]
                    d1(x)
    return x


def d2(x):
    try:
        a = x.index('零')
        if x[a - 1] in ['十', '百', '千', '零']:
            del x[a - 1]
            d2(x[a + 1])
    except:
        pass
    return x


def fw(x):
    if len(x) >= 9:
        if x[8] == '零':
            del x[8]
    return x


def dl(x):
    try:
        if x[0] == '零':
            del x[0]
    except:
        pass
    x.reverse()
    x = ''.join(x)
    return x


def puredigit2zh(string):
    rank = ""
    i = list(string)
    for j in i:
        rank += num[int(j)]
    return rank


def hasNumbers(inputString):
   return bool(re.search(r'\d', inputString))


def d2zh(complex_string, cmode="pure"):
    """
    输入字符串并非纯数字字符串
    如果不包含数字，则不处理
    如果包含数字，则替换数字

    mode说明
    pure: 单个数字转汉字，比如：1000 —— 一零零零
    pure+: 原阿拉伯 和 单个数字转汉字，两个版本
    zh: 数字转汉字，比如：1000 —— 一千
    zh+: 原阿拉伯 和 数字转汉字，两个版本
    all[默认]： 原阿拉伯 和 单个数字转汉字 和 数字转汉字，三个版本

    """
    if not hasNumbers(complex_string):
        return complex_string

    str_len = len(complex_string)
    idx_dict = {0:[0, str_len]}
    purezh_str_lst = []
    numzh_str_lst = []
    cnt = 0
    for m in re.finditer(r"\d+", complex_string):
        pure_num = m.group(0)

        # 特殊处理：00123，以及数字的长度大于6
        if (len(pure_num) >=2 and int(pure_num) < 10**(int(len(pure_num))-1)) or len(pure_num) > 6:
            purezh_str = puredigit2zh(pure_num)
            numzh_str = purezh_str
        else:
            purezh_str = puredigit2zh(pure_num)
            numzh_str = rankis(pure_num)

        if m.start() == idx_dict[cnt][0]:
            idx_dict[cnt] = [m.start(), m.end()]
            purezh_str_lst.append(purezh_str)
            numzh_str_lst.append(numzh_str)
            cnt += 1
            idx_dict[cnt] = [m.end(), str_len]

        else:
            idx_dict[cnt][1] = m.start()
            pure_str = complex_string[idx_dict[cnt][0]:idx_dict[cnt][1]]
            purezh_str_lst.append(pure_str)
            numzh_str_lst.append(pure_str)
            purezh_str_lst.append(purezh_str)
            numzh_str_lst.append(numzh_str)
            cnt += 1
            idx_dict[cnt] = [m.start(), m.end()]
            cnt += 1
            idx_dict[cnt] = [m.end(), str_len]

    if idx_dict[cnt][0] == str_len:
        idx_dict.pop(cnt)
        cnt -= 1
    else:
        last_str = complex_string[idx_dict[cnt][0]:idx_dict[cnt][1]]
        purezh_str_lst.append(last_str)
        numzh_str_lst.append(last_str)

    purezh_rst = "".join(purezh_str_lst)
    numzh_rst = "".join(numzh_str_lst)

    if cmode == "pure":
        result = purezh_rst
    elif cmode == "pure+":
        result = complex_string + CMBER + purezh_rst
    elif cmode == "zh":
        result = numzh_rst
    elif cmode == "zh+":
        result = complex_string + CMBER + numzh_rst
    elif cmode == "all":
        if purezh_rst != numzh_rst:
            result = complex_string + CMBER + purezh_rst + CMBER + numzh_rst
        else:
            result = complex_string + CMBER + purezh_rst

    return result


if __name__ == '__main__':
    str = 'a10023abcd111ddd'
    print d2zh(str)



