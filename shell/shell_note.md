# Linux-Shell-Scripting-Cookbook-Third-Edition
Unix刚开始只支持一种交互式shell，它是由Stephen Bourne所编写的**Bourne Shell（sh）**。1989年，GNU项目的Brian Fox吸收了大量其他用户界面的特性，编写出了一种全新的shell：**Bourne Again Shell（bash）**。bash shell与Bourne Shell完全兼容，同时又增添了一些来自csh、ksh等的功能。

shell脚本通常以shebang起始：`#!/bin/bash`

shebang是一个文本行，其中#!位于解释器路径之前。/bin/bash是Bash的解释器命令路径。bash将以#符号开头的行视为注释。脚本中只有第一行可以使用shebang来定义解释该脚本所使用的解释器。

## 在echo中转义换行符
默认情况下，echo会在输出文本的尾部追加一个换行符。可以使用选项`-n`来禁止这种行为。echo同样接受包含转义序列的双引号字符串作为参数。在使用转义序列时，需要使用echo -e"包含转义序列的字符串"这种形式。例如`echo -e "1\t2\t3"`


## stdout, 重定向操作符
0 —— stdin（标准输入），1 —— stdout（标准输出），2 —— stderr（标准错误）

当一个命令发生错误并退回时，它会返回一个非0的退出状态；而当命令成功完成后，它会返回为0的退出状态。退出状态可以从特殊变量$?中获得，在命令结束之后立刻运行`echo $?`，就可以打印出退出状态。


如果你不想看到或保存错误信息，那么可以将stderr的输出重定向到/dev/null，保证一切都会被清除得干干净净。

`/dev/null`是一个特殊的设备文件，它会丢弃接收到的任何数据。null设备通常也被称为黑洞，因为凡是进入其中的数据都将一去不返。
```
ls 2>stderr.txt 1>stdout.txt
#将stderr转换成stdout，使得stderr和stdout都被重定向到同一个文件中
ls 2>&1 output.txt
ls 2>&1 /dev/null
```

## 函数
- $0是脚本名称
- $1是第一个参数
- $2是第二个参数
- $n是第n个参数
- "$@"被扩展成"$1" "$2" "$3"等
- "$*"被扩展成"$1$2$3"

```
function fname()
{
    statements;
}
fname()
{
    statements;
}
```
## 管道操作符 |
`ls | cat -n > out.txt`

ls（列出当前目录内容）的输出被传给cat -n，后者为通过stdin所接收到的输入内容加上行号，然后将输出重定向到文件out.txt。

## IFS, 内部字段分隔符
IFS(Internal Field Separator)的默认值为空白字符（换行符、制表符或者空格）。
```
#!/bin/bash
#用途: 演示IFS的用法
line="root:x:0:0:root:/root:/bin/bash"
oldIFS=$IFS;
IFS=":"
count=0
for item in $line;
do
  [$count -eq 0]   && user=$item;
  [$count -eq 6]   && shell=$item;
let count++
done;
IFS=$oldIFS
echo $user's shell is $shell;
#输出为：root's shell is /bin/bash
```
## if条件
```
if condition;
then
    commands;
fi

if condition;
then
    commands;
else if condition; then
    commands;
else
    commands;
fi

```

