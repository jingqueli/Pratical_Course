# Impl Merkle Tree following RFC6962

## 运行指导

* IDLE可以直接运行python代码。默认输出结果是Merkle Tree各层节点信息，以及根节点hash值

* Mekrle Tree with RFC6962 使用sha-256作为默认hash函数，每个节点的hash值都是基于其子节点的hash值计算得到的

* 除叶子节点外的其他节点都是内部节点。内部节点的值通过将其两个子节点的哈希值连接并进行哈希运算来计算得到。
