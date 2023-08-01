# AES / SM4 software implementation

* 使用visual studio可以运行代码

* AES全部内容在AES.cpp中，导入即可运行，默认的输出结果是：第一轮字节替换，第一轮行移位，第一轮列混合，第一轮轮密钥异或后的结果，以及最终的密文输出。

* sm4内容包括.h头文件，sm4.cpp是函数主体，test文件可以运行，运行时需要修改路径，把加密文件路径改成自己需要加密的文件路径，输出.txt文本同样需要修改路径