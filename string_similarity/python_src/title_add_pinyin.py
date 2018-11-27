#!/usr/bin/env python
# -*- coding: utf-8 -*-


import io
import sys
import json
import string
from utils.format_util import *


reload(sys)
sys.setdefaultencoding('utf-8')


spell_map_file = "../dict/title_spell.dict"
phoneme_map_file = "../dict/title_phoneme.dict"

resource_file = "../rawdict/resource.json"

phoneme_map_dict = {}
with io.open(phoneme_map_file, encoding='utf-8') as fn:
    for line in fn.readlines():
        line_lst = line.strip("\n").strip("\r").strip().split("\t")
        instr = line_lst[0].strip()
        pinyin_str = line_lst[1].strip()
        if not instr:
            continue
        if instr not in phoneme_map_dict:
            phoneme_map_dict[instr] = pinyin_str
fn.close()

spell_map_dict = {}
with io.open(spell_map_file, encoding='utf-8') as fn:
    for line in fn.readlines():
        line_lst = line.strip("\n").strip("\r").strip().split("\t")
        instr = line_lst[0].strip()
        pinyin_str = line_lst[1].strip()
        if not instr:
            continue
        if instr not in spell_map_dict:
            spell_map_dict[instr] = pinyin_str
fn.close()

rstfile = "../dict/resource_spell_phoneme.json"
idx = 0
icnt = 0

with io.open(resource_file, encoding='utf-8') as fin, io.open(rstfile, 'w', encoding='utf-8') as fout:
    for line in fin.readlines():
        icnt += 1
        rst_line = json.loads(line)
        if "title" in rst_line:
            title = rst_line["title"]
            title = title.encode("utf-8")
            # # 删除标点符号
            title = strQ2B(title)
            table = string.maketrans("", "")
            title = title.translate(table, string.punctuation)

        if title in spell_map_dict:
            idx += 1
            rst_line["title_spell"] = spell_map_dict[title]

        if title in phoneme_map_dict:
            rst_line["title_phoneme"] = phoneme_map_dict[title]
#       else:
#           print title


        fout.write(unicode(json.dumps(rst_line, ensure_ascii=False)) + '\n')


print idx, "/", icnt
