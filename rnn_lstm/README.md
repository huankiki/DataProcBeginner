## RNN/LSTM Note
循环神经网络，Recurrent Neutral Network，RNN  
长短时记忆网络，Long Short Term Memory Network, LSTM  
参考资料：
- [Understanding LSTM Networks-colah](http://colah.github.io/posts/2015-08-Understanding-LSTMs/)
- [Understanding LSTM Networks-cola-中文翻译版](https://mp.weixin.qq.com/s?__biz=MzI0ODcxODk5OA==&mid=2247485477&idx=1&sn=0d6bd491b593b497eb1f9d92f9afb10d&chksm=e99d3bdcdeeab2ca436750184f999a58b849be41a3a4ec1bd039b531accae124a2297e57ac0e&scene=21#wechat_redirect)
- [零基础入门深度学习(5)-循环神经网络](https://zybuluo.com/hanbingtao/note/541458)，需要的公式推导都在这里！
- [零基础入门深度学习(6)-长短时记忆网络(LSTM)](https://zybuluo.com/hanbingtao/note/581764)，需要的公式推导都在这里！
- [循环神经网络(RNN)模型与前向反向传播算法](https://www.cnblogs.com/pinard/p/6509630.html)，简易版公式推导
- [LSTM模型与前向反向传播算法](https://www.cnblogs.com/pinard/p/6519110.html)，简易版公式推导

------
## RNN简介
![rnn](./graph/rnn.jpg)  

一个简单的循环神经网络由输入层、隐藏层和输出层组成。与全连接神经网络相比，增加了中间的W。循环神经网络的隐藏层的值s不仅仅取决于当前这次的输入x，还取决于上一次隐藏层的值s。  
原始RNN可以很好的解决短时依赖问题，但无法处理长距离依赖。

------
## LSTM简介
- 原始RNN
![rnn](./graph/LSTM3-SimpleRNN.png)  

- LSTM，一定程度上解决长时依赖的问题
![lstm](./graph/LSTM3-chain.png)  

- 遗忘门
![lstm-f](./graph/LSTM3-focus-f.png)  

- 输入门
![lstm-i](./graph/LSTM3-focus-i.png)  

- 输出门
![lstm-o](./graph/LSTM3-focus-o.png)  

![lstm-c](./graph/LSTM3-C-line.png)   
![lstm-gate](./graph/LSTM3-var-peepholes.png)  
