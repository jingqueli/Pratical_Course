# RangeProof

## impl this protocol with actual network communication

## 运行指导

* 三份代码分别表示可信任第三方，Alice，Bob两个交互者。代码均可以用IDLE打开

* 运行时我使用命令行运行，打开三个命令行，分别运行。

* 先运行Alice与Bob，二者开始时处于监听状态；最后运行Issuer。

* 如果使用多台设备模拟该过程，需要将绑定的IP分别改成各自IP，因为我使用的都是运行代码的本机IP，所以可以且只能在一台设备模拟三方交互过程。

* 默认输出结果是待签名消息，签名等一系列信息，以及最后是否证明成功的消息
