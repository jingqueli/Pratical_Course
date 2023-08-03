# 汇总报告：Project1-22

## Project-1,implement the naïve birthday attack of reduced SM3

### 1，实验内容

分为两部分解释：sm3实现和生日攻击

> **sm3的实现** 

* 代码前半部分是sm3的实现，其中seg_func（）函数是主体，体现了sm3的逻辑，包括了消息填充，消息扩展，压缩函数等函数的调用，最后只需要调用seg_func（）就能得出hash值。
  
  手动实现sm3的主体部分代码如下（即seg_func（））
  
  ```python
  def seg_func(data):
      #输入信息类型为bit stream
      IV=[]
      group_number=int(len(data)/64)+1#64byte per group
      if(group_number==1):
          padding_data=padding_func(data[:])
          IV=compression_func(IV0,padding_data)
          for i in range(0,8):
              IV[i]=hex(IV[i])[2:]
          padded_IV=[s.zfill(8) for s in IV]
          final_IV=''.join(padded_IV)
          return final_IV
      for i in range(0,group_number):
          if(i==0):
              IV=compression_func(IV0,data[0:64])
              continue
          if(i==group_number-1):
              padding_data=padding_func(data[64*i:])
              #获得填充后信息
              IV=compression_func(IV,padding_data)
              for i in range(0,8):
                  IV[i]=hex(IV[i])[2:]
              padded_IV = [s.zfill(8) for s in IV]
              final_IV=''.join(padded_IV)
              return final_IV
          else:
              IV=compression_func(IV,data[64*i:64*(i+1)])
              continue
  ```

* 参数选取：
  
  > 初始IV：查阅相关信息后可以得到初始IV
  > 
  > 常量T：本代码中，前16轮使用一个T，后面的轮数使用另一个T值

> **朴素生日攻击** 

* 即在主函数里随机选取两个信息，进行hash值的比对，是没有任何方法的随机选择的消息。通过Index变量控制要比对的碰撞的位数，是4*Index位。

* 通过时间测试函数，最后输出找到碰撞的时间

### 2，运行指导

* 直接用IDLE运行代码即可

### 3，实验结果及分析

> #### 1,手动实现sm3与库函数sm3的时间比较
> 
> 运行程序，得到如下结果：
> 
> ![](C:\Users\Mr.smile\AppData\Roaming\marktext\images\2023-08-01-23-50-06-image.png)
> 
> 可以发现，手动实现的时间与库函数时间相差并不多，如果再能把padding_func（）等函数做更多的优化，效果会更好。
> 
> #### 2，不同长度碰撞的时间
> 
> 通过修改Index，可以测试不同长度碰撞，运行程序得到如下结果：
> 
> **Index=2** ：
> 
> 可能是选择的位数过短，有时能在几次内就找到，时间非常快，测试多次后，得到如下：
> 
> ![](C:\Users\Mr.smile\AppData\Roaming\marktext\images\2023-08-01-23-59-16-image.png)
> 
> **Index=3** :
> 
> ![](C:\Users\Mr.smile\AppData\Roaming\marktext\images\2023-08-02-00-04-19-image.png)
> 
> **Index=4** :
> 
> ![](C:\Users\Mr.smile\AppData\Roaming\marktext\images\2023-08-02-00-09-09-image.png)
> 
> **Index=5** ：
> 
> ![](C:\Users\Mr.smile\AppData\Roaming\marktext\images\2023-08-02-00-24-28-image.png)

## Project-2， implement the Rho method of reduced SM3

### 1，实验内容

同样使用手动实现sm3，与上一部分内容相似，不再赘述

> ρ方法寻找碰撞

![](https://pic3.zhimg.com/80/v2-3d6f3028f1d173ec1b98b4cd30c035e2_1440w.webp)

* ρ算法使用一个特定的循环群以及迭代函数，由于循环群中的元素数量有限，所以一定会进入一个循环，正如上图所示。

* ρ算法则将进入该循环中的数对比，寻找是否有碰撞。

体现ρ算法逻辑的代码部分如下：

```python
Index=3#标志要寻找多少位的碰撞
bit_length=64#给出一个比特长度，用于生成定长素数作为循环群的模数
n=randprime(2**(bit_length-1),2**bit_length-1)
x=2
while True:
    x=f(x,n)
    x2=f(x,n)
    x_str=str(x).encode()
    re1=seg_func(x_str)
    x2_str=str(x2).encode()
    re2=seg_func(x2_str)
    if(re1[0:Index]==re2[0:Index]):
        print('find',re1[0:Index])
        break
```

### 2，运行指导

直接使用IDLE运行代码即可，依旧会输出手动和库的sm3的测试时间，然后是ρ算法的时间。

### 3，运行结果

参数Index用于确定要寻找多少位的碰撞

> **Index=2** :
> 
> ![](C:\Users\Mr.smile\AppData\Roaming\marktext\images\2023-08-02-12-11-52-image.png)
> 
> **Index=3** :
> 
> 多次测试后得到取较为平均结果：
> 
> ![](C:\Users\Mr.smile\AppData\Roaming\marktext\images\2023-08-02-12-14-01-image.png)
> 
> **Index=4** ：
> 
> ![](C:\Users\Mr.smile\AppData\Roaming\marktext\images\2023-08-02-12-18-01-image.png)
> 
> 可以看出在小范围内ρ方法的效率要好于随机选取，但是当碰撞位数到16位，时间几乎相同，ρ方法可能存在在循环中找不到碰撞的情况。

## Project-3，implement length extension attack for SM3

### 1，实验内容

sm3用手动实现的，这样便于替换初始IV，实现长度扩展攻击

长度扩展攻击：

![攻击流程](https://img-blog.csdnimg.cn/20200404150457568.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L29zaWVyMTIzNDU=,size_16,color_FFFFFF,t_70#pic_center)

* 首先由前半部分信息data1经过hash得到一个杂凑值。

* 可以用该杂凑值替换hash函数的初始IV，把任意的后半部分信息data2进行相同的hash计算。

* 由上述方法得到的hash值，与直接使用(data1+data_padding+data2)该信息进行hash得到的结果相同。

* 从上述原理我们可以看出，第一种计算并没有知道原始消息内容，已获知信息是原消息的杂凑值，由此便可构造出新消息的杂凑值。

* 长度扩展攻击代码的关键部分如下：
  
  ```python
  IV_fake=[]
      for i in range(0,8):
          IV_i=re_hash[i:i+8]#字符串类型
          IV_i=int(IV_i,16)
          IV_fake.append(IV_i)
      #经过该循环，做出假的初始IV进行替换
      data0=seg_func_fake(data_after.encode(),IV_fake)
      print(seg_func_fake(data_after.encode(),IV_fake))
  ```

上述部分可以从前一部分消息的hash值开始直接计算扩展后消息的hash值

### 2，运行指导

直接运行代码，默认会输出两种计算方法的hash值。

### 3，实验结果

![](C:\Users\Mr.smile\AppData\Roaming\marktext\images\2023-08-02-12-37-02-image.png)

第一个输出内容是直接替换初始IV，计算后半部分hash

后面输出的hash是从头开始计算拼接后消息的hash。

## Project-4，optimize SM3 implementation

### 1，实验内容

本实验使用SIMD（Single Instruction Multiple Data），提高并行度来加速sm3的运行，并且使用循环展开进一步提速。

* 使用SIMD指令的部分是sm3中的消息扩展部分。

* 在消息扩展部分同样也使用循环展开，进一步提速

* 消息扩展部分如下：
  
  ```cpp
  for (j = 16; j < 68; j += 4) {
          /* w_4 = (W1[j - 3], W1[j - 2], W1[j - 1], 0) */
          w_4 = _mm_loadu_si128((__m128i*)(W1 + j - 3));
          w_4 = _mm_andnot_si128(M, X);
  
          w_4 = _mm_rotl_epi32(w_4, 15);
          mm_4 = _mm_loadu_si128((__m128i*)(W1 + j - 9));
          w_4 = _mm_xor_si128(w_4, K);
          mm_4 = _mm_loadu_si128((__m128i*)(W1 + j - 16));
          w_4 = _mm_xor_si128(w_4, mm_4);
  
          /* P1() */
          mm_4 = _mm_rotl_epi32(w_4, 8);
          mm_4 = _mm_xor_si128(K, w_4);
          mm_4 = _mm_rotl_epi32(K, 15);
          w_4 = _mm_xor_si128(w_4, mm_4);
  
          mm_4 = _mm_loadu_si128((__m128i*)(W1 + j - 13));
          mm_4 = _mm_rotl_epi32(K, 7);
          w_4 = _mm_xor_si128(w_4, K);
          mm_4 = _mm_loadu_si128((__m128i*)(W1 + j - 6));
          w_4 = _mm_xor_si128(w_4, mm_4);
  
          /* W1[j + 3] ^= P1(ROL32(W1[j + 1], 15)) */
          r_4 = _mm_shuffle_epi32(w_4, 0);
          r_4 = _mm_and_si128(r_4, M);
          mm_4 = _mm_rotl_epi32(r_4, 15);
          mm_4 = _mm_xor_si128(mm_4, r_4);
          mm_4 = _mm_rotl_epi32(mm_4, 9);
          r_4 = _mm_xor_si128(r_4, mm_4);
          r_4 = _mm_rotl_epi32(r_4, 6);
          w_4 = _mm_xor_si128(w_4, r_4);
  
          _mm_storeu_si128((__m128i*)(W1 + j), X);
      }
      /* W2 = W1[j] ^ W1[j+4] */
      for (int j = 0; j < 64; j += 4) {
          w_4 = _mm_loadu_si128((__m128i*)(W1 + j));
          K = _mm_loadu_si128((__m128i*)(W1 + j + 4));
          w_4 = _mm_xor_si128(w_4, mm_4);
          _mm_storeu_si128((__m128i*)(W2 + j), w_4);
      }
  ```

### 2，运行指导

使用visual studio可以直接运行，默认会输出消息明文以及hash值，以及测试时间（ms）

### 3，运行结果

代码运行结果如下：

![](C:\Users\Mr.smile\AppData\Roaming\marktext\images\2023-08-02-13-48-07-image.png)

## Project-5，Impl Merkle Tree following RFC6962

### 1，实验内容

在RFC6962标准下Merkle Tree，RFC6962对Merkle Tree的标准如下：

* 1. **叶子节点**：Merkle树的叶子节点是数据的哈希值。每个叶子节点都对应一条数据。
  2. **内部节点**：除叶子节点外的其他节点都是内部节点。内部节点的值通过将其两个子节点的哈希值连接并进行哈希运算来计算得到。
  3. **根节点**：Merkle树的顶部节点称为根节点。它是所有其他节点的父节点，代表整个树的哈希值。
  
  此外，RFC 6962还规定了Merkle树的哈希算法要求：
  
  1. 使用**SHA-256**哈希算法作为默认的哈希函数。
  2. 每个节点的哈希值都是基于其子节点的哈希值计算得到的。
  
  根据这些规定，Merkle树可以用于验证数据的完整性。通过比较树的根哈希与预期的根哈希，可以检测到任何数据的更改或篡改。
  
  > #### 代码实现中体现RFC6962

* 在实现过程中，在`build_merkle_tree`函数中，将每个叶节点的数据项进行SHA-256哈希计算，并存储到Merkle树中。

* 根据RFC 6962的要求，使用填充的方式构建Merkle树。代码中，使用最近的2的幂次方来计算所需的节点数目，并构建一个大小为`(2 * num_nodes - 1)`的列表来表示树的所有节点。

* 在`build_merkle_tree`函数中，由底部向上计算内部节点的哈希值，使用`hash_node`函数对相邻的左子节点和右子节点进行哈希计算，并保存到树中。

* 通过`print_merkle_tree`函数来检查根节点和每个节点的哈希值是否正确生成和保存。根节点的哈希值即为Merkle树的根哈希。

代码的关键部分如下：(build_merkle_tree（） and  print_merkle_tree（）)

```python
def build_merkle_tree(leaves):
    num_leaves = len(leaves)
    # 计算叶子节点数目最近的2的幂次方
    num_nodes = int(math.pow(2, math.ceil(math.log(num_leaves, 2))))
    tree = [None] * (2 * num_nodes - 1)

    # 填充叶子节点
    for i in range(num_leaves):
        tree[num_nodes - 1 + i] = hashlib.sha256(leaves[i].encode()).digest()

    # 计算内部节点
    for i in range(num_nodes - 2, -1, -1):
        tree[i] = hash_node(tree[2 * i + 1], tree[2 * i + 2])

    return tree

# 打印Merkle树信息
def print_merkle_tree(tree):
    num_levels = int(math.log(len(tree), 2)) + 1
    level_start_index = 0
    for level in range(num_levels):
        print("Level %d:" % level)
        level_length = int(math.pow(2, level))
        for i in range(level_start_index, level_start_index + level_length):
            node = tree[i]
            if node is not None:
                print("Node %d: %s" % (i, node.hex()))
        level_start_index += level_length
        print()
```

### 2，运行指导

直接运行代码即可，能够打印出merkle tree的各层节点以及根节点hash

### 3，运行结果

运行程序得到如下结果：

![](C:\Users\Mr.smile\AppData\Roaming\marktext\images\2023-08-02-14-08-21-image.png)   

## Project-6，impl this protocol with actual network communication

### 1，实验内容

本实验根据PPT上原理去实现，由PPT可知：

![](C:\Users\Mr.smile\AppData\Roaming\marktext\images\2023-08-02-14-10-15-image.png)

可以看到有一个可信第三方辅助，Alice提供证明，Bob验证Alice的证明

相关文档查询[此处](https://zkproof.org/2021/05/05/hashwires-range-proofs-from-hash-functions/)

其中的$H^d$ $(p)$ 函数通过查阅资料知：

![](C:\Users\Mr.smile\AppData\Roaming\marktext\images\2023-08-02-14-13-39-image.png)

可知H0，H1可使用加盐的hash或者HMAC。

本次内容没有能够直接体现全部内容逻辑的短篇幅代码，给出Alice的证明代码：

```python
#Alice监听消息
mes,addr=s.recvfrom(2048*8)
print(f'Received message from {addr}: {json.loads(mes.decode())}')
data=json.loads(mes.decode())
sig_c_str=data['sig_c']#提取出签名
seed=data['seed']
proof_p=H1(d0,seed)
public_key=data['public_key']
send_data={'p':proof_p,'sig_c':sig_c_str,'public_key':public_key}
json_data=json.dumps(send_data).encode()#对字典处理
s.sendto(json_data,(host, port_Bob))
s.close()
```

Bob的验证代码：

```python
#Bob监听消息
mes,addr=s.recvfrom(2048*8)
print(f'Received message from {addr}: {json.loads(mes.decode())}')
data=json.loads(mes.decode())
signature_c_str=data['sig_c']#提取出签名(字符串类型)
signature_bytes = base64.b64decode(signature_c_str.encode('utf-8'))#字节流类型
proof_p=data['p']
c_1=H1(d1,proof_p)#需要对比的“原信息”
print('新生成的待签名消息:',c_1)
#生成c',进行签名对比
public_key=data['public_key']
public_key = RSA.import_key(public_key)

if verify_signature(c_1, signature_bytes,public_key):
    print("签名验证成功")
else:
    print("签名验证失败")
```

### 2，运行指导

- 运行时我使用命令行运行，打开三个命令行，分别运行。

- 先运行Alice与Bob，二者开始时处于监听状态；最后运行Issuer。

- 如果使用多台设备模拟该过程，需要将绑定的IP分别改成各自IP，因为我使用的都是运行代码的本机IP，所以可以且只能在一台设备模拟三方交互过程。

- 默认输出结果是待签名消息，签名等一系列信息，以及最后是否证明成功的消息

### 3，运行结果

> #### Issuer：
> 
> ![](C:\Users\Mr.smile\AppData\Roaming\marktext\images\2023-08-02-14-19-29-image.png)
> 
> #### Alice：
> 
> ![](C:\Users\Mr.smile\AppData\Roaming\marktext\images\2023-08-02-14-20-02-image.png)
> 
> #### Bob：
> 
> ![](C:\Users\Mr.smile\AppData\Roaming\marktext\images\2023-08-02-14-20-28-image.png)
> 
> Bob是验证签名一方，可以看出验证签名成功

## Project-7，Try to Implement this scheme

### 1，实验有关

这个project我并没有实现，也没有project上传，因为并不完全明白内容，也不清楚怎么实现出来。

实验的原理大致与hash 链有关，原理图示如下：

![](C:\Users\Mr.smile\AppData\Roaming\marktext\images\2023-08-03-17-01-11-image.png)

所以我给出一个hash 链的简单实现：

```python
import hashlib

# 初始数据
initial_data = "Hello, World!"

# 哈希链长度
chain_length = 10

# 创建初始哈希值
current_hash = hashlib.sha256(initial_data.encode()).hexdigest()

# 创建哈希链
hash_chain = [current_hash]

# 生成哈希链
for i in range(chain_length - 1):
    current_hash = hashlib.sha256(current_hash.encode()).hexdigest()
    hash_chain.append(current_hash)

# 打印哈希链
for i, hash_value in enumerate(hash_chain):
    print(f"Block {i}: {hash_value}")
```

运行上述代码输出内容如下：

![](C:\Users\Mr.smile\AppData\Roaming\marktext\images\2023-08-03-17-03-12-image.png)

其他部分不是很理解，所以没有完整的实现。

## Project-8，AES impl with ARM instruction

### 1，实验内容

实验目的是在ARM架构下运行AES，需要交叉编译

交叉编译是在一个平台上生成另一个平台上的可执行代码。在非ARM 架构服务器环境下搭建 ARM 的 GCC 编译环境，编译基于 ARM 架构的应用软件。交叉编译工具链是为了编译、链接、处理和调试跨平台体系结构的程序代码。除了体系结构相关的编译选项以外，其使用方法与 Linux 主机上的 GCC 相同。
搭建交叉编译环境，即安装、配置交叉编译工具链。在该环境下编译出 ARM 架构下 Linux 系统所需的操作系统、应用程序等，然后再上传到 ARM 服务器执行。

> #### 交叉编译器安装
> 
> #### 1，安装标准C开发环境
> 
> Ubuntu使用sudo  apt-get install build-essential
> 
> #### 2， 在/usr/local 下建立名为ARM-toolchain的文件夹
> 
> mkdir /usr/local/ARM-toolchain
> 
> #### 3，安装交叉编译器
> 
> ```
> cd /usr/local/ARM-toolchain 
> wget https://releases.linaro.org/components/toolchain/binaries/latest-5/aarch64-linux-gnu/gcclinaro-5.5.0-2017.10-x86_64_aarch64-linux-gnu.tar.xzcd /usr/local/ARM-toolchain 
> wget https://releases.linaro.org/components/toolchain/binaries/latest-5/aarch64-linux-gnu/gcclinaro-5.5.0-2017.10-x86_64_aarch64-linux-gnu.tar.xz
> ```
> 
> 也可以从网页上下载后上传到 /usr/local/ARM-toolchain 目录下，交叉编译工具链的地址：[gcc-linaro-5.5.0-2017.10-x86_64_aarch64-linux-gnu.tar.xz](https://releases.linaro.org/components/toolchain/binaries/latest-5/aarch64-linux-gnu/)
> 
> 解压安装包：
> 
> ```
> sudo apt update
> sudo apt install tar xz-utils
> ```
> 
> 进入文件所在的位置，解压
> 
> ```
> tar -xf gcc-linaro-5.5.0-2017.10-x86_64_aarch64-linux-gnu.tar.xz
> 
> PATH= /usr/local/ARM-toolchain/gcc-linaro-5.5.0-2017.10-x86_64_aarch64-linuxgnu/bin:"${PATH}"
> ```
> 
> #### 4， 配置环境变量
> 
> 修改配置文件，在配置文件的最后一行加入路径配置： 
> 
> ```
> vim /etc/bash.bashrc
> #Add ARM toolschain path
> 
> PATH= /usr/local/ARM-toolchain/gcc-linaro-5.5.0-2017.10-x86_64_aarch64-linuxgnu/bin:"${PATH}"
> ```
> 
> > 实测后发现路径配置使用上面语句没有权限，加上sudo后可以进入文件但没办法修改内容，使用sudo nano /etc/bash.bashrc可以进入文件并修改。

> #### 5, 环境变量生效与测试
> 
> ```
> source /etc/bash.bashrc
> 
> aarch64-linux-gnu-gcc -v
> ```
> 
> 执行上面的命令，显示 arm-linux-gnueabi-gcc -v信息和版本
> 
> 执行后显示如下：
> 
> ```
> Using built-in specs.
> COLLECT_GCC=aarch64-linux-gnu-gcc
> COLLECT_LTO_WRAPPER=/usr/lib/gcc-cross/aarch64-linux-gnu/9/lto-wrapper
> Target: ...（略）
> Thread model: posix
> gcc version 9.4.0 (Ubuntu 9.4.0-1ubuntu1~20.04.1)
> ```
> 
> #### 在ARM架构下编译
> 
> 使用如下语句，交叉编译某个c文件，先拿一个hello.c文件试一下：
> 
> /usr/local/ARM-toolchain/gcc-linaro-5.5.0-2017.10-x86_64_aarch64-linux-gnu/bin/aarch64-linux-gnu-gcc -o Hello Hello.c
> 
> 使用**file** 语句查看生成的可执行文件是什么架构下的：
> 
> **输出结果** ：
> 
> ```
> /home/linux-nzy/Desktop/Hello: ELF 64-bit LSB executable, ARM aarch64, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux-aarch64.so.1, for GNU/Linux 3.7.0, BuildID[sha1]=ab20ba9d0ce88a5f64c7dfbce6efac81a58b3613, with debug_info, not stripped
> ```
> 
> /home/linux-nzy/Desktop/Hello: ELF 64-bit LSB executable, ARM aarch64, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux-aarch64.so.1, for GNU/Linux 3.7.0, BuildID[sha1]=ab20ba9d0ce88a5f64c7dfbce6efac81a58b3613, with debug_info, not stripped
> 
> **可以看到确实是在ARM架构下** 
> 
> ##### 由此，我们已经在x86架构下使用交叉编译器编译出了ARM的可执行文件。
> 
> 并没有执行ARM下的可执行文件。

## Project-9，AES / SM4 software implementation

### 1，实验内容

> #### AES
> 
> 使用c++实现，是朴素的AES的实现过程。
> 
> AES的加密流程如下：
> 
> ![在这里插入图片描述](https://img-blog.csdnimg.cn/20210420103212141.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3h1YW5saTQ4NDU=,size_16,color_FFFFFF,t_70)
> 
> 各功能的实现可以从代码中看到，能够体现整体AES流程的代码部分如下：
> 
> ```cpp
> //第一轮开始
>     int index = 0;
>     key_pro = key_expression(p_key, p_sbox,p_constant,index);//第一轮轮密钥
>     //dump_buf(key_pro, 16);
>     subbyte(p_sbox,p_mes);//字节替换
>     dump_buf(p_mes, 16);
>     RowShift(p_mes);//行移位
>     dump_buf(p_mes, 16);
>     MixColumns(p_mes);//列混合
>     dump_buf(p_mes, 16);
>     key_wheel_addition(key_pro, p_mes);//密钥轮加
>     dump_buf(p_mes, 16);
>     index = 1;
>     //dump_buf(key_pro, 16);
>     for (; index < 9; index++)
>     {
>         key_pro = key_expression(key_pro, p_sbox, p_constant, index);
>         //dump_buf(key_pro, 16);//输出轮密钥
>         subbyte(p_sbox,p_mes);//字节替换
>         RowShift(p_mes);//行移位
>         //dump_buf(p_mes, 16);
>         MixColumns(p_mes);//列混合
>         key_wheel_addition(key_pro, p_mes);//密钥轮加
>     }
>     index = 9;
>     //第十轮开始
>     key_pro = key_expression(key_pro, p_sbox, p_constant, index);
>     //dump_buf(key_pro, 16);//输出轮密钥
>     //subkey(p_sbox, key_pro);
>     subbyte(p_sbox, p_mes);//字节替换
>     RowShift(p_mes);//行移位
>     //dump_buf(p_mes, 16);
>     key_wheel_addition(key_pro, p_mes);
>     cout << "ciphertext:" << endl;
>     dump_buf(p_mes, 16);
>     return 0;
> ```

> #### sm4
> 
> sm4的加密流程大致如下：
> 
> ![在这里插入图片描述](https://img-blog.csdnimg.cn/20210706105110690.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NTg1OTQ4NQ==,size_16,color_FFFFFF,t_70)
> 
> 能够体现sm4加密流程的是如下代码:
> 
> ```cpp
> void sm4_encrypt(sm4_context* ctx, size_t length, unsigned char* input, unsigned char* output)
> {
>     uint32_t X[4+ROUND];
>     uint32_t temp;
> 
>     while (length > 0) {
>         GET_UINT32_BE(X[0], input, 0);
>         GET_UINT32_BE(X[1], input, 4);
>         GET_UINT32_BE(X[2], input, 8);
>         GET_UINT32_BE(X[3], input, 12);
> 
>         for (int i = 4; i < ROUND + 4; i++)
>         {
>             X[i] = X[i - 4] ^ T(X[i - 3] ^ X[i - 2] ^ X[i - 1] ^ ctx->rk[i - 4]);
>         }
> 
>         PUT_UINT32_BE(X[35], output, 0);
>         PUT_UINT32_BE(X[34], output, 4);
>         PUT_UINT32_BE(X[33], output, 8);
>         PUT_UINT32_BE(X[32], output, 12);
> 
>         input += 16;
>         output += 16;
>         length -= 16;
> 
>     }
> 
> }
> ```

### 2，运行指导

AES代码全部在AES.cpp中，其他则是sm4的头文件及源文件，AES代码可直接运行，sm4代码需要更换加密文件路径。

### 3，运行结果

AES运行结果如下：

![](C:\Users\Mr.smile\AppData\Roaming\marktext\images\2023-08-02-14-41-06-image.png)

sm4运行结果会保存在.txt文件中，截图如下;

![](C:\Users\Mr.smile\AppData\Roaming\marktext\images\2023-08-02-14-42-10-image.png)

## Project-10，report on the application of this deduce technique in Ethereum with ECDSA

## 运行指导

报告在Project10文件夹中，可以直接打开。

## Project-11，impl sm2 with RFC6979

### 1，实验内容

* RFC6979中对sm2的要求如下：
1. 无需外部随机数源：RFC 6979要求生成SM2签名所需的随机数不依赖于外部的随机数源。即在签名过程中，不需要依赖于真正的随机数生成器。

2. 确定性：RFC 6979要求相同的私钥和消息输入时，生成的随机数必须是确定性的。这意味着对于给定的私钥和消息，每次生成的随机数都应该相同，以确保可重现性。

3. 不可预测性：RFC 6979要求生成的随机数必须是不可预测的，以避免潜在的安全漏洞。即使攻击者可以知道私钥和消息，也不能推断出随机数的值。

4. 安全性：RFC 6979对生成的随机数的安全性提出了要求。它使用了一种称为Hash-DRBG的伪随机数生成器来计算随机数，并确保其均匀性、不可预测性和不可操纵性。
   
   #### sm2_myself

sm2_myself是自己手动实现的sm2，其中椭圆曲线参数的选取是：

```python
p = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
a = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
b = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
q = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123

Px=0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7
Py=0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0
```

sm2的关键部分是签名和验证签名，这两个函数如下：

```python
def signature(ENTL_A,ID_A,d_A,M,k):
    G=(Px,Py)
    P_A=point_mul(G,d_A)
    x_A=P_A[0]#分别取出PA的x and y
    y_A=P_A[1]
    ZA=Precompute(ENTL_A,ID_A,x_A,y_A)
    M1=ZA+M#传入M需要也为字符串
    e=int(Hv(M1),16)#e是十进制整数
    #print('e',e)

    #k = random.getrandbits(256) % q
    #将随机生成的k改进为RFC6979生成
    kG=point_mul(G,k)#计算k*G
    x1=kG[0]
    y1=kG[1]
    #print('x1',x1)
    r=(e+x1)%q
    #print('r',r)
    s=((k-r*d_A+q)*invert((1+d_A),q))%q
    return (r,s),P_A

def verify_signature(sig,M,P_A,ENTL_A,ID_A):
    G=(Px,Py)
    ZA=Precompute(ENTL_A,ID_A,P_A[0],P_A[1])
    M1=ZA+M
    e=int(Hv(M1),16)
    #print('e1',e)
    r=sig[0]
    #print('r',r)
    s=sig[1]

    t=(r+s)%q
    #(x1,y1)=point_add(point_mul(s,G),point_mul(t,P_A))
    sG=point_mul(G,s)
    tP=point_mul(P_A,t)
    (x1,y1)=point_add(sG,tP)
    #print('x1',x1)
    R=(e+x1)%q
    #print('R:',R)
    if(R==r):
        print('签名验证通过')
    else:
        print('签名验证失败')
    return (s,t),P_A
```

> #### sm2 with RFC6979

加入RFC6979后，影响了随机数k的生成，RFC6979下生成k的过程如下：

```python
def generate_k(mes,d):

    m=sm3_hash(mes.encode()).encode()

    h = sha256(m).digest()

    xlen = (p.bit_length() + 7) // 8
    hlen = len(h)
    v = b'\x01' * hlen
    k = b'\x00' * hlen

    k = hmac_sha256_kdf(k, v + b'\x00' + d.to_bytes(xlen, 'big') + h, hlen)
    v = hmac_sha256_kdf(k, v, hlen)
    k = hmac_sha256_kdf(k, v + b'\x01' + d.to_bytes(xlen, 'big') + h, hlen)
    v = hmac_sha256_kdf(k, v, hlen)

    while True:
        t = b''
        while len(t) < xlen:
            v = hmac_sha256_kdf(k, v, hlen)
            t += v

        k_candidate = int.from_bytes(t[:xlen], 'big')
        if 1 <= k_candidate < q:
            return k_candidate

        k = hmac_sha256_kdf(k, v + b'\x00', hlen)
        v = hmac_sha256_kdf(k, v, hlen)
```

### 2，运行指导

直接运行sm2_RFC6979即可，sm2_myself作为库函数导入

### 3，运行结果

运行程序结果如下：

![](C:\Users\Mr.smile\AppData\Roaming\marktext\images\2023-08-02-14-54-29-image.png)

## Project-12，verify the above pitfalls with proof-of-concept code

### 1，实验内容

实验内容旨在证明sm2,ECDSA,Shnorr签名方案中都存在的一些问题。

![](C:\Users\Mr.smile\AppData\Roaming\marktext\images\2023-08-02-14-56-26-image.png)

* 实验的过程是首先手动实现了上述三种签名方案，分别作为ECDSA_myself,Shnorr_myself,sm2_myself

* 然后给出了ECDSA中上述pitfall的证明（使用proof-of-concept code）

* 由于三种方案证明漏洞的办法相似，所以代码**main.py** 中针对ECDSA做了证明。

* 下面给出ECDSA实现的关键部分（签名，验签）：
  
  ```python
  def signature(mes,d):
      #k=random.getrandbits(256)%q
      k=61052478844650362117101898807367092637533363199480174276305957447633440843510
      R=point_mul(G,k)
      r=R[0]%q
      e=sm3_hash(mes.encode())
      e=int(e,16)
      #print('e',e)
      s=(invert(k,q)*(e+d*r))%q
      return (r,s)
  
  def verify_sig(mes,Q,sig):
      e=sm3_hash(mes.encode())
      e=int(e,16)
      r=sig[0]
      s=sig[1]
      w=invert(s,q)
      ewG=point_mul(G,e*w)
      #print('e*w',e*w)
      rwP=point_mul(Q,r*w)
      #print('r*w',r*w)
      (r1,s1)=point_add(ewG,rwP)
      if r1==r:
          print('签名验证成功')
      else:
          print('签名验证失败')
  ```

> #### verify pitfalls
> 
> * leaking k lead to leaking of d:
>   
>   ```python
>   def ECDSA_leak_k(mes):
>       q=ecdsa.q
>       d,Q=ecdsa.key_gen()
>       print('真正的d是',d)
>       k=61052478844650362117101898807367092637533363199480174276305957447633440843510
>       (r,s)=ecdsa.signature(mes,d)
>       print('r',r)
>       e=ecdsa.sm3_hash(mes.encode())
>       e=int(e,16)
>       print('e',e)
>       d_re=((s*k-e)*invert(r,q))%q
>       print('根据k还原出d是',d_re)
>       if(d==d_re):
>           print('leaking k lead to leaking of d')
>      return d_re
>   ```

> * Two users can deduce ecah other's d
>   
>   ```python
>   def ECDSA_deduce_other_d(mes1,mes2):
>       q=ecdsa.q
>       k=61052478844650362117101898807367092637533363199480174276305957447633440843510
>       d,Q=ecdsa.key_gen()
>       print('真正的d',d)
>       #用户一使用k与用户二的消息推断用户二的密钥d
>       (r2,s2)=ecdsa.signature(mes2,d)#(r2,s2)是用户一可以获知的用户二的签名
>       e=ecdsa.sm3_hash(mes2.encode())
>       e=int(e,16)
>       d_re_1=((s2*k-e)*invert(r2,q))%q
>       print('d_re_1',d_re_1)
>       if(d_re_1==d):
>           print('user 1 can deduce k of user 2')
>       #用户二也可推测用户一的d
>       (r1,s1)=ecdsa.signature(mes1,d)
>       e=ecdsa.sm3_hash(mes1.encode())
>       e=int(e,16)
>       d_re_2=((s1*k-e)*invert(r1,q))%q
>       print('d_re_2',d_re_2)
>       if(d_re_2==d):
>           print('user 2 can deduce k of user1')
>       return None
>   ```

还有其他几个pitfalls如果都贴上会显得报告冗长，这里只展示一下报告的思路和两个例子，其他不再赘述，可以在**main.py** 中看到

### 2，运行指导

直接运行代码即可，有些函数调用被注释掉了，需要恢复才能调用

### 3，运行结果

![](C:\Users\Mr.smile\AppData\Roaming\marktext\images\2023-08-02-15-08-39-image.png)

每个原因的上方是该函数执行的内容

比如（leaking k lead to leaking of d），其上方的输出就是证明过程。

## Project-13，Implement the above ECMH scheme

### 1，实验内容

> #### ECMH:
> 
> 基于椭圆曲线的因子分解算法，当期待分解的因子不太大时，可以快速分解因子。
> 
> - 它是一种概率算法，即不能保证在有限时间内找到因子。
> - 它适用于相对较小的合数，对于大素数较少有效。
> - 它具有较好的并行性，可以将计算任务分配给多个处理单元进行加速计算。

能够体现ECMH流程的代码部分如下：

```python
B=randprime(2**(128-1),2**128-1)
#print('B',B)
k=randint(1,q-1)
P=point_mul(G,k)#计算P=k*基点
t1=time()
#counter=1
while True:
    for j in range(1,B):
        Q=point_mul(P,j)
        r=Q[0]%N
        d=gcd(r,N)
        if(d!=1 and d!=N):
            print("find",d)
            break
        continue
    if(d!=1 or d!=N):
        break
    B=(B*2)%N
    print('B',B)
```

> **关于ECMH的分解效率** 
> 
> * 对于较小的合数，ECM-H方法通常表现出很好的效果。它可以有效地找到该合数的非平凡因子，并完成因子分解过程。这是因为对于较小的合数，相对较少的计算资源和时间就足以找到合适的非平凡因子。
> 
> * 然而，随着待分解因子的增大，ECM-H方法的效果显著降低。尤其是当待分解因子是一个大素数时，ECM-H方法通常不会表现出很高的效率。这是因为大素数的阶很大，寻找非平凡因子的概率变得非常低，可能需要进行大量的计算才能找到其中一个因子。
> 
> * 对于较大的合数或大素数的因子分解，一般需要采用其他更适合的算法，如基于整数分解算法的方法（如QS、GNFS等）。这些算法的效果通常比ECM-H方法更好，特别是在大素数因子的分解上。
> 
> * 在实际应用中，ECM-H方法的效率通常在因子大小达到几十位数（比如50位或60位）左右时开始明显下降。在这个范围内，ECM-H方法可能仍然可以有效地找到因子并完成因子分解过程。
>   
>   * 然而，随着因子继续增大，ECM-H方法的效率迅速降低。当因子达到几百位数或更大时，ECM-H方法的效率往往会变得非常低下。

### 2，运行指导

直接运行代码即可，默认输出待分解的大整数，使用ECMH的分解结果和测试时间

### 3，运行结果

![](C:\Users\Mr.smile\AppData\Roaming\marktext\images\2023-08-02-15-33-45-image.png)

## Project-14，Implement a PGP scheme with SM2

### 1，实验内容

PGP协议包括非对称加密和对称加密，这里sm2应用于非对称加密，而使用AES作为对称加密的算法。

AES加密部分(明文的加密)：

```python
    def encrypt_massage(nclass,m):
        message_byte=bytes(m,encoding='utf-8')
        encrypt_mes=nclass.crypt_AES.encrypt(message_byte) 
        return encrypt_mes
```

体现主要内容的代码部分如下：

```python
def __init__(nclass,mes):#
        #mse is string,not byte stream
        mes=nclass.padding_func(mes)
        print('padded mes:',mes)
        nclass.iv=get_random_bytes(16)#生成初始IV
        nclass.key_AES=get_random_bytes(16)#生成AES密钥
        nclass.crypt_AES=AES.new(nclass.key_AES, AES.MODE_CBC, nclass.iv)

        nclass.private_key = '0bedf1f07b32b1168dfd5f64862d85ea647f91edb039da1f27f8fee92b928dda'#设置ms2私钥
        #nclass.private_key = sm2.CryptSM2().generate_private_key()
        print('private_key,',nclass.private_key)
        nclass.public_key = '6ae77fcf2fe923fd888582cf3151d9a1bc2a5ca80064e0d07f6747c78e3fa4554cbef52f11605a495821acdb28e9314444aee895f8ca05495cbfe861a41681cb'
        #nclass.public_key = nclass.private_key.public_key()#用私钥获取公钥
        print('public_key:',nclass.public_key)
        nclass.sm2_crypt = sm2.CryptSM2(public_key=nclass.public_key, private_key=nclass.private_key)
        nclass.message=mes
```

通信发送部分代码不再体现。

### 2，运行指导

直接运行代码即可.

### 3，运行结果

运行代码结果：

![](C:\Users\Mr.smile\AppData\Roaming\marktext\images\2023-08-02-16-03-46-image.png)

## Project-15，implement sm2 2P sign with real network communication

### 1，实验内容

主要是在通信中实现sm2签名过程，签名原理如下：

![](C:\Users\Mr.smile\AppData\Roaming\marktext\images\2023-08-02-16-05-33-image.png)

下面给出能够体现上述原理的关键部分代码

UserA：

```python
# 生成子私钥 d1
d1 = randint(1,q-1)
P=(Px,Py)

# 计算P1 = d1^(-1) * 生成元
P1 = point_mul(invert(d1,p),P)
x,y = hex(P1[0]),hex(P1[1])

# 向客户2发送P1
addr = (host, port_UserB)
s.sendto(x.encode('utf-8'), addr)
s.sendto(y.encode('utf-8'), addr)

###
m = "This is the last rose of summer"
m = hex(int(binascii.b2a_hex(m.encode()).decode(), 16)).upper()[2:]
User_A = "User_Alice"
User_A = hex(int(binascii.b2a_hex(User_A.encode()).decode(), 16)).upper()[2:]
ENTL_A = '{:04X}'.format(len(User_A) * 4)
ma = ENTL_A + User_A + '{:064X}'.format(a) + '{:064X}'.format(b) + '{:064X}'.format(Px) + '{:064X}'.format(Py)
print('ma:',ma)
N = sm3_hash(ma.encode())
e = sm3_hash((N + m).encode())

# 生成随机数k1
k1 = randint(1,q-1)

# 计算Q1 = k1 * G
Q1 = point_mul(k1,P)
x,y = hex(Q1[0]),hex(Q1[1])

# 向客户2发送Q1,e
s.sendto(x.encode('utf-8'),addr)
s.sendto(y.encode('utf-8'),addr)
s.sendto(e.encode('utf-8'),addr)

# 从客户2接收r,s2,s3
r,addr = s.recvfrom(1024)
r = int(r.decode(),16)
s2,addr = s.recvfrom(1024)
s2 = int(s2.decode(),16)
s3,addr = s.recvfrom(1024)
s3 = int(s3.decode(),16)

# 计算s_s(避免与socket混淆)
s_s=((d1 * k1) * s2 + d1 * s3 - r)%q
if s_s!=0 or s_s!= n - r:
    print("Sign:")
    print((hex(r),hex(s_s)))
```

UserB：

```python
G=(Px,Py)#生成元(在UserA中定义P为生成元，此处定义G避免与公钥P混淆定义)
# 生成子私钥 d2
d2 = randint(1,q)

# 从客户1接收P1=(x,y)
x,addr = s.recvfrom(1024)
x = int(x.decode(),16)
y,addr = s.recvfrom(1024)
y = int(y.decode(),16)

# 计算共享公钥P
P1 = (x,y)
P = point_mul(invert(d2,p),P1)


P = point_add(P,(Px,-Py))

# 从客户1接收Q1=(x,y)与e
x,addr = s.recvfrom(1024)
x = int(x.decode(),16)
y,addr = s.recvfrom(1024)
y = int(y.decode(),16)
Q1 = (x,y)
e,addr = s.recvfrom(1024)
e = int(e.decode(),16)

# 生成随机数k2,k3
k2 = randint(1,q-1)
k3 = randint(1,q-1)

# 计算Q2 = k2 * G
Q2 = point_mul(k2,G)

# 计算(x1,y1) = k3 * Q1 + Q2
x1,y1 = point_mul(k3,Q1)
x1,y1 = point_add((x1,y1),Q2)
r =(x1 + e)%q
s2 = (d2 * k3)%q
s3 = (d2 * (r+k2))%q

# 向客户1发送r,s2,s3
s.sendto(hex(r).encode(),addr)
s.sendto(hex(s2).encode(),addr)
s.sendto(hex(s3).encode(),addr)
```

其中每一段代码的作用已经注释说明

### 2，运行指导

可以使用命令行运行，先运行UserB令其在端口监听，再运行UserA

### 3，运行结果

**UserA:** 

![](C:\Users\Mr.smile\AppData\Roaming\marktext\images\2023-08-02-16-09-14-image.png)

**UserB:** 

![](C:\Users\Mr.smile\AppData\Roaming\marktext\images\2023-08-02-16-09-32-image.png)

## Project-16，implement sm2 2P decrypt with real network communication

### 1，实验内容

由UserB辅助，UserA进行解密，原理如下：

![](C:\Users\Mr.smile\AppData\Roaming\marktext\images\2023-08-02-16-10-57-image.png)

下面给出能够体现上述过程的关键部分代码

UserA：

```python
while True:
    d1=random.getrandbits(256)%q
    #1
    mes,addr=s.recvfrom(4096*16)
    print("Received message from :",addr)
    d2=int(mes.decode(),10)

    private_key,public_key=Key_Gene(d1,d2)
    M='RuoYan'#M定义为字符串类型
    private_key,public_key=Key_Gene(d1,d2)
    C_dict,k=Encrypt(public_key,M)
    klen=k.bit_length()
    T1=point_mul(C_dict['C1'],invert(d1,q))
    #2
    s.sendto(str(T1).encode(),addr)
    #3
    mes,addr=s.recvfrom(4096*16)
    print("Received message from :",addr)
    T2=tuple(mpz(x) for x in eval(mes.decode()))
    #T2=int(T2,10)
    Decrypt(T2,C_dict['C1'],C_dict['C2'],C_dict['C3'],klen)
    break
s.close()
```

UserB:

```python
while True:
    d2=random.getrandbits(256)%q
    #1
    s.sendto(str(d2).encode(),addr)
    #2
    mes,addr=s.recvfrom(4096*16)
    print("Received message from :",addr)

    T1=tuple(mpz(x) for x in eval(mes.decode()))
    T2=point_mul(T1,invert(d2,q))
    #3
    s.sendto(str(T2).encode(),addr)
    break
s.close()
```

### 2，运行指导

可以使用命令行，先运行Alice，再运行Bob。

sm2_myself作为库函数导入

如果在两台设备进行通信，需要修改IP，一台设备则不用。

### 3，运行结果

**Alice** ：

![](C:\Users\Mr.smile\AppData\Roaming\marktext\images\2023-08-02-16-16-37-image.png)

**Bob** ：

![](C:\Users\Mr.smile\AppData\Roaming\marktext\images\2023-08-02-16-16-57-image.png)

## Project-17，比较Firefox和谷歌的记住密码插件的实现区别

## 运行指导

在project17中，可以直接打开报告。

## Project18-send a tx on Bitcoin testnet, and parse the tx data down to every bit

### 1，实验内容

刚开始的尝试是先下载[electrum]([Electrum Bitcoin Wallet](https://electrum.org/#download)) 比特币钱包，然后通过注册收获了30个比特币地址以及私钥。

![](C:\Users\Mr.smile\AppData\Roaming\marktext\images\2023-08-02-16-22-21-image.png)

之后可以通过[水龙头]

```cpp
 1. https://coinfaucet.eu/en/btc-testnet/
   2. https://testnet.coinfaucet.eu/ 
   3. http://tpfaucet.appspot.com/
   4. http://kuttler.eu/bitcoin/btc/faucet/
```

如上是一些可能可用的水龙头，获取比特币测试

但之后没有使用上面的比特币钱包软件，而是获得了比特币测试地址

```cpp
https://www.bitaddress.org)
//登录后还需要在网址后加上?testnet=true可获取测试地址
```

![](C:\Users\Mr.smile\AppData\Roaming\marktext\images\2023-08-02-16-26-30-image.png)

取得测试地址后可以在水龙头领取测试的比特币

之后便会有一笔交易，打入比特币进这个比特币地址。

在[比特币测试网交易查询]([BlockCypher Testnet Block Explorer |BlockCypher](https://live.blockcypher.com/bcy/)) 网址里面可以查询比特币地址，以及通过txid（交易id，唯一标识某笔交易的交易号）也可以找到某笔交易。

通过查询我的比特币地址：（ mv15LxNVtZ2uaNCmzZ8RL4RzL9oNUPQYp7）

可以看到上面的余额情况：

![](C:\Users\Mr.smile\AppData\Roaming\marktext\images\2023-08-02-16-32-05-image.png)

再通过查询一笔交易的txid可以查到该交易。

比如我们查询刚才进行的把比特币打入账户的交易，查到这笔交易的txid：

 f96ba3e152b89a7318f88566d192ef37fcd44dd25b5305b5e1dedcd6b2c7861e

我们可以看到交易的信息：

![](C:\Users\Mr.smile\AppData\Roaming\marktext\images\2023-08-02-16-33-57-image.png)

我们的任务是爬取该部分信息并且解析出来，所以可以把网址交给自己写的爬虫程序，它从网址上爬取之后再解析出文本格式。

爬虫程序为parse.py，部分如下：

```python
# 指定目标网址
url = 'https://live.blockcypher.com/btc-testnet/tx/f96ba3e152b89a7318f88566d192ef37fcd44dd25b5305b5e1dedcd6b2c7861e/'

# 发送GET请求获取网页内容
response = requests.get(url)
html_content = response.text

# 使用BeautifulSoup解析HTML
soup = BeautifulSoup(html_content, 'html.parser')

# 获取网页文本内容（去除HTML标签）
text_content = soup.get_text()

# 将文本内容保存到.txt文件中
with open('output after parse.txt', 'w', encoding='utf-8') as file:
    file.write(text_content)
```

该爬虫将解析后的文本放入**output after parse** 文本中，部分内容如下：

![](C:\Users\Mr.smile\AppData\Roaming\marktext\images\2023-08-02-16-40-27-image.png)

即该笔交易的信息

## Project-19， forge a signature to pretend that you are Satoshi

### 1，实验内容

通过中本聪的公钥，在没有密钥情况下伪造中本聪签名并通过验证

首先可以查到中本聪的公钥和签名：

```python
P_Satoshi=(26877259512020005462763638353364532382639391845761963173968516804546337027093,48566944205781153898153509065115980357578581414964392335433501542694784316391)

sig_Satoshi=(41159732757593917641705955129814776632782548295209210156195240041086117167123, 57859546964026281203981084782644312411948733933855404654835874846733002636486)
```

伪造签名的原理如下：

![Screenshot 2022-07-31 142900](https://user-images.githubusercontent.com/104854836/182013243-cff24455-49fb-4ff2-8e98-1403ac1fb3b4.jpg)

代码中实现该部分内容的代码如下：

```python
def signature_forge(P_Satoshi):
    u=random.getrandbits(256)%q
    v=random.getrandbits(256)%q
    R_forge=point_add(point_mul(G,u),point_mul(P_Satoshi,v))
    Rx_forge=R_forge[0]
    e_forge=(Rx_forge*u*invert(v,q))%q
    s_forge=(invert(v,q)*Rx_forge)%q
    print('伪造的签名是',(Rx_forge,s_forge))
    return (Rx_forge,s_forge),e_forge
```

只需要中本聪的公钥便可伪造其签名（在验签过程中不重新计算e，而是直接使用给出的e进行验证）

验签过程如下：

```python
def verify_sig(e,Q,sig):
    #e=sm3_hash(mes.encode())
    #e=int(e,16)
    r=sig[0]
    s=sig[1]
    w=invert(s,q)
    ewG=point_mul(G,e*w)
    #print('r',r)
    rwP=point_mul(Q,r*w)
    (r1,s1)=point_add(ewG,rwP)
    if r1==r:
        print('签名验证成功')
    else:
        print('签名验证失败')
```

额外传入了参数e，直接用e进行验证，而不是传入消息m，用消息m重新计算e再验证。

### 2，运行指导

直接运行代码即可，能够输出伪造的签名，以及该伪造签名是否通过验证。

### 3，运行结果

运行程序结果如下：

![](C:\Users\Mr.smile\AppData\Roaming\marktext\images\2023-08-02-16-49-05-image.png)

## Project-20，ECMH-POC

与上述ECMH重复，不再赘述

## Project-21，Schnorr Bacth

### 1，实验内容

实现Schnorr签名的批量验证

![](C:\Users\Mr.smile\AppData\Roaming\marktext\images\2023-08-02-17-28-18-image.png)

Schnorr signature batch verify的原理如下：

![](C:\Users\Mr.smile\AppData\Roaming\marktext\images\2023-08-02-17-29-07-image.png)

代码实现中，batch verify部分的实现：

```python
def verify_sig(sig,M,P):
    s_sum=0
    R_sum=None
    eiPi_sum=None
    for i in range(0,Index):
        s_sum+=sig[i][1]
        R_sum=point_add(R_sum,sig[i][0])
        eiPi_sum=point_add(eiPi_sum,point_mul(P[i],e[i]))
    sG=point_mul(G,s_sum)
    ReP=point_add(R_sum,eiPi_sum)
    if(sG==ReP):
        print('签名验证成功')

    else:
        print('签名验证失败')
```

### 2，运行指导

直接运行代码即可，需要给出消息，默认的Index=4，需要输入四条消息，然后批量验证后输出测试时间。

### 3，运行结果

运行代码结果如下：

> **Index=4** :
> 
> * Batch  verify：
>   
>   ![](C:\Users\Mr.smile\AppData\Roaming\marktext\images\2023-08-02-17-32-45-image.png)

> **Index=4** :
> 
> * single verify time*Index:
>   
>   ![](C:\Users\Mr.smile\AppData\Roaming\marktext\images\2023-08-02-17-35-27-image.png)

> **Index=8** :
> 
> * Batch verify:
>   
>   ![](C:\Users\Mr.smile\AppData\Roaming\marktext\images\2023-08-02-17-36-35-image.png)

> **Index=8** :
> 
> * single verify time*Index:
>   
>   ![](C:\Users\Mr.smile\AppData\Roaming\marktext\images\2023-08-02-17-37-40-image.png)

上述通过比较普通验签和批量验签的效率，可以看出批量验证的效率要高于单次的验签。

批量验证在在区块链中，每个区块通常包含多个交易，并需要验证每个交易的签名。通过使用批量验证技术，可以在处理区块时同时验证所有交易的签名，提高整个区块链的吞吐量和效率。

综上，batch verify可以提高验签效率。

## Project-22， research report on MPT

## 运行指导

报告在Project22中，直接打开即可。
