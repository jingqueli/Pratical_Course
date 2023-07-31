# implement length extension attack for SM3

## 运行指导

* 直接运行即可，默认运行结果是：更换IV，用后半部分data计算得出的hash；拼接后的消息；用拼接后消息计算出的hash，经比对结果一致

* 其中命名为seg_func_fake的函数是便于替换初始IV而做的，与seg_func的区别仅在增加参数IV_fake用于替换。

* sm3_hash是调用库函数的sm3，旨在与手写sm3对比或其他用处。由于project1,2中均进行了测试时间对比，本内容中不涉及测试时间等操作
