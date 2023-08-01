#ECMH
from sympy import randprime
from hashlib import sha256
from random import randint
import hashlib
import socket
from gmpy2 import invert
import binascii
import random
from math import gcd
from time import time

p = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
a = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
b = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
q = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123

Px=0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7
Py=0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0
G = (0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7, 0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0)


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



bit_length=512
N=random.randrange(2**(bit_length-1), 2**bit_length)
while(N%2==0):
    N=random.randrange(2**(bit_length-1), 2**bit_length)
l_factor=random.getrandbits(64)
#print('little factor',l_factor)
N=N*l_factor

#N=p*q
print("N:",N)
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

t2=time()
print('ECMH time:',(t2-t1),'s')

#与暴力破解时间对比
t3=time()
for i in range(2,int(N**(1/2))):
    if(gcd(i,N)!=1):
        print('i',i)
        break
    #break
t4=time()
print('time:',(t4-t3),'s')


    
