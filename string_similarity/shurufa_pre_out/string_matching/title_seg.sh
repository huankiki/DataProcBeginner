#!/bin/bash


# in python_src dir, Usage:
#+ bash ../shurufa_pre_out/string_matching/title_seg.sh ../dict/title_clean


if [ $# -ne 1 ];then
    echo "Usage: $0 to_seg_file"
    exit 1
fi

to_seg_file="$1"

loc_dir="$(cd $(dirname $0); pwd)"

pre_list_bin_dir="${loc_dir}/.."
split_dir="${pre_list_bin_dir}/split"
seg_dir="${pre_list_bin_dir}/seg"

# 运行pre_list.sh必须在路径${pre_list_bin_dir}
cd ${pre_list_bin_dir}
pre_list_bin="${pre_list_bin_dir}/pre_list.sh"

# copy to split
cp ${to_seg_file}  ${split_dir}/title

# utf8转成gbk
iconv -f utf8 -t gbk ${split_dir}/title -o ${split_dir}/title_gbk
sed -i 's/$/\t1/' ${split_dir}/title_gbk

# 分词
echo "title_gbk" > ${pre_list_bin_dir}/string_matching/list

bash ${pre_list_bin_dir}/pre_list.sh ${pre_list_bin_dir}/string_matching/list > /dev/null 2>&1
sleep 4
[ $? -ne 0 ] && echo "pre_list.sh fail" && exit 1

# 得到分词结果，不需要热度
cat ${seg_dir}/title_gbk.seg | awk -F "\t" '{print $2}' > ${pre_list_bin_dir}/string_matching/title_gbk_seg
rm ${split_dir}/title
rm ${split_dir}/title_gbk

# 转换成utf-8
iconv -f gbk -t utf8 ${pre_list_bin_dir}/string_matching/title_gbk_seg -o ${pre_list_bin_dir}/string_matching/title_utf8_seg
rm ${pre_list_bin_dir}/string_matching/title_gbk_seg
[ ! -e ${pre_list_bin_dir}/string_matching/title_utf8_seg ] && exit 1

# update
mv ${pre_list_bin_dir}/string_matching/title_utf8_seg ${pre_list_bin_dir}/string_matching/title_seg

sed -i -e 's/[ ][ ]*/ /g; s/^ //; s/ $// ' ${pre_list_bin_dir}/string_matching/title_seg

#echo "title seg done";echo
