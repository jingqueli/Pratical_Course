#sm2_2P UserA
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
s.bind((host, port_UserA))        # 绑定端口

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

s.close()




