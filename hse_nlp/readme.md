# Week 1
### Part I: Introduction to NLP and our course
方法：基于规则的方法，机器学习，深度学习。  
![course_content](./graph/week1_1_1.png)

### Part II：Text classification
1，分词(Tokenization)  
将文本(text)看作是词(token)的序列。
2，提取特征，Feature extraction
- BOW，Bag of words，词袋模型，会丢失词序信息  
计算文本中词出现的次数，得到文本的向量表示。
- n-gram，N元模型  
n-gram，即当前词和前面(n-1)个词组成一个新的特征。可以保留部分词序信息，但特征数增加。  
实际使用时，会移除频度过高或者过低的特征。比如，停用词（介词等）出现过多，但不是有用的信息。频度过低的词也不需要，否则很容易过拟合。  
![](./graph/bow_ngram.png)
- TF-IDF，term frequency–inverse document frequency，词频-逆文本频率指数  
移除出现次数过高或过低的特征后，我们得到了中等频度的特征。那么对这些特征而言，有什么更多的信息呢？  
主要思想：如果某个词或短语在一篇文章中出现的频率高，并且在其他文章中很少出现，则认为此词或者短语具有很好的类别区分能力，适合用来分类。

