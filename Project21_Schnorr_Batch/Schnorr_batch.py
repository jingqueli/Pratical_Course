#Schnorr signature
from hashlib import sha256
from random import randint
import random
import hashlib
from gmpy2 import invert
from time import time

'''
# 定义有限域 Fp 的参数
p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
a = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2C
b = 0x28E9FA9E9D9F5E3448DE6470264F98A48F8C70A9D578D948C539EBD10162E5DB
q = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF6C611070995AD10045841B09B761B893#q是阶

# 定义椭圆曲线 E 上的生成元 P
Px = 0x32C4AE2C1A86E372FEF09E0A81FFB960248607C3EE0D73FA7575F085051561DC
Py = 0xA78F61D07314897B263C4E84D2F910B0863896E661D4EBDABAF41B6E87DADA36
'''
p = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
a = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
b = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
q = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123

Px=0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7
Py=0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0
G = (0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7, 0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0)

Index=4#定义batch的数量
M=[]
d=[]
P=[]
R=[]
e=[]
#群的阶为q，P是加法群的生成元

# 点的加法运算
def point_add(P,Q):
    
    
    if P is None:
        return Q
    elif Q is None:
        return P
    elif P[0]==Q[0] and P[1]!=Q[1]:
        return None
    #elif P == point_neg(Q):
        return None

    x1, y1 = P[0], P[1]
    x2, y2 = Q[0], Q[1]
    
    if P == Q:
        lam = ((3 * x1 * x1 + a) * invert(2*y1,p)) % p
    else:
        lam = ((y2 - y1) * invert(x2-x1,p)) % p

    x3 = (lam * lam - x1 - x2) % p
    y3 = (lam * (x1 - x3) - y1) % p
    
    return (x3,y3)

# 点的取反运算
def point_neg(P):
    if P is None:
        return None

    x, y = P
    return x, (-y) % p

# 标量乘运算

def point_mul(P,k):
    
    k=k%q
    if k % q == 0 or P is None:
        return None

    if k < 0:
        #return point_neg(point_mul(-k, P))
        return point_mul(q-k,P)
    
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

def key_gen():
    d = random.getrandbits(256) % q
    P = point_mul(G,d)
    return (d,P)
def signature(M,d):
    sig=[]
    for i in range(0,Index):
        ki=random.getrandbits(256)%q
        Ri=point_mul(G,ki)
        Rix=Ri[0]
        ei=sm3_hash((str(Rix)+M[i]).encode())
        ei=int(ei,16)
        e.append(ei)
        si=(ki+ei*d[i])%q
        sig.append((Ri,si))
    return sig

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


if __name__=='__main__':
    #d,P=key_gen()
    for i in range(0,Index):
        m=input('input M')
        #m='RuoYan'
        M.append(m)
        di,Pi=key_gen()
        d.append(di)
        P.append(Pi)
        
    #M='Ruo Yan'
    t1=time()
    sig=signature(M,d)
    #t1=time()
    verify_sig(sig,M,P)
    t2=time()
    print('time:',(t2-t1),'s')

