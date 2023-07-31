# implement the naïve birthday attack of reduced SM3

## 运行指导

* 直接运行即可，默认的结果会输出：手写sm3的测试时间，库函数sm3的测试时间，寻找碰撞的时间

* 主函数部分，变量$index$ 标志要寻找前$4*index$  位的碰撞，修改不同$index$ 值可以寻找不同位数的碰撞并测试时间

* 默认$index=3$ ,即前十二位碰撞的测试时间 
