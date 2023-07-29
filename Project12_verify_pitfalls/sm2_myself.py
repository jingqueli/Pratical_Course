#本内容旨在实现一个SM2算法
#from sympy import randprime
from hashlib import sha256
from random import randint
import random
import hashlib
from gmpy2 import invert

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


#群的阶为q，P是加法群的生成元


def Precompute(ENTL_A,ID_A,x_A,y_A):
    sm3_data=ENTL_A+ID_A+str(a)+str(b)+str(Px)+str(Py)+str(x_A)+str(y_A)
    sm3_data=sm3_data.encode()
    ZA=sm3_hash(sm3_data)
    return ZA#ZA为字符串类型
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
    Q = point_mul(G,d)
    return (d,Q)

def Hv(mes):
    mes=mes.encode()
    H_mes=sm3_hash(mes)
    return H_mes[0:8]




def signature(ENTL_A,ID_A,d_A,M):
    G=(Px,Py)
    P_A=point_mul(G,d_A)
    x_A=P_A[0]#分别取出PA的x and y
    y_A=P_A[1]
    ZA=Precompute(ENTL_A,ID_A,x_A,y_A)
    M1=ZA+M#传入M需要也为字符串
    e=int(Hv(M1),16)#e是十进制整数
    #print('e',e)
    
    k = random.getrandbits(256) % q
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
        print('签名验证通过。')
    else:
        print('签名验证不通过')
    return (s,t),P_A

if __name__=='__main__':
    #d_A=randint(2,q-1)
    ENTL_A='ENTLA'
    ID_A='RuoYan'
    M='O my Luve is like a red, red rose,That is newly sprung in June,O my Luve is like the melodyThat is sweetly played in tune.'
    #M初始为字符串类型
    G=(Px,Py)
    d_A,Q=key_gen()
    print('Q',Q)
    x_A=Q[0]#分别取出x and y
    y_A=Q[1]
    ZA=Precompute(ENTL_A,ID_A,x_A,y_A)

    sig,P_A=signature(ENTL_A,ID_A,d_A,M)
    verify_signature(sig,M,P_A,ENTL_A,ID_A)


