#!/usr/bin/env python
# -*- coding: utf-8 -*-

from shutil import copyfile
from string_match_util import *

reload(sys)
sys.setdefaultencoding('utf-8')

# 与分词工具的接口文件和执行shell脚本
# + 无声调的字典
local_path = os.path.abspath(os.path.dirname(__file__))
seg_shell_name = "title_seg.sh"
seg_shell_dir = os.path.abspath(local_path+os.path.sep+".."+os.path.sep+"shurufa_pre_out/string_matching")
seg_shell_bin = seg_shell_dir + os.path.sep + seg_shell_name
seg_rst_file = seg_shell_dir + os.path.sep + "title_seg"
spell_dict_file = os.path.abspath(local_path+os.path.sep+".."+os.path.sep+"dict/spell_sum_wo_tone.utf8")
phoneme_dict_file = os.path.abspath(local_path+os.path.sep+".."+os.path.sep+"dict/phoneme_sum_wo_tone.utf8")

def str2spell(input, output, data_mode="file", dict_mode="phoneme"):
    """
    字符串转拼音串的完整流程
    1, 预处理
    2, 分词, 调用分词工具
    3, 分词结果，全角转半角
    4, 根据分词结果，字符串转拼音串

    Input:
        - input, 输入文件或输入字符串, 与data_mode有关
        - data_mode, 默认为"file", 即输入为文件
    Output:
        - output, 字符串转拼音串的结果文件
        输出格式： 原始字符串 \t 拼音串
    Return: list, example:
            [u'test	test']
            [u'abc	abc', u'all is good	all is good']
    """

    #################################################
    # 初始化                                         #
    #################################################
    # convert to absolute dir
    pinyin_str_f = os.path.abspath(output)

    # check output dir
    output_path = os.path.abspath(os.path.dirname(pinyin_str_f))
    if not os.path.isdir(output_path):
        os.mkdir(output_path)

    # 若是字符串，则转成文件
    if data_mode == "file":
        raw_str_f = os.path.abspath(input)
    else:
        raw_str = input
        raw_str_f = output_path + os.path.sep + "rawstr.lst"
        tmp_f = open(raw_str_f, 'w')
        tmp_f.write(raw_str)
        tmp_f.close()
    if dict_mode == "spell":
        dict_file = spell_dict_file
    else:
        dict_file = phoneme_dict_file

    # 归一化之后的字符串文件
    norm_str_f = output_path + os.path.sep + "normstr.lst"
    clean_str_f = output_path + os.path.sep + "cleanstr.lst"

    # 分词的结果文件
    seg_rst_tmp_f = output_path + os.path.sep + "seg_tmp.lst"
    seg_rst_f = output_path + os.path.sep + "seg.lst"

    #################################################
    # 预处理
    # 全角转半角，繁体转简体
    # 删除标点符号
    # 判断是否包含了非[中|英|数字|空格]的字符，若包含，则删除
    # 删除空行
    # 判断是否为空文件，若为空，则不需要进行后续的操作
    # 若输入为字符串，则在空文件的情况下，给出提示信息
    # 数字转汉字，只需要一种转换方法, example：666 → 六六六
    #################################################
    flag = str_pre_norm(raw_str_f, norm_str_f, clean_str_f)
    # 若预处理之后, 文件为空, 则退出, 且有提示信息
    if flag is False:
        os.remove(norm_str_f)
        os.remove(clean_str_f)
        return -1

    #################################################
    # 分词
    #################################################
    seg_cmd = "bash " + seg_shell_bin + " " + norm_str_f
    seg_flag = os.system(seg_cmd)
    # 分词结果为为空, 则退出, 且有提示信息
    if seg_flag != 0:
        print "seg result is Null."
        os.remove(norm_str_f)
        os.remove(clean_str_f)
        return -1
    copyfile(seg_rst_file, seg_rst_tmp_f)

    #################################################
    # 分词结果，全角转半角
    #################################################
    strQ2B_file(seg_rst_tmp_f, seg_rst_f)
    os.remove(seg_rst_tmp_f)

    #################################################
    # 根据分词结果，字符串转拼音串
    # 输入文件：原始字符串文件，归一化之后的字符串文件，分词之后的结果
    # 功能：根据分词的结果，得到对应的拼音串
    # 输出结果：一个文件，包含了三种字符串，格式如下：
    # 原始字符串 \t 归一化之后的字符串 \t 拼音串（对应了归一化之后的字符串）
    #################################################
    result = str2spell_file(clean_str_f, norm_str_f, seg_rst_f, pinyin_str_f, dict_file)

    #################################################
    # 结果输出
    # 若data_mode是str，则打印output_file的内容
    # 删除中间文件
    # #################################################
    os.remove(norm_str_f)
    os.remove(clean_str_f)
    #os.remove(seg_rst_f)

    if data_mode == "str":
        os.remove(raw_str_f)

    return result



if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Usage: %s [input_file | input_str] output_file [data_mode] [dict_mode]'% sys.argv[0]
        sys.exit(1)

    """
    根据字符串、分词工具、字典，得到字符串对应的拼音串
    输入：字符串或字符串列表文件
    输出：string or file
    格式：原始字符串 \t 归一化之后的字符串 \t 拼音串（对应了归一化之后的字符串）
    data_mode：str | file, 默认：file

    """
    # get data_mode
    if len(sys.argv) == 3:
        data_mode = "file"
        dict_mode = "phoneme"
    elif len(sys.argv) == 4:
        data_mode = sys.argv[3]

        dict_mode = "phoneme"
    else:
        data_mode = sys.argv[3]
        dict_mode = sys.argv[4]

    if data_mode not in ["str", "file"]:
        print 'data_mode must be "str" or "file", not "%s".' % data_mode
        sys.exit(1)
    if dict_mode not in ["spell", "phoneme"]:
        print 'dict_mode must be "spell" or "phoneme", not "%s".' % dict_mode
        sys.exit(1)


    str2spell(sys.argv[1], sys.argv[2], data_mode, dict_mode)

