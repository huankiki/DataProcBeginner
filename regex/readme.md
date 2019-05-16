## regex
regular expression，正则表达式
> 把必须匹配的情况考虑周全并写出一个匹配结果符合预期的正则表达式很容易，但把不需要匹配的情况也考虑周全并确保它们都被排除在匹配结果以外，往往要困难得多。
### 《正则表达式必知必会》Note
[正则表达式必知必会（修订版）](https://book.douban.com/subject/26285406/)  
之前看过很多介绍正则表达式的教程，长篇大论，看不懂。但自从读了这本小小的薄薄的书，对正则表达式的认识很清晰，所以**非常推荐这本书作为正则表达式的入门书，剩下的就是实践、实践、实践**。  
**Notebook：[regex](./regex.ipynb)**

### 实践： Python + 正则表达式
python中的re模块，Notebook：[python_regex](./python_regex.ipynb)

### 实践：demo_regex.py
难点：有很多限定条件，不满足限定条件的情况绝对不能匹配到，否则是严重的bug。
```
# 运行
python2 demo_regex.py
```
