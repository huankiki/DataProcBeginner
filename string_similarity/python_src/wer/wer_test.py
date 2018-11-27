#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

'''
用Python实现WER（Word Error Rate, 字错误率）计算的脚本
参考：https://martin-thoma.com/word-error-rate-calculation/
'''

r = ["q", "ing", "h", "ua", "c", "iy"]
h = ["a", "q", "ing", "h", "ua"]

# 青花瓷 青花 青花词
# r = ["青", "花", "瓷"]
r = ["青"]
h = ["青", "花"]
# h = ["青", "花", "词"]
# # test
# r = "who is there".split()
# h = "is there".split()

d = numpy.zeros((len(r) + 1) * (len(h) + 1), dtype=numpy.uint8)
d = d.reshape((len(r) + 1, len(h) + 1))
for i in range(len(r) + 1):
    for j in range(len(h) + 1):
        if i == 0:
            d[0][j] = j
        elif j == 0:
            d[i][0] = i

print d
# computation
for i in range(1, len(r) + 1):
    for j in range(1, len(h) + 1):
        if r[i - 1] == h[j - 1]:
            d[i][j] = d[i - 1][j - 1]
            substitution = 0
            insertion = 0
            deletion = 0
        else:
            substitution = d[i - 1][j - 1] + 1
            insertion = d[i][j - 1] + 1
            deletion = d[i - 1][j] + 1
            d[i][j] = min(substitution, insertion, deletion)
        print i,j,substitution, insertion, deletion
        print d

print d[len(r)][len(h)]
