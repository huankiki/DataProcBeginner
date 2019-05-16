#!/bin/bash

####################
# 以Tab键分割，打印某几列，这里的逗号会产生多余的空格，是不对的
cat file_name | awk -F '\t' '{print $4, "\t", $7, "\t", $2, "\t", $6}' > new_file

####################
# 以Tab键分割，打印某几列。可以与上面的例子做对比
cat file_name | awk -F '\t' '{print $4"\t"$7"\t"$6}' > new_file

####################
# 第二列的值大于99，才打印第二列
cat file_name | awk -F '\t' '{if($2>99){print $2}}'

####################
# sed的用法，1,多个处理，-e; 2,删除多个空格;
sed -e 's/(.*)//g; s/\[ wb \]//g; s/_T[0-9]//g; s/[ ][ ]*/ /g; s/\t/ /g; s/ /\t/' file_name

####################
# grep和sed的用法, 1,删除空行; 2,删除英文标点符号; 3,删除每行结尾的空格
grep -o -P '"title": ".*?"'  resource.json | awk -F ': ' '{print $2}' | sed -e 's/[[:punct:]]//g; /^$/d; s/ $//g' > title

sed 's/[[:punct:]]//g' file_name
sed 's/^$//g' file_name

####################
