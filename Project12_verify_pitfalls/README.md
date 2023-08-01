# verify the above pitfalls with proof-of-concept code

## 运行指导

* 使用IDLE可以运行

* 三个.py文件：ECDSA,sm2,Schnorr是手动实现的三种数字签名，作为库导入main函数，每个签名方案都可独立运行，如果作为库函数导入时，main文件中有许多函数，通过名字可以辨别，每一个实现了什么功能

* 每个函数都对应了PPT中所写的一个pitfall。默认运行的是最后一个：使用相同d和k导致d泄露的函数，通过还原出d来证明该漏洞存在，其他的函数也写上了，但是被注释掉了，随时可以恢复并执行该函数；

* main.py中实现的都是针对ECDSA中的pitfall的证明，因为三种签名的漏洞证明方法异曲同工，所以只给出了ECDSA，其他两种签名只是手动实现，没有再重复漏洞的证明。


