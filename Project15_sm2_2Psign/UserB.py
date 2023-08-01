#UserB
from hashlib import sha256
from random import randint
import hashlib
import socket
from gmpy2 import invert
import binascii

# 定义有限域 Fp 的参数
p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
a = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2C
b = 0x28E9FA9E9D9F5E3448DE6470264F98A48F8C70A9D578D948C539EBD10162E5DB
q = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF6C611070995AD10045841B09B761B893

# 定义椭圆曲线 E 上的生成元 P
Px = 0x32C4AE2C1A86E372FEF09E0A81FFB960248607C3EE0D73FA7575F085051561DC
Py = 0xA78F61D07314897B263C4E84D2F910B0863896E661D4EBDABAF41B6E87DADA36

#群的阶为q，P是加法群的生成元

# 点的加法运算
def point_add(P, Q):
    if P is None:
        return Q
    elif Q is None:
        return P
    elif P == point_neg(Q):
        return None

    x1, y1 = P[0], P[1]
    x2, y2 = Q[0], Q[1]

    if P == Q:
        lam = ((3 * x1 * x1 + a) * pow(2 * y1, p - 2, p)) % p
    else:
        lam = ((y2 - y1) * pow(x2 - x1, p - 2, p)) % p

    x3 = (lam * lam - x1 - x2) % p
    y3 = (lam * (x1 - x3) - y1) % p

    return x3, y3

# 点的取反运算
def point_neg(P):
    if P is None:
        return None

    x, y = P
    return x, (-y) % p

# 标量乘运算
def point_mul(k, P):
    if k % q == 0 or P is None:
        return None

    if k < 0:
        return point_neg(point_mul(-k, P))

    Q = None
    while k:
        if k & 1:
            Q = point_add(Q, P)
        P = point_add(P, P)
        k >>= 1

    return Q

#下面是库函数的hash_SM3    
def sm3_hash(data):
    hash_object = hashlib.new('sm3')
    hash_object.update(data)
    hash_value = hash_object.hexdigest()
    return hash_value


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)         # 创建 socket 对象
host = socket.gethostname() # 获取本地主机名
port_UserA = 12345   # 设置端口
port_UserB=10001
s.bind((host, port_UserB))        # 绑定端口


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

print("close")




