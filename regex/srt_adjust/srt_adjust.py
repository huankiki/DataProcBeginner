#! /usr/bin/python
#coding=utf-8


import sys
import io, re

'''
python2
reload(sys)
sys.setdefaultencoding('utf8')
'''


def srt_adjust(ens, zhs, out):
    '''
    将中文字幕的时间轴和英文字幕的字幕内容合并成新的字幕文件
    难点：会出现两种特殊情况： 1，字幕内容为空， 2，字幕内容为多行内容
    41
    00:01:44,981 --> 00:01:49,148
    -Just once when I say 'suit up', I wish you'd put on a suit.
    -I did, that one time.

    41
    00:01:40,599 --> 00:01:44,595
    -我跟你说穿得好一点，就是说要你穿上西服！
    -我穿过……一回
    '''
    outfile = open(out, 'w')
    timeline = []
    enshooter = []
    zhshooter = []
    idx = 0
    flag = False
    en_srt_content = ""
    # 英文字幕，提取字幕内容
    with io.open(ens, 'r', encoding="utf-8") as fe:
        for line in fe.readlines():
            line = line.strip().strip("\n")
            if (not re.match("^[0-9]+$", line)) and (flag == True) and (line != ""):     # english
                en_srt_content += line + "\n"
                # test
                # if idx == 41:
                #     print(en_srt_content)
            ## 时间轴
            #+ 当时间轴出现过，则flag为True，意味着后续出现的就是字幕内容
            elif "-->" in line:
                flag = True
                en_srt_content = ""
                idx += 1
            elif flag == True and line == "":
                flag = False
                enshooter.append(en_srt_content)
                en_srt_content = ""
            else:
                pass
    # print(idx)
    idx = 0

    ## 中文字幕，提取字幕时间轴
    with io.open(zhs, 'r', encoding="utf-8") as fz:
        for line in fz.readlines():
            line = line.strip().strip("\n")
            if "-->" in line:   # timeline
                timeline.append(line)
                idx += 1
    # print(idx)

    ## 得到最终字幕，并输出
    assert(len(enshooter) == len(timeline))
    for i in range(len(timeline)):
        rst = str(i+1) + "\n" + timeline[i] + "\n" + enshooter[i] + "\n"
        # print(rst)
        outfile.write(rst)

    outfile.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        en_srt_file = "./en.srt"
        zh_srt_file = "./zh.srt"
        out_file = "./new.srt"
    else:
        try:
            en_srt_file, zh_srt_file, out_file = sys.argv[1], sys.argv[2], sys.argv[3]
        except IndexError:
            print("Usage: python3 %s en_srt zh_srt out_file" % sys.argv[0])
            sys.exit()

    srt_adjust(en_srt_file, zh_srt_file, out_file)

