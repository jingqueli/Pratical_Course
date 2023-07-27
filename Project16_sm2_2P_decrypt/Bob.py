#Bob

import socket
from sm2_myself import *
import json
import random
from gmpy2 import invert
from gmpy2 import mpz

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)         # 创建 socket 对象
host = socket.gethostname() # 获取本地主机名
port_Alice = 12345   # 设置端口
port_Bob=10001
s.bind((host, port_Bob))        # 绑定端口
addr=(host,port_Alice)

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
    
'''
import gmpy2
from gmpy2 import mpz
# 原始的 mpz 元组
original_tuple = (gmpy2.mpz(123), gmpy2.mpz(456), gmpy2.mpz(789))
print(original_tuple)

# 将元组转换为字符串
tuple_str = str(original_tuple)
print(tuple_str)
# 将字符串转换回 mpz 元组
restored_tuple = tuple(mpz(x) for x in eval(tuple_str))

# 输出结果
print(restored_tuple)
'''    
