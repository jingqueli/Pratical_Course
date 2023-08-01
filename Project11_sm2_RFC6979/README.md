# impl sm2 with RFC6979

## 运行指导

* IDLE可以打开并运行代码

* sm2_myself作为库文件导入sm2_RFC6979中，sm2_myself是我手动实现的sm2，加入RFC6979的关键在于将随机生成的k替换成了按照RFC6979标准生成的k。

* 运行前需要将sm2_melf与sm2_RFC6979同时保存，运行后者的默认输出结果是签名的验证是否成功。
