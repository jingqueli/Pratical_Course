# forge a signature to pretend that you are Satoshi

## 伪造签名原理：

![Screenshot 2022-07-31 142900](https://user-images.githubusercontent.com/104854836/182013243-cff24455-49fb-4ff2-8e98-1403ac1fb3b4.jpg)

> 从上述推导可以知，如果能得到Satoshi的公钥P，在随机选取参数$u$  ,$v$ 的情况下可以伪造签名（在验证方并不对信息进行处理，而是直接用$e$  进行验证的情况下）

## 运行指导

* 直接运行代码forge_signature即可。默认的结果是使用伪造好的签名进行验证而输出的结果。

* 两个签名函数，signature是正确签名，带有forege后缀是伪造签名过程。默认是进行了伪造过程。
